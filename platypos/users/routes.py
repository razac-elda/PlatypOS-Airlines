from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, current_user, logout_user

from platypos import bcrypt
from platypos.models import *
from platypos.users.utils import load_user

users_account = Blueprint('users_account', __name__, template_folder='templates', static_folder='static')


# Viene preferito l'uso di current_user.is_authenticated per poter reindirizzare invece che @login_required

@users_account.route('/profilo')
def profile():
    if current_user.is_authenticated:
        if current_user.get_permission() > 0:
            #se da problemi cancellare la riga che inizia con with e  mettere solo connection = engine.connect() e lasciare le query

            #usato il valore REPEATABLE READ  xk in questa transazione le query leggono solo
            #se un amministratore cancella un volo nell'esatto istante che un utente carica il proprio profilo non si creano valori sporchi
            with engine.connect().execution_options(isolation_level="REPEATABLE READ") as connection:
                planes = connection.execute(select([airplanes.c.plane_code]). \
                                        order_by(airplanes.c.plane_code))
                airports_from = connection.execute(select([airports.c.name]). \
                                               order_by(airports.c.name))
                airports_to = connection.execute(select([airports.c.name]). \
                                             order_by(airports.c.name))
            #in teoria non serve il la chiusura della connessione xk viene automaticamente chiusa alla fine del with
            connection.close()
            return render_template('amministrazione.html', title='Amministrazione',
                                   dynamic_airport_from=airports_from,
                                   dynamic_airport_to=airports_to, dynamic_plane=planes,
                                   logged_in=current_user.is_authenticated)
        else:
            # Viene utilizzata la sessione dell'utente per ottenere i suoi dati personali
            return render_template('profilo.html', title='Profilo personale', name=current_user.get_name(),
                                   surname=current_user.get_surname(), email=current_user.get_mail(),
                                   logged_in=current_user.is_authenticated)
    else:
        return redirect(url_for('users_account.access_page'))


@users_account.route('/profilo/cambio_password', methods=['GET', 'POST'])
def change_password():
    if current_user.is_authenticated:
        if request.method == 'POST':
            connection = engine.connect()
            results = connection.execute(select([users.c.password]). \
                                         where(users.c.user_id == current_user.get_id()))

            connection.close()
            password = results.fetchone()['password']
            if bcrypt.check_password_hash(password, request.form['old_psw']):
                hashed_password = bcrypt.generate_password_hash(request.form['new_psw']).decode('utf-8')
                connection = engine.connect()
                connection.execute(users.update().values(password=hashed_password). \
                                   where(users.c.user_id == current_user.get_id()))
                connection.close()
                return redirect(url_for('users_account.logout'))
            else:
                return render_template('profilo.html', title='Profilo personale', name=current_user.get_name(),
                                       surname=current_user.get_surname(), email=current_user.get_mail(),
                                       logged_in=current_user.is_authenticated, invalid=True)
    return redirect(url_for('users_account.profile'))


@users_account.route('/profilo/nuovo_volo', methods=['GET', 'POST'])
def new_flight():
    if current_user.is_authenticated and current_user.get_permission() > 0:
        if request.method == 'POST':
            connection = engine.connect()
            airports_from = connection.execute(select([airports.c.airport_id]). \
                                               where(airports.c.name == request.form['fly_from']))
            airports_to = connection.execute(select([airports.c.airport_id]). \
                                             where(airports.c.name == request.form['fly_to']))
            airport_from = airports_from.fetchone()['airport_id']
            airport_to = airports_to.fetchone()['airport_id']
            connection.execute(flights.insert(), departure_time=request.form['fly_dep_date'],
                               arrival_time=request.form['fly_arrival_date'],
                               departure_airport=airport_from, arrival_airport=airport_to,
                               plane_code=request.form['plane_code'])
            connection.close()
    return redirect(url_for('users_account.profile'))


@users_account.route('/profilo/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
    return redirect(url_for('users_account.access_page'))


@users_account.route('/')
@users_account.route('/autenticazione')
def access_page():
    if current_user.is_authenticated:
        return redirect(url_for('users_account.profile'))
    else:
        return render_template('autenticazione.html', title='Accedi / Registrati', logged_in=False)


@users_account.route('/accesso', methods=['GET', 'POST'])
def form_login():
    if current_user.is_authenticated:
        return redirect(url_for('users_account.profile'))
    if request.method == 'POST':
        connection = engine.connect()
        # Vengono prelevate la password e l'id corrispondenti alla mail
        results = connection.execute(select([users.c.password, users.c.user_id]). \
                                     where(users.c.email == request.form['email'].lower()))
        connection.close()
        real_password = None
        user_id = None
        for row in results:
            real_password = row['password']
            user_id = row['user_id']
        # Se l'utente esiste e la password e' corretta si procede al login
        if real_password and user_id:
            if bcrypt.check_password_hash(real_password, request.form['pass']):
                # Creazione istanza classe User tramite id
                user = load_user(user_id)
                # Passaggi a flask-login
                login_user(user)
                return redirect(url_for('users_account.profile'))
        return render_template('autenticazione.html', title='Accedi / Registrati', logged_in=False, invalid=True)
    return render_template('autenticazione.html', title='Accedi / Registrati', logged_in=False)


@users_account.route('/registrazione', methods=['GET', 'POST'])
def form_register():
    if current_user.is_authenticated:
        return redirect(url_for('users_account.profile'))
    if request.method == 'POST':
        # Controllo che non esista gia' un utente con la mail passata
        connection = engine.connect()
        results = connection.execute(select([users]). \
                                     where(users.c.email == request.form['new_email'].lower()))
        connection.close()
        user_exists = False
        for row in results:
            user_exists = True
        if not user_exists:
            # Hashing della password con flask-bcrypt
            hashed_password = bcrypt.generate_password_hash(request.form['new_pass']).decode('utf-8')
            # Inserimento nuovo utente
            connection = engine.connect()
            connection.execute(users.insert(), email=request.form['new_email'].lower(), password=hashed_password,
                               name=request.form['new_name'], surname=request.form['new_surname'])
            connection.close()
            return redirect(url_for('users_account.profile'))
        else:
            return render_template('autenticazione.html', title='Accedi / Registrati', logged_in=False, exist=True)
    return render_template('autenticazione.html', title='Accedi / Registrati', logged_in=False)

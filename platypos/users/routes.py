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
        # Gli admin hanno pagine più avanzate
        if current_user.get_permission() > 0:
            # Vari elementi per poter inserire i voli, READ COMMITTED perchè se si vuole inserire un volo ci si aspetta
            # che l'operatore conosca già quale volo inserire
            with engine.connect().execution_options(isolation_level="READ COMMITTED") as connection:

                planes = connection.execute(select([airplanes.c.plane_code]). \
                                            order_by(airplanes.c.plane_code))
                airports_from = connection.execute(select([airports.c.name]). \
                                                   order_by(airports.c.name))
                airports_to = connection.execute(select([airports.c.name]). \
                                                 order_by(airports.c.name))
            return render_template('amministrazione.html', title='Amministrazione',
                                   dynamic_airport_from=airports_from,
                                   dynamic_airport_to=airports_to, dynamic_plane=planes,
                                   logged_in=current_user.is_authenticated)
        else:
            # Viene prelevato l'elenco delle prenotazioni di un utente
            # SERIALIZABLE permette di visualizzare correttamente tutte le prenotazioni fino all'ultimo momento
            with engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
                s = text(
                    " SELECT a1.name as departure_airport, a2.name as arrival_airport, f.departure_time as departure_time, f.arrival_time as arrival_time, f.plane_code as plane_code, b.seat_column as seat_column, b.seat_number as seat_number, f.flight_code as flight_code "
                    " FROM bookings b JOIN flights f ON b.flight_code=f.flight_code JOIN airports a1 ON a1.airport_id=f.departure_airport JOIN airports a2 ON a2.airport_id=f.arrival_airport"
                    " WHERE b.user_id=:user_id"
                )
                user_bookings = connection.execute(s, user_id=current_user.get_id())
            # Viene utilizzata la sessione dell'utente per ottenere i suoi dati personali
            return render_template('profilo.html', title='Profilo personale', name=current_user.get_name(),
                                   surname=current_user.get_surname(), email=current_user.get_mail(),
                                   bookings=user_bookings,
                                   logged_in=current_user.is_authenticated)
    else:
        return redirect(url_for('users_account.access_page'))


@users_account.route('/profilo/cambio_password', methods=['GET', 'POST'])
def change_password():
    if current_user.is_authenticated:
        if request.method == 'POST':
            # Viene prelevata la password, READ COMMITTED per evitare che la password sia gia stata modificata
            with engine.connect().execution_options(isolation_level="READ COMMITTED") as connection:
                results = connection.execute(select([users.c.password]). \
                                             where(users.c.user_id == current_user.get_id()))
            # Confronto vecchia-nuova password tramite la funzione di flask-bcrypt
            password = results.fetchone()['password']
            if bcrypt.check_password_hash(password, request.form['old_psw']):
                # Generazione nuovo hash
                hashed_password = bcrypt.generate_password_hash(request.form['new_psw']).decode('utf-8')
                # Aggionamento della password senza livello di isolazione
                with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
                    connection.execute(users.update().values(password=hashed_password). \
                                       where(users.c.user_id == current_user.get_id()))
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
            # Inserimento di un nuovo volo, si prelevano i campi necessari partendo dal nome degli aeroporti
            # SERIALIZABLE evita la concorrenza tra più operatori
            with engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
                airports_from = connection.execute(select([airports.c.airport_id]). \
                                                   where(airports.c.name == request.form['fly_from']))
                airports_to = connection.execute(select([airports.c.airport_id]). \
                                                 where(airports.c.name == request.form['fly_to']))
                airport_from = airports_from.fetchone()['airport_id']
                airport_to = airports_to.fetchone()['airport_id']
                # La data viene unita all'orario per essere salvato in un timestamp nel database
                departure_time = request.form['fly_dep_date'] + " " + request.form['departure_hour'] + ":" + \
                                 request.form['departure_minute']
                arrival_time = request.form['fly_arrival_date'] + " " + request.form['arrival_hour'] + ":" + \
                               request.form['arrival_minute']
                try:
                    connection.execute(flights.insert(), departure_time=departure_time, arrival_time=arrival_time,
                                       departure_airport=airport_from, arrival_airport=airport_to,
                                       plane_code=request.form['plane_code'])
                except:
                    msg = "Presta più attenzione ai campi inseriti, l'operazione non è andata a buon fine!"
                    return render_template('errors.html', error_msg=msg, logged_in=current_user.is_authenticated)
    return redirect(url_for('users_account.profile'))


@users_account.route('/profilo/nuovo_aeroporto', methods=['GET', 'POST'])
def new_airport():
    if current_user.is_authenticated and current_user.get_permission() > 0:
        if request.method == 'POST':
            # Inserimento di nuovi aeroporti, SERIALIZABLE evita la concorrenza tra più operatori
            with engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
                connection.execute(airports.insert(),
                                   name=request.form['airport_name'],
                                   city=request.form['city'],
                                   province=request.form['province'])
    return redirect(url_for('users_account.profile'))


@users_account.route('/profilo/nuovo_aereo', methods=['GET', 'POST'])
def new_plane():
    if current_user.is_authenticated and current_user.get_permission() > 0:
        if request.method == 'POST':
            # Inserimento di nuovi aerei, SERIALIZABLE evita la concorrenza tra più operatori
            with engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
                connection.execute(airplanes.insert(), seats=request.form['plane_seats'])
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
        # Ricerca dell'utente registrato, SERIALIZABLE evita di avere campi nuovi non letti
        with engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
            results = connection.execute(select([users.c.password, users.c.user_id]). \
                                         where(users.c.email == request.form['email'].lower()))
        real_password = None
        user_id = None
        for row in results:
            real_password = row['password']
            user_id = row['user_id']
        # Se l'utente esiste e la password e' corretta si procede al login
        if real_password and user_id:
            # Funzione di flask-bcrypt per confrontare password
            if bcrypt.check_password_hash(real_password, request.form['pass']):
                # Creazione istanza classe User tramite id
                user = load_user(user_id)
                # Passaggio a flask-login
                login_user(user)
                return redirect(url_for('users_account.profile'))
        return render_template('autenticazione.html', title='Accedi / Registrati', logged_in=False, invalid=True)
    return render_template('autenticazione.html', title='Accedi / Registrati', logged_in=False)


@users_account.route('/registrazione', methods=['GET', 'POST'])
def form_register():
    if current_user.is_authenticated:
        return redirect(url_for('users_account.profile'))
    if request.method == 'POST':
        # # Ricerca dell'utente registrato, SERIALIZABLE evita di avere campi nuovi non letti
        with engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
            results = connection.execute(select([users]). \
                                         where(users.c.email == request.form['new_email'].lower()))
        user_exists = False
        for row in results:
            user_exists = True
        if not user_exists:
            # Hashing della password con flask-bcrypt
            hashed_password = bcrypt.generate_password_hash(request.form['new_pass']).decode('utf-8')
            # Inserimento nuovo utente, non è necessario isolamento
            with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
                connection.execute(users.insert(), email=request.form['new_email'].lower(), password=hashed_password,
                                   name=request.form['new_name'], surname=request.form['new_surname'])
            return redirect(url_for('users_account.profile'))
        else:
            return render_template('autenticazione.html', title='Accedi / Registrati', logged_in=False, exist=True)
    return render_template('autenticazione.html', title='Accedi / Registrati', logged_in=False)


@users_account.route('/profilo/statistiche')
def statistics():
    if current_user.is_authenticated and current_user.get_permission() > 0:
        # Creazione statistiche
        # REPEATABLE READ per evitare che una riga cambi valore
        with engine.connect().execution_options(isolation_level="REPEATABLE READ") as connection:
            # Clienti fedeli
            s = text(
                " SELECT u.name, u.surname, b.user_id , COUNT(*) as flights_number"
                " FROM bookings b JOIN users u ON b.user_id = u.user_id"
                " GROUP BY b.user_id, u.name, u.surname"
                " ORDER BY flights_number DESC"
                " LIMIT 10"
            )
            top_clients = connection.execute(s)
            # Voli per anno
            s = text(
                " SELECT  CAST( date_part('year', departure_time)as int )  as years, count(*) as flights_number"
                " FROM flights"
                " GROUP BY years "
                " ORDER BY years desc"
            )
            flights_per_year = connection.execute(s)
            # Citta piu visitate
            s = text(
                "SELECT a.province, count(f.flight_code) as numero_voli"
                " FROM airports a JOIN flights f ON a.airport_id=f.arrival_airport "
                " GROUP BY a.province"
                " ORDER BY numero_voli DESC"
                " LIMIT 10"
            )
            top_cities = connection.execute(s)
            # Media prenotazioni per cliente per anno
            s = text(
                " SELECT CAST( date_part('year', f.departure_time)as int ) as years ,"
                " CASE WHEN count(distinct b.user_id) > 0 THEN CAST(count(b.booking_id)AS DOUBLE PRECISION)/CAST(count(distinct b.user_id)AS DOUBLE PRECISION)"
                " ELSE 0 END"
                " AS average"
                " FROM flights f LEFT JOIN bookings b ON f.flight_code = b.flight_code"
                " GROUP BY years"
            )
            avg_booking_per_year = connection.execute(s)
            # Aerei con numero posti prenotati dal 2000 ad oggi
            s = text(
                "SELECT f1.plane_code, count(f1.plane_code) as numero_posti"
                " FROM airplanes a1 JOIN flights f1 ON a1.plane_code=f1.plane_code "
                " JOIN bookings b1 ON f1.flight_code=b1.flight_code"
                " WHERE CAST( date_part('year', f1.departure_time)as int )  BETWEEN 2000 AND date_part('year', CURRENT_DATE)"
                " GROUP BY f1.plane_code"
            )
            plane_with_places = connection.execute(s)
        return render_template('statistiche.html', title='Statistiche', logged_in=current_user.is_authenticated,
                               top_clients=top_clients, flights_per_year=flights_per_year,
                               avg_booking_per_year=avg_booking_per_year,
                               plane_with_places=plane_with_places, top_cities=top_cities)
    return redirect(url_for('users_account.profile'))

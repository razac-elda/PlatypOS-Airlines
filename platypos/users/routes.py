from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, current_user

from platypos.models import *
from platypos.users.utils import load_user

users_account = Blueprint('users_account', __name__, template_folder='templates', static_folder='static')


@users_account.route('/')
@users_account.route('/autenticazione')
def access_page():
    if current_user.is_authenticated:
        return redirect(url_for('notizie'))
    else:
        return render_template('autenticazione.html', title='Accedi / Registrati')


@users_account.route('/<user>')
def profile(user):
    return render_template('autenticazione.html', title='Profilo', new_user=1)


@users_account.route('/accesso', methods=['GET', 'POST'])
def form_login():
    if current_user.is_authenticated:
        return redirect(url_for('notizie'))
    if request.method == 'POST':
        connection = engine.connect()
        results = connection.execute(select([users.c.password]). \
                                     where(users.c.email == request.form['email']))
        real_password = ''
        for row in results:
            real_password = row['password']
        connection.close()
        if request.form['pass'] == real_password:
            user = load_user(request.form['email'])
            login_user(user)
            return redirect(url_for('notizie'))
        else:
            return render_template('autenticazione.html', title='Accedi / Registrati Errore')
    return render_template('autenticazione.html', title='Accedi / Registrati')


@users_account.route('/registrazione', methods=['GET', 'POST'])
def form_register():
    if current_user.is_authenticated:
        return redirect(url_for('notizie'))
    if request.method == 'POST':
        connection = engine.connect()
        results = connection.execute(select([users]). \
                                     where(users.c.email == request.form['new_email']))
        exists = false
        for row in results:
            exists = true
        if not exists:

            connection.execute(users.insert(), email=request.form['new_email'], password=request.form['new_pass'],
                               name=request.form['new_name'], surname=request.form['new_surname'])
            connection.close()
            return redirect(url_for('users_account.access_page'))
        else:
            return render_template('autenticazione.html', title='Accedi / Registrati Errore')
    return render_template('autenticazione.html', title='Accedi / Registrati')
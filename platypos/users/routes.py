from flask import Blueprint, render_template, request, redirect, url_for
from platypos.models import *

users_account = Blueprint('users_account', __name__, template_folder='templates', static_folder='static')


@users_account.route('/')
@users_account.route('/autenticazione')
def access_page():
    return render_template('autenticazione.html', title='Accedi / Registrati')


@users_account.route('/<user>')
def profile(user):
    return render_template('autenticazione.html', title='Profilo', new_user=1)


@users_account.route('/accesso', methods=['GET', 'POST'])
def form_login():
    username = 'leo'
    return redirect(url_for('users_account.profile', username=username))


@users_account.route('/registrazione', methods=['GET', 'POST'])
def form_register():
    name = request.form['new_name']
    surname = request.form['new_surname']
    email = request.form['new_email']
    password = request.form['new_pass']
    connection = engine.connect()
    ins = users.insert()
    connection.execute(ins, email=email, password=password, name=name, surname=surname)
    connection.close()
    account_error = 'none'
    # I risultati li potete leggere dalla console
    if account_error == 'email':
        # Stampare messaggio errore
        return render_template('autenticazione.html', title='Accedi / Registrati Errore')
    else:
        # Stampare messaggio successo
        return render_template('autenticazione.html', title='Accedi / Registrati')

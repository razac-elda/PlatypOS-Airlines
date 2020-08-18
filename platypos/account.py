from flask import Blueprint, render_template, request, redirect, url_for
from platypos.models import connection, users

account = Blueprint('account', __name__, template_folder='templates', static_folder='static')


@account.route('/')
@account.route('/autenticazione')
def access():
    return render_template('autenticazione.html', title='Accedi / Registrati')



@account.route('/autenticazioneErrore')
def error():
    return render_template('autenticazione.html', title='Accedi / Registrati')


@account.route('/<user>')
def user_profile(user):
    return render_template('autenticazione.html', title='Profilo', new_user=1)


@account.route('/accesso', methods=['GET', 'POST'])
def form_login():
    name = 'leo'
    return redirect(url_for('account.user_profile', name=name))


@account.route('/registrazione', methods=['GET', 'POST'])
def form_register():
    name = request.form['new_name']
    surname = request.form['new_surname']
    email = request.form['new_email']
    password = request.form['new_pass']
    ins = users.insert()
    connection.execute(ins, email=email, password=password, name=name, surname=surname)
    # I risultati li potete leggere dalla console
    return redirect(url_for('account.access'))

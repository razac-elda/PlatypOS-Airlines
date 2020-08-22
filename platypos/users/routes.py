from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, current_user, logout_user

from platypos import login_manager
from platypos.models import *
from platypos.users.utils import load_user

users_account = Blueprint('users_account', __name__, template_folder='templates', static_folder='static')


@users_account.route('/profilo')
def profile():
    if current_user.is_authenticated:
        return render_template('profilo.html', title='Profilo', name=current_user.get_name(),
                               surname=current_user.get_surname(), email=current_user.get_mail(),
                               logged_in=current_user.is_authenticated)
    else:
        return redirect(url_for('users_account.access_page'))


@users_account.route('/logout')
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
        results = connection.execute(select([users.c.password, users.c.user_id]). \
                                     where(users.c.email == request.form['email']))
        real_password = None
        user_id = None
        for row in results:
            real_password = row['password']
            user_id = row['user_id']
        connection.close()
        if request.form['pass'] == real_password:
            user = load_user(user_id)
            login_user(user)
            return redirect(url_for('users_account.profile'))
        else:
            return render_template('autenticazione.html', title='Accedi / Registrati Errore', logged_in=False)
    return render_template('autenticazione.html', title='Accedi / Registrati', logged_in=False)


@users_account.route('/registrazione', methods=['GET', 'POST'])
def form_register():
    if current_user.is_authenticated:
        return redirect(url_for('users_account.profile'))
    if request.method == 'POST':
        connection = engine.connect()
        results = connection.execute(select([users]). \
                                     where(users.c.email == request.form['new_email']))
        user_exists = False
        for row in results:
            user_exists = True
        if not user_exists:
            connection.execute(users.insert(), email=request.form['new_email'], password=request.form['new_pass'],
                               name=request.form['new_name'], surname=request.form['new_surname'])
            connection.close()
            return redirect(url_for('users_account.profile'))
        else:
            return render_template('autenticazione.html', title='Accedi / Registrati Errore', logged_in=False)
    return render_template('autenticazione.html', title='Accedi / Registrati', logged_in=False)

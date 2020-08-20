from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user
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
    # if request.method == 'POST':
    #     connection = engine.connect()
    #     results = connection.execute(select([users.c.password]). \
    #                                  where(users.c.email == request.form['email']))
    #     real_password = results.fetchone()['password']
    #     connection.close()
    #     if request.form['pass'] == real_password:
    #         user = User(request.form['email'], request.form['pass'])
    #         login_user(user)
    #         return redirect(url_for(access_page))
    #     else:
    #         return redirect(url_for(access_page))
    return redirect(url_for(access_page))


@users_account.route('/registrazione', methods=['GET', 'POST'])
def form_register():
    # if request.method == 'POST':
    #     connection = engine.connect()
    #     results = connection.execute(select([users]). \
    #                                  where(users.c.email == request.form['new_email']))
    #     data = [dict(row) for row in results]
    #     if not data:
    #
    #         connection.exeute(users.insert(), email=request.form['new_email'], password=request.form['new_pass'],
    #                           name=request.form['new_name'], surname=request.form['new_surname'])
    #         connection.close()
    #         account_error = 'none'
    #         # I risultati li potete leggere dalla console
    #         if account_error == 'email':
    #             # Stampare messaggio errore
    #             return render_template('autenticazione.html', title='Accedi / Registrati Errore')
    #         else:
    #             # Stampare messaggio successo
    #             return render_template('autenticazione.html', title='Accedi / Registrati')
    #
    #     else:
    #         connection.close()
    #         return redirect(url_for(access_page))
    # else:
        return redirect(url_for(access_page))

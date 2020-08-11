from flask import Blueprint, render_template, request, redirect, url_for

account = Blueprint('account', __name__, template_folder='templates', static_folder='static')


@account.route('/')
@account.route('/autenticazione')
def access():
    return render_template('autenticazione.html', title='Accedi / Registrati')


@account.route('/<email>')
def user_profile(email):
    emails = ['leo@leo']  # DB
    if email in emails:
        return render_template('profilo.html', title='Profilo', user=email)
    else:
        return render_template('autenticazione.html', title='Profilo', new_user=1)


@account.route('/accesso', methods=['GET', 'POST'])
def form_login():
    email = request.form["user"]
    password = request.form["pass"]
    return redirect(url_for('account.user_profile', email=email))


@account.route('/registrazione', methods=['GET', 'POST'])
def form_register():
    return redirect(url_for('account.access'))

from flask import Blueprint, render_template, request, redirect, url_for

account = Blueprint('account', __name__, template_folder='templates', static_folder='static')


@account.route('/')
def access():
    return render_template('accesso.html', title='Profilo')


@account.route('/<username>')
def user_profile(username):
    users = ['leo']  # DB
    if username in users:
        return render_template('profilo.html', title='Profilo', user=username)
    else:
        return render_template('accesso.html', title='Profilo', new_user=1)


@account.route('/login', methods=['GET', 'POST'])
def form_login():
    user = request.form["user"]
    return redirect(url_for('account.user_profile', username=user))


@account.route('/register', methods=['GET', 'POST'])
def form_register():
    return redirect(url_for('account.access'))

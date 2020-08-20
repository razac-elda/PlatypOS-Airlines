from flask import Flask, render_template
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sonounachiavesegreta'

# login_manager = LoginManager()
# login_manager.init_app(app)

from platypos.main.routes import main
from platypos.users.routes import users_account

app.register_blueprint(main)
app.register_blueprint(users_account, url_prefix="/utente")


@app.route('/voli')
def voli():
    return render_template('voli.html', title='Voli', active_menu=1)


@app.route('/notizie')
def notizie():
    return render_template('notizie.html', title='Notizie', active_menu=2)


@app.route('/contatti')
def contatti():
    return render_template('contatti.html', title='Contatti', active_menu=3)

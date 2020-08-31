from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sonounachiavesegreta'

# Inizializzazione  di flask-login e flask-bcrypt
login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)

# Le pagine vengono divise con delle blueprint in base al ruolo.
# main contiene la pagina principale con la ricerca e prenotazione
# users_account gestisce l'interazione con l'account degli utenti
from platypos.main.routes import main
from platypos.users.routes import users_account

app.register_blueprint(main)
app.register_blueprint(users_account, url_prefix="/utente")


@app.route('/contatti')
def contatti():
    return render_template('contatti.html', title='Contatti', active_menu=1, logged_in=current_user.is_authenticated)

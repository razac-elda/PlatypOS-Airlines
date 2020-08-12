from platypos import app
from flask import render_template
from platypos.account import account

app.register_blueprint(account, url_prefix="/utenti")


# Ogni route sarebbe da mettere in una dedicata blueprint

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', active_menu=0)


@app.route('/voli')
def voli():
    return render_template('voli.html', title='Voli', active_menu=1)


@app.route('/notizie')
def notizie():
    return render_template('notizie.html', title='Notizie', active_menu=2)


@app.route('/contatti')
def contatti():
    return render_template('contatti.html', title='Contatti', active_menu=3)

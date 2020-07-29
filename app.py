from flask import Flask, render_template
from account import account

app = Flask(__name__)
app.register_blueprint(account, url_prefix="/profilo")


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
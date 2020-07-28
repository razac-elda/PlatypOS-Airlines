from flask import Flask, render_template
from account import account

app = Flask(__name__)
app.register_blueprint(account, url_prefix="/profilo")


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/voli')
def voli():
    return render_template('voli.html', title='Voli')


@app.route('/notizie')
def notizie():
    return render_template('notizie.html', title='Notizie')


@app.route('/contatti')
def contatti():
    return render_template('contatti.html', title='Contatti')
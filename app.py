from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
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


@app.route('/account')
def account():
    return render_template('account.html', title='Account')

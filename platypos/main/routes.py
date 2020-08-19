from flask import Blueprint, render_template

from platypos.models import *

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')


@main.route('/')
@main.route('/home')
def homepage():
    results = connection.execute(select([airports.c.name]).\
                                 order_by(airports.c.name))

    return render_template('home.html', active_menu=0, answer=results)



""""
@main.route('/home/result', methods=['POST'])
def homepage():
    mail = request.form['email']
    return render_template('home.html', active_menu=0)
"""



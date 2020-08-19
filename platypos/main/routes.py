from flask import Blueprint, render_template

from platypos.models import *

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')


@main.route('/')
@main.route('/home')
def homepage():
    connection = engine.connect();
    results = connection.execute(select([airports.c.city]). \
                                 group_by(airports.c.city))
    connection.close();
    return render_template('home.html', active_menu=0, answer=results)


@main.route('/result', methods=['GET'])
def search_results():
    return render_template('home.html', active_menu=0)

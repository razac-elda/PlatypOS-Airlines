from flask import Blueprint, render_template, request
from platypos.models import *

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')


@main.route('/')
@main.route('/home')
def homepage():
    connection = engine.connect()

    results = connection.execute("SELECT distinct city FROM airports ORDER BY city")
    connection.close()
    return render_template('home.html', active_menu=0, answer=results)


@main.route('/result', methods=['get'])
def search_results():
    """
        flyFrom = request.form['fly_from']
        flyTo = request.form['fly_to']
        #valori possibli di flyght_type sono fromTo e fromOnly
        flyType = request.form['flight_type']
        flyDepDate = request.form['fly_dep_date']
        flyReturnDate = request.form['fly_return_date']
    """

    connection = engine.connect()
    s = text("SELECT  f.flight_code as flight_code ,a1.name as departure_airport , a2.name as arrival_airport , f.departure_time as departure_time, f.arrival_time as arrival_time"
            " FROM airports a1 JOIN flights f ON a1.airport_id = f.departure_airport JOIN airports a2 ON a2.airport_id = f.arrival_airport")
    results = connection.execute(s)
    connection.close()

    return render_template('home.html', active_menu=0)



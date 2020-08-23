from flask import Blueprint, render_template, request
from flask_login import current_user
from platypos.models import *

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')


@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def homepage():
    connection = engine.connect()
    dynamiclist = connection.execute("SELECT distinct city FROM airports ORDER BY city")
    connection.close()
    if request.method == 'POST':
        flyFrom = request.form['fly_from']
        flyTo = request.form['fly_to']
        # Valori possibli di flyght_type sono oneway e roundtrip
        flyType = request.form['flight_type']
        flyDepDate = request.form['fly_dep_date']
        if flyType == 'roundtrip':
            flyReturnDate = request.form['fly_return_date']

            # DA MODIFICARE PER IL RITORNO

            s = text(
                "SELECT  f.flight_code as flight_code ,a1.name as departure_airport , a2.name as arrival_airport , f.departure_time as departure_time, f.arrival_time as arrival_time"
                " FROM airports a1 JOIN flights f ON a1.airport_id = f.departure_airport JOIN airports a2 ON a2.airport_id = f.arrival_airport"
                " WHERE a1.city=:cityfrom AND a2.city=:cityto AND date(f.departure_time)=:departure")
            connection = engine.connect()
            results = connection.execute(s, cityfrom=flyFrom, cityto=flyTo, departure=flyDepDate)
            connection.close()
        else:
            s = text(
                "SELECT  f.flight_code as flight_code ,a1.name as departure_airport , a2.name as arrival_airport , f.departure_time as departure_time, f.arrival_time as arrival_time"
                " FROM airports a1 JOIN flights f ON a1.airport_id = f.departure_airport JOIN airports a2 ON a2.airport_id = f.arrival_airport"
                " WHERE a1.city=:cityfrom AND a2.city=:cityto AND date(f.departure_time)=:departure")
            connection = engine.connect()
            results = connection.execute(s, cityfrom=flyFrom, cityto=flyTo, departure=flyDepDate)
            connection.close()
        return render_template('home.html', active_menu=0, result=results, dynamiclist=dynamiclist, logged_in=current_user.is_authenticated)
    return render_template('home.html', active_menu=0, dynamiclist=dynamiclist, logged_in=current_user.is_authenticated)

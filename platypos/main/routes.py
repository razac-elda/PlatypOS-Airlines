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


@main.route('/result', methods=['GET'])
def search_results():
    
    flyFrom = request.form['fly_from']
    flyTo = request.form['fly_to']
    #valori possibli di flyght_type sono fromTo e fromOnly
    flyType = request.form['flight_type']
    flyDepDate = request.form['fly_dep_date']
    flyReturnDate = request.form['fly_return_date']
    return render_template('home.html', active_menu=0)

'''
    connection = engine.connect();
    if flyType == 'fromOnly':
        s = text (
            " SELECT a1.name , a2.name , f.departureTime , f.flightCode "
            "FROM flighs JOIN  airports a1 ON f.departureAirport = a1.airportId JOIN airports a2 ON a2.airportId = f.arrivalAirporta "
            "WHERE a1.name = flyFrom AND flyTo = a2.name AND flyType = fromOnly"  
        )
        results = connection.execute(s)
        connection.close();

    return render_template('home.html', active_menu=0, resultsFlights=results)
'''


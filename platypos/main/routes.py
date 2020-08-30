from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from platypos.models import *

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')


@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        connection = engine.connect()
        connection.execute(bookings.insert(), seat_number=1, user_id=current_user.get_id(),
                           flight_code=request.form['flight_code'])
        connection.close()
    connection = engine.connect()
    dynamiclist = connection.execute(select([airports.c.province]). \
                                     order_by(airports.c.province). \
                                     distinct())
    connection.close()
    return render_template('home.html', active_menu=0, dynamiclist=dynamiclist, logged_in=current_user.is_authenticated)


@main.route('/book_outbound', methods=['GET', 'POST'])
def book_outbound():
    if request.method == 'POST':
        flyFrom = request.form['fly_from']
        flyTo = request.form['fly_to']
        # Valori possibli di flyght_type sono oneway e roundtrip
        flyType = request.form['flight_type']
        flyDepDate = request.form['fly_dep_date']
        flyReturnDate = None
        if flyType == 'roundtrip':
            flyReturnDate = request.form['fly_return_date']
        s = text(
            "SELECT  f.flight_code as flight_code ,a1.name as departure_airport , a2.name as arrival_airport , f.departure_time as departure_time, f.arrival_time as arrival_time, a1.province as province_from, a2.province as province_to, f.plane_code as plane_code"
            " FROM airports a1 JOIN flights f ON a1.airport_id = f.departure_airport JOIN airports a2 ON a2.airport_id = f.arrival_airport"
            " WHERE a1.province=:provincefrom AND a2.province=:provinceto AND date(f.departure_time)=:departure")
        connection = engine.connect()
        outbound = connection.execute(s, provincefrom=flyFrom, provinceto=flyTo, departure=flyDepDate)
        # booked_flights = connection.execute(select([bookings.c.flight_code]). \
        #                                     order_by(bookings.c.flight_code))
        # booked_seats = {}
        # for flight in booked_flights:
        #     # Posti aereo?
        #     seats = connection.execute(select([bookings.c.seat_column, bookings.c.seat_number]). \
        #                                where(bookings.c.flight_code == flight['flight_code']))
        #     for row in seats:
        #         merge = row['seat_column'] + "" + str(row['seat_number'])
        #         booked_seats[flight['flight_code']].append(merge)
        connection.close()
        return render_template('booking.html', active_menu=0, flyReturnDate=flyReturnDate, book_outbound=True,
                               results_outbound=outbound,  # booked_seats=booked_seats,
                               logged_in=current_user.is_authenticated)
    return redirect(url_for('main.homepage'))


@main.route('/book_return', methods=['GET', 'POST'])
def book_return():
    if request.method == 'POST':
        connection = engine.connect()
        connection.execute(bookings.insert(), seat_number=1, user_id=current_user.get_id(),
                           flight_code=request.form['flight_code'])
        connection.close()
        flyFrom = request.form['province_to']
        flyTo = request.form['province_from']
        flyDepDate = request.form['fly_return_date']
        s = text(
            "SELECT  f.flight_code as flight_code ,a1.name as departure_airport , a2.name as arrival_airport , f.departure_time as departure_time, f.arrival_time as arrival_time, a1.province as province_from, a2.province as province_to, f.plane_code as plane_code"
            " FROM airports a1 JOIN flights f ON a1.airport_id = f.departure_airport JOIN airports a2 ON a2.airport_id = f.arrival_airport"
            " WHERE a1.province=:provincefrom AND a2.province=:provinceto AND date(f.departure_time)=:departure")
        connection = engine.connect()
        outbound_return = connection.execute(s, provincefrom=flyFrom, provinceto=flyTo, departure=flyDepDate)
        connection.close()
        return render_template('booking.html', active_menu=0, book_outbound=False, results_return=outbound_return,
                               logged_in=current_user.is_authenticated)
    return redirect(url_for('main.homepage'))

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from platypos.models import *

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')


@main.route('/')
@main.route('/home')
def homepage():
    connection = engine.connect()
    dynamiclist = connection.execute(select([airports.c.province]). \
                                     order_by(airports.c.province). \
                                     distinct())
    connection.close()
    return render_template('home.html', active_menu=0, dynamiclist=dynamiclist, logged_in=current_user.is_authenticated)


@main.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        flyFrom = None
        flyTo = None
        flyType = None
        flyDepDate = None
        flyReturnDate = None
        if request.form['search'] == 'True':
            flyFrom = request.form['fly_from']
            flyTo = request.form['fly_to']
            # Valori possibli di flyght_type sono oneway e roundtrip
            flyType = request.form['flight_type']
            flyDepDate = request.form['fly_dep_date']
            if flyType == 'roundtrip':
                flyReturnDate = request.form['fly_return_date']
        else:
            if request.form['book_outbound'] == 'True':
                if request.form['return'] == 'True':
                    seat_list = request.form['seats'].split('-')
                    connection = engine.connect()
                    connection.execute(bookings.insert(), seat_number=seat_list[1], seat_column=seat_list[0], user_id=current_user.get_id(),
                                       flight_code=request.form['flight_code'])
                    connection.close()
                    flyFrom = request.form['province_to']
                    flyTo = request.form['province_from']
                    flyDepDate = request.form['fly_return_date']
        if request.form['book_return'] == 'False':
            s = text(
                "SELECT  f.flight_code as flight_code ,a1.name as departure_airport , a2.name as arrival_airport , f.departure_time as departure_time, f.arrival_time as arrival_time, a1.province as province_from, a2.province as province_to, f.plane_code as plane_code, p.seats as seats"
                " FROM airports a1 JOIN flights f ON a1.airport_id = f.departure_airport JOIN airports a2 ON a2.airport_id = f.arrival_airport JOIN airplanes p ON f.plane_code=p.plane_code"
                " WHERE a1.province=:provincefrom AND a2.province=:provinceto AND date(f.departure_time)=:departure")
            connection = engine.connect()
            outbound = connection.execute(s, provincefrom=flyFrom, provinceto=flyTo, departure=flyDepDate)
            booked_flights = connection.execute(select([bookings.c.flight_code.distinct()]). \
                                                order_by(bookings.c.flight_code))
            booked_seats = {}
            column_char = ['A', 'B', 'C', 'D', 'E']
            for flight in booked_flights:
                booked_seats[flight['flight_code']] = []
                temp_list = []
                seats = connection.execute(select([bookings.c.seat_column, bookings.c.seat_number]). \
                                           where(bookings.c.flight_code == flight['flight_code']))
                for row in seats:
                    merge = row['seat_column'] + str(row['seat_number'])
                    temp_list.append(merge)
                booked_seats[flight['flight_code']] = temp_list
            connection.close()
            if request.form['search'] == 'True':
                return render_template('booking.html', active_menu=0, flyReturnDate=flyReturnDate, book_outbound=True,
                                       results=outbound, booked_seats=booked_seats, column_char=column_char,
                                       logged_in=current_user.is_authenticated)
            else:
                return render_template('booking.html', active_menu=0, book_outbound=False,
                                       results=outbound,
                                       booked_seats=booked_seats, column_char=column_char,
                                       logged_in=current_user.is_authenticated)
        else:
            seat_list = request.form['seats'].split('-')
            connection = engine.connect()
            connection.execute(bookings.insert(), seat_number=seat_list[1], seat_column=seat_list[0], user_id=current_user.get_id(),
                               flight_code=request.form['flight_code'])
            connection.close()
    return redirect(url_for('main.homepage'))

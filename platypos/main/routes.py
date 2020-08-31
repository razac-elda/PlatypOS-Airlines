from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from platypos.models import *

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')


@main.route('/')
@main.route('/home')
def homepage():
    # Query per ottenere le provincie degli aeroporti
    with engine.connect().execution_options(isolation_level="READ COMMITTED") as connection:
        dynamiclist = connection.execute(select([airports.c.province]). \
                                         order_by(airports.c.province). \
                                         distinct())

        flights_presents = connection.execute(
            "SELECT  f.flight_code as flight_code ,a1.name as departure_airport , a2.name as arrival_airport , f.departure_time as departure_time, f.arrival_time as arrival_time,"
            " a1.province as province_from, a2.province as province_to, f.plane_code as plane_code, p.seats as seats"
            " FROM airports a1 JOIN flights f ON a1.airport_id = f.departure_airport JOIN airports a2 ON a2.airport_id = f.arrival_airport JOIN airplanes p ON f.plane_code=p.plane_code"
            " WHERE f.departure_time > CURRENT_DATE"
            " LIMIT 5")
    return render_template('home.html', active_menu=0, dynamiclist=dynamiclist, logged_in=current_user.is_authenticated,
                           flights_presents=flights_presents)


@main.route('/prenotazione', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        flyFrom = None
        flyTo = None
        flyDepDate = None
        flyReturnDate = None
        # I valori sono stringhe 'True' o 'False' perchè sono campi hidden nei form
        # Nel caso si arrivi dalla home
        if request.form['search'] == 'True':
            flyFrom = request.form['fly_from']
            flyTo = request.form['fly_to']
            # Valori possibli di flyght_type sono oneway e roundtrip
            flyType = request.form['flight_type']
            flyDepDate = request.form['fly_dep_date']
            if flyType == 'roundtrip':
                flyReturnDate = request.form['fly_return_date']
        else:
            # Si deve prenotare il ritorno
            if request.form['book_outbound'] == 'True':
                if request.form['return'] == 'True':
                    # Separazione del campo seats in due campi separati per righa e colonna
                    seat_list = request.form['seats'].split('-')
                    # Inserimento del volo andata con isolamento SERIALIZABLE per assicurarsi il posto
                    with engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
                        connection.execute(bookings.insert(), seat_number=seat_list[1], seat_column=seat_list[0],
                                           user_id=current_user.get_id(),
                                           flight_code=request.form['flight_code'])

                    flyFrom = request.form['province_to']
                    flyTo = request.form['province_from']
                    flyDepDate = request.form['fly_return_date']
        # Questa sezione viene visualizzata una volta per solo andata e due volte per andata e ritono
        if request.form['book_return'] == 'False':
            s = text(
                " SELECT  f.flight_code as flight_code ,a1.name as departure_airport , a2.name as arrival_airport , f.departure_time as departure_time, f.arrival_time as arrival_time, a1.province as province_from, a2.province as province_to, f.plane_code as plane_code, p.seats as seats"
                " FROM airports a1 JOIN flights f ON a1.airport_id = f.departure_airport JOIN airports a2 ON a2.airport_id = f.arrival_airport JOIN airplanes p ON f.plane_code=p.plane_code"
                " WHERE a1.province=:provincefrom AND a2.province=:provinceto AND date(f.departure_time)=:departure"
            )
            # Vengono prelevati i vari attributi da mostrare all'utente per poter decidere il volo da prenotare
            # Viene utilizzato l'isolamento SERIALIZABLE a causa della selezione del posto
            with engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
                outbound = connection.execute(s, provincefrom=flyFrom, provinceto=flyTo, departure=flyDepDate)
                planned_flights = connection.execute(select([flights.c.flight_code.distinct()]). \
                                                     order_by(flights.c.flight_code))
                # I posti già prenotati vengono salvati in un dizionario {volo1:[posto1,posto2...], volo2...}
                booked_seats = {}
                column_char = ['A', 'B', 'C', 'D', 'E']
                # Viene creato il dizionario con chiave ogni volo esistente
                for flight in planned_flights:
                    booked_seats[flight['flight_code']] = []
                    temp_list = []
                    # Si prelevano i posti prenotati di un volo
                    seats = connection.execute(select([bookings.c.seat_column, bookings.c.seat_number]). \
                                               where(bookings.c.flight_code == flight['flight_code']))
                    # I posti vengono inseriti in una lista
                    for row in seats:
                        # Merge della stringa colonna e numero riga
                        merge = row['seat_column'] + str(row['seat_number'])
                        temp_list.append(merge)
                    # Inserimento nella posizione del volo x la sua lista di posti prenotati che verranno eliminati
                    # dalle possibili scelte
                    booked_seats[flight['flight_code']] = temp_list
            # Visualizzazione della pagina come andata o ritorno
            permission = -1
            if current_user.is_authenticated:
                permission = current_user.get_permission()
            if request.form['search'] == 'True':
                return render_template('booking.html', active_menu=0, flyReturnDate=flyReturnDate, book_outbound=True,
                                       results=outbound, booked_seats=booked_seats, column_char=column_char,
                                       logged_in=current_user.is_authenticated,
                                       permission=permission)
            else:
                return render_template('booking.html', active_menu=0, book_outbound=False,
                                       results=outbound,
                                       booked_seats=booked_seats, column_char=column_char,
                                       logged_in=current_user.is_authenticated,
                                       permission=permission)
        else:
            # Inserimento di sola andata oppure ritorno dell'andata con ritorno
            seat_list = request.form['seats'].split('-')
            with engine.connect().execution_options(isolation_level="SERIALIZABLE") as connection:
                connection.execute(bookings.insert(), seat_number=seat_list[1], seat_column=seat_list[0],
                                   user_id=current_user.get_id(),
                                   flight_code=request.form['flight_code'])
    return redirect(url_for('main.homepage'))

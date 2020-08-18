from sqlalchemy import *

# Scegliere il db da usare, ci sono cose che funzionano diversamente tra i db

# La password è quella che chiede quando si installa postgres, mettere "passwordsupersegreta" per facilitare lo sviluppo
# "platypos_airlines" è il nome del db da creare da shell o pgadmin4
# Da fare: pip install psycopg2
uri = 'postgres+psycopg2://postgres:passwordsupersegreta@localhost:5432/test'
engine = create_engine(uri, echo=True)

# Per TESTARE in memoria con SQLite, serve il parametro check_same_thread
# uri = 'sqlite:///:memory:'
# engine = create_engine(uri, echo=True, connect_args={"check_same_thread": False})

metadata = MetaData()

# Dichiarare le tabelle cosi, cercatevi i parametri
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('email', String(254), unique=True, nullable=False),
              Column('password', String(128), nullable=False),
              Column('name', String(255), nullable=False),
              Column('surname', String(255), nullable=False),
              )

airports = Table('airports', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('city', String(255)),
                 Column('country', String(255)),
                 Column('name', String(255)),
                 )

airplanes = Table('airplanes', metadata,
                  Column('planeCode', Integer, primary_key=True),
                  Column('aviableSeats', Integer),
                  )

flights = Table('flights', metadata,
                Column('flightCode', Integer, primary_key=True),
                Column('departureTime', TIMESTAMP),
                Column('arrivalTime', TIMESTAMP),
                Column('departureAirport', String(255), ForeignKey(airports.id)),
                Column('arrivalAirport', String(255), ForeignKey(airports.id)),
                Column('planeCode', Integer, ForeignKey(airplanes.planeCode)),
                )

book = Table('book', metadata,
             Column('flightCode', Integer, ForeignKey(flights.flightCode)),
             Column('seat', Integer, ),
             Column('idUser', Integer, ForeignKey('users.id')),
             Column('idBook', Integer, primary_key=True),
             )

metadata.create_all(engine)
connection = engine.connect()

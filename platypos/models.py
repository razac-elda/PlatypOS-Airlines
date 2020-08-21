from flask_login import UserMixin
from sqlalchemy import *


class User(UserMixin):
    def __init__(self, id, email, pwd):
        self.id = id
        self.email = email
        self.pwd = pwd
        self.authenticated = False

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


uri = 'postgres+psycopg2://postgres:passwordsupersegreta@localhost:5432/platypos_airlines'
engine = create_engine(uri, echo=True)

metadata = MetaData()

users = Table('users', metadata,
              Column('user_id', Integer, primary_key=True),
              Column('email', String(254), unique=True, nullable=False),
              Column('password', String(128), nullable=False),
              Column('name', String(255), nullable=False),
              Column('surname', String(255), nullable=False),
              )

airports = Table('airports', metadata,
                 Column('airport_id', Integer, primary_key=True),
                 Column('name', String(255), nullable=False),
                 Column('city', String(255), nullable=False),
                 Column('province', String(255), nullable=False),
                 )

airplanes = Table('airplanes', metadata,
                  Column('plane_code', Integer, primary_key=True),
                  Column('seats', Integer, nullable=False),
                  )

flights = Table('flights', metadata,
                Column('flight_code', Integer, primary_key=True),
                Column('departure_time', DateTime, nullable=False),
                Column('arrival_time', DateTime, nullable=False),
                Column('departure_airport', Integer, ForeignKey('airports.airport_id')),
                Column('arrival_airport', Integer, ForeignKey('airports.airport_id')),
                Column('plane_code', Integer, ForeignKey('airplanes.plane_code')),
                )

bookings = Table('bookings', metadata,
                 Column('bookingId', Integer, primary_key=True),
                 Column('seatNumber', Integer, nullable=False),
                 Column('userId', Integer, ForeignKey('users.user_id')),
                 Column('flightCode', Integer, ForeignKey('flights.flight_code')),
                 )

metadata.create_all(engine)

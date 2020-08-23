from flask_login import UserMixin
from sqlalchemy import *


# Classe User per flask-login

class User(UserMixin):
    def __init__(self, id, email, name, surname, pwd):
        self.id = id
        self.email = email
        self.name = name
        self.surname = surname
        self.pwd = pwd
        self.authenticated = False

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def get_mail(self):
        return text(self.email)

    def get_name(self):
        return text(self.name)

    def get_surname(self):
        return text(self.surname)

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


# Nome utente, password e DB da modificare in base alle esigenze
uri = 'postgres+psycopg2://postgres:passwordsupersegreta@localhost:5432/platypos_airlines'
engine = create_engine(uri, echo=True)

metadata = MetaData()

# Schema DB

users = Table('users', metadata,
              Column('user_id', Integer, primary_key=True),
              Column('email', String(254), unique=True, nullable=False),
              Column('password', String(60), nullable=False),
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
                 Column('booking_id', Integer, primary_key=True),
                 Column('seat_number', Integer, nullable=False),
                 Column('user_id', Integer, ForeignKey('users.user_id')),
                 Column('flight_code', Integer, ForeignKey('flights.flight_code')),
                 )

metadata.create_all(engine)

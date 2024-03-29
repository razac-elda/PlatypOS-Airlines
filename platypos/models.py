from flask_login import UserMixin
from sqlalchemy import *


# Classe User per flask-login


class User(UserMixin):
    def __init__(self, id, email, name, surname, pwd, permission_level):
        self.id = id
        self.email = email
        self.name = name
        self.surname = surname
        self.pwd = pwd
        self.permission_level = permission_level
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

    def get_permission(self):
        return self.permission_level

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


# Nome utente, password e DB da modificare in base alle esigenze
uri = 'postgres+psycopg2://postgres:passwordsupersegreta@localhost:5432/platypos_airlines'
engine = create_engine(uri)

metadata = MetaData()

# Schema DB

users = Table('users', metadata,
              Column('user_id', Integer, primary_key=True),
              Column('email', String(254), unique=True, nullable=False),
              Column('password', String(60), nullable=False),
              Column('name', String(255), nullable=False),
              Column('surname', String(255), nullable=False),
              Column('permission_level', Integer, default=0),
              )

airports = Table('airports', metadata,
                 Column('airport_id', Integer, primary_key=True),
                 Column('name', String(255), nullable=False),
                 Column('city', String(255), nullable=False),
                 Column('province', String(255), nullable=False),
                 )

airplanes = Table('airplanes', metadata,
                  Column('plane_code', Integer, primary_key=True),
                  Column('seats', Integer, CheckConstraint('seats>0'), nullable=False),
                  )

flights = Table('flights', metadata,
                Column('flight_code', Integer, primary_key=True),
                Column('departure_time', DateTime, nullable=False),
                Column('arrival_time', DateTime, nullable=False),
                Column('departure_airport', Integer, ForeignKey('airports.airport_id')),
                Column('arrival_airport', Integer, ForeignKey('airports.airport_id')),
                Column('plane_code', Integer, ForeignKey('airplanes.plane_code')),
                CheckConstraint('arrival_time >= departure_time'),
                CheckConstraint('arrival_airport <> departure_airport')
                )

bookings = Table('bookings', metadata,
                 Column('booking_id', Integer, primary_key=True),
                 Column('seat_column', String(1), nullable=False),
                 Column('seat_number', Integer, nullable=False),
                 Column('user_id', Integer, ForeignKey('users.user_id')),
                 Column('flight_code', Integer, ForeignKey('flights.flight_code')),
                 UniqueConstraint('seat_column', 'seat_number', 'flight_code')
                 )

metadata.create_all(engine)

from sqlalchemy import *

uri = 'postgres+psycopg2://postgres:passwordsupersegreta@localhost:5432/platypos_airlines'
engine = create_engine(uri, echo=True)


# uri = 'sqlite:///:memory:'
# engine = create_engine(uri, echo=True, connect_args={"check_same_thread": False})

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

# Date -> Postgres Date
# DateTime -> Postgres Timestamp without timezone
# Da scoprire cosa si puo inserire veramente
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

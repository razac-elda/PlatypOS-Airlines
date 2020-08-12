from sqlalchemy import *

# Scegliere il db da usare, ci sono cose che funzionano diversamente tra i db

# La password è quella che chiede quando si installa postgres, mettere "passwordsupersegreta" per facilitare lo sviluppo
# "platypos_airlines" è il nome del db da creare da shell o pgadmin4
# Da fare: pip install psycopg2
# uri = 'postgres+psycopg2://postgres:passwordsupersegreta@localhost:5432/platypos_airlines'
# engine = create_engine(uri, echo=True)

# Per TESTARE in memoria con SQLite, serve il parametro check_same_thread
uri = 'sqlite:///:memory:'
engine = create_engine(uri, echo=True, connect_args={"check_same_thread": False})

metadata = MetaData()

# Dichiarare le tabelle cosi, cercatevi i parametri
users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('email', String(254), unique=True, nullable=False),
              Column('password', String(128), nullable=False),
              Column('name', String(255), nullable=False),
              Column('surname', String(255), nullable=False),
              )

metadata.create_all(engine)
connection = engine.connect()

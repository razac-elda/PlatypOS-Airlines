from platypos import login_manager
from platypos.models import *


@login_manager.user_loader
def load_user(uid):
    # Vengono prelevati i dati di un utente per la creazione di un istanza di User
    # READ COMMITTED è sufficiente perchè l'utente che si logga avrà già un account
    with engine.connect().execution_options(isolation_level="READ COMMITTED") as connection:
        result = connection.execute(select([users]). \
                                    where(users.c.user_id == uid))
    email = None
    name = None
    surname = None
    psw = None
    permission_level = None
    for row in result:
        email = row['email']
        name = row['name']
        surname = row['surname']
        psw = row['password']
        permission_level = row['permission_level']
    return User(uid, email, name, surname, psw, permission_level)

from platypos import login_manager
from platypos.models import *


@login_manager.user_loader
def load_user(uid):
    connection = engine.connect()
    result = connection.execute(select([users]). \
                                where(users.c.user_id == uid))
    email = None
    name = None
    surname = None
    psw = None
    for row in result:
        email = row['email']
        name = row['name']
        surname = row['surname']
        psw = row['password']
    return User(uid, email, name, surname, psw)

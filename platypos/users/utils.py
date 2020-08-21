from platypos.models import *
from platypos import login_manager


@login_manager.user_loader
def load_user(email):
    connection = engine.connect()
    result = connection.execute(select([users.c.user_id, users.c.password]). \
                                where(users.c.email == email))
    id = ''
    psw = ''
    for row in result:
        id = row['user_id']
        psw = row['password']
    return User(id, email, psw)

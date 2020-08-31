from connections import *

def setUserCount():
    db.execute("SELECT COUNT(id) FROM users WHERE id != 4")
    count = db.fetchone()
    count = int(count[0])
    r.set('ripple:registered_users', count, 0)

    print('Registered Users: Done!')
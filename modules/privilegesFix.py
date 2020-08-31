from connections import *

def fixPrivileges():
    db.execute('UPDATE users SET privileges = 1048576 WHERE privileges > 955252735 AND ban_datetime = 0 AND id > 5')
    print('Privileges Fix: Done!')
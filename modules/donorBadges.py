import time
import config
from connections import *

def checkBadges():
    current = int(time.time())
    db.execute(f'SELECT id, username FROM users WHERE privileges = 7 AND donor_expire > {current}')
    badges = db.fetchall()
    for user in badges:
        db.execute(f'SELECT can_custom_badge, id FROM users_stats WHERE id = {user[0]}')
        can = db.fetchall()
        for give in can:
            if give[0] == 0:
                db.execute(f'SELECT username FROM users WHERE id = {give[1]}')
                username = db.fetchall()
                print(f'Allowing badge permissions to {username[0]}...')
                db.execute(f'UPDATE users_stats SET can_custom_badge = 1 WHERE id = {give[1]}')

    print('Donor Badges: Done!')
    
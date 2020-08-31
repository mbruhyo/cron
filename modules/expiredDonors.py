import time
import config
from connections import *

def removeDonor():
    current = int(time.time())
    db.execute(f'SELECT id, username FROM users WHERE privileges = 7 AND donor_expire < {current}')
    expired = db.fetchall()
    for user in expired:
        print(f'Removing donor privileges from {user[1]}...')
        db.execute(f'UPDATE users SET privileges = 3 AND donor_expire = 0 WHERE id = {user[0]}')
        db.execute(f'UPDATE users_stats SET can_custom_badge = 0 AND show_custom_badge = 0 WHERE id = {user[0]}')
        db.execute(f'DELETE FROM user_badges WHERE badge = {config.DonorBadgeID} AND user = {user[0]}')

    print('Expired Donors: Done!')
    
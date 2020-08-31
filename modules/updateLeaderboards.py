from connections import *
import time

def updateLeaderboards():
    r.delete(r.keys("ripple:leaderboard:*"))

    for gamemode in ['std', 'taiko', 'ctb', 'mania']:
        db.execute(f'SELECT users_stats.id, users_stats.pp_{gamemode}, users_stats.country, users.latest_activity FROM users_stats LEFT JOIN users ON users.id = users_stats.id WHERE users_stats.pp_{gamemode} > 0 AND users.privileges > 2 ORDER BY pp_{gamemode} DESC')

        timee = int(time.time())
        for stats in db.fetchall():
            userID = int(stats[0])
            pp = int(stats[1])
            country = stats[2].lower()
            activity = int(stats[3])
            inactivity = (timee - activity) / 60 / 60 / 24

            if inactivity < 60:
                r.zadd(f'ripple:leaderboard:{gamemode}', userID, pp)
                if country != 'xx':
                    r.zincrby('hanayo:country_list', country, 1)
                    r.zadd(f'ripple:leaderboard:{gamemode}:{country}', userID, pp)

    print('Vanilla Leaderboards: Done!')

from connections import *
import time

def updateLeaderboardsRX():
    r.delete(r.keys("ripple:leaderboard_relax:*"))

    for gamemode in ['std', 'taiko', 'ctb']:
        db.execute(f'SELECT rx_stats.id, rx_stats.pp_{gamemode}, rx_stats.country, users.latest_activity FROM rx_stats LEFT JOIN users ON users.id = rx_stats.id WHERE rx_stats.pp_{gamemode} > 0 AND users.privileges > 2 ORDER BY pp_{gamemode} DESC')

        timee = int(time.time())
        for stats in db.fetchall():
            userID = int(stats[0])
            pp = int(stats[1])
            country = stats[2].lower()
            activity = int(stats[3])
            inactivity = (timee - activity) / 60 / 60 / 24

            if inactivity < 60:
                r.zadd(f'ripple:leaderboard_relax:{gamemode}', userID, pp)
                if country != 'xx':
                    r.zincrby('hanayo:country_list', country, 1)
                    r.zadd(f'ripple:leaderboard_relax:{gamemode}:{country}', userID, pp)

    print('Relax Leaderboards: Done!')

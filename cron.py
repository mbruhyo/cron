import os
import mysql.connector
import redis
import shutil

if not os.path.isfile('config.ini'):
    if not os.path.isfile('config.sample.ini'):
        print('Config generation failed! Please ensure all files were cloned/downloaded correctly and run cron again.')
        exit()
    else:
        shutil.copyfile('config.sample.ini', 'config.ini')
        print('Config generated! Please edit the config and run cron again.')
        exit()

with open(f'{os.path.dirname(os.path.realpath(__file__))}/config.ini', 'r') as file:
    config = file.read().splitlines()

for _line in config:
    if not _line: continue
    line = _line.split('=')
    cfg = line[0].rstrip()
    val = line[1].lstrip()

    if cfg == 'DBUsername':
	    DBUsername = val
    elif cfg == 'DBPassword':
	    DBPassword = val
    elif cfg == 'DBHost':
	    DBHost = val
    elif cfg == 'DBDatabase':
	    DBDatabase = val
    elif cfg == 'RedisHost':
        RedisHost = val
    elif cfg == 'RedisPort':
        RedisPort = val
    elif cfg == 'HasRelax':
        HasRelax = val
    elif cfg == 'HasAutopilot':
        HasAutopilot = val

if any(not cnf for cnf in [DBUsername, DBPassword, DBHost, DBDatabase, RedisHost, RedisPort, HasRelax, HasAutopilot]):
    print('Not all configuration values have been found. Please make sure none are missing and run cron again.')
    exit()

# Grab required databases
sql = mysql.connector.connect(user=DBUsername, password=DBPassword, host=DBHost, database=DBDatabase, autocommit=True)
db = sql.cursor()
r = redis.Redis(host=RedisHost, port=RedisPort, db=0)

def updateLeaderboards():
    print('Calculating vanilla leaderboards for all modes...')

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
                
    print('Calculating vanilla leaderboards complete!')

def updateLeaderboardsRX():
    print('Calculating relax leaderboards for compatible modes...')

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
                
    print('Calculating relax leaderboards complete!')

def updateLeaderboardsAuto():
    print('Calculating autopilot leaderboards...')

    r.delete(r.keys("ripple:leaderboard_ap:*"))

    for gamemode in ['std', 'taiko', 'ctb']:
        db.execute(f'SELECT ap_stats.id, ap_stats.pp_{gamemode}, ap_stats.country, users.latest_activity FROM ap_stats LEFT JOIN users ON users.id = ap_stats.id WHERE ap_stats.pp_{gamemode} > 0 AND users.privileges > 2 ORDER BY pp_{gamemode} DESC')

        timee = int(time.time())
        for stats in db.fetchall():
            userID = int(stats[0])
            pp = int(stats[1])
            country = stats[2].lower()
            activity = int(stats[3])
            inactivity = (timee - activity) / 60 / 60 / 24

            if inactivity < 60:
                r.zadd(f'ripple:leaderboard_ap:{gamemode}', userID, pp)
                if country != 'xx':
                    r.zincrby('hanayo:country_list', country, 1)
                    r.zadd(f'ripple:leaderboard_ap:{gamemode}:{country}', userID, pp)
                
    print('Calculating autopilot leaderboards complete!')

if __name__ == '__main__':
    print('Starting cron...')
    updateLeaderboards()
    if HasRelax:
        updateLeaderboardsRX()
    if HasAutopilot:
        updateLeaderboardsAuto()
    
    print('Cron completed.')
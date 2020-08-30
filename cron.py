import os
import mysql.connector
import redis
import shutil

if not os.path.isfile('config.ini'):
    shutil.copyfile('config.sample.ini', 'config.ini')
    if not os.path.isfile('config.sample.ini'):
        print('Config generation failed! Please ensure all files were cloned/downloaded correctly and run cron again.')
        exit()
    else:
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

# Grab required databases
sql = mysql.connector.connect(user=DBUsername, password=DBPassword, host=DBHost, database=DBDatabase, autocommit=True)
db = sql.cursor()
r = redis.Redis(host=RedisHost, port=RedisPort, db=0)

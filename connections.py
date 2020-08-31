import mysql.connector
import redis
import config

config.ensureConfig()
config.getConfig()
if config.configExists and config.configValid:
    sql = mysql.connector.connect(user=config.DBUsername, password=config.DBPassword, host=config.DBHost, database=config.DBDatabase, autocommit=True)
    db = sql.cursor()
    r = redis.Redis(host=config.RedisHost, port=config.RedisPort, db=0)
    global connectionsFailed
    connectionsFailed = False
else:
    connectionsFailed = True

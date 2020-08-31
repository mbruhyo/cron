import os

def ensureConfig():
    if not os.path.isfile('config.ini'):
        if not os.path.isfile('config.sample.ini'):
            print('Config generation failed! Please ensure all files were cloned/downloaded correctly and run cron again.')
        else:
            shutil.copyfile('config.sample.ini', 'config.ini')
            print('Config generated! Please edit the config and run cron again.')
        global configExists
        configExists = False
    else:
        configExists = True

def getConfig():
    with open(f'{os.path.dirname(os.path.realpath(__file__))}/config.ini', 'r') as file:
        config = file.read().splitlines()

    for _line in config:
        if not _line: continue
        line = _line.split('=')
        cfg = line[0].rstrip()
        val = line[1].lstrip()

        if cfg == 'DBUsername':
	        global DBUsername
	        DBUsername = val
        elif cfg == 'DBPassword':
	        global DBPassword
	        DBPassword = val
        elif cfg == 'DBHost':
	        global DBHost
	        DBHost = val
        elif cfg == 'DBDatabase':
	        global DBDatabase
	        DBDatabase = val
        elif cfg == 'RedisHost':
	        global RedisHost
	        RedisHost = val
        elif cfg == 'RedisPort':
	        global RedisPort
	        RedisPort = val
        elif cfg == 'HasRelax':
	        global HasRelax
	        HasRelax = val
        elif cfg == 'HasAutopilot':
	        global HasAutopilot
	        HasAutopilot = val
        elif cfg == 'DonorBadgeID':
	        global DonorBadgeID
	        DonorBadgeID = val

    if any(not cnf for cnf in [DBUsername, DBPassword, DBHost, DBDatabase, RedisHost, RedisPort, HasRelax, HasAutopilot, DonorBadgeID]):
        global configValid
        configValid = False
        print('Some config values are missing! Please check your config and try again.')
    else:
        configValid = True

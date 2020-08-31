import config
import connections
from modules.updateLeaderboards import updateLeaderboards
from modules.updateLeaderboardsRX import updateLeaderboardsRX
from modules.updateLeaderboardsAuto import updateLeaderboardsAuto
from modules.userCount import setUserCount

if __name__ == '__main__':
    print('Starting cron...')
    config.ensureConfig()
    config.getConfig()
    if not config.configExists:
        exit()
    elif not config.configValid:
        exit()
    elif connections.connectionsFailed:
        exit()
    elif not config.configExists and not config.configValid and connections.connectionsFailed:
        exit()
    else:
        updateLeaderboards()
        if config.HasRelax:
            updateLeaderboardsRX()
        if config.HasAutopilot:
            updateLeaderboardsAuto()
        setUserCount()
        print('Cron completed.')

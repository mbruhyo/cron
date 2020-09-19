import config
import connections
from modules.updateLeaderboards import updateLeaderboards
from modules.updateLeaderboardsRX import updateLeaderboardsRX
from modules.updateLeaderboardsAuto import updateLeaderboardsAuto
from modules.userCount import setUserCount
from modules.expiredDonors import removeDonor
from modules.donorBadges import checkBadges
from modules.unrankedScores import removeUnrankedScores
from modules.unrankedScoresRX import removeUnrankedScoresRX
from modules.unrankedScoresAuto import removeUnrankedScoresAuto
from modules.qualifiedMaps import rankQualified
from modules.expiredFrozen import freezeUsers
from modules.privilegesFix import fixPrivileges
from modules.negativeFix import fixNegatives
from modules.negativeFixRX import fixNegativesRX
from modules.negativeFixAuto import fixNegativesAuto

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
        removeDonor()
        checkBadges()
        removeUnrankedScores()
        if config.HasRelax:
            removeUnrankedScoresRX()
        if config.HasAutopilot:
            removeUnrankedScoresAuto()
        if config.RankQualifiedMaps:
            rankQualified()
        if config.HasFrozen:
            freezeUsers()
        if config.PanelPrivileges:
            fixPrivileges()
        fixNegatives()
        if config.HasRelax:
            fixNegativesRX()
        if config.HasAutopilot:
            fixNegativesAuto()
        print('Cron completed!')

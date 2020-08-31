from connections import *

def removeUnrankedScoresAuto():
    db.execute(f'SELECT scores_ap.id, scores_ap.beatmap_md5 FROM scores_ap JOIN beatmaps USING(beatmap_md5) WHERE scores_ap.completed = 3 AND beatmaps.ranked < 2')
    remove = db.fetchall()
    for scores in remove:
        db.execute(f'SELECT song_name FROM beatmaps WHERE beatmap_md5 = "{scores[1]}"')
        name = db.fetchall()
        print(f'Removing Autopilot score ID {scores[0]} from {name[0][0]}...')
        db.execute(f'UPDATE scores_ap SET pp = 0 WHERE id = {scores[0]}')
    
    print('Unranked Autopilot Scores: Done!')
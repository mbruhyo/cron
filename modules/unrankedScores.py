from connections import *

def removeUnrankedScores():
    db.execute(f'SELECT scores.id, scores.beatmap_md5 FROM scores JOIN beatmaps USING(beatmap_md5) WHERE scores.completed = 3 AND beatmaps.ranked < 2')
    remove = db.fetchall()
    for scores in remove:
        db.execute(f'SELECT song_name FROM beatmaps WHERE beatmap_md5 = "{scores[1]}"')
        name = db.fetchall()
        print(f'Removing Vanilla score ID {scores[0]} from {name[0][0]}...')
        db.execute(f'UPDATE scores SET pp = 0 WHERE id = {scores[0]}')
    
    print('Unranked Vanilla Scores: Done!')
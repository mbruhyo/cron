from connections import *

def removeUnrankedScoresRX():
    db.execute(f'SELECT scores_relax.id, scores_relax.beatmap_md5 FROM scores_relax JOIN beatmaps USING(beatmap_md5) WHERE scores_relax.completed = 3 AND beatmaps.ranked < 2')
    remove = db.fetchall()
    for scores in remove:
        db.execute(f'SELECT song_name FROM beatmaps WHERE beatmap_md5 = "{scores[1]}"')
        name = db.fetchall()
        print(f'Removing Relax score ID {scores[0]} from {name[0][0]}...')
        db.execute(f'UPDATE scores_relax SET pp = 0 WHERE id = {scores[0]}')
    
    print('Unranked Relax Scores: Done!')
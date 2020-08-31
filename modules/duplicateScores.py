# I fucking hate this file please james fix this in the future JESUS
from connections import *

def fixDuplicates():
    db.execute('SELECT id, beatmap_md5, userid, score, max_combo, mods, play_mode, accuracy, COUNT(*) a FROM scores WHERE completed = 3 GROUP BY id, beatmap_md5, userid, score, max_combo, mods, play_mode, accuracy HAVING a > 1')
    duplicates = db.fetchall()
    for row in duplicates:
        print(f'Found duplicate score ID {row[0]}')
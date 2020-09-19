from connections import *

def rankQualified():
    db.execute(f'SELECT beatmap_md5, song_name FROM beatmaps WHERE ranked = 4')
    maps = db.fetchall()
    for fix in maps:
        print(f'Ranking qualified map {fix[1]}...')
        db.execute(f'UPDATE beatmaps SET ranked = 2 WHERE beatmap_md5 = "{fix[0]}"')

    print('Qualified Maps: Done!')
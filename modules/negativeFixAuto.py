from connections import *

def fixNegativesAuto():
    db.execute('UPDATE ap_stats SET ranked_score_ctb = ABS(ranked_score_ctb) WHERE ranked_score_ctb < 0')
    db.execute('UPDATE ap_stats SET ranked_score_std = ABS(ranked_score_std) WHERE ranked_score_std < 0')
    db.execute('UPDATE ap_stats SET ranked_score_mania = ABS(ranked_score_mania) WHERE ranked_score_mania < 0')
    db.execute('UPDATE ap_stats SET ranked_score_taiko = ABS(ranked_score_taiko) WHERE ranked_score_taiko < 0')
    print('Autopilot Negatives Fix: Done!')
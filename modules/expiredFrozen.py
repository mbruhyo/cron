import time
import webhook
from connections import *
from config import *

def freezeUsers():
    bantime = int(time.time())
    db.execute("SELECT id, username FROM users WHERE freezedate < %s AND frozen = 1 AND privileges > 2", (bantime,))
    checkfrozen = db.fetchall()
    id = checkfrozen
    reason = "Auto-restricted for not submitting a liveplay upon request."
    if id is not None:
        for row in checkfrozen:
            user = row[0]
            name = row[1]
            print(f"Restricting {name} for expired freeze timer...")
            db.execute("UPDATE users SET privileges = 2, ban_datetime = %s WHERE id = %s", (bantime, user))
            if config.Webhook is not None:
                db.execute("UPDATE users SET notes = %s WHERE id = %s", (reason, user))
                logs = "has auto-restricted " + name + " for not submitting a liveplay upon request."
                db.execute("INSERT INTO `rap_logs` (`id`, `userid`, `text`, `datetime`, `through`) VALUES (NULL, '4', %s, %s, 'Misumi Admin Panel')", (logs, bantime))
                webhookdesp = "{} has been autorestricted from failing to provide a liveplay".format(name)
                webhook = webhook.Webhook(config.Webhook, color=0xadd8e6, footer="Misumi Anti Cheat")
                webhook.set_author(name='Nahoko', icon='https://a.misumi.me/4', url="https://misumi.me/u/4")
                webhook.set_title(title="osu!Misumi", url='https://misumi.me')
                webhook.set_desc(webhookdesp)
                webhook.post()
    print('Expired Freeze Timers: Done!')
import sopel
import redis
import unicodedata

bucket='rcarsvehicle'

@sopel.module.commands('vehicle')

def vehicle(bot, trigger):
    n=trigger.nick
    r=" has a: "
    l=""
    if not trigger.group(2):
        fetch=existdb(n.lower())
        if fetch:
            l=readdb(n.lower())
        else:
            r=": Tell me what vehicle you have: "
    else:
        t = unicodedata.normalize('NFKD', trigger.group(2)).encode('ascii', 'ignore').split(' ')
        if len(t) >= 1:
            if t[0] == 'set':
                if len(t) < 2:
                    r=': You forgot to tell me what vehicle you have!'
                else:
                    updatedbattr(n.lower(), trigger.group(2)[4:])
                    return bot.say('Saving your vehicle!')
            else:
                n=t[0].lower()
                fetch=existdb(n)
                if fetch:
                    l=readdb(n)
                else:
                    r=": Give me a vehicle with .vehicle set <vehicle type>"
    return bot.say(n + r + l)


def readdb(key):
    r=redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)
    modkey = bucket + key
    print r.get(modkey)
    return b.get(modkey)


def existdb(key):
    r=redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)
    modkey = bucket + key
    return r.exists(modkey)


def updatedbattr(key, data):
    r=redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)
    modkey = bucket + key
    r.set(modkey, data)

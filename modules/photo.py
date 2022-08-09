import sopel
import redis
import unicodedata

bucket='rcarsphoto'

@sopel.module.commands('photo')


def photo(bot, trigger):
    n=trigger.nick
    r="'s pride and joy looks like: "
    l=""
    if not trigger.group(2):
        fetch=existdb(n.lower())
        if fetch:
            l=readdb(n.lower())
        else:
            r=": Give me a photo URL with .photo set url"
    else:
        t = unicodedata.normalize('NFKD', trigger.group(2)).split(' ')
        if len(t) >= 1:
            if t[0] == 'set':
                if len(t) < 2:
                    r=': You forgot to give me the URL!'
                else:
                    updatedbattr(n.lower(), trigger.group(2)[4:])
                    return bot.say('Saving your photo!')
            else:
                n=t[0].lower()
                fetch=existdb(n)
                if fetch:
                    l=readdb(n)
                else:
                    r=": Give me a photo URL with .photo set url"
    return bot.say(n + r + l)

def readdb(key):
    r=redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)
    modkey = bucket + key
    return r.get(modkey)


def existdb(key):
    r=redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)
    modkey = bucket + key
    return r.exists(modkey)


def updatedbattr(key, data):
    r=redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)
    modkey = bucket + key
    r.set(modkey, data)

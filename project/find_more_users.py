__author__ = 'k.stroykova'

import os
import sys
import thread
import time
import twitter
import json

import nltk
from textblob import TextBlob
import traceback

MIN_STATUSES = 10




CONSUMER_KEY = "NIdJmEzKanvYMoZMQOLRIWGhu"
CONSUMER_SECRET = "OJVCVs1sG5RxOR1XRn30rj2x5BoPZvPzmSmA8kfLMBr2JjH5yZ"

ACCESS_TOKEN_KEY = "105892440-hiutXI6zWd1XjrQJaotg7GbW6Mt1gihXCnE4njZH"
ACCESS_TOKEN_SECRET = "RxIHlIylRycp8dPZfV8fXSM2WtMP74lteIp5P6jxwh4XW"

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)


r = [
    # "Bush", "#AllinForJeb", "#JebBush", "Carson", "#BC2DC16", "#ImWithBen", "#Carson2016", "#BenCarson", "Cruz",
    #   "#CruzCrew", "#TedCruz", "Fiorina", "#Carly2016", "#CarlyFiorina", "Graham", "#LindseyGraham",
     "Huckabee", "#MikeHuckabee", "Pataki", "#Pataki2016", "#GovernorPataki", "Paul", "#StandWithRand", "#RandPaul",
     "Perry", "#Perry2016", "#RickPerry", "Rubio", "#TeamMarcoFL", "#TeamMarcoPA", "#TeamMarcoSC", "#TeamMarco",
     "#MarcoRubio", "Santorum", "#Rick2016", "#SantorumCrowds", "#RickSantorum", "Trump", "#Trump", "#DonaldTrump",
     "#Trump2016", "#DonaldTrumpforPresient", '#tedcruz', '#cruz2016', '#choosecruz', '#GOPDebate', '#tcot', '#GOP',
     '#DemTownHall', '#MakeAmericaGreatAgain', '#teaparty'
     ]

d = ["Chafee", "#Chafee", "#LincolnChafee", "#Chafee2016", "Clinton", "#Hillary2016", "#HillaryClinton", "O'Malley",
     "#OMalley", "#OMalley2016", "#MartinOMalley", "Sanders", "Bernie", "#Sanders", "#BernieSanders", "#BernieSanders2016",
     "#Sanders2016", '#muslimsforbernie', '#democrats', '#berniewillwin', '#berniesandersforpresident',
     '#bernie4president', '#feelthebern', '#presidentbernie',
     '#berniesanders2016', '#voteforbernie', '#bernieisbae', '#berniesanders', '#bernie2016', '#jewsforbernie',
     '#bernie', '#latinosforbernie', '#orlandoforbernie', '#iowaforbernie',
     '#millennialsforbernie', '#womenforbernie', '#babesforbernie', '#swedesforbernie2016', '#unicornsforbernie',
     '#hillary', "#DemDebate", '#ImWithHer', '#DebateWithBernie', '#Obama', '#VoteTogether', '#p2', ]


r_h = set()
r_w = set()
for i in r:
    w = i.strip('#').lower()
    if i.startswith('#'):
        r_h.add(w)
    r_w.add(w)

print r_h
print r_w

d_h = set()
d_w = set()
for i in d:
    w = i.strip('#').lower()
    if i.startswith('#'):
        d_h.add(w)
    d_w.add(w)

print d_h
print d_w


kws = []

for k in d:
    kws.append(k.lower().strip('#'))

for k in r:
    kws.append(k.lower().strip('#'))


seen_users = set()
with open('classified_users') as f:
    for line in f:
        user, pol = line.split('\t')
        seen_users.add(int(user))


def parse_user(user_id):
    seen_users.add(int(user_id))

    retry = True
    br = False
    while retry:
        try:
            timeline = api.GetUserTimeline(user_id=user_id, trim_user=True, exclude_replies=True, count=200)
            retry = False
        except twitter.TwitterError as ex:
            if ex.message == u"Not authorized.":
                print "Not auth"
                br = True
                break

            if ex.message == "json decoding":
                br = True
                break

            msg = ex.message[0]
            if type(msg) == dict and 'code' in msg and msg['code'] == 88:
                sleep_time = api.GetSleepTime("statuses/user_timeline")
                print "sleep for ", sleep_time
                time.sleep(sleep_time)
                continue
            br = True
            break

    if br:
        return

    user_tweets = []

    for item in timeline:
        if item.lang != 'en':
            continue

        if item.retweeted:
            continue

        if item.truncated:
            continue

        if item.user_mentions:
            continue

        if item.media:
            continue

        if item.urls:
            continue

        user_tweets.append(item.AsDict())

    if len(user_tweets) > 10:
        return user_tweets

def classsify(tweets):

    user_polarity = 0
    polarities = []
    for t in tweets:

        is_d = False
        is_r = False
        if "hashtags" in t:
            for ht in t["hashtags"]:
                ht = ht.strip('#').lower()
                if ht in d_h:
                    is_d = True
                if ht in r_h:
                    is_r = True

        text = t['text'].lower()

        blob = TextBlob(text)
        if blob.sentiment.polarity == 0:
            continue

        lemmas = [w.lemma for w in blob.words]
        if any(l in d_w for l in lemmas):
            is_d = True
        if any(l in r_w for l in lemmas):
            is_r = True

        words = [w for w in blob.words]
        if any(l in d_w for l in words):
            is_d = True
        if any(l in r_w for l in words):
            is_r = True

        if is_d and is_r:
            continue

        if (not is_d) and (not is_r):
            continue

        if is_d:
            polarities.append(blob.sentiment.polarity)
        if is_r:
            polarities.append(-1 * blob.sentiment.polarity)

    if polarities:
        user_polarity = sum(polarities) / len(polarities)

    user_polarity = (user_polarity + 1) / 2.0

    return user_polarity

try:
    for kw in kws:
        print kw
        page = 0
        while True:
            print "page: ", page

            try:
                result = api.GetUsersSearch(kw, page=page)
            except twitter.TwitterError as ex:
                print ex.message[0]['message']
                traceback.format_exc()
                if ex.message[0]['code'] == 44:
                    break

                if ex.message[0]['code'] == 88:
                    sleep_time = api.GetSleepTime("users/search")
                    if sleep_time > 0:
                        print "Sleeping: %d" % (sleep_time / 60.0)
                        time.sleep(sleep_time)

                    continue

                print "some other error:", ex
                break
            except Exception as ex:
                print ex
                traceback.format_exc()
                break

            for user in result:
                if int(user.id) in seen_users:
                    continue

                if not user.lang or user.lang != 'en':
                    continue

                if not user.statuses_count or user.statuses_count < MIN_STATUSES:
                    continue

                user_tweets = parse_user(user.id)
                if not user_tweets:
                    continue

                polarity = classsify(user_tweets)
                if polarity != 0.5:
                    with open('new_users', 'a') as f:
                        f.write('{0}\t{1}\n'.format(int(user.id), polarity))

                print polarity
            page += 1


except Exception as ex:
    print traceback.format_exc()
    print ex

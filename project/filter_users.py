__author__ = 'k.stroykova'
import json
import twitter
import os
import time


CONSUMER_KEY = "ARbSfECKob6IqdKmlQKIG2Tl4"
CONSUMER_SECRET = "dUH9royJj0nzPlDWea33MZpZONKqV0YbY46Ht2OcFa7yMRa1U7"

ACCESS_TOKEN_KEY = "2979985961-3Sm5ljZ39YilsHwJ5q5LxsWfzFO07hnHGSH8Qul"
ACCESS_TOKEN_SECRET = "yI5oR83fTgDP2PujLKkK1euU976ucYHGdPGpB5GofA2ND"


api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)


users = 'politics_users'

users_filtered = 'politics_users_filtered'
users_seen = 'politics_users_seen'

users_found = set()


def write(f_name, data):
    with open(f_name, 'a') as f:
        f.write(data)


if os.path.exists(users_filtered):
    for line in open(users_filtered):
        if not line.strip():
            continue

        try:
            user, tweets = json.loads(line)
        except:
            print line
            raise
        users_found.add(user)


if os.path.exists(users_seen):
    for line in open(users_seen):
        l = line.strip()
        if not l:
            continue
        user = int(l)
        users_found.add(user)


str_idx = 0
count = 0
for line in open(users):
    print len(users_found)

    if not line.strip():
        continue

    str_idx += 1

    user = json.loads(line)
    user_id = user['id']
    if user_id in users_found:
        continue

    print user_id

    print "found:", str(len(users_found))
    print "filtered:", str(str_idx)
    print ""

    retry = True
    br = False
    while retry:
        try:
            timeline = api.GetUserTimeline(user_id=user_id, trim_user=True, exclude_replies=True, count=200)
            retry = False
        except twitter.TwitterError as ex:
            if ex.message == u"Not authorized.":
                write(users_seen, str(user_id) + '\n')
                print user_id
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
        continue

    write(users_seen, str(user_id) + '\n')

    users_found.add(user_id)

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
        write(users_filtered, json.dumps((user_id, user_tweets)) + '\n')
        print "found_user", user_id

    print len(users_found)

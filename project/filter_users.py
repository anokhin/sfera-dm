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


found_followers = set()


if os.path.exists("filtered_home.json_lines"):
    for line in open("filtered_home.json_lines"):
        if not line.strip():
            continue

        try:
            user, tweets = json.loads(line)
        except:
            print line
            raise
        found_followers.add(user)

    followers_file = open("filtered_home.json_lines", 'a')
else:
    followers_file = open("filtered_home.json_lines", 'w')

if os.path.exists("seen_home.list"):
    for line in open("seen_home.list"):
        l = line.strip()
        if not l:
            continue
        user = int(l)
        found_followers.add(user)
    seen_followers_file = open("seen_home.list", 'a')
else:
    seen_followers_file = open("seen_home.list", 'w')


str_idx = 0
count = 0
for line in open("home_users.json_lines"):
    print len(found_followers)

    if not line.strip():
        continue
    str_idx += 1
    if str_idx < 8000:
        continue

    user = json.loads(line)
    user_id = user['id']
    if user_id in found_followers:
        continue

    print user_id

    print "found:", str(len(found_followers))
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
                seen_followers_file.write(str(user_id))
                print user_id
                print "Not auth"
                br = True
                break

            if ex.message == "json decoding":
                br = True
                break

            print ex.args
            print ex.message

            if ex.message[0]['code'] == 88:
                sleep_time = api.GetSleepTime("statuses/user_timeline")
                print "sleep for ", sleep_time
                time.sleep(sleep_time)
                continue
            br = True
            break

    if br:
        continue

    seen_followers_file.write(str(user_id))
    seen_followers_file.write('\n')

    found_followers.add(user_id)

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
        followers_file.write(json.dumps((user_id, user_tweets)))
        followers_file.write("\n")
        print "found_user", user_id

    print len(found_followers)

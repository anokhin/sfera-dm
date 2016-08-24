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
                  access_token_secret=ACCESS_TOKEN_SECRET, sleep_on_rate_limit=True)


alive = set()
dead = set()
with open('../../data_sphere/all_list') as f:
    for line in f:
        alive.add(tuple(sorted(line.strip().lower().split())))
with open('../../data_sphere/dead_list') as f:
    for line in f:
        dead.add(tuple(sorted(line.strip().lower().split())))
alive = alive - dead
all_kw = alive | dead

users_f_name = '/home/stroykova/Dropbox/data_sphere/users'

filtered_users_f_name = "/home/stroykova/Dropbox/data_sphere/filtered_users"
alive_users_f_name = "/home/stroykova/Dropbox/data_sphere/alive_users"
dead_users_f_name = "/home/stroykova/Dropbox/data_sphere/dead_users"

users = set()
with open(users_f_name) as f:
    for line in f:
        if not line or line.isspace():
            continue
        try:
            user = json.loads(line)
        except Exception as ex:
            continue
        users.add(user['id'])
print 'total users', len(users)


def read_file(filename):

    users = set()
    if os.path.exists(filename):
        with open(filename) as f:
            for line in f:
                if not line.strip():
                    continue

                try:
                    user, tweets = json.loads(line)
                except:
                    continue

                users.add(user)

    f = open(filename, 'a')

    return f, users


filtered_file, filtered_users = read_file(filtered_users_f_name)
print 'filtered users', len(filtered_users)
alive_file, alive_users = read_file(alive_users_f_name)
print 'alive users', len(alive_users)
dead_file, dead_users = read_file(dead_users_f_name)
print 'dead users', len(dead_users)


def append_user(f, users_set, user, tweets):
    f.write(json.dumps((user, tweets)))
    f.write("\n")
    users_set.add(user)


for idx, user in enumerate(users):
    if idx % 100 == 0:
        print idx, 'of', len(users)
        print 'filtered users', len(filtered_users)
        print 'alive users', len(alive_users)
        print 'dead users', len(dead_users)

    if user in filtered_users:
        continue
    if user in alive_users:
        continue
    if user in dead_users:
        continue

    retry = True
    br = False
    while retry:
        try:
            timeline = api.GetUserTimeline(user_id=user, trim_user=False, include_rts=True, exclude_replies=False, count=1000)
            print len(timeline)
            retry = False
        except twitter.TwitterError as ex:
            if ex.message == u"Not authorized.":
                print "Not auth"
                br = True
                break

            if ex.message == "json decoding":
                br = True
                break

            print ex.args
            print ex.message

            if ex.message[0]['code'] == 88:
                sleep_time = 60
                print "sleep for ", sleep_time
                time.sleep(sleep_time)
                continue
            br = True
            break

        except IOError:
            sleep_time = 60
            print "sleep for ", sleep_time
            time.sleep(sleep_time)

    if br:
        continue

    user_tweets = []

    for item in timeline:
        if item.lang != 'en':
            continue

        user_tweets.append(item.AsDict())

    tweets_words = list()
    for ut in user_tweets:
        tweet_words = set()
        tweet_words.update(t.strip() for t in ut['text'].lower().split() if bool(t.strip()) and not t.isspace())
        hashtags = ' '.join(ht['text'] for ht in ut["hashtags"])
        tweet_words.update(t.strip() for t in hashtags.lower().split() if bool(t.strip()) and not t.isspace())
        tweets_words.append(tweet_words)

    is_dead = False
    is_alive = False

    for tokens in alive:
        is_alive |= any(all(t in tweet_words for t in tokens) and any(t in tweet_words for t in ('marvel', 'comics', 'hero', 'comic')) for tweet_words in tweets_words)
    for tokens in dead:
        is_dead |= any(all(t in tweet_words for t in tokens) and any(t in tweet_words for t in ('marvel', 'comics', 'hero', 'comic')) for tweet_words in tweets_words)

    print user, is_dead, is_alive
    if (is_dead and is_alive) or ((not is_dead) and (not is_alive)):
        append_user(filtered_file, filtered_users, user, user_tweets)
    elif is_dead:
        append_user(dead_file, dead_users, user, user_tweets)
    elif is_alive:
        append_user(alive_file, alive_users, user, user_tweets)

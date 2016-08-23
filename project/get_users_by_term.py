import os
import sys
import thread
import time
import twitter
import json
import random

MIN_STATUSES = 10

CONSUMER_KEY = "NIdJmEzKanvYMoZMQOLRIWGhu"
CONSUMER_SECRET = "OJVCVs1sG5RxOR1XRn30rj2x5BoPZvPzmSmA8kfLMBr2JjH5yZ"

ACCESS_TOKEN_KEY = "105892440-hiutXI6zWd1XjrQJaotg7GbW6Mt1gihXCnE4njZH"
ACCESS_TOKEN_SECRET = "RxIHlIylRycp8dPZfV8fXSM2WtMP74lteIp5P6jxwh4XW"

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


users_f_name = '../../data_sphere/users'


class UsersWriter:
    def __init__(self):
        self.users = set()
        try:
            with open(users_f_name) as f:
                for line in f:
                    if not line or line.isspace():
                        continue
                    user = json.loads(line)
                    self.users.add(user['id'])
        except Exception as ex:
            print line
            print ex
            pass

        print len(self.users)

        self.users_file = open(users_f_name, 'a')

    def write_user(self, user):
        if 'status' in user:
            del user['status']
        self.users_file.write('\n')
        self.users_file.write(json.dumps(user))

    def append_user(self, user):
        if user.id in self.users:
            return

        self.users.add(user.id)
        self.write_user(user.AsDict())

    def close(self):
        self.users_file.close()


def main():
    print "Data gathering via twitter API"

    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET, sleep_on_rate_limit=True)

    tweet_writer = UsersWriter()

    try:
        while all_kw:
            kw = random.sample(all_kw, 1)[0]
            kw = ' '.join(kw + ('marvel', 'comics'))
            print kw

            try:
                result = api.GetSearch(kw, count=10000)
            except twitter.TwitterError as ex:
                print ex.message[0]['message']
                if ex.message[0]['code'] == 44:
                    break
                if ex.message[0]['code'] == 88:
                    sleep_time = 100
                    print "sleep for ", sleep_time
                    time.sleep(sleep_time)
                    continue
            except IOError:
                sleep_time = 100
                print "sleep for ", sleep_time
                time.sleep(sleep_time)
                continue

            for status in result:
                # print user.id
                user = status.user
                if not user.lang or user.lang != 'en':
                    continue

                if not user.statuses_count or user.statuses_count < MIN_STATUSES:
                    continue

                # print "user found: %s" % user.id
                tweet_writer.append_user(user)

            print 'users found: %s' % len(tweet_writer.users)

    except Exception as ex:
        print ex
        tweet_writer.close()


if __name__ == "__main__":
    main()

import os
import sys
import thread
import time
import twitter
import json
import random
import time
import datetime
import urllib

MIN_STATUSES = 10

CONSUMER_KEY = "NIdJmEzKanvYMoZMQOLRIWGhu"
CONSUMER_SECRET = "OJVCVs1sG5RxOR1XRn30rj2x5BoPZvPzmSmA8kfLMBr2JjH5yZ"

ACCESS_TOKEN_KEY = "105892440-hiutXI6zWd1XjrQJaotg7GbW6Mt1gihXCnE4njZH"
ACCESS_TOKEN_SECRET = "RxIHlIylRycp8dPZfV8fXSM2WtMP74lteIp5P6jxwh4XW"

alive = set()
dead = set()

# base_path = "/home/stroykova/Dropbox/data_sphere/"
base_path = "/media/d_500/Dropbox/data_sphere/"

with open(base_path + 'all_list') as f:
    for line in f:
        alive.add(tuple(sorted(line.strip().lower().split())))

with open(base_path + 'dead_list') as f:
    for line in f:
        dead.add(tuple(sorted(line.strip().lower().split())))


alive = alive - dead

all_kw = alive | dead

users_f_name = base_path + 'users'

dt = time.mktime((datetime.datetime.now() - datetime.timedelta(30)).timetuple())


# # import requests
# import logging
#
# # These two lines enable debugging at httplib level (requests->urllib3->http.client)
# # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# # The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1
#
# # You must initialize logging, otherwise you'll not see debug output.
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True

# requests.get('https://httpbin.org/headers')


class UsersWriter:
    def __init__(self):
        self.users = set()
        if os.path.exists(users_f_name):
            with open(users_f_name) as f:
                for line in f:
                    if not line or line.isspace():
                        continue
                    try:
                        user = json.loads(line)
                    except Exception as ex:
                        print line
                        print ex
                        continue

                    self.users.add(user['id'])

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
            kw = ','.join(kw + ('marvel', 'comics'))

            print kw

            try:
                result = api.GetSearch(kw, count=10000, result_type='recent')
            except twitter.TwitterError as ex:
                if ex.message == "json decoding":
                    break

                print ex
                print ex.message[0]['message']
                if ex.message[0]['code'] == 44:
                    break
                if ex.message[0]['code'] == 88:
                    print ex.message
                    sleep_time = 60
                    print "sleep for ", sleep_time
                    time.sleep(sleep_time)
                    api = twitter.Api(consumer_key=CONSUMER_KEY,
                                      consumer_secret=CONSUMER_SECRET,
                                      access_token_key=ACCESS_TOKEN_KEY,
                                      access_token_secret=ACCESS_TOKEN_SECRET, sleep_on_rate_limit=True)
                    continue
            except IOError:
                print ex.message
                sleep_time = 60
                print "sleep for ", sleep_time
                time.sleep(sleep_time)
                api = twitter.Api(consumer_key=CONSUMER_KEY,
                                  consumer_secret=CONSUMER_SECRET,
                                  access_token_key=ACCESS_TOKEN_KEY,
                                  access_token_secret=ACCESS_TOKEN_SECRET, sleep_on_rate_limit=True)
                continue

            for status in result:
                if status.created_at_in_seconds < dt:
                    continue

                user = status.user
                if not user.lang or user.lang != 'en':
                    continue

                if not user.statuses_count or user.statuses_count < MIN_STATUSES:
                    continue

                # print "user found: %s" % user.id
                tweet_writer.append_user(user)

            print 'users found: %s' % len(tweet_writer.users)
            break
    except Exception as ex:
        raise
        tweet_writer.close()

    return len(tweet_writer.users)


if __name__ == "__main__":
    while main() < 20000:
        pass

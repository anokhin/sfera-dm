import os
import sys
import thread
import time
import twitter
import json
import traceback

MIN_STATUSES = 10

CONSUMER_KEY = "NIdJmEzKanvYMoZMQOLRIWGhu"
CONSUMER_SECRET = "OJVCVs1sG5RxOR1XRn30rj2x5BoPZvPzmSmA8kfLMBr2JjH5yZ"

ACCESS_TOKEN_KEY = "105892440-hiutXI6zWd1XjrQJaotg7GbW6Mt1gihXCnE4njZH"
ACCESS_TOKEN_SECRET = "RxIHlIylRycp8dPZfV8fXSM2WtMP74lteIp5P6jxwh4XW"


users = 'politics_users'
users_list = 'politics_users_list'


class UsersWriter:
    def __init__(self):

        self.users = set()
        if os.path.exists(users_list):
            with open(users_list) as f:
                for line in f:
                    self.users.add(line.strip())

    def open(self):
        self.users_file = open(users, 'a')
        self.users_list_file = open(users_list, 'a')

    def close(self):
        self.users_file.close()
        self.users_list_file.close()

    def write_user(self, user):
        self.users_file.write('\n')
        self.users_file.write(json.dumps(user))
        self.users_list_file.write('\n')
        self.users_list_file.write(str(user['id']))

    def append_user(self, user):
        if user.id in self.users:
            return

        self.open()
        self.users.add(user.id)
        self.write_user(user.AsDict())
        self.close()



def main():
    print "Data gathering via twitter API"

    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)

    tweet_writer = UsersWriter()
    kws = 'election2016 #hillaryclinton #hillary2016 #muslimsforbernie #democrats #berniewillwin #politics ' \
    '#berniesandersforpresident #demtownhall #bernie4president #feelthebern #presidentbernie #notmeus ' \
    '#berniesanders2016 #voteforbernie #bernieisbae #election #berniesanders #bernie2016 #jewsforbernie ' \
    '#bernie #latinosforbernie #orlandoforbernie #iowaforbernie #uniteblue #liberal #congress #lgbtq ' \
    '#unicornsforbernie #youngdemocrats #vote2016 #2016election #millennialsforbernie #womenforbernie ' \
    '#tedcruz #cruz2016 #choosecruz #presidentialelection #babesforbernie #campaigntrail2016 #caucas2016 ' \
    '#2016campaign #hillary #democraticparty #democrat #campaign2016 #housedemocrats #2016caucas ' \
    '#nhpolitics #vote #chasetherace2016 #swedesforbernie2016 #clinton #liberalsarestupid #nohillary #nobernie ' \
    '#nobama #republican #marcorubio #liberals #conservative #thetruth #nohillary2016 #sanders #trump ' \
    '#donaldtrump #jackrussell #jackrussellsofig'

    l = kws.split(' #')

    for kw in l:
        print kw
        try:
        # if True:
            page = 1

            while True:
                print "page: ", page
                # if True:
                try:
                    result = api.GetUsersSearch(kw, page=page)
                except twitter.TwitterError as ex:
                    print ex.message[0]['message']
                    traceback.format_exc()
                    if ex.message[0]['code'] == 44:
                        break
                    if ex.message[0]['code'] == 88:
                        print "sleep for ", sleep_time
                        time.sleep(sleep_time)
                        continue

                    print "some other error:", ex
                    break
                except Exception as ex:
                    print ex
                    traceback.format_exc()
                    break

                for user in result:
                    # print user.id
                    if not user.lang or user.lang != 'en':
                        continue

                    if not user.statuses_count or user.statuses_count < MIN_STATUSES:
                        continue

                    # print "user found: %s" % user.id
                    tweet_writer.append_user(user)
                page += 1

                print 'users found: %s' % len(tweet_writer.users)
                sleep_time = api.GetSleepTime("users/search")
                if sleep_time > 0:
                    print "Sleeping: %d" % (sleep_time / 60.0)
                    time.sleep(sleep_time)

        except Exception as ex:
            traceback.format_exc()
            print ex

    tweet_writer.close()


if __name__ == "__main__":
    main()

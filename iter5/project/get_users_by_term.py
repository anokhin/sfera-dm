import os
import sys
import thread
import time
import twitter
import json

MIN_STATUSES = 10

CONSUMER_KEY = "NIdJmEzKanvYMoZMQOLRIWGhu"
CONSUMER_SECRET = "OJVCVs1sG5RxOR1XRn30rj2x5BoPZvPzmSmA8kfLMBr2JjH5yZ"

ACCESS_TOKEN_KEY = "105892440-hiutXI6zWd1XjrQJaotg7GbW6Mt1gihXCnE4njZH"
ACCESS_TOKEN_SECRET = "RxIHlIylRycp8dPZfV8fXSM2WtMP74lteIp5P6jxwh4XW"


class UsersWriter:
    def __init__(self):

        self.users_file = open('home_users.json_lines', 'a')

        try:
            self.users_list_file = open('home_users_list.json')
            self.users = set(json.loads(self.users_list_file.read()))
            self.users_list_file = open('home_users_list.json', 'w')
        except:
            self.users_list_file = open('home_users_list.json', 'w')
            self.users = set()

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
        self.users_list_file.write(json.dumps([u for u in self.users]))
        self.users_list_file.close()


def main():
    print "Data gathering via twitter API"

    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)

    tweet_writer = UsersWriter()
    # ['Game of Thrones', 'GameofThrones', 'GoT', 'Greyjoy', 'GoTSeason5', 'GoTSeason4', 'GoTSeason3', 'GoTSeason2', 'GoTSeason1', 'Meryn Trant', 'Mother of dragons']
    # l = ['sansa Stark', 'ned stark', 'arya stark', 'lannister']
    #l = ['tirion lannister', 'Baratheon', 'Martell', 'A Song of Ice and Fire', 'House Tyrell', 'Maester Luwin', 'Targaryen', 'Bolton', 'Lord Snow']
    #l = ['Dothraki', 'Westeros', 'Ygritte', 'Valar Dohaeris', 'Khaleesi', 'khalasar', 'A Storm of Swords', 'Kissed By Fire', 'Bran Stark', 'Jorah Mormont', 'Braavosi', 'Valyrian']
    # l = ['Talisa Maegyr', 'Brienne of Tarth', 'Robert Baratheon', 'Cersei Lannister', "Petyr Baelish", "Lord Varys", "Ellaria Sand", "Margaery Tyrell", "Viserys", "Daenerys Targaryen", "Missandei", "Daario Naharis" ]
    # l = ['The Big Bang Theory', 'Sheldon Cooper', 'Leonard Hofstadter', 'Howard Wolowitz', 'Raj Koothrappali', 'Bernadette Rostenkowski', 'Amy Farrah Fowler', 'Stuart Bloom', 'bigbangtheory', 'tbbt', 'bbt', 'sheldon', 'bazinga', 'thebigbangtheory']
    # l = ['House of Cards', 'Rachel Posner', 'Frank Underwood', 'Zoe Barnes', 'Peter Russo', 'Claire Underwood', 'Remy Danton', 'Jacqueline Sharp', 'Edward Meechum', 'Doug Stamper', 'Linda Vasquez', 'Janine Skorsky', 'Lucas Goodwin', 'Tom Hammerschmidt', 'Christina Gallagher', 'Garrett Walker', 'Gillian Cole', 'Adam Galloway', 'Jim Matthews']
    l = ['houseofcards']
    for kw in l:
        print kw
        try:
        # if True:
            page = 1

            while len(tweet_writer.users) < 100000:
                print "page:", page,
                try:
                    result = api.GetUsersSearch(kw, page=page)
                except twitter.TwitterError as ex:
                    print ex.message[0]['message']
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
            print ex

    tweet_writer.close()


if __name__ == "__main__":
    main()

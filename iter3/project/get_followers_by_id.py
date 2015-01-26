import os
import time
import twitter
import json

MIN_STATUSES = 10

CONSUMER_KEY = "ARbSfECKob6IqdKmlQKIG2Tl4"
CONSUMER_SECRET = "dUH9royJj0nzPlDWea33MZpZONKqV0YbY46Ht2OcFa7yMRa1U7"

ACCESS_TOKEN_KEY = "2979985961-3Sm5ljZ39YilsHwJ5q5LxsWfzFO07hnHGSH8Qul"
ACCESS_TOKEN_SECRET = "yI5oR83fTgDP2PujLKkK1euU976ucYHGdPGpB5GofA2ND"

# собранные фоловеры обамы: https://cloud.mail.ru/public/df9807a3a755/users.json_lines


class UsersWriter:
    def __init__(self):

        self.users = set()
        if os.path.exists("users.json_lines"):
            print "reading file"
            f = open("users.json_lines")
            for line in f:
                l = line.strip()
                if not l:
                    continue
                try:
                    user = json.loads(l)
                except:
                    print l
                    raise ValueError
                self.users.add(user['id'])
            f.close()
            print "read users:", len(self.users)

            self.users_file = open('users.json_lines', 'a')
        else:
            self.users_file = open('users.json_lines', 'w')

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

    def append_user_dict(self, user):
        if user['id'] in self.users:
            return

        self.users.add(user['id'])
        self.write_user(user)

    def close(self):
        self.users_file.close()


def main():
    print "Data gathering via twitter API"

    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)

    tweet_writer = UsersWriter()

    # if True:
    try:
        next_cursor = 1490729552100521423
        while True:
            print "page:", next_cursor
            try:
                next_cursor, previous_cursor, data = api.GetFollowersPaged(screen_name="BarackObama", skip_status=True, include_user_entities=True, cursor=next_cursor)
                print 'next page: ', next_cursor
            except twitter.TwitterError as ex:
                print ex.message[0]['message']
                if ex.message[0]['code'] == 44:
                    break
                if ex.message[0]['code'] == 88:
                    sleep_time = api.GetSleepTime("followers/list")
                    print "sleep for ", sleep_time
                    time.sleep(sleep_time)
                    continue

                print "some other error:", ex
                break
            except Exception as ex:
                print ex
                break

            for user in data['users']:
                if not 'lang' in user or user['lang'] != 'en':
                    continue

                if 'statuses_count' not in user or user['statuses_count'] < MIN_STATUSES:
                    continue

                print "user found: %s" % user['id']
                tweet_writer.append_user_dict(user)

            print 'users found: %s' % len(tweet_writer.users)

    except Exception as ex:
        print ex

    tweet_writer.close()


if __name__ == "__main__":
    main()

import twitter

CONSUMER_KEY = "NIdJmEzKanvYMoZMQOLRIWGhu"
CONSUMER_SECRET = "OJVCVs1sG5RxOR1XRn30rj2x5BoPZvPzmSmA8kfLMBr2JjH5yZ"

ACCESS_TOKEN_KEY = "105892440-hiutXI6zWd1XjrQJaotg7GbW6Mt1gihXCnE4njZH"
ACCESS_TOKEN_SECRET = "RxIHlIylRycp8dPZfV8fXSM2WtMP74lteIp5P6jxwh4XW"


def main():
    print "Data gathering via twitter API"

    api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN_KEY,
                      access_token_secret=ACCESS_TOKEN_SECRET)

    # print api.VerifyCredentials()

    users = set()
    for status in api.GetSearch("datamining", locale="en", count=100):
        print status    


if __name__ == "__main__":
    main()
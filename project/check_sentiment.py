from collections import defaultdict

__author__ = 'k.stroykova'

import json
import nltk
from textblob import TextBlob
pattern = "(?x)([A-Z]\.)+|\$?\d+(\.\d+)?%?|\w+([-']\w+)*|[+/\-@&*]"

r = ["Bush", "#AllinForJeb", "#JebBush", "Carson", "#BC2DC16", "#ImWithBen", "#Carson2016", "#BenCarson", "Cruz",
      "#CruzCrew", "#TedCruz", "Fiorina", "#Carly2016", "#CarlyFiorina", "Graham", "#LindseyGraham",
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


def get_words(text):
    words = [t.lower() for t in nltk.regexp_tokenize(text, pattern)]
    return words


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

total_polarities = []

def classsify():

    both = 0
    none = 0

    idx = 0


    users_f = open('classified_users', 'w')

    with open('politics_users_filtered') as f:
        for line in f:

            user, tweets = json.loads(line)



            # print '\n'
            if idx % 1000 == 0:
                print 'idx', idx

            # if int(user) not in users:
            #     idx += 1
            #     continue

            # print user

            user_polarity = 0
            polarities = []
            for t in tweets:

                is_d = False
                is_r = False
                if "hashtags" in t:
                    # print 'hashtags', t["hashtags"]

                    for ht in t["hashtags"]:
                        ht = ht.strip('#').lower()
                        if ht in d_h:
                            is_d = True
                        if ht in r_h:
                            is_r = True

                text = t['text'].lower()
                # print 'text', text

                blob = TextBlob(text)

                # print 'sentiment', blob.sentiment
                if blob.sentiment.polarity == 0:
                    continue


                lemmas = [w.lemma for w in blob.words]
                # print 'lemmas', lemmas
                if any(l in d_w for l in lemmas):
                    is_d = True
                if any(l in r_w for l in lemmas):
                    is_r = True

                words = [w for w in blob.words]
                # print 'lemmas', lemmas
                if any(l in d_w for l in words):
                    is_d = True
                if any(l in r_w for l in words):
                    is_r = True

                # print 'parties', is_d, is_r
                if is_d and is_r:
                    # print 'is both, skip\n'
                    both += 1
                    continue

                if (not is_d) and (not is_r):
                    # print 'none, skip\n'
                    none += 1
                    continue

                # if blob.sentiment.polarity <= 0:
                #     continue

                if is_d:
                    polarities.append(blob.sentiment.polarity)
                if is_r:
                    polarities.append(-1 * blob.sentiment.polarity)


            # print 'polarities', polarities
            if polarities:
                user_polarity = sum(polarities) / len(polarities)

            user_polarity = (user_polarity + 1) / 2.0

            # print 'polarity', user_polarity


            # if user_polarity == 0.5:
                # print 'user', user

            total_polarities.append(user_polarity)
            if user_polarity != 0.5:
                users_f.write('{0}\t{1}\n'.format(user, user_polarity))

            idx += 1


    print ''
    print len(total_polarities)
    print max(total_polarities)
    print min(total_polarities)
    print sum(total_polarities) / float(len(total_polarities))
    print both
    print none

    hist = defaultdict(int)
    for p in total_polarities:
        hist['%.1f' % p] += 1

    print len([p for p in total_polarities if p < 0.5])
    print len([p for p in total_polarities if p > 0.5])

    for i in sorted(hist.iteritems(), key=lambda x: x[0]):
        print i



def hashtags():
    idx = 0

    popular_hashtags = defaultdict(int)

    with open('politics_users_filtered') as f:
        for line in f:

            user, tweets = json.loads(line)
            print '\n'

            if idx % 100 == 0:
                print idx

            for t in tweets:

                if "hashtags" in t:

                    for ht in t['hashtags']:
                        popular_hashtags[ht] += 1
            idx += 1

    for i in sorted(popular_hashtags.iteritems(), key=lambda x: x[1]):
        print i


classsify()
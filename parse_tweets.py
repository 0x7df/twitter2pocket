# Requires pandas and matplotlib to be installed, e.g.
#
#     `sudo apt-get install pandas-python`

import json
import re
import pandas as pd
import matplotlib.pyplot as plt
import sys

tweets_data_path = './twitter_data.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")

for line in tweets_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue

print len(tweets_data)

tweets = pd.DataFrame()


def getData(tweet, key):
    try:
       txt = tweet[key]
    except:
       return ''
    return txt

tweets['text'] = map(lambda tweet: getData(tweet, 'text') if getData(tweet, \
    'text') != None else '', tweets_data)
tweets['lang'] = map(lambda tweet: getData(tweet, 'lang') if getData(tweet,
    'lang') != None else '', tweets_data)
tweets['country'] = map(lambda tweet: getData(tweet, 'place')['country'] if getData(tweet,
    'place') != None else None, tweets_data)


#tweets_by_lang = tweets['lang'].value_counts()
#tweets_by_country = tweets['country'].value_counts()

#fig, ax = plt.subplots()
#ax.tick_params(axis = 'x', labelsize = 15)
#ax.tick_params(axis = 'y', labelsize = 10)
#ax.set_xlabel('Languages',     fontsize = 15)
#ax.set_ylabel('No. of tweets', fontsize = 15)
#ax.set_title('Top five languages', fontsize = 15, fontweight = 'bold')
#tweets_by_lang[:5].plot(ax = ax, kind = 'bar', color = 'red')
#tweets_by_country[:5].plot(ax = ax, kind = 'bar', color = 'blue')
##plt.show()

def word_in_text(word, text):
    if re.search(word.lower(), text.lower()):
        return True
    return False

tweets['python'] = \
    tweets['text'].apply(lambda tweet: word_in_text('python', tweet))

tweets['javascript'] = \
    tweets['text'].apply(lambda tweet: word_in_text('javascript', tweet))

tweets['ruby'] = \
    tweets['text'].apply(lambda tweet: word_in_text('ruby', tweet))

print tweets['python'].value_counts()[True]
print tweets['javascript'].value_counts()[True]
print tweets['ruby'].value_counts()[True]


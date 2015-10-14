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

tweets['text'] = map(lambda tweet: tweet['text'], tweets_data)
#tweets['text'] = map(lambda tweet: getData(tweet, 'text') if getData(tweet, \
#    'text') != None else '', tweets_data)
#tweets['lang'] = map(lambda tweet: getData(tweet, 'lang') if getData(tweet,
#    'lang') != None else '', tweets_data)
#tweets['country'] = map(lambda tweet: getData(tweet, 'place')['country'] if getData(tweet,
#    'place') != None else None, tweets_data)


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

tweets['fortran'] = \
    tweets['text'].apply(lambda tweet: word_in_text('fortran', tweet))

tweets['bash'] = \
    tweets['text'].apply(lambda tweet: word_in_text('bash', tweet))

tweets['linux'] = \
    tweets['text'].apply(lambda tweet: word_in_text('linux', tweet))

tweets['programming'] = \
    tweets['text'].apply(lambda tweet: word_in_text('programming', tweet))

tweets['tutorial'] = \
    tweets['text'].apply(lambda tweet: word_in_text('tutorial', tweet))

#tweets['relevant'] = \
#    tweets['text'].apply(lambda tweet: word_in_text('tutorial', tweet) or
#                                       word_in_text('programming', tweet))

tweets['relevant'] = \
    tweets['text'].apply(lambda tweet: word_in_text('tutorial', tweet))


print "Python:", tweets['python'].value_counts()[True]
print "JavaScript:", tweets['javascript'].value_counts()[True]
#print "Ruby:", tweets['ruby'].value_counts()[True]
print "Programming:", tweets['programming'].value_counts()[True]
print "Tutorial: ", tweets['tutorial'].value_counts()[True]
print "Relevant:", tweets['relevant'].value_counts()[True]
print "Relevant Python:", tweets[tweets['relevant'] == \
    True]['python'].value_counts()[True]
print "Relevant JavaSc:", tweets[tweets['relevant'] == \
    True]['javascript'].value_counts()[True]

def extract_link(text):
    regex = r'https?:..[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''

tweets['link'] = tweets['text'].apply(lambda tweet: extract_link(tweet))

tweets_relevant = tweets[tweets['relevant'] == True]
tweets_relevant_with_link = tweets_relevant[tweets_relevant['link'] != '']

print tweets_relevant_with_link[tweets_relevant_with_link['python'] == True]['link']
print tweets_relevant_with_link[tweets_relevant_with_link['python'] == True]['text']

for tweet in tweets_relevant_with_link[tweets_relevant_with_link['python'] ==
    True]['link']:
    print tweet


#for tweet in tweets_relevant_with_link[tweets_relevant_with_link['python'] ==
#    True]['text']:
#    print tweet
#    print


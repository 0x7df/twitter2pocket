# Requires pandas and matplotlib to be installed, e.g.
#
#     `sudo apt-get install pandas-python`

import json
import re
import pandas as pd
import matplotlib.pyplot as plt

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


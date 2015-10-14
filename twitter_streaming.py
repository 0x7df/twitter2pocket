# Call without any argument, e.g.:
#
#     `python twitter_streaming.py`
#
# Output is automatically written to file, in JSON format.

# This uses Tweepy, a Python library for accessing the Twitter API:
# http://www.tweepy.org. Install with `pip install tweepy`.

# The details of using Tweepy with the Twitter streaming API is in:
# http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
import pocket

# Read the Twitter API key data from a file (not in the repository)
with open('twitter_api_key.txt') as fileHandle:
    (access_token, access_token_secret, consumer_key, consumer_secret) = \
        [item.strip('\n') for item in fileHandle.readlines()]

with open('pocket_api_key.txt') as fileHandle:
    (pckt_consumer_key, pckt_access_token) = \
        [item.strip('\n') for item in fileHandle.readlines()]

# Set the keywords to filter the Twitter stream for
keywords = ['python', 'javascript', 'fortran', 'bash', 'linux', 'css', 'jquery',
            'api', 'git']

def getData(tweet, key):
    try:
        val = tweet[key]
    except:
        return ''
    return val

def word_in_text(word, text):
    if re.search(word.lower(), text.lower()):
        return True
    return False

def extract_link(text):
    regex = r'https?:..[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''

def myrespond(data):
    tweet = json.loads(data)
    #fileUnit.write(data)
    #testUnit.write(json.dumps(tweet)+"\n") 
    text = getData(tweet, 'text')
    link = extract_link(text)
    if (word_in_text('tutorial', text) and link != ''):
        print text
        print link
        print "-----------------------------------------------------------"



# This is a basic listener that prints received tweets to stdout
# Over-ride the tweepy.Stream listener to provide methods
class StdOutListener(StreamListener):

    def on_data(self, data):
        myrespond(data)
        return True

    def on_error(self, status):
        print status
        if status == 420:
            return False
        return False
        sys.exit(1)

if __name__ == "__main__":

    #testUnit = open('twitter_test.txt', 'w')
    #fileUnit = open('twitter_data.txt', 'w')
    
    # Handle Twitter authentication and connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
   
    # Pocket authentication
    request_token = pocket.Pocket.get_request_token(consumer_key=consumer_key,
    redirect_uri=redirect_uri) 
     
    # Filter Twitter stream according to keywords
    #stream.filter(track = keywords)

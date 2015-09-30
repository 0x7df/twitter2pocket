# Pipe the output of this to file, e.g.:
#
#     `python twitter_streaming.py > twitter_data.txt`
#
# The output is in JSON format.

# This uses Tweepy, a Python library for accessing the Twitter API:
# http://www.tweepy.org. Install with `pip install tweepy`.

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

with open('twitter_api_key.txt') as fileHandle:
    (access_token, access_token_secret, consumer_key, consumer_secret) = \
        [item.strip('\n') for item in fileHandle.readlines()]

print access_token
print access_token_secret
print consumer_key
print consumer_secret

keywords = ['python', 'javascript', 'ruby']

# This is a basic listener that prints received tweets to stdout

class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status

if __name__ == "__main__":

    # Handle Twitter authentication and connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    # Filter Twitter stream according to keywords
    stream.filter(track = keywords)

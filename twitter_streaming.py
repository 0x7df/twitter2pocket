# Pipe the output of this to file, e.g.:
#
#     `python twitter_streaming.py > twitter_data.txt`
#
# The output is in JSON format.

# This uses Tweepy, a Python library for accessing the Twitter API:
# http://www.tweepy.org. Install with `pip install tweepy`.

# The details of using Tweepy with the Twitter streaming API is in:
# http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Read the Twitter API key data from a file (not in the repository)
with open('twitter_api_key.txt') as fileHandle:
    (access_token, access_token_secret, consumer_key, consumer_secret) = \
        [item.strip('\n') for item in fileHandle.readlines()]

# Set the keywords to filter the Twitter stream for
keywords = ['python', 'javascript', 'ruby']

# This is a basic listener that prints received tweets to stdout
# Over-ride the tweepy.Stream listener to provide methods
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status
        if status == 420:
            return False
        return False
        sys.exit(1)

if __name__ == "__main__":

    # Handle Twitter authentication and connection to Twitter Streaming API
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)

    # Filter Twitter stream according to keywords
    stream.filter(track = keywords)

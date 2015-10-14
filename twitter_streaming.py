"""Extract relevant tweets from Twitter Streaming API and save URLs to Pocket.

Call without any argument, e.g.:

    `python twitter_streaming.py`

Add argument 'authorise_pocket' to use this script to authorise Pocket
instead of running the stream listener - gets credentials to add to file

This uses Tweepy, a Python library for accessing the Twitter API:
http://www.tweepy.org. Install with `pip install tweepy`.

The details of using Tweepy with the Twitter streaming API is in:
http://docs.tweepy.org/en/v3.4.0/streaming_how_to.html
"""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re
import pocket
import sys

try:
    authorise_pocket = (sys.argv[1] == 'authorise_pocket')
except IndexError:
    authorise_pocket = False


def pocket_auth():
    """Authorise Pocket app given redirect URL and consumer key."""
    request_token = pocket.Pocket.get_request_token(
        consumer_key=pckt_consumer_key,
        redirect_uri=redirect_uri
    )
    print "Request token =", request_token

    auth_url = pocket.Pocket.get_auth_url(
        code=request_token,
        redirect_uri=redirect_uri
    )

    print "Please visit the following URL to authorize the app:"
    print auth_url
    print "When complete, type y"
    user_input = "n"
    while user_input != "y":
        user_input = raw_input("-->")

    user_credentials = pocket.Pocket.get_credentials(
        consumer_key=pckt_consumer_key,
        code=request_token
    )

    new_pckt_access_token = user_credentials['access_token']
    print "Access token = ", new_pckt_access_token


# Read the Twitter API key data from a file (not in the repository)
with open('twitter_api_key.txt') as fileHandle:
    (access_token, access_token_secret, consumer_key, consumer_secret) = \
        [item.strip('\n') for item in fileHandle.readlines()]

with open('pocket_api_key.txt') as fileHandle:
    (pckt_consumer_key, pckt_access_token, redirect_uri) = \
        [item.strip('\n') for item in fileHandle.readlines()]

# Set the keywords to filter the Twitter stream for
keywords = ['python', 'javascript', 'fortran', 'bash', 'linux', 'css',
            'jquery', 'api', 'git', 'vim', 'julia']


def getdata(tweet, key):
    """Get dictionary value given key."""
    try:
        val = tweet[key]
    except KeyError:
        return ''
    return val


def word_in_text(word, text):
    """Search for work in text string."""
    if re.search(word.lower(), text.lower()):
        return True
    return False


def extract_link(text):
    """Extract link from tweet or return null string."""
    regex = r'https?:..[^\s<>"]+|www\.[^\s<>"]+'
    match = re.search(regex, text)
    if match:
        return match.group()
    return ''


def myrespond(data):
    """Respond to relevant tweet."""
    tweet = json.loads(data)
    lang = getdata(tweet, 'lang')
    if lang == 'en':
        text = getdata(tweet, 'text')
        link = extract_link(text)
        if word_in_text('tutorial', text) and link != '':
            print text
            print link
            print pocket_instance.add(url=link)
            print "-----------------------------------------------------------"


# This is a basic listener that prints received tweets to stdout
# Over-ride the tweepy.Stream listener to provide methods
class StdOutListener(StreamListener):

    """Create stream listener class for Twitter Streaming API."""

    def on_data(self, data):
        """Process individual tweet."""
        myrespond(data)
        return True

    def on_error(self, status):
        """Handle error from Twitter Streaming API."""
        print status
        if status == 420:
            return False
        return False

if __name__ == "__main__":

    if authorise_pocket:
        pocket_auth()

    else:

        # Handle Twitter authentication and connection to Twitter Streaming API
        listener = StdOutListener()
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        stream = Stream(auth, listener)

        # Pocket authentication
        pocket_instance = pocket.Pocket(pckt_consumer_key, pckt_access_token)

        # Filter Twitter stream according to keywords
        stream.filter(track=keywords)

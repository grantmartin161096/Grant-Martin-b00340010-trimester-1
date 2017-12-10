from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sentiment_mod as s

# The above import sentiment_mod as s line of code imports the sentiment analysis fuction from the last piec of code.
# tweepy is the python client for the official Twitter API to gather tweets through Twitter API

# To receive your own consumer key and secret, access token and secret
# You need to view my user guide for the instructions on how to do this
# Consumer keys and access tokens, used for OAuth (OAuthentication)
# It is used for security and to make sure you have permission to use the Twitter API data

consumer_key = "hJKfi8A4bpvGnra7R5TYuxCJ8"
consumer_secret = "tMZso3E2P1NduV1wyOxPd3XkeTe0JQ57UkOZr54uOraebYEDRb"
access_token = "923539440307441665-jMpKkc7cGOmZlIwobX4ytUS0H0dr9oS"
access_secret = "UYzq7kegTpPa5PV5DemQbfWvn1lsy2Dq73C84uy83liFe"

# Line 4 of the code 'import json' allows me to use the json module to load the tweet data with the code below 'json.loads(data)'
# The line of code below 'tweet = all_data["text"]' allows me to target the tweets specifically
# Once I have a tweet I can pass it through the sentiment_mod
# In the code below the line 'output = open("twitter-out.txt", "a")' and the code that follows will output the tweets into a json file with its sentiment score

class listener(StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)

        tweet = all_data["text"]
        sentiment_value, confidence = s.sentiment(tweet)
        print(tweet, sentiment_value, confidence)

        if confidence * 100 >= 80:
            output = open("twitter-out.txt", "a")
            output.write(sentiment_value)
            output.write('\n')
            output.close()

        return True

    def on_error(self, status):
        print(status)

# OAuth process, using the keys and tokens

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
twitterStream = Stream(auth, listener())
twitterStream.filter(track=["justice league"])

# The stream is retreiving all the live tweets about your chosen query, in this case justice league.

# Reference for the code used: https://pythonprogramming.net/twitter-sentiment-analysis-nltk-tutorial/
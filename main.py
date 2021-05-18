import tweepy
from tweepy import Stream
from dotenv import load_dotenv
import os
from stream import listener
load_dotenv()

consumer_key = os.getenv("API_Key")
consumer_secret = os.getenv('API_Secret_Key')
access_token = os.getenv('Access_Token')
access_token_secret = os.getenv('Access_Token_Secret')

Auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
Auth.set_access_token(access_token, access_token_secret)

twitterStream = Stream(Auth, listener())
twitterStream.filter(track=["@NeoAnderson1999"])

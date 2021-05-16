import tweepy
import sys
from tweepy import Stream
from tweepy.streaming import StreamListener
import dotenv
from dotenv import load_dotenv
import os
import requests
from urllib.parse import quote
load_dotenv()

consumer_key = os.getenv("API_Key")
consumer_secret = os.getenv('API_Secret_Key')
access_token = os.getenv('Access_Token')
access_token_secret = os.getenv('Access_Token_Secret')

Auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
Auth.set_access_token(access_token, access_token_secret)


class listener(StreamListener):

    def on_status(self, status):
        print(status.id)

    def on_error(self, status):
        print("error",status)
        pass



twitterStream = Stream(Auth, listener())
twitterStream.filter(track=["@NeoAnderson1999"])
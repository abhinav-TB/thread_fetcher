import tweepy
from tweepy import Stream
from dotenv import load_dotenv
import os
from utils import create_api
from stream import listener

api ,auth = create_api()

twitterStream = Stream(auth, listener(api))
twitterStream.filter(track=["@threadfetch"])

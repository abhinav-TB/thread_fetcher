import tweepy
from tweepy.streaming import StreamListener
from dotenv import load_dotenv
import os
load_dotenv()
from coversations import conversations


conv = conversations()
class listener(StreamListener):

    def on_status(self, status):
        conv(status.in_reply_to_status_id_str)

    def on_error(self, status):
        print("error",status)
        pass


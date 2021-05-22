
from operator import truediv
import tweepy
from dotenv import load_dotenv
import os


def create_api():
    load_dotenv()

    consumer_key = os.getenv("API_Key")
    consumer_secret = os.getenv('API_Secret_Key')
    access_token = os.getenv('Access_Token')
    access_token_secret = os.getenv('Access_Token_Secret')

    Auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    Auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(Auth)
    return api , Auth

def is_thread (obj):
    # obj:json_object  with conversations
    if(obj['meta']['result_count'] != 0):
        return True
    else:
        return False

api , _ = create_api()
def handle_is_thread(tweet_id):
    
    api.update_status('🛑This tweet does not have any threads!!',in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)

def handle_follow(tweet):
    # inputs 
    #  tweet:status_object
    # The fucntion takes in a tweet a checks whether its a tweet by a person who followed the bot
    # if followed return true else reply to the usr to follow threadfetcher
    tweet_id = tweet.id
    usr_name = tweet.user.screen_name
    status = api.show_friendship(source_screen_name = 'threadfetcher',target_screen_name = usr_name)
    if(status[1].following):
        return True
    else:
        api.update_status('You have to follow @threadfetcher before tagging ',in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)
        return False


    

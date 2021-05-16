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

class Listener(StreamListener):
    def __init__(self, output_file=sys.stdout):
        super(Listener,self).__init__()
        self.output_file = output_file
    def on_status(self, status):
        print(status.text, file=self.output_file)
    def on_error(self, status_code):
        print(status_code)
     

def auth():
    return os.getenv("Bearer_Token")
def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()

def get_conversation_from_id(conversation_id, author_id):
    tweet_fields = "tweet.fields=author_id"
    query = f"from:{author_id} conversation_id:{conversation_id}"
    # query = f"conversation_id:{conversation_id}"
    max_results = 100
    # print(conversation_id)
    url = f"https://api.twitter.com/2/tweets/search/recent?query={quote(query)}&max_results={max_results}&{tweet_fields}"
    bearer_token = auth()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    return json_response

def get_conversation_id(tweet_id):
    tweet_fields = "tweet.fields=conversation_id,author_id"
    url = f"https://api.twitter.com/2/tweets?ids={tweet_id}&{tweet_fields}"
    bearer_token = auth()
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    conversation_id = json_response["data"][0]["conversation_id"]
    author_id = json_response["data"][0]["author_id"]
    return conversation_id, author_id



api = tweepy.API(Auth)
public_tweets = api.mentions_timeline()
tweet_id = public_tweets[0].in_reply_to_status_id_str
conversation_id , author_id = get_conversation_id(tweet_id)
conversations = get_conversation_from_id(conversation_id , author_id)

print(conversations['data'][0])


source_tweet = api.get_status(tweet_id)
name = source_tweet.user.screen_name
print(name)


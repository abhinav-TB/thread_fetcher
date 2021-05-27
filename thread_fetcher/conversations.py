import tweepy
from tweepy import API

import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv
from firebase import Firebase_util
from html_generation import HTML
from utils import is_thread, handle_is_thread

load_dotenv()

consumer_key = os.getenv("API_Key")
consumer_secret = os.getenv('API_Secret_Key')
access_token = os.getenv('Access_Token')
access_token_secret = os.getenv('Access_Token_Secret')

Auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
Auth.set_access_token(access_token, access_token_secret)

api_v1 = API(Auth)


class conversations:
    def __init__(self):
        self.app = Firebase_util()
        self.tweet_id = None
        self.conversation_id = None
        self.author_id = None
        self.author_name = ''
        self.json_response = None
        self.created_at = ''

    def __call__(self, usr_tweet_id, tweet_id, user_name):
        self.tweet_id = tweet_id
        self.user_name = user_name
        self.get_conversation_id()
        self.get_conversation_from_id()
        if is_thread(self.json_response):
            self.save_as_html()
        else:
            handle_is_thread(usr_tweet_id)
            return None
        self.app.add_to_bucket(self.conversation_id, user_name)
        if os.path.exists(f"{self.conversation_id}.html"):
            os.remove(f"{self.conversation_id}.html")
            print("Local copy of HTML deleted")
        return self.conversation_id

    def is_replying_to_author(self, tweet_id):
        _, replied_to, author_id = self.get_reply_tweet(tweet_id)
        return replied_to == author_id

    def save_as_html(self):
        tweet_ids = [int(tweet["id"]) for tweet in self.json_response['data']]

        # Remove tweets which are not replying to the original author
        tweet_ids = list(filter(self.is_replying_to_author, tweet_ids))

        first_tweet_id, _, _ = self.get_reply_tweet(tweet_ids[-1])
        if first_tweet_id:
            tweet_ids.append(int(first_tweet_id))
            tweet_ids.reverse()
            tweets_dict = self.get_tweets_dict(tweet_ids)
            html_file = HTML(
                f'Thread by @{self.author_name} on {self.created_at}', self.conversation_id)
            for tweet_id in tweet_ids:
                tweet = tweets_dict[tweet_id]
                html_file.add_tweet_card(
                    tweet_text=tweet["text"], tweet_media_type=tweet['media_type'], tweet_media_urls=tweet['media_urls'])
            html_file.save()
            print("Thread saved locally as HTML")

    def auth(self):
        return os.getenv("Bearer_Token")

    def create_headers(self, bearer_token):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers

    def connect_to_endpoint(self, url, headers):
        response = requests.request("GET", url, headers=headers)
        # print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            )
        return response.json()

    def get_reply_tweet(self, parent_tweet_id):
        tweet_fields = "tweet.fields=in_reply_to_user_id,author_id"
        expansions = "expansions=referenced_tweets.id,in_reply_to_user_id"
        url = f"https://api.twitter.com/2/tweets?ids={parent_tweet_id}&{tweet_fields}&{expansions}"
        bearer_token = self.auth()
        headers = self.create_headers(bearer_token)
        json_response = self.connect_to_endpoint(url, headers)
        if "in_reply_to_user_id" not in json_response["data"][0]:
            print("Not called on a thread")
            return None, None
        else:
            # print(json_response)
            tweet_id = json_response['includes']['tweets'][0]['id']
            # replied_to = json_response['includes']['tweets'][0]['author_id']
            author_id = json_response['data'][0]['author_id']
            replied_to = json_response['data'][0]['in_reply_to_user_id']
            return tweet_id, replied_to, author_id

    def get_tweets_dict(self, id_list):
        tweets = api_v1.statuses_lookup(
            id_list, include_entities=True, tweet_mode='extended')
        tweets_dict = dict()
        for tweet in tweets:
            tweet_dict = {'text': tweet.full_text,
                          'media_type': None, 'media_urls': None}
            if 'extended_entities' in dir(tweet):
                tweet_dict['media_type'] = tweet.extended_entities['media'][0]['type']
                if tweet_dict['media_type'] == 'animated_gif' or tweet_dict['media_type'] == 'video':
                    tweet_dict['media_urls'] = [
                        tweet.extended_entities['media'][0]['video_info']['variants'][0]['url']]
                elif tweet_dict['media_type'] == 'photo':
                    tweet_dict['media_urls'] = [medium['media_url_https']
                                                for medium in tweet.extended_entities['media']]
                else:
                    print('Something went wrong in conversations.get_tweets_dict')
            tweets_dict[int(tweet.id)] = tweet_dict
        return tweets_dict

    def get_conversation_from_id(self):
        tweet_fields = "tweet.fields=author_id"
        media_fields = "media.fields=type,url"
        query = f"from:{self.author_id} conversation_id:{self.conversation_id}"
        # query = f"conversation_id:{conversation_id}"
        max_results = "max_results=100"
        # print(conversation_id)
        url = f"https://api.twitter.com/2/tweets/search/recent?query={quote(query)}&expansions=attachments.media_keys&{max_results}&{tweet_fields}&{media_fields}"
        bearer_token = self.auth()
        headers = self.create_headers(bearer_token)
        self.json_response = self.connect_to_endpoint(url, headers)

    def get_conversation_id(self):
        tweet_fields = "tweet.fields=conversation_id,author_id,created_at"
        user_fields = "user.fields=username"
        url = f"https://api.twitter.com/2/tweets?ids={self.tweet_id}&expansions=author_id&{tweet_fields}&{user_fields}"
        bearer_token = self.auth()
        headers = self.create_headers(bearer_token)
        json_response = self.connect_to_endpoint(url, headers)
        # print(json_response)
        self.conversation_id = json_response["data"][0]["conversation_id"]
        self.author_id = json_response["data"][0]["author_id"]
        self.author_name = json_response["includes"]["users"][0]["username"]
        self.created_at = json_response["data"][0]["created_at"][:10]

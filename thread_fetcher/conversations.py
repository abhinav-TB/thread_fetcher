import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv
from firebase import Firebase_util

from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.flowables import PageBreakIfNotEmpty

load_dotenv()


class PDF:
    def __init__(self, title_text, file_name) -> None:
        self.flowables = []
        self.items_in_last_page = 0
        self.line_break = '<br/><br/><br/><br/><br/>'
        self.doc_file = SimpleDocTemplate(f'{file_name}.pdf')
        self.styles = getSampleStyleSheet()
        font_file = 'Symbola.ttf'
        symbola_font = TTFont('Symbola', font_file)
        pdfmetrics.registerFont(symbola_font)
        self.styles["BodyText"].fontName = 'Symbola'
        self.styles["BodyText"].fontSize = 16
        self.styles["BodyText"].leading = 16
        self.styles["Heading1"].fontSize = 30
        self.styles["Heading1"].leading = 18
        title = Paragraph(title_text + self.line_break,
                          self.styles['Heading1'])
        self.flowables.append(title)
        self.items_in_last_page += 1

    def add_tweet_text(self, tweet_text):
        tweet = Paragraph(tweet_text + self.line_break,
                          self.styles["BodyText"])
        if (self.items_in_last_page >= 5):
            self.flowables.append(PageBreakIfNotEmpty())
            self.items_in_last_page -= 5
        self.flowables.append(tweet)
        self.items_in_last_page += 1

    def save(self):
        self.doc_file.build(self.flowables)


class conversations:

    def __init__(self):
        self.app = Firebase_util()
        self.tweet_id = None
        self.conversation_id = None
        self.author_id = None
        self.author_name = None
        self.json_response = None

    def __call__(self, tweet_id, user_name):
        self.tweet_id = tweet_id
        self.user_name = user_name
        self.get_conversation_id()
        self.get_conversation_from_id()
        self.save_as_pdf()
        self.app.add_to_bucket(self.conversation_id, user_name)
        if os.path.exists(f"{self.conversation_id}.pdf"):
            os.remove(f"{self.conversation_id}.pdf")
            print("Local copy of PDF deleted")
        return self.conversation_id

    def save_as_pdf(self):
        tweets = [(tweet["text"], tweet["id"])
                  for tweet in self.json_response['data']]

        # Remove tweets which are not replying to the original author
        indices_to_remove = list()
        for i in range(len(tweets)):
            _, replied_to = self.get_reply_tweet(tweets[i][1])
            if replied_to != self.author_id:
                indices_to_remove.append(i)
        for index in indices_to_remove:
            del tweets[index]

        first_tweet_text, _ = self.get_reply_tweet(tweets[-1][1])
        if first_tweet_text:
            tweet_texts = [tweet_tuple[0]
                           for tweet_tuple in tweets] + [first_tweet_text]
            tweet_texts.reverse()
            pdf = PDF('Saved Twitter Thread', self.conversation_id)
            for tweet_text in tweet_texts:
                pdf.add_tweet_text(tweet_text)
            pdf.save()
            print("Thread saved locally as a PDF")

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
        expansions = "expansions=referenced_tweets.id"
        url = f"https://api.twitter.com/2/tweets?ids={parent_tweet_id}&{tweet_fields}&{expansions}"
        bearer_token = self.auth()
        headers = self.create_headers(bearer_token)
        json_response = self.connect_to_endpoint(url, headers)
        if "in_reply_to_user_id" not in json_response["data"][0]:
            print("Not called on a thread")
            return None, None
        else:
            # print(json_response)
            tweet_text = json_response['includes']['tweets'][0]['text']
            replied_to = json_response['includes']['tweets'][0]['author_id']
            return tweet_text, replied_to

    def get_conversation_from_id(self):
        tweet_fields = "tweet.fields=author_id"
        query = f"from:{self.author_id} conversation_id:{self.conversation_id}"
        # query = f"conversation_id:{conversation_id}"
        max_results = 100
        # print(conversation_id)
        url = f"https://api.twitter.com/2/tweets/search/recent?query={quote(query)}&max_results={max_results}&{tweet_fields}"
        bearer_token = self.auth()
        headers = self.create_headers(bearer_token)
        self.json_response = self.connect_to_endpoint(url, headers)

    def get_conversation_id(self):
        tweet_fields = "tweet.fields=conversation_id,author_id"
        user_fields = "user.fields=username"
        url = f"https://api.twitter.com/2/tweets?ids={self.tweet_id}&expansions=author_id&{tweet_fields}&{user_fields}"
        bearer_token = self.auth()
        headers = self.create_headers(bearer_token)
        json_response = self.connect_to_endpoint(url, headers)
        self.conversation_id = json_response["data"][0]["conversation_id"]
        self.author_id = json_response["data"][0]["author_id"]
        print(json_response)

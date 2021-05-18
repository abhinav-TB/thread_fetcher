import os
import requests
from urllib.parse import quote
from dotenv import load_dotenv
from fpdf import FPDF
from firebase import Firebase_util

load_dotenv()


class PDF(FPDF):
    def header(self):
        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Saved Twitter Thread', 0, 1, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')


class conversations:

    def __init__(self):
        self.app = Firebase_util()
        self.tweet_id = None
        self.conversation_id = None
        self.author_id = None
        self.json_response = None
        

    def __call__(self, tweet_id ,user_name):
        self.tweet_id = tweet_id
        self.user_name = user_name
        self.get_conversation_id()
        self.get_conversation_from_id()
        self.save_as_pdf()
        self.app.add_to_bucket(self.conversation_id,user_name)
        if os.path.exists(f"{self.conversation_id}.pdf"):
            os.remove(f"{self.conversation_id}.pdf")
       
    def save_as_pdf(self):

        tweets = [(tweet["text"], tweet["id"]) for tweet in self.json_response['data']]
        first_tweet_text = self.get_reply_tweet_text(tweets[-1][1])
        if first_tweet_text:
            tweet_texts = [tweet_tuple[0]
                           for tweet_tuple in tweets] + [first_tweet_text]
            tweet_texts.reverse()
            pdf = PDF()
            pdf.alias_nb_pages()
            pdf.add_page()
            pdf.set_font('Times', '', 12)
            for tweet_text in tweet_texts:
                tweet_text = tweet_text.encode('latin-1', 'replace').decode('latin-1')
                pdf.cell(0, 10, tweet_text, 0, 1, 'C')
            pdf.output(f"{self.conversation_id}.pdf", "F")
            print("Thread saved locally")

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

    def get_reply_tweet_text(self, parent_tweet_id):
        tweet_fields = "tweet.fields=in_reply_to_user_id"
        expansions = "expansions=referenced_tweets.id"
        url = f"https://api.twitter.com/2/tweets?ids={parent_tweet_id}&{tweet_fields}&{expansions}"
        bearer_token = self.auth()
        headers = self.create_headers(bearer_token)
        json_response = self.connect_to_endpoint(url, headers)
        if "in_reply_to_user_id" not in json_response["data"][0]:
            print("Not called on a thread")
            return None
        else:
            # print(json_response)
            return json_response['includes']['tweets'][0]['text']

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
        url = f"https://api.twitter.com/2/tweets?ids={self.tweet_id}&{tweet_fields}"
        bearer_token = self.auth()
        headers = self.create_headers(bearer_token)
        json_response = self.connect_to_endpoint(url, headers)
        self.conversation_id = json_response["data"][0]["conversation_id"]
        self.author_id = json_response["data"][0]["author_id"]

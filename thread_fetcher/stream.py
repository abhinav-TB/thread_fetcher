from utils import handle_follow
from tweepy.streaming import StreamListener
from conversations import conversations
from dotenv import load_dotenv

load_dotenv()
addr = "https://storage.cloud.google.com/thread-fetcher.appspot.com/"
conv = conversations()


class listener(StreamListener):

    def __init__(self, api):
        self.api = api

    def on_status(self, status):
        if(not handle_follow(status)):return
        conv_id = conv(status.id_str ,status.in_reply_to_status_id_str,
                       status.user.screen_name)
        if(not conv_id):return
        print("Tagged by: " + status.user.screen_name)
        url = addr+status.user.screen_name+'/'+conv_id
        print(url)
        mssg = f"Hi {status.user.name} here is the thread you have requested 😉 \n"
        self.api.send_direct_message(status.user.id_str, mssg +url)

    def on_error(self, status):
        print("error", status)
        pass

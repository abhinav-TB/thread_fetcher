# Thread_fetcher
[Thread_fetcher](https://twitter.com/threadfetcher) is an amazing twitter-bot which when tagged on a useful thread will send back the thread as a hosted website which can be shared and downloaded in various formats.
## Link to product walkthrough
 [Link to the demo video](https://www.loom.com/share/ce0bff00a4714b6790b61be7ccf3b855)
## How it Works?
1. Follow the bot [@threadfetcher on twitter](https://twitter.com/threadfetcher) (The bot will not have the permission to send you a dm if this step is not done)
2. Find a thread you need to save and tag the bot in reply to any of the tweet in the thread (The bot will give you an error message as reply if the tweet does not have any thread)
3. Wait for a couple of seconds for the bot to process the tweet and voilà! your thread formated and hosted as a web page and the link for the same is sent to you as a direct message
4. You can open the webpage to see all the text, video, images, and gifs in the thread with an additional option to download the pdf of the same 
## Libraries used
tweepy - v3.10.0
## Prerequisites
1. python 3.6+ (tested on python3.7)
2. Twitter developer account
3. A google-cloud/firebase account
## How to configure
1. Clone the repository ```git clone https://github.com/abhinav-TB/thread_fetcher.git```
2. RUN ```pip install -r requirements.txt```
3. Change directory to thread_fetcher
4. Create a file called `.env` then copy all contents of `.env_sample` to env file, fill the values of env variables from the ones you recieved after registering the app using the twitter dev account 
5. create a file called `key.json` to put all the firebase configs and place it inside a folder called `config` inside the `thread_fetcher` subfolder (to access a free gcloud storage bucket to store all threads)
6. Add the handle of your bot to `thread_fetcher/main.py`
## How to Run
1. change directory to thread_fetcher folder inside the root folder
2. RUN ```python main.py```

## Run using Docker
If you finding trouble with setting up a dev environment, we have made a dockerfile to make the setup process easier.

Note: make sure the .env file and key.json file are in the right location before building the docker image
1. RUN ```docker build -t thread_fetcher .```
2. RUN ```docker run thread_fetcher ```

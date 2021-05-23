![BFH Banner](https://trello-attachments.s3.amazonaws.com/542e9c6316504d5797afbfb9/542e9c6316504d5797afbfc1/39dee8d993841943b5723510ce663233/Frame_19.png)
# Thread_fetcher
Thread_fetcher is an amazing twitter-bot which when tagged on a usefull thread will send back the thread as a hosted website witch can be shared and downloaded in various formats
## Team members
1. Abhinav TB https://github.com/abhinav-TB
2. FazilBabu https://github.com/fazil47
## Team Id
BFH/recr4RwI8ceNDt7j5/2021
## Link to product walkthrough
[link to video]
## How it Works ?
1. Follow the bot @threadfetcher in twitter (The bot will not have the permission to send you a dm if this step is not done)
2. Find a thread you need to save and tag the bot in reply to any of the tweet in the thread( The bot will give you an eroor message as reply if the tweet does not have any thread)
3. Wait for a couple of seconds for the bot to process the tweet and wohala your thread formated and hosted as a web page and the link for the same is send to you as a direct message
4. You can open the webpage to see all the text , vedio ,images ,gifs in the thread with an additional option to download the pdf of the same 
## Libraries used
tweepy - latest
## Prerequisites
1. python3.6+ (tested on python3.7)
2. Twitter developer account
## How to configure
1. clone the repository ```git clone git@github.com:abhinav-TB/thread_fetcher.git```
2. change directory to thread_fetcher
3. RUN ```pip install -r requirements.txt```
4. create a file called .env then copy all contents of .env_sample to env file ,fill the values of env variables from the ones you recieved after registring the app using the twitter dev account 
## How to Run
1. change directory to thread_fetcher folder inside the root folder
2. RUN ```python main.py```

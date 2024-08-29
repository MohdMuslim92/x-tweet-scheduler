"""
This script automates the process of posting tweets to Twitter using the Tweepy library. 
It authenticates with the Twitter API using OAuth 1.1a and creates a client object for 
Twitter API v2 to post tweets from a predefined list of messages. The script logs all 
tweeting activities, including successful posts and errors, into a log file named 'tweet_log.txt'. 

The key functionalities of this script include:
1. Authenticating to Twitter using API keys and tokens.
2. Posting tweets using the Twitter API v2 client.
3. Logging each tweet and any errors that occur during the process to a log file.
4. Adding a delay between tweets to prevent rate limiting.

To use this script, you need to have the required API keys and tokens, and a list of tweets
in a config file.
"""

import logging  # Import the logging module for logging tweet activity and errors
import time  # Import the time module for adding a delay between tweets
import tweepy  # Import the Tweepy library for Twitter API
from tweets import TWEETS  # Import the list of tweets from tweets.py

# Import the config module for reading the Twitter API credentials
from config import ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET_KEY, BEARER_TOKEN

# Configure logging to write log messages to 'tweet_log.txt'
logging.basicConfig(
    filename='tweet_log.txt',  # Log file path
    level=logging.INFO,  # Logging level set to INFO
    format='%(asctime)s %(message)s'  # Log message format with timestamp
)

# Authenticate to Twitter using OAuth 1.1a credentials
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)  # Set up the API key and secret
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)  # Set up the access token and secret

# Create an API object for Twitter API v1.1 for possible legacy use cases
api = tweepy.API(auth)

# Create a Twitter API v2 client for modern API interactions
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,  # Twitter API bearer token for v2
    access_token=ACCESS_TOKEN,  # Access token for the user's Twitter account
    access_token_secret=ACCESS_TOKEN_SECRET,  # Access token secret
    consumer_key=API_KEY,  # Consumer API key
    consumer_secret=API_SECRET_KEY  # Consumer API secret key
)

def tweet(tweepy_client, message):
    """
    Post a tweet using the provided client object.
    
    Parameters:
    - client: The Tweepy client object configured with Twitter API v2 credentials.
    - message: The text of the tweet to be posted.
    
    Logs the outcome of each attempt to post a tweet, including any errors encountered.
    """
    try:
        # Check if the client object has the 'create_tweet' method
        if not hasattr(tweepy_client, 'create_tweet'):
            raise AttributeError("The client object does not have the 'create_tweet' method.")
        response = tweepy_client.create_tweet(text=message)  # Post the tweet using Twitter API v2
        logging.info("Tweeted: %s", message)  # Log the tweet content using lazy formatting
        # Log the API response for the tweet using lazy formatting
        logging.info("Response: %s", response)
    except tweepy.TweepyException as error:
        # Log any errors from the Tweepy library using lazy formatting
        logging.error("Tweepy error: %s", error)
    except Exception as error:
        # Don't catch AttributeError here; let it propagate for the test
        if not isinstance(error, AttributeError):
            # Log any unexpected errors using lazy formatting
            logging.error("Unexpected error: %s", error)
        raise  # Reraise the exception

def post_all_tweets(tweepy_client):
    """
    Post all tweets from the predefined list TWEETS.

    Iterates through the list of tweets and posts each one using the `tweet` function.
    Includes a delay between each tweet to avoid hitting Twitter's rate limits.
    """
    logging.info("Posting tweets...")  # Log the start of the posting process
    for tweet_message in TWEETS:
        tweet(tweepy_client, tweet_message)  # Post each tweet
        time.sleep(10)  # Wait 10 seconds between tweets to avoid rate limiting

if __name__ == "__main__":
    post_all_tweets(client)  # Execute the tweet posting function when the script runs

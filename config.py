# config.py
"""
Configuration file for Twitter API credentials and other settings.
"""
from tweets import TWEETS  # Import the list of tweets from tweets.py
import os

# Read Twitter API credentials from environment variables
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

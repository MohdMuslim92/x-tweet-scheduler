"""
This module contains unit tests for the Twitter posting functions in main.py.
It uses the unittest framework alongside the unittest.mock module to simulate
different scenarios when interacting with the Twitter API using the Tweepy library.
The key functionalities tested include:

1. Successful tweet posting.
2. Handling of Tweepy exceptions.
3. Handling of unexpected exceptions.
4. Posting multiple tweets in sequence.
5. Handling of empty tweet messages.
6. Handling of partial failures when posting multiple tweets.
7. Handling of tweets containing special characters.
8. Handling of network issues.
9. Handling of null or invalid client objects.

Each test is implemented as a method of the TestTwitterPosting class, which is
a subclass of unittest.TestCase.
Mocking is extensively used to simulate different behaviors of the Twitter client
and to isolate the functions from actual Twitter API calls.
"""

import unittest
from unittest.mock import patch, MagicMock  # Import patch and MagicMock for mocking dependencies
import tweepy  # Import Tweepy to handle exceptions in the tests
from main import tweet, post_all_tweets  # Import the functions to be tested from main.py

class TestTwitterPosting(unittest.TestCase):
    """
    Test case class for testing the Twitter posting functionalities in main.py.
    Each test method within this class tests a specific aspect of the tweet or
    post_all_tweets functions.
    """

    @patch('main.client')  # Mock the client object from main.py to prevent actual API calls
    def test_tweet_success(self, mock_client):
        """
        Test the tweet function for successful tweet posting.
        
        Mocks the Twitter client to simulate a successful tweet posting. 
        Asserts that the create_tweet method was called with the correct parameters.
        """
        # Arrange: Set up the mock client to return a fake tweet ID
        mock_client.create_tweet.return_value = {"data": {"id": "12345"}}
        message = "This is a test tweet."

        # Act: Call the tweet function with the mocked client and a test message
        tweet(mock_client, message)

        # Assert: Verify that create_tweet was called once with the correct text argument
        mock_client.create_tweet.assert_called_with(text=message)

    @patch('main.client')
    def test_tweet_tweepy_exception(self, mock_client):
        """
        Test the tweet function for handling Tweepy exceptions.
        
        Simulates a scenario where the Tweepy client throws an exception.
        Verifies that the exception is logged correctly.
        """
        # Arrange: Set up the mock client to raise a TweepyException when create_tweet is called
        mock_client.create_tweet.side_effect = tweepy.TweepyException("API error")
        message = "This is a test tweet."

        # Act: Call the tweet function with the mocked client and a test message
        tweet(mock_client, message)

        # Assert: Verify that create_tweet was attempted with the correct text argument
        mock_client.create_tweet.assert_called_with(text=message)

    @patch('logging.error')
    def test_tweet_unexpected_exception(self, mock_logging_error):
        """
        Test the tweet function for handling unexpected exceptions.
        
        Simulates an unexpected exception during tweet posting and ensures the error
        is logged correctly.
        """
        # Arrange: Create a mock client and set up a side effect to raise a general Exception
        mock_client = MagicMock()
        exception_instance = Exception("Unexpected error")
        mock_client.create_tweet.side_effect = exception_instance
        message = "This is a test tweet."

        # Act and Assert: Call the tweet function and expect an exception to be raised
        with self.assertRaises(Exception) as context:
            tweet(mock_client, message)

        # Assert: Verify that the error was logged with the expected format and the actual
        # exception instance
        mock_logging_error.assert_called_with("Unexpected error: %s", exception_instance)
        self.assertIn("Unexpected error", str(context.exception))

    @patch('main.client')
    def test_post_all_tweets(self, mock_client):
        """
        Test the post_all_tweets function to ensure it posts all tweets.

        Mocks the list of tweets and the Twitter client to verify that each
        tweet is posted in sequence.
        """
        # Arrange: Mock the client to return a fake tweet ID and provide a list of messages to tweet
        mock_client.create_tweet.return_value = {"data": {"id": "12345"}}
        tweet_messages = ["Tweet 1", "Tweet 2", "Tweet 3"]

        with patch('main.TWEETS', tweet_messages):
            # Act: Call the post_all_tweets function with the mocked client
            post_all_tweets(mock_client)

        # Assert: Verify that create_tweet was called the expected number of times
        self.assertEqual(mock_client.create_tweet.call_count, len(tweet_messages))

    @patch('main.client')
    def test_tweet_empty_message(self, mock_client):
        """
        Test the tweet function for handling an empty message.

        Ensures that the function can handle empty tweet content without errors.
        """
        # Arrange: Set up the mock client and an empty message
        mock_client.create_tweet.return_value = {"data": {"id": "12345"}}
        message = ""

        # Act: Call the tweet function with an empty message
        tweet(mock_client, message)

        # Assert: Verify that create_tweet was called with an empty text argument
        mock_client.create_tweet.assert_called_with(text=message)

    @patch('main.client')
    def test_post_all_tweets_some_failures(self, mock_client):
        """
        Test post_all_tweets function handling partial failures.

        Simulates some tweets failing to post and verifies that the function continues
        processing subsequent tweets.
        """
        # Arrange: Mock the client to simulate some tweets failing and others succeeding
        mock_client.create_tweet.side_effect = [None, tweepy.TweepyException("API error"), {
            "data": {"id": "67890"}}]
        tweet_messages = ["Tweet 1", "Tweet 2", "Tweet 3"]

        with patch('main.TWEETS', tweet_messages):
            # Act: Call the post_all_tweets function
            post_all_tweets(mock_client)

        # Assert: Verify that create_tweet was called the correct number of times
        self.assertEqual(mock_client.create_tweet.call_count, len(tweet_messages))

    @patch('main.client')
    def test_tweet_special_characters(self, mock_client):
        """
        Test the tweet function for handling special characters.

        Verifies that the function correctly handles messages containing special characters.
        """
        # Arrange: Set up the mock client and a message with special characters
        mock_client.create_tweet.return_value = {"data": {"id": "12345"}}
        message = "This is a test tweet with special characters! @#&*()"

        # Act: Call the tweet function with a message containing special characters
        tweet(mock_client, message)

        # Assert: Verify that create_tweet was called with the correct text argument
        mock_client.create_tweet.assert_called_with(text=message)

    @patch('main.client')
    def test_tweet_network_issue(self, mock_client):
        """
        Test the tweet function for handling network issues such as timeout or DNS errors.

        Simulates a network issue and verifies that the function attempts to handle it gracefully.
        """
        # Arrange: Mock the client to raise a TweepyException indicating a network issue
        mock_client.create_tweet.side_effect = tweepy.TweepyException("Network is unreachable")
        message = "This is a test tweet."

        # Act: Call the tweet function and handle the network issue
        tweet(mock_client, message)

        # Assert: Verify that create_tweet was called with the correct text argument
        mock_client.create_tweet.assert_called_with(text=message)

    def test_tweet_null_client(self):
        """
        Test the tweet function for handling a null client object.

        Verifies that the function raises an AttributeError when the client object is None.
        """
        # Arrange: Set up a None client and a test message
        mock_client = None
        message = "This is a test tweet."

        # Act and Assert: Expect an AttributeError due to the None client
        with self.assertRaises(AttributeError):
            tweet(mock_client, message)

def test_tweet_invalid_client(self):
    """
    Test the tweet function for handling an invalid client object.

    Ensures the function raises an AttributeError when the client does not have
    the expected method.
    """
    # Arrange: Define an invalid client class that lacks the create_tweet method
    # pylint: disable=too-few-public-methods
    class InvalidClient:
        """A mock client class used for testing that does not implement required methods."""

    invalid_client = InvalidClient()
    message = "This is a test tweet."

    # Act and Assert: Expect an AttributeError due to the invalid client
    with self.assertRaises(AttributeError) as context:
        tweet(invalid_client, message)

    # Check if the exception message is as expected
    self.assertIn(
        "The client object does not have the 'create_tweet' method.",
        str(context.exception)
    )

if __name__ == '__main__':
    unittest.main()  # Run all test cases

#!/usr/bin/env python3
"""
Twitter Integration Module

This module provides functionality for interacting with Twitter API,
including fetching direct messages, getting mentions, and posting tweets.
It displays messages on a flipdot display using different transitions.
"""

import random
import time
from typing import List, Dict, Any, Optional, Union
from requests import ConnectionError
from transition import transition
from twython import Twython, TwythonError, TwythonRateLimitError

__author__ = 'boselowitz (modernized version)'

# Twitter API credentials
# Note: In a production environment, these should be stored in environment variables
# or a secure configuration file, not hardcoded in the script
APP_KEY = "7z2ojwJHMvqgtEVacwGQ"
APP_SECRET = "SMxNf5P8ROHs3qtxtDhFV0O1u8y56x2H79zvo3H7lA"
OAUTH_TOKEN = "1483550870-WlhywvYdmyNp5BPtpcYazI7QjO8ubgw1per0rej"
OAUTH_TOKEN_SECRET = "1j4zzqLg21l5YuvYVAAt3ZmBjwNDpCnevgPZcuHH4I"

# State tracking
LAST_DM_ID: Optional[int] = None
LAST_DM_CALL: Optional[float] = None
LAST_MENTION_ID: Optional[int] = None
LAST_MENTION_CALL: Optional[float] = None

# Rate limiting constants
RATE_LIMIT_WAIT_TIME = 60  # seconds

# Initialize Twitter client
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# Verify credentials on startup
try:
    twitter.verify_credentials()
    print("Twitter credentials verified successfully")
except (TwythonError, TwythonRateLimitError, ConnectionError) as e:
    print(f"Error verifying Twitter credentials: {e}")


class TwitterRateLimitError(Exception):
    """Exception raised when hitting Twitter rate limits."""
    pass


def rate_limited(min_interval: float = RATE_LIMIT_WAIT_TIME):
    """
    Decorator to rate limit function calls.
    
    Args:
        min_interval: Minimum time between calls in seconds
        
    Returns:
        Decorated function
    """
    def decorator(func):
        last_called = {}
        
        def wrapper(*args, **kwargs):
            current_time = time.time()
            if func.__name__ in last_called:
                elapsed = current_time - last_called[func.__name__]
                if elapsed < min_interval:
                    wait_time = min_interval - elapsed
                    print(f"Rate limiting {func.__name__}, waiting {wait_time:.2f}s")
                    time.sleep(wait_time)
            
            last_called[func.__name__] = time.time()
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


def display_direct_messages() -> None:
    """
    Fetch and display direct messages on the flipdot display.
    Responds to each message with confirmation and deletes it.
    """
    global LAST_DM_ID
    direct_messages = get_latest_direct_messages()

    for dm in direct_messages:
        # Update the last seen DM ID
        if not LAST_DM_ID or int(dm["id"]) > LAST_DM_ID:
            LAST_DM_ID = int(dm["id"])

        # Process the message text and hashtags
        if dm["entities"]["hashtags"]:
            # Strip out hashtags from text (we don't want to display them)
            dm_text = " ".join([word for word in dm["text"].split() if not word.startswith("#")])

            # Find transitions based on hashtags
            possible_transitions = []
            for hashtag in dm["entities"]["hashtags"]:
                try:
                    transition_func = getattr(transition, hashtag["text"])
                    possible_transitions.append(transition_func)
                except AttributeError as e:
                    print(f"Unknown transition: {hashtag['text']}, {e}")

            # Display using a random matching transition or default
            if possible_transitions:
                random.choice(possible_transitions)(dm_text)
            else:
                transition.randomgeneral(dm_text)
        else:
            # No hashtags, use a random general transition
            transition.randomgeneral(dm["text"])

        # Send confirmation message
        try:
            message_preview = dm["text"]
            if len(message_preview) > 130:
                message_preview = message_preview[:126] + "..."
            
            twitter.send_direct_message(
                user_id=dm["sender_id"],
                text=f"Displayed: {message_preview}"
            )
        except (TwythonError, TwythonRateLimitError, ConnectionError) as e:
            print(f"Error sending confirmation DM: {e}")

        # Delete the processed message
        try:
            twitter.destroy_direct_message(id=dm["id"])
        except (TwythonError, TwythonRateLimitError, ConnectionError) as e:
            print(f"Error deleting DM: {e}")


@rate_limited(min_interval=60)
def get_latest_direct_messages() -> List[Dict[str, Any]]:
    """
    Get the latest direct messages from Twitter.
    Rate limited to one call per minute.
    
    Returns:
        List of direct message objects
    """
    global LAST_DM_ID
    
    try:
        if LAST_DM_ID:
            direct_messages = twitter.get_direct_messages(since_id=LAST_DM_ID)
        else:
            direct_messages = twitter.get_direct_messages()
            
        # Update the last seen DM ID
        for dm in direct_messages:
            if not LAST_DM_ID or int(dm["id"]) > LAST_DM_ID:
                LAST_DM_ID = int(dm["id"])
                
        return direct_messages
    
    except (TwythonError, TwythonRateLimitError, ConnectionError) as e:
        print(f"Error getting direct messages: {e}")
        return []


@rate_limited(min_interval=60)
def get_latest_mentions() -> List[Dict[str, Any]]:
    """
    Get the latest mentions from Twitter.
    Rate limited to one call per minute.
    
    Returns:
        List of mention objects
    """
    global LAST_MENTION_ID
    
    try:
        if LAST_MENTION_ID:
            mentions = twitter.get_mentions_timeline(since_id=LAST_MENTION_ID)
        else:
            mentions = twitter.get_mentions_timeline()
            
        # Update the last seen mention ID
        for mention in mentions:
            if not LAST_MENTION_ID or int(mention["id"]) > LAST_MENTION_ID:
                LAST_MENTION_ID = int(mention["id"])
                
        return mentions
    
    except (TwythonError, TwythonRateLimitError, ConnectionError) as e:
        print(f"Error getting mentions: {e}")
        return []


def send_tweet(message: str) -> bool:
    """
    Send a tweet with the given message.
    
    Args:
        message: Text content of the tweet
        
    Returns:
        True if successful, False otherwise
    """
    try:
        twitter.update_status(status=message)
        return True
    except (TwythonError, TwythonRateLimitError, ConnectionError) as e:
        print(f"Error sending tweet: {e}")
        return False


if __name__ == "__main__":
    print("Twitter Integration Module")
    print("This module is intended to be imported, not run directly.")

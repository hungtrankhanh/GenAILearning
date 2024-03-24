import os
from datetime import datetime, timezone
import logging

import requests
import tweepy

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("twitter")

auth = tweepy.OAuthHandler(
    os.environ.get("TWITTER_API_KEY"), os.environ.get("TWITTER_API_SECRET")
)
auth.set_access_token(
    os.environ.get("TWITTER_ACCESS_TOKEN"), os.environ.get("TWITTER_ACCESS_SECRET")
)
api = tweepy.API(auth)


def scrape_user_tweets(username, num_tweets=20):
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """

    # tweets = api.user_timeline(screen_name=username, count=num_tweets)
    tweet_list = requests.get("https://gist.github.com/hungtrankhanh/0fcf456a3258296a2edfd04aa0b03da3/raw/4e52e88d25ca02c2691e3b1e7759af89d12c2c98/eden_tweet.json")
    #
    # for tweet in tweets:
    #     if "RT @" not in tweet.text and not tweet.text.startswith("@"):
    #         tweet_dict = {}
    #         tweet_dict["time_posted"] = str(
    #             datetime.now(timezone.utc) - tweet.created_at
    #         )
    #         tweet_dict["text"] = tweet.text
    #         tweet_dict["url"] = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
    #         tweet_list.append(tweet_dict)

    return tweet_list
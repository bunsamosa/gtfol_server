import re
from typing import Dict

import httpx
from tweety import types

from dbsetup.tweets import TWEETS_ATTRIBUTES
from utils.score_calculator import calculate_score


async def preprocess_text(text: str) -> str:
    """
    Preprocess tweet text to update URLs redirects
    :return: preprocessed tweet text.
    """
    # find all URLs
    urls = re.findall(r"http[s]?://t.co/\w+", text)

    # replace URLs with their final destination
    async with httpx.AsyncClient() as client:
        for twitter_url in urls:
            try:
                response = await client.head(
                    url=twitter_url,
                    follow_redirects=True,
                    timeout=30.0,
                )
                text = text.replace(twitter_url, str(response.url))
            except Exception:
                continue
    return text


async def prep_tweet_data(tweet: types.Tweet) -> Dict:
    """
    Prepares the tweet data before uploading to the database.
    :param tweet: tweety tweet object.
    :return: dict of tweet data.
    """
    response = {
        "tweet_id": int(tweet.id),
    }
    for key, metadata in TWEETS_ATTRIBUTES.items():
        value = tweet.__dict__.get(key)

        # if value is None, set it to the default value
        if value is None:
            value = metadata["default"]

        # parse datetime to isoformat
        if metadata["type"] == "datetime":
            value = value.isoformat()

        # parse media urls
        if key == "media":
            media_arr = tweet.__dict__.get("media", [])
            value = [ele["media_url_https"] for ele in media_arr]

        # parse hashtags
        if key == "hashtags":
            hashtag_arr = tweet.__dict__.get("hashtags", [])
            value = [ele["text"] for ele in hashtag_arr]

        # parse symbols
        if key == "symbols":
            symbol_arr = tweet.__dict__.get("symbols", [])
            value = [ele["text"] for ele in symbol_arr]

        # parse place
        if key == "place":
            place = tweet.__dict__.get("place")
            if place:
                value = place["full_name"]

        meta_key = metadata.get("key", key)
        response[meta_key] = value

    # process tweet text
    response["tweet_text"] = await preprocess_text(text=response["tweet_text"])

    # calculate score
    response["score"] = calculate_score(
        likes=response["likes"],
        comments=response["reply_counts"],
        retweets=response["retweet_counts"] + response["quote_counts"],
    )

    # fetch user id
    response["user_id"] = str(tweet.author.rest_id)

    return response

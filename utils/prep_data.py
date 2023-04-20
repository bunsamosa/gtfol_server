from typing import Dict

from tweety import types

from dbsetup.tweets import TWEETS_ATTRIBUTES
from utils.score_calculator import calculate_score


def prep_tweet_data(tweet: types.Tweet) -> Dict:
    """
    Prepares the tweet data before uploading to the database.
    :param tweet: tweety tweet object.
    :return: dict of tweet data.
    """
    response = {}
    for key, metadata in TWEETS_ATTRIBUTES.items():
        value = tweet.__dict__.get(key, None)

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
            place = tweet.__dict__.get("place", None)
            if place:
                value = place["full_name"]

        response[key] = value

    # calculate score
    response["score"] = calculate_score(
        likes=response["likes"],
        comments=response["reply_counts"],
        retweets=response["retweet_counts"] + response["quote_counts"],
    )

    # fetch user id
    response["user_id"] = tweet.author.rest_id

    return response

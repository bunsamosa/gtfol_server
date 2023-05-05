import logging
import re
from typing import Dict
from typing import Optional

from tweety.bot import Twitter

TWEET_URL_REGEX = r"https?://twitter\.com/\w+/status/(\d+)"
GENERIC_URL_REGEX = r"https?://[^\s]+"


def prep_data(row: Dict) -> Optional[Dict]:
    """
    Prepares the leader board data before uploading to the database.
    :param row: a row from the leader board data.
    """
    response_data = {"twitter_connected": False}

    # check if the demo video is a tweet
    search_text = ""
    demo_url = row["demo_video"]
    is_tweet = re.search(TWEET_URL_REGEX, demo_url)
    is_url = re.search(GENERIC_URL_REGEX, demo_url)

    # check if demo is a tweet
    if is_tweet:
        tweet_id = is_tweet.group(1)
    elif is_url:
        demo_url = is_url.group(0)
    else:
        logging.error(f"Invalid demo video URL: {demo_url}")
        demo_url = ""

    # fetch the launch tweet to read userID and username
    if is_tweet:
        try:
            app = Twitter()
            demo_tweet = app.tweet_detail(identifier=tweet_id)
            tweet_author = demo_tweet.author
            response_data["twitter_user_id"] = tweet_author.rest_id
            response_data["twitter_handle"] = tweet_author.username
            response_data["twitter_user_name"] = tweet_author.name
            response_data["twitter_connected"] = True
            search_text = f"{tweet_author.username} {tweet_author.name}"
        except Exception as e:
            logging.error(f"Error fetching demo tweet: {e}")

    # parse row data
    try:
        response_data["project_name"] = row["project name"].strip()
        response_data["project_description"] = row[
            "what's your one-liner?"
        ].strip()

        search_text = f'{search_text}\
            {response_data["project_namef"]}\
                {response_data["project_description"]}'
        response_data["search_text"] = search_text

        # parse short url
        short_url = row.get("drop a link to your shorts launch post.", None)
        if short_url:
            is_url = re.search(GENERIC_URL_REGEX, short_url)
            if is_url:
                short_url = is_url.group(0)
            else:
                short_url = None

        response_data["project_short_url"] = short_url
        response_data["project_demo_url"] = demo_url
        response_data["points"] = row["points"]
        response_data["house"] = row["house"]
        response_data["rank"] = row["rank"]

        # parse the metric
        current_metric = row["what's the main thing you're focusing on rn?"]
        metric_type = "users"
        if "money" in current_metric:
            metric_type = "revenue"
        response_data["metric_type"] = metric_type

        # parse this week and last week metric
        if metric_type == "users":
            response_data["last_week_metric"] = row[
                "how many users did you have the previous week?"
            ]
            response_data["this_week_metric"] = row[
                "how many user's do you have?"
            ]
        else:
            response_data["last_week_metric"] = row[
                "how much revenue did you have the previous week?"
            ]
            response_data["this_week_metric"] = row["what's your revenue at?"]

        response_data["metric_change"] = round(
            response_data["this_week_metric"]
            - response_data["last_week_metric"],
            2,
        )
    except Exception as e:
        logging.error(f"Error parsing row data: {e}")
        logging.error(f"Row data: {row}")
        return None

    return response_data

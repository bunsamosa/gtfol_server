import logging
import os

from appwrite.client import Client
from appwrite.services.databases import Databases

from core.tweet_loader import load_tweets

# read environment variables
appwrite_endpoint = os.getenv("APPWRITE_ENDPOINT")
appwrite_project = os.getenv("APPWRITE_PROJECT")
appwrite_api_key = os.getenv("APPWRITE_API_KEY")
appwrite_database_id = os.getenv("APPWRITE_DATABASE_ID")
twitter_cookie = os.getenv("TWITTER_COOKIE")

if not all(
    (
        appwrite_endpoint,
        appwrite_project,
        appwrite_api_key,
        appwrite_database_id,
        twitter_cookie,
    ),
):
    raise ValueError("Missing environment variables.")

# setup appwrite client
appwrite = Client()
appwrite.set_endpoint(appwrite_endpoint).set_project(appwrite_project).set_key(
    appwrite_api_key,
)

# setup collections
context = {
    "database_id": appwrite_database_id,
    "collection_id": "tweets",
    "collection_name": "tweets",
    "twitter_cookie": twitter_cookie,
}
databases = Databases(appwrite)

# setup logging
log_file_path = os.path.join(os.getcwd(), "logs", "log_general.log")
logging.basicConfig(
    filename=log_file_path,
    filemode="w",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)

# scrape data
load_tweets(
    query="(@_buildspace OR @_nightsweekends) -filter:nativeretweets -filter:retweets -filter:quote -filter:replies",
    keywords=["@_buildspace", "@_nightsweekends"],
    search_filter=None,
    db=databases,
    context=context,
    exponential_backoff=True,
    max_tweets=1000000,
)

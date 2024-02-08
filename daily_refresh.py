import logging
import os

from appwrite.client import Client
from appwrite.services.databases import Databases

from archive.tweet_updater import update_tweets

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
log_file_path = os.path.join(os.getcwd(), "logs", "log_refresh.log")
logging.basicConfig(
    filename=log_file_path,
    filemode="w",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)
# update tweets
update_tweets(db=databases, context=context, max_tweets=100000)

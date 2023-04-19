import os

from appwrite.client import Client
from appwrite.services.databases import Databases
from tweety import filters

from tweet_loader import load_tweets

# read environment variables
appwrite_endpoint = os.getenv("APPWRITE_ENDPOINT")
appwrite_project = os.getenv("APPWRITE_PROJECT")
appwrite_api_key = os.getenv("APPWRITE_API_KEY")
appwrite_database_id = os.getenv("APPWRITE_DATABASE_ID")

if not all(
    (
        appwrite_endpoint,
        appwrite_project,
        appwrite_api_key,
        appwrite_database_id,
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
}
databases = Databases(appwrite)

# scrape data
load_tweets(
    keyword="@_buildspace",
    search_filter=filters.SearchFilters.Latest(),
    db=databases,
    context=context,
    max_tweets=1000,
)

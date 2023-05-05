import asyncio
import logging
import os

from appwrite.client import Client
from appwrite.services.databases import Databases

from core.house_points import setup
from core.leaderboard_loader import update_leaderboard

# read environment variables
appwrite_endpoint = os.getenv("APPWRITE_ENDPOINT")
appwrite_project = os.getenv("APPWRITE_PROJECT")
appwrite_api_key = os.getenv("APPWRITE_API_KEY")
appwrite_database_id = os.getenv("APPWRITE_DATABASE_ID")
leaderboard_url = os.getenv("LEADERBOARD_URL")
leaderboard_token = os.getenv("LEADERBOARD_TOKEN")

if not all(
    (
        appwrite_endpoint,
        appwrite_project,
        appwrite_api_key,
        appwrite_database_id,
        leaderboard_url,
        leaderboard_token,
    ),
):
    raise ValueError("Missing environment variables.")

# setup appwrite client
appwrite = Client()
appwrite.set_endpoint(appwrite_endpoint).set_project(appwrite_project).set_key(
    appwrite_api_key,
)

# setup collections
points_collection_context = {
    "database_id": appwrite_database_id,
    "collection_id": "buildspace_house_points",
    "collection_name": "buildspace house points",
}

context = {
    "database_id": appwrite_database_id,
    "collection_id": "buildspace_leaderboard",
    "collection_name": "buildspace leaderboard",
    "points_context": points_collection_context,
}
databases = Databases(appwrite)

# setup logging
log_file_path = os.path.join(os.getcwd(), "logs", "log_leaderboard.log")
logging.basicConfig(
    filename=log_file_path,
    filemode="w",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)

# setup points collection
setup(db=databases, context=points_collection_context)

# scrape data
asyncio.run(
    update_leaderboard(
        url=leaderboard_url,
        token=leaderboard_token,
        db=databases,
        context=context,
    ),
)

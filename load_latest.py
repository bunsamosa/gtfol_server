import asyncio
import logging
import os

import asyncpg
from tweety import filters

from core.tweet_loader import load_tweets
from utils.query_builder import build_insert_query

# read environment variables
postgres_url = os.getenv("POSTGRES_URL")
postgres_schema = os.getenv("POSTGRES_SCHEMA")
twitter_cookie = os.getenv("TWITTER_COOKIE")

if not all(
    (
        postgres_url,
        postgres_schema,
        twitter_cookie,
    ),
):
    raise ValueError("Missing environment variables.")


# setup collections
context = {
    "postgres_url": postgres_url,
    "postgres_schema": postgres_schema,
    "collection_name": "tweets",
    "twitter_cookie": twitter_cookie,
}

# setup logging
log_file_path = os.path.join(os.getcwd(), "logs", "log_latest.log")
logging.basicConfig(
    filename=log_file_path,
    filemode="w",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)


async def load_data():
    """
    Load latest tweets into the database.
    """
    # connect to postgres
    conn = await asyncpg.connect(postgres_url)

    # set search path (schema)
    await conn.execute(f"SET search_path TO {postgres_schema}")

    # read tweet data
    tweet_data = load_tweets(
        query="(@_buildspace OR @_nightsweekends) -filter:nativeretweets -filter:retweets -filter:quote -filter:replies",
        keywords=["@_buildspace", "@_nightsweekends"],
        search_filter=filters.SearchFilters.Latest(),
        context=context,
        max_tweets=100,
        time_sleep=15,
    )

    insert_query = build_insert_query(tweets=tweet_data, context=context)
    response = await conn.execute(insert_query)
    logging.info(f"Result: {response} tweets")


if __name__ == "__main__":
    asyncio.run(load_data())

import time

from appwrite.query import Query
from appwrite.services.databases import Databases
from tweety.bot import Twitter

from utils import docbuilder
from utils.prep_data import prep_tweet_data


def update_data(db: Databases, results: list, context: dict) -> None:
    """
    Update tweet data in database.
    :param db: appwrite database instance
    :param results: list of tweet data
    :param context: context dictionary
    """
    for row in results["documents"]:
        tweet_id = row["$id"]

        # fetch tweet data
        print(f"Fetching tweet {tweet_id}...")
        app = Twitter()
        try:
            tweet = app.tweet_detail(tweet_id)
            upload_data = prep_tweet_data(tweet)
        except Exception:
            print(f"Error fetching tweet {tweet_id}...")
            continue

        # update tweet data
        docbuilder.update_document(
            db=db,
            data=upload_data,
            document_id=tweet.id,
            context=context,
        )
        print(f"Updated tweet {tweet_id}...")


def update_tweets(db: Databases, context: dict, max_tweets=1000) -> None:
    """
    Fetch tweets from DB and update their latest data.
    :param db: appwrite database instance
    :param context: context dictionary
    :param max_tweets: max number of tweets to update
    """
    print("Starting tweet updater...")
    print("------------------------------------------------")

    offset = 0
    limit = 20

    if max_tweets < limit:
        limit = max_tweets

    # fetch and update tweets
    while limit <= max_tweets:
        print(f"Updating tweets {offset} to {offset + limit}...")

        results = db.list_documents(
            database_id=context["database_id"],
            collection_id=context["collection_id"],
            queries=[
                Query.order_desc("created_on"),
                Query.limit(limit),
                Query.offset(offset),
            ],
        )

        update_data(db=db, results=results, context=context)
        print(f"Updated {len(results['documents'])} tweets...")
        print("------------------------------------------------")

        offset += limit
        limit += 20
        time.sleep(5)

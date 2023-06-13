import logging
import time

from appwrite.query import Query
from appwrite.services.databases import Databases
from tweety.bot import Twitter

from utils import docbuilder
from utils.prep_tweet_data import prep_tweet_data


def update_data(app, db: Databases, results: list, context: dict) -> int:
    """
    Update tweet data in database.
    :param db: appwrite database instance
    :param results: list of tweet data
    :param context: context dictionary
    """
    err_count = 0
    for row in results["documents"]:
        tweet_id = row["$id"]

        # fetch tweet data
        logging.info(f"Fetching tweet {tweet_id}...")
        try:
            tweet = app.tweet_detail(tweet_id)
            upload_data = prep_tweet_data(tweet)
        except Exception:
            logging.info(f"Error fetching tweet {tweet_id}...")
            err_count += 1
            continue
        else:
            # count only consecutive errors
            err_count = 0

        # update tweet data
        docbuilder.update_document(
            db=db,
            data=upload_data,
            document_id=tweet.id,
            context=context,
        )
        logging.info(f"Updated tweet {tweet_id}...")
    return err_count


def update_tweets(db: Databases, context: dict, max_tweets=1000) -> None:
    """
    Fetch tweets from DB and update their latest data.
    :param db: appwrite database instance
    :param context: context dictionary
    :param max_tweets: max number of tweets to update
    """
    logging.info("Starting tweet updater...")
    logging.info("------------------------------------------------")
    offset = 0
    limit = 20

    if max_tweets < limit:
        limit = max_tweets

    app = Twitter(context["twitter_cookie"])
    # fetch and update tweets
    while offset <= max_tweets:
        logging.info(f"Updating tweets {offset} to {offset + limit}...")

        # fetch results from database
        results = db.list_documents(
            database_id=context["database_id"],
            collection_id=context["collection_id"],
            queries=[
                Query.order_desc("created_on"),
                Query.limit(limit),
                Query.offset(offset),
            ],
        )
        results_len = len(results["documents"])
        if results_len == 0:
            logging.info("No more tweets to update...")
            break

        # update tweet data
        err_count = update_data(
            app=app,
            db=db,
            results=results,
            context=context,
        )

        # retry if too many errors
        time_sleep = 5
        while err_count > 5:
            logging.info(
                f"Too many errors {err_count}, Retrying in {time_sleep}...",
            )
            time.sleep(time_sleep)

            app = Twitter(cookies=context["twitter_cookie"])
            err_count = update_data(
                app=app,
                db=db,
                results=results,
                context=context,
            )

            # exponential backoff
            if time_sleep < 300:
                time_sleep += 10

        logging.info(f"Updated {len(results['documents'])} tweets...")
        logging.info("------------------------------------------------")

        offset += limit
        time.sleep(5)

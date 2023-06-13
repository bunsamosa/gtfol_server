import logging
import time

from appwrite.services.databases import Databases
from tweety.bot import Twitter

from dbsetup.common import setup_collection
from dbsetup.tweets import TWEETS_ATTRIBUTES
from utils import docbuilder
from utils.prep_tweet_data import prep_tweet_data


def load_tweets(
    query: str,
    keywords: list[str],
    search_filter: str,
    db: Databases,
    context: dict,
    exponential_backoff: bool = False,
    max_tweets: int = 100000,
) -> None:
    """
    Scrape tweets from twitter and upload to appwrite database.
    :param keyword: keyword to search for
    :param search_filter: filter to apply to search
    :param db: appwrite database instance
    :param context: context dictionary
    :param max_tweets: maximum number of tweets to scrape
    """
    logging.info("------------------------------------------------")
    logging.info(f"Starting scraper for {keywords}")
    total_scraped = 0
    total_errors = 0
    total_inserted = 0
    total_ignored = 0
    total_updated = 0
    page_number = 0

    # setup collection
    app = Twitter(cookies=context["twitter_cookie"])
    setup_collection(attributes=TWEETS_ATTRIBUTES, db=db, context=context)

    # search for tweets
    results_cursor = results = app.search(
        keyword=query,
        wait_time=5,
        filter_=search_filter,
    )

    # run until max tweets reached or no more results
    while results:
        page_number += 1
        logging.info(f"Scraping page {page_number}...")

        # upload to database
        for tweet in results:
            total_scraped += 1
            logging.info(f"Processing tweet {total_scraped}...")
            upload_data = prep_tweet_data(tweet=tweet)

            # ignore retweets, replies, quoted tweets,
            # and possibly sensitive tweets
            if not any(word in tweet.text for word in keywords):
                total_ignored += 1
                continue

            # create a document if it doesn't exist, otherwise update it
            try:
                document_exists = docbuilder.create_document(
                    db=db,
                    data=upload_data,
                    document_id=tweet.id,
                    context=context,
                )
                if document_exists:
                    docbuilder.update_document(
                        db=db,
                        data=upload_data,
                        document_id=tweet.id,
                        context=context,
                    )
                    total_updated += 1
                else:
                    total_inserted += 1
            except Exception as e:
                total_errors += 1
                logging.info("-----------------------------------------------")
                logging.info(upload_data)
                logging.info(e)
                logging.info("-----------------------------------------------")

        logging.info("------------------------------------------------")
        logging.info(f"Page {page_number} scraped.")
        logging.info(f"Total scraped: {total_scraped}")
        logging.info(f"Total inserted: {total_inserted}")
        logging.info(f"Total updated: {total_updated}")
        logging.info(f"Total ignored: {total_ignored}")
        logging.info(f"Total errors: {total_errors}")
        logging.info(f"Do we have next page: {results_cursor.is_next_page}")
        logging.info("------------------------------------------------")

        # check if max tweets reached
        if total_scraped >= max_tweets:
            logging.info("------------------------------------------------")
            logging.info(f"Max tweets reached: {max_tweets}")
            logging.info("------------------------------------------------")
            break

        # check if next page exists
        if not results_cursor.is_next_page:
            logging.info("------------------------------------------------")
            logging.info("No more results.")
            logging.info("------------------------------------------------")
            break

        # get next page of results
        # retry if error fetching next page
        results = False
        retries = 0
        time_sleep = 5
        while not results:
            logging.info(f"Fetching next page, retries: {retries}")
            logging.info(f"Wait time: {time_sleep} seconds")
            try:
                retries += 1
                time.sleep(time_sleep)
                results = results_cursor.get_next_page()
            except Exception:
                logging.info("Error while fetching data from next page")

            if exponential_backoff and time_sleep < 300:
                time_sleep += 10

import logging
import time
from typing import List

from tweety import Twitter

from utils.processor import prep_tweet_data


async def load_tweets(
    query: str,
    keywords: list[str],
    search_filter: str,
    context: dict,
    max_tweets: int = 100000,
    exponential_backoff: bool = False,
    time_sleep: int = 5,
) -> List:
    """
    Scrape tweets from twitter given a search query and keywords to look for.
    :param query: twitter search query
    :param keywords: a list of keywords to look for in the tweets
    :param search_filter: filter to apply to search
    :param context: context dictionary
    :param max_tweets: maximum number of tweets to scrape
    :param exponential_backoff: whether to use exponential backoff
    :param time_sleep: time to sleep between retries
    :return: list of tweets
    """
    logging.info("------------------------------------------------")
    logging.info(f"Starting scraper for {keywords}")
    total_scraped = 0
    total_ignored = 0
    page_number = 0
    data_fetched = []

    # setup twitter client
    app = Twitter("session")

    # try:
    #     app.load_cookies(context["twitter_cookie"])
    # except Exception as exc:
    #     logging.error("Unable to login from session")
    #     logging.error(exc)
    logging.info("Signing in with password")
    app.sign_in(context["twitter_username"], context["twitter_pwd"])

    # search for tweets
    results_cursor = results = app.search(
        keyword=query,
        wait_time=time_sleep,
        filter_=search_filter,
    )

    # run until max tweets reached or no more results
    while results:
        page_number += 1
        logging.info(f"Scraping page {page_number}...")

        # process tweets
        for tweet in results:
            total_scraped += 1
            logging.info(f"Processing tweet {total_scraped}...")
            json_data = await prep_tweet_data(tweet=tweet)

            # ignore retweets, replies, quoted tweets,
            # and possibly sensitive tweets
            if not any(word in tweet.text for word in keywords):
                total_ignored += 1
                continue

            data_fetched.append(json_data)

        logging.info("------------------------------------------------")
        logging.info(f"Page {page_number} scraped.")
        logging.info(f"Total scraped: {total_scraped}")
        logging.info(f"Total ignored: {total_ignored}")
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
        # retry if error fetching next page - max 20 retries
        results = False
        retries = 0
        while not results and retries < 20:
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

    return data_fetched

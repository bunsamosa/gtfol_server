from typing import Dict
from typing import List

from pypika import PostgreSQLQuery as Query
from pypika import Table


data_columns = (
    "tweet_id",
    "created_on",
    "tweet_text",
    "bookmark_count",
    "quote_counts",
    "likes",
    "reply_counts",
    "retweet_counts",
    "tweet_language",
    "place",
    "media",
    "hashtags",
    "symbols",
    "score",
    "user_id",
)


def build_insert_query(tweets: List, context: Dict) -> str:
    """
    Given tweets, build a query string to insert into the database.
    :param tweets: List of tweet objects
    :param context: Context object
    """
    # define tweets table
    table = Table(context["collection_name"])

    # build query
    insert_query = Query.into(table).columns(*data_columns)
    values_to_insert = [
        (tweet[key] for key in data_columns) for tweet in tweets
    ]
    insert_query = insert_query.insert(*values_to_insert)
    sql_query = insert_query.get_sql()

    # add ON CONFLICT clause to handle duplicates
    on_conflict_columns = [col for col in data_columns if col != "tweet_id"]
    on_conflict_assignments = ", ".join(
        f"{col} = EXCLUDED.{col}" for col in on_conflict_columns
    )
    on_conflict_clause = (
        f" ON CONFLICT (tweet_id) DO UPDATE SET {on_conflict_assignments}"
    )
    sql_query = sql_query + on_conflict_clause

    return sql_query

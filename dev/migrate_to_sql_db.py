import asyncio
import os

import asyncpg
from appwrite.client import Client
from appwrite.query import Query as AppwriteQuery
from appwrite.services.databases import Databases
from pypika import PostgreSQLQuery as Query
from pypika import Table

# read environment variables
appwrite_endpoint = os.getenv("APPWRITE_ENDPOINT")
appwrite_project = os.getenv("APPWRITE_PROJECT")
appwrite_api_key = os.getenv("APPWRITE_API_KEY")
appwrite_database_id = os.getenv("APPWRITE_DATABASE_ID")

postgres_url = os.getenv("POSTGRES_URL")
postgres_schema = os.getenv("POSTGRES_SCHEMA")

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
context = {
    "database_id": appwrite_database_id,
    "collection_id": "tweets",
    "collection_name": "tweets",
}
databases = Databases(appwrite)
data_columns = (
    "tweet_id",
    "created_on",
    "tweet_text",
    "bookmark_count",
    "quote_count",
    "likes",
    "reply_count",
    "retweet_count",
    "tweet_language",
    "place",
    "media",
    "hashtags",
    "symbols",
    "score",
    "user_id",
)


async def migrate_data():
    """
    Migrate data from Appwrite NOSQL to Postgres
    """
    # connect to postgres
    conn = await asyncpg.connect(postgres_url)

    # set search path (schema)
    await conn.execute(f"SET search_path TO {postgres_schema}")

    # read data from appwrite and insert into postgres
    return_rows = 10
    total = 0
    limit = 1000

    # Define the tweets table
    tweets = Table(context["collection_name"])

    # Create an INSERT query for multiple records
    insert_query = Query.into(tweets).columns(*data_columns)

    while return_rows > 0:
        # read data
        rows = databases.list_documents(
            collection_id=context["collection_id"],
            database_id=context["database_id"],
            queries=[
                AppwriteQuery().offset(total),
                AppwriteQuery().limit(limit),
            ],
        )
        return_rows = len(rows["documents"])
        total += return_rows
        print(f"Rows fetched: {return_rows}, Total: {total}")

        if return_rows == 0:
            break

        # insert into postgres
        values_to_insert = [
            (
                int(tweet["$id"]),
                tweet["created_on"],
                tweet["text"],
                tweet["bookmark_count"],
                tweet["quote_counts"],
                tweet["likes"],
                tweet["reply_counts"],
                tweet["retweet_counts"],
                tweet["language"],
                tweet["place"],
                tweet["media"],
                tweet["hashtags"],
                tweet["symbols"],
                tweet["score"],
                tweet["user_id"],
            )
            for tweet in rows["documents"]
        ]
        query = insert_query.insert(*values_to_insert)
        sql_query = query.get_sql()

        # Add ON CONFLICT clause to handle duplicates
        on_conflict_columns = [
            col for col in data_columns if col != "tweet_id"
        ]
        on_conflict_assignments = ", ".join(
            f"{col} = EXCLUDED.{col}" for col in on_conflict_columns
        )
        on_conflict_clause = (
            f" ON CONFLICT (tweet_id) DO UPDATE SET {on_conflict_assignments}"
        )
        sql_query = sql_query + on_conflict_clause

        result = await conn.execute(sql_query)
        print(f"Inserted {result} rows")

    await conn.close()


asyncio.run(migrate_data())

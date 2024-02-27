import asyncio
import logging
import os

import asyncpg
from pypika import PostgreSQLQuery as Query

from core.context_loader import load_context
from core.embed import embed_text
from core.tables import tweet_embeds_table
from core.tables import tweets_table


# load context
context = load_context()

# setup logging
log_file_path = os.path.join(os.getcwd(), "logs", "embeddings.log")
logging.basicConfig(
    filename=log_file_path,
    filemode="w",
    format="%(asctime)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.INFO,
)


async def generate_embeddings():
    """
    Generate embeddings for all tweets in the database.
    """
    # connect to postgres
    conn = await asyncpg.connect(context["postgres_url"])

    # set search path (schema)
    await conn.execute(f"SET search_path TO {context['postgres_schema']}")

    # load all tweets from DB
    query = (
        Query.from_(tweets_table)
        .select("tweet_id", "tweet_text")
        .where(
            tweets_table.field("tweet_id").notin(
                tweet_embeds_table.select("tweet_id"),
            ),
        )
    )
    query = query.get_sql()
    tweets = await conn.fetch(query)
    logging.info(f"Fetched {len(tweets)} tweets for embedding generation")

    # insert query
    insert_query = Query.into(tweet_embeds_table).columns(
        "tweet_id",
        "embedding",
    )

    # generate embeddings
    insert_values = []
    for tweet in tweets:
        tweet_text = tweet["tweet_text"]
        tweet_id = tweet["tweet_id"]

        try:
            embedding = await embed_text(tweet_text)
        except Exception as exc:
            logging.error(f"Error generating embedding {tweet_id}: {exc}")
            continue

        if len(embedding.data) > 1:
            logging.warning(f"Multiple embeddings for tweet {tweet_id}")
            continue

        vector = embedding.data[0].embedding
        insert_values.append((tweet_id, vector))

        if len(insert_values) >= 10:
            query = insert_query.insert(*insert_values)
            query = query.get_sql()
            response = await conn.execute(query)
            logging.info(f"Inserted {response} tweet embeddings")
            insert_values = []

    # insert remaining values
    if insert_values:
        query = insert_query.insert(*insert_values)
        query = query.get_sql()
        response = await conn.execute(query)
        logging.info(f"Inserted {response} tweet embeddings")

    await conn.close()


if __name__ == "__main__":
    asyncio.run(generate_embeddings())

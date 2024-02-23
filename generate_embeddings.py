import asyncio

import asyncpg

from core.context_loader import load_context
from core.embed import embed_text


# load context
context = load_context()


async def generate_embeddings():
    """
    Generate embeddings for all tweets in the database.
    """
    # connect to postgres
    conn = await asyncpg.connect(context["postgres_url"])

    # set search path (schema)
    await conn.execute(f"SET search_path TO {context['postgres_schema']}")

    # load all tweets from DB
    tweets = await conn.fetch("SELECT * FROM tweets LIMIT 10")

    for tweet in tweets:
        tweet_text = tweet["tweet_text"]

        # generate embeddings
        embedding = await embed_text(tweet_text)
        print(embedding.data)

    await conn.close()


if __name__ == "__main__":
    asyncio.run(generate_embeddings())

import asyncio

import asyncpg

from core.context_loader import load_context
from utils.processor import preprocess_text


async def main():
    context = load_context()
    conn = await asyncpg.connect(context["postgres_url"])
    await conn.execute(f"SET search_path TO {context['postgres_schema']}")

    # load all tweets from DB and preprocess the text
    tweets = await conn.fetch("SELECT * FROM tweets")

    for tweet in tweets:
        tweet_text = tweet["tweet_text"]

        # preprocess tweet text
        tweet_text = await preprocess_text(tweet_text)
        await conn.execute(
            "UPDATE tweets SET tweet_text = $1 WHERE tweet_id = $2",
            tweet_text,
            tweet["tweet_id"],
        )

    await conn.close()


if __name__ == "__main__":
    asyncio.run(main())

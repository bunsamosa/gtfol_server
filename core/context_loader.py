import os


def load_context():
    """
    Load context data from environment variables.
    """
    context = {
        "postgres_url": "POSTGRES_URL",
        "postgres_schema": "POSTGRES_SCHEMA",
        "twitter_cookie": "TWITTER_COOKIE",
        "tweets_db": "TWEETS_DB",
    }

    for key, env_var in context.items():
        value = os.getenv(env_var)
        if not value:
            raise ValueError(f"Missing environment variable: {env_var}")

        context[key] = value

    return context

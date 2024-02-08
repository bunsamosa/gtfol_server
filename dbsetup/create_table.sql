CREATE TABLE tweets (
    tweet_id VARCHAR(100) PRIMARY KEY,
    created_on TIMESTAMP NOT NULL,
    tweet_text TEXT NOT NULL,
    bookmark_count INTEGER NOT NULL CHECK (bookmark_count >= 0),
    quote_counts INTEGER NOT NULL CHECK (quote_counts >= 0),
    likes INTEGER NOT NULL CHECK (likes >= 0),
    reply_counts INTEGER NOT NULL CHECK (reply_counts >= 0),
    retweet_counts INTEGER NOT NULL CHECK (retweet_counts >= 0),
    tweet_language VARCHAR(10) NOT NULL,
    place VARCHAR(1000),
    media TEXT[] DEFAULT ARRAY[]::TEXT[], -- Default empty array
    hashtags TEXT[] DEFAULT ARRAY[]::TEXT[], -- Default empty array
    symbols TEXT[] DEFAULT ARRAY[]::TEXT[], -- Default empty array
    score BIGINT NOT NULL CHECK (score >= 0),
    user_id VARCHAR(100) NOT NULL
);

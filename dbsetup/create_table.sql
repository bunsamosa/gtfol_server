CREATE TABLE tweets (
    tweet_id BIGINT PRIMARY KEY,
    created_on TIMESTAMP NOT NULL,
    tweet_text VARCHAR(500) NOT NULL,
    bookmark_count INTEGER NOT NULL CHECK (bookmark_count >= 0),
    quote_count INTEGER NOT NULL CHECK (quote_count >= 0),
    likes INTEGER NOT NULL CHECK (likes >= 0),
    reply_count INTEGER NOT NULL CHECK (reply_count >= 0),
    retweet_count INTEGER NOT NULL CHECK (retweet_count >= 0),
    tweet_language VARCHAR(10) NOT NULL,
    place VARCHAR(1000),
    media TEXT[] DEFAULT ARRAY[]::TEXT[], -- Default empty array
    hashtags TEXT[] DEFAULT ARRAY[]::TEXT[], -- Default empty array
    symbols TEXT[] DEFAULT ARRAY[]::TEXT[], -- Default empty array
    score BIGINT NOT NULL CHECK (score >= 0),
    user_id VARCHAR(100) NOT NULL
);

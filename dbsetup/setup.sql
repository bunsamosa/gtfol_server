-- Table for storing tweet data
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


-- Table for storing tweet embeddings
CREATE TABLE tweet_embeds (
  tweet_id VARCHAR(100) PRIMARY KEY,
  embedding vector(1536)
);


-- Function for fetching tweets
CREATE OR REPLACE FUNCTION match_tweets (
  query_embedding vector(1536),
  match_threshold FLOAT,
  match_count INT
)
RETURNS TABLE (
  tweet_id VARCHAR(100),
  similarity FLOAT
)
LANGUAGE SQL stable
AS $$
  SELECT
    t1.tweet_id,
    1 - (t1.embedding <=> query_embedding) AS similarity
  FROM gtfol.tweet_embeds t1
  WHERE 1 - (t1.embedding <=> query_embedding) > match_threshold
  ORDER BY (t1.embedding <=> query_embedding) ASC
  LIMIT match_count;
$$;

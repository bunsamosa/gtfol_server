# GTFOL server
Scrape tweets, calculate score and generate embeddings for semantic search.

### Loading data
- Every 15 minutes, read latest 500 tweets that mention @_buildspace or @_nightsweekends and insert them to DB.
- If the tweets already exist, update their stats (likes, retweets, replies)
- If the tweets are counted. Retweets, quote mentions, reply mentions are not counted.

### Embedding generation
- Preprocessing
    - Convert to lowercase
    - Replace attachment and demo URLs with placeholders
    - Remove emojis, multiple spaces and newlines
- Generate embedding using OpenAI `text-embedding-3-small` model
- Store the embeddings on Postgres with `pg-vector` (self-hosted supabase instance)

### Scoring
- Generate a score based on engagement using below weights
    - 1 like = 1 point
    - 1 reply = 5 points
    - 1 retweet = 10 points
- Bonus points
    - 10 of anything = 20% extra points
    - 100 of anything = 35% extra points
    - 1000 of anything = 50% extra points
    - Bonus points are stacked. So 1000 likes = 2050 points (105% extra points)

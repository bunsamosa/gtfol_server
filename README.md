# Tweet loader
Tweet loader for GTFOL

### Loading data
- Every 15 minutes, read latest 500 tweets that mention @_buildspace or @_nightsweekends and insert them to DB.
- If the tweets already exist, update their stats (likes, retweets, replies)
- If the tweets are counted. Retweets, quote mentions, reply mentions are not counted.

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

The code does not follow many conventions and best practices. It is written to get the job done.

Feel free to send a PR if you want to improve it.

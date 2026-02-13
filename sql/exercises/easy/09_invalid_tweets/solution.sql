-- Solution: Invalid Tweets
SELECT
    tweet_id
FROM tweets
WHERE LENGTH(content) > 140
ORDER BY tweet_id;

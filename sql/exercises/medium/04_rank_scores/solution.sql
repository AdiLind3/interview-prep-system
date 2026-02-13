-- Solution: Rank Scores
SELECT
    score,
    DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank
FROM scores
ORDER BY score DESC;

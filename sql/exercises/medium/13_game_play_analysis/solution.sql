-- Solution: Game Play Analysis IV
WITH first_login AS (
    SELECT
        player_id,
        MIN(event_date) AS first_date
    FROM activity
    GROUP BY player_id
)
SELECT
    ROUND(
        SUM(CASE WHEN a.event_date IS NOT NULL THEN 1 ELSE 0 END) * 1.0
        / COUNT(f.player_id),
        2
    ) AS fraction
FROM first_login f
LEFT JOIN activity a
    ON f.player_id = a.player_id
    AND a.event_date = DATE(f.first_date, '+1 day');

-- Solution: Confirmation Rate
SELECT
    s.user_id,
    ROUND(IFNULL(
        AVG(CASE WHEN c.action = 'confirmed' THEN 1.0 ELSE 0.0 END),
        0.00
    ), 2) AS confirmation_rate
FROM signups s
LEFT JOIN confirmations c ON s.user_id = c.user_id
GROUP BY s.user_id
ORDER BY s.user_id;

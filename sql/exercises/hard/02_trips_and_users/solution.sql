-- Solution: Trips and Users
SELECT
    t.request_at AS day,
    ROUND(
        SUM(CASE WHEN t.status LIKE 'cancelled%' THEN 1.0 ELSE 0.0 END) / COUNT(*),
        2
    ) AS cancellation_rate
FROM trips t
INNER JOIN users c ON t.client_id = c.users_id AND c.banned = 'No'
INNER JOIN users d ON t.driver_id = d.users_id AND d.banned = 'No'
WHERE t.request_at BETWEEN '2024-10-01' AND '2024-10-03'
GROUP BY t.request_at
ORDER BY t.request_at;

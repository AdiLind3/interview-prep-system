-- Solution: Friend Requests Acceptance Rate
SELECT
    ROUND(
        IFNULL(
            (SELECT COUNT(DISTINCT requester_id || '-' || accepter_id) FROM request_accepted) * 1.0
            / (SELECT COUNT(DISTINCT sender_id || '-' || send_to_id) FROM friend_request),
            0.00
        ),
        2
    ) AS accept_rate;

-- Insert friend requests
INSERT INTO friend_request (sender_id, send_to_id, request_date) VALUES
(1, 2, '2024-06-01'),
(1, 3, '2024-06-01'),
(1, 4, '2024-06-01'),
(2, 3, '2024-06-02'),
(3, 4, '2024-06-09'),
(1, 2, '2024-06-11');

-- Insert accepted requests
INSERT INTO request_accepted (requester_id, accepter_id, accept_date) VALUES
(1, 2, '2024-06-03'),
(1, 3, '2024-06-08'),
(2, 3, '2024-06-08'),
(3, 4, '2024-06-09'),
(3, 4, '2024-06-10');

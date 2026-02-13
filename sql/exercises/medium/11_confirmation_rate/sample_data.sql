-- Insert signups
INSERT INTO signups (user_id, time_stamp) VALUES
(3, '2024-03-01 09:00:00'),
(7, '2024-03-05 10:00:00'),
(2, '2024-03-08 11:00:00'),
(6, '2024-03-12 14:00:00');

-- Insert confirmations
INSERT INTO confirmations (user_id, time_stamp, action) VALUES
(3, '2024-03-01 09:05:00', 'timeout'),
(3, '2024-03-02 10:00:00', 'timeout'),
(7, '2024-03-05 10:05:00', 'confirmed'),
(7, '2024-03-06 11:00:00', 'confirmed'),
(7, '2024-03-07 09:00:00', 'confirmed'),
(2, '2024-03-08 11:05:00', 'confirmed'),
(2, '2024-03-09 12:00:00', 'timeout');

-- Insert users (clients and drivers)
INSERT INTO users (users_id, banned, role) VALUES
(1, 'No', 'client'),
(2, 'Yes', 'client'),
(3, 'No', 'client'),
(4, 'No', 'client'),
(10, 'No', 'driver'),
(11, 'No', 'driver'),
(12, 'No', 'driver'),
(13, 'No', 'driver');

-- Insert trips
INSERT INTO trips (id, client_id, driver_id, city_id, status, request_at) VALUES
(1, 1, 10, 1, 'completed', '2024-10-01'),
(2, 2, 11, 1, 'cancelled_by_driver', '2024-10-01'),
(3, 3, 12, 6, 'completed', '2024-10-01'),
(4, 4, 13, 6, 'cancelled_by_client', '2024-10-01'),
(5, 1, 10, 1, 'completed', '2024-10-02'),
(6, 2, 11, 6, 'completed', '2024-10-02'),
(7, 3, 12, 6, 'completed', '2024-10-02'),
(8, 2, 12, 12, 'completed', '2024-10-03'),
(9, 3, 10, 12, 'completed', '2024-10-03'),
(10, 4, 13, 12, 'cancelled_by_driver', '2024-10-03');

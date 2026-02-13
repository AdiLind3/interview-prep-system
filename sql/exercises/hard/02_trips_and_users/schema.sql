-- Create users table
CREATE TABLE users (
    users_id INTEGER PRIMARY KEY,
    banned TEXT NOT NULL CHECK (banned IN ('Yes', 'No')),
    role TEXT NOT NULL CHECK (role IN ('client', 'driver', 'partner'))
);

-- Create trips table
CREATE TABLE trips (
    id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL,
    driver_id INTEGER NOT NULL,
    city_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    request_at DATE NOT NULL,
    FOREIGN KEY (client_id) REFERENCES users(users_id),
    FOREIGN KEY (driver_id) REFERENCES users(users_id)
);

-- Create signups table
CREATE TABLE signups (
    user_id INTEGER PRIMARY KEY,
    time_stamp DATETIME NOT NULL
);

-- Create confirmations table
CREATE TABLE confirmations (
    user_id INTEGER NOT NULL,
    time_stamp DATETIME NOT NULL,
    action TEXT NOT NULL CHECK (action IN ('confirmed', 'timeout')),
    FOREIGN KEY (user_id) REFERENCES signups(user_id)
);

-- Create friend_request table
CREATE TABLE friend_request (
    sender_id INTEGER NOT NULL,
    send_to_id INTEGER NOT NULL,
    request_date DATE NOT NULL
);

-- Create request_accepted table
CREATE TABLE request_accepted (
    requester_id INTEGER NOT NULL,
    accepter_id INTEGER NOT NULL,
    accept_date DATE NOT NULL
);

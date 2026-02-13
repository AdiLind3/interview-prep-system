-- Create transactions table
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    country TEXT,
    state TEXT NOT NULL CHECK (state IN ('approved', 'declined')),
    amount INTEGER NOT NULL,
    trans_date DATE NOT NULL
);

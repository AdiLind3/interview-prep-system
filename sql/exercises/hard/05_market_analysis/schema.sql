-- Create users table
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    join_date DATE NOT NULL,
    favorite_category TEXT NOT NULL
);

-- Create items table
CREATE TABLE items (
    item_id INTEGER PRIMARY KEY,
    item_category TEXT NOT NULL
);

-- Create orders table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    order_date DATE NOT NULL,
    item_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (buyer_id) REFERENCES users(user_id),
    FOREIGN KEY (seller_id) REFERENCES users(user_id)
);

-- Create customers table
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- Create orders table
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customerId INTEGER NOT NULL,
    FOREIGN KEY (customerId) REFERENCES customers(id)
);

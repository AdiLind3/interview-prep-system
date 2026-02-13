-- Create products table
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    low_fats TEXT NOT NULL CHECK (low_fats IN ('Y', 'N')),
    is_recyclable TEXT NOT NULL CHECK (is_recyclable IN ('Y', 'N'))
);

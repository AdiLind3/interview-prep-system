-- Create product table
CREATE TABLE product (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL
);

-- Create sales table
CREATE TABLE sales (
    sale_id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    year INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price INTEGER NOT NULL,
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

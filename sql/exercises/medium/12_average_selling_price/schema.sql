-- Create prices table
CREATE TABLE prices (
    product_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    price INTEGER NOT NULL
);

-- Create units_sold table
CREATE TABLE units_sold (
    product_id INTEGER NOT NULL,
    purchase_date DATE NOT NULL,
    units INTEGER NOT NULL
);

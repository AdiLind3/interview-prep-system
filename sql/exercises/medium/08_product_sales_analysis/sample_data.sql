-- Insert products
INSERT INTO product (product_id, product_name) VALUES
(100, 'Nokia'),
(200, 'Apple'),
(300, 'Samsung');

-- Insert sales
INSERT INTO sales (sale_id, product_id, year, quantity, price) VALUES
(1, 100, 2008, 10, 5000),
(2, 100, 2009, 12, 5000),
(3, 100, 2010, 15, 4500),
(4, 200, 2011, 15, 9000),
(5, 200, 2012, 20, 8500),
(6, 300, 2012, 8, 7000),
(7, 300, 2013, 10, 7200),
(8, 300, 2014, 12, 6800);

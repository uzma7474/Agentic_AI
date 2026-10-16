-- Customer Support Agent - Database Schema
-- Run this file to initialize the database

CREATE DATABASE IF NOT EXISTS customer_support_db;
USE customer_support_db;

-- Drop tables if they exist (for clean re-initialization)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

-- Customers table
CREATE TABLE customers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(30)
);

-- Orders table
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    status VARCHAR(30) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    expected_delivery DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Order items table
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Insert sample customers
INSERT INTO customers (name, email, phone) VALUES
('Amit Sharma', 'amit@example.com', '+91-9876543210'),
('Priya Patel', 'priya@example.com', '+91-9876543211'),
('Rahul Verma', 'rahul@example.com', '+91-9876543212');

-- Insert sample orders
-- Order 1: Amit - PROCESSING (eligible for cancellation)
INSERT INTO orders (id, customer_id, order_date, status, total_amount, expected_delivery) VALUES
(101, 1, '2026-09-01', 'SHIPPED', 4500.00, '2026-09-10');

-- Order 2: Amit - PROCESSING (eligible for cancellation)
INSERT INTO orders (id, customer_id, order_date, status, total_amount, expected_delivery) VALUES
(102, 1, '2026-09-05', 'PROCESSING', 1200.00, '2026-09-15');

-- Order 3: Priya - DELIVERED
INSERT INTO orders (id, customer_id, order_date, status, total_amount, expected_delivery) VALUES
(103, 2, '2026-08-20', 'DELIVERED', 8999.00, '2026-08-28');

-- Order 4: Priya - SHIPPED
INSERT INTO orders (id, customer_id, order_date, status, total_amount, expected_delivery) VALUES
(104, 2, '2026-09-03', 'SHIPPED', 3200.00, '2026-09-12');

-- Order 5: Rahul - PROCESSING
INSERT INTO orders (id, customer_id, order_date, status, total_amount, expected_delivery) VALUES
(105, 3, '2026-09-07', 'PROCESSING', 2500.00, '2026-09-18');

-- Order 6: Amit - CANCELLED
INSERT INTO orders (id, customer_id, order_date, status, total_amount, expected_delivery) VALUES
(106, 1, '2026-08-25', 'CANCELLED', 750.00, NULL);

-- Order 7: Rahul - SHIPPED
INSERT INTO orders (id, customer_id, order_date, status, total_amount, expected_delivery) VALUES
(107, 3, '2026-09-02', 'SHIPPED', 6400.00, '2026-09-11');

-- Insert order items
-- Order 101 items
INSERT INTO order_items (order_id, product_name, quantity, price) VALUES
(101, 'Mechanical Keyboard', 1, 3500.00),
(101, 'Keyboard Wrist Rest', 1, 1000.00);

-- Order 102 items
INSERT INTO order_items (order_id, product_name, quantity, price) VALUES
(102, 'USB Hub 4-Port', 1, 1200.00);

-- Order 103 items
INSERT INTO order_items (order_id, product_name, quantity, price) VALUES
(103, 'Wireless Mouse', 1, 2500.00),
(103, 'Mouse Pad XL', 1, 999.00),
(103, 'USB-C Cable 2m', 2, 1500.00);

-- Order 104 items
INSERT INTO order_items (order_id, product_name, quantity, price) VALUES
(104, 'Webcam HD 1080p', 1, 3200.00);

-- Order 105 items
INSERT INTO order_items (order_id, product_name, quantity, price) VALUES
(105, 'Monitor Stand', 1, 2500.00);

-- Order 106 items
INSERT INTO order_items (order_id, product_name, quantity, price) VALUES
(106, 'USB Cable', 3, 750.00);

-- Order 107 items
INSERT INTO order_items (order_id, product_name, quantity, price) VALUES
(107, '27-inch Monitor', 1, 5500.00),
(107, 'HDMI Cable 1.5m', 1, 900.00);

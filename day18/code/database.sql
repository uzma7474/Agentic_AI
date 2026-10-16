CREATE DATABASE IF NOT EXISTS mcp_demo;
USE mcp_demo;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'processing'
);

CREATE TABLE users (
    username VARCHAR(100) PRIMARY KEY,
    password VARCHAR(255) NOT NULL,
    permissions JSON NOT NULL
);

INSERT INTO products (name, price) VALUES
    ('MacBook Pro', 1999.00),
    ('iPhone', 999.00),
    ('AirPods', 249.00);

INSERT INTO orders (product_id, quantity, status) VALUES
    (1, 1, 'shipped'),
    (3, 2, 'processing');

INSERT INTO users (username, password, permissions) VALUES
    ('alice', 'alice123', JSON_ARRAY('products:read', 'orders:read', 'profile:read')),
    ('admin', 'admin123', JSON_ARRAY('products:read', 'products:write', 'orders:read', 'orders:write', 'profile:read'));

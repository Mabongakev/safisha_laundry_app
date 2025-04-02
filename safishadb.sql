CREATE DATABASE safisha_laundry;
USE safisha_laundry;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    physical_address VARCHAR(100) NOT NULL,
    collection_date DATE NOT NULL,
    quantity INT CHECK (quantity BETWEEN 1 AND 20) NOT NULL,
    clothing_type ENUM('suit', 'tshirt', 'jeans', 'shirt', 'beddings') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

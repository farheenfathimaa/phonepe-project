CREATE DATABASE IF NOT EXISTS phonepe_pulse;
USE phonepe_pulse;

CREATE TABLE IF NOT EXISTS Aggregated_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Transaction_type VARCHAR(100),
    Transaction_count BIGINT,
    Transaction_amount FLOAT
);

CREATE TABLE IF NOT EXISTS Aggregated_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Brand VARCHAR(100),
    User_count BIGINT,
    User_percentage FLOAT
);

CREATE TABLE IF NOT EXISTS Aggregated_insurance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Insurance_type VARCHAR(100),
    Insurance_count BIGINT,
    Insurance_amount FLOAT
);

CREATE TABLE IF NOT EXISTS Map_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    District VARCHAR(100),
    Transaction_count BIGINT,
    Transaction_amount FLOAT
);

CREATE TABLE IF NOT EXISTS Map_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    District VARCHAR(100),
    Registered_users BIGINT,
    App_opens BIGINT
);

CREATE TABLE IF NOT EXISTS Map_insurance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    District VARCHAR(100),
    Insurance_count BIGINT,
    Insurance_amount FLOAT
);

CREATE TABLE IF NOT EXISTS Top_transaction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Pincode VARCHAR(20),
    Transaction_count BIGINT,
    Transaction_amount FLOAT
);

CREATE TABLE IF NOT EXISTS Top_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Pincode VARCHAR(20),
    Registered_users BIGINT
);

CREATE TABLE IF NOT EXISTS Top_insurance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    State VARCHAR(100),
    Year INT,
    Quarter INT,
    Pincode VARCHAR(20),
    Insurance_count BIGINT,
    Insurance_amount FLOAT
);

CREATE DATABASE IF NOT EXISTS directory_scraper;
USE directory_scraper;

-- Queue table for tracking task states and enabling resumability
CREATE TABLE IF NOT EXISTS crawl_queue (
    record_id VARCHAR(64) PRIMARY KEY,
    status ENUM('pending', 'in_progress', 'completed', 'failed', 'captcha') DEFAULT 'pending',
    attempts INT DEFAULT 0,
    last_error TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Data table for storing structured records
CREATE TABLE IF NOT EXISTS extracted_architects (
    record_id VARCHAR(64) PRIMARY KEY,
    full_name VARCHAR(255),
    registration_no VARCHAR(100),
    state VARCHAR(100),
    address TEXT,
    valid_upto VARCHAR(50),
    source_url TEXT,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (record_id) REFERENCES crawl_queue(record_id) ON DELETE CASCADE
);

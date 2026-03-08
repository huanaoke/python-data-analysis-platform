-- 创建数据库
CREATE DATABASE IF NOT EXISTS data_platform DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 切换到该数据库
USE data_platform;

-- 创建天气数据表
CREATE TABLE IF NOT EXISTS weather_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    weather VARCHAR(50) NOT NULL,
    crawl_time DATETIME DEFAULT CURRENT_TIMESTAMP
);
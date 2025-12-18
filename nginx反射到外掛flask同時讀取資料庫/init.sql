-- 初始化資料庫腳本

-- 建立 users 資料表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 插入範例資料
INSERT INTO users (name, email) VALUES
    ('張三', 'zhang@example.com'),
    ('李四', 'li@example.com'),
    ('王五', 'wang@example.com'),
    ('趙六', 'zhao@example.com'),
    ('錢七', 'qian@example.com');

-- 微信小程序背单词应用数据库初始化脚本
-- 基础版本：包含用户表、生词本表、查询历史表

-- 删除已存在的表（谨慎使用）
-- DROP TABLE IF EXISTS query_history;
-- DROP TABLE IF EXISTS vocabulary_book;
-- DROP TABLE IF EXISTS users;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    openid VARCHAR(100) UNIQUE NOT NULL,
    nickname VARCHAR(50),
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建生词本表
CREATE TABLE IF NOT EXISTS vocabulary_book (
    vocab_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word VARCHAR(50) NOT NULL,
    phonetic VARCHAR(100),
    definition TEXT,
    english_definition TEXT,
    examples TEXT,  -- JSON格式存储例句
    memory_tips TEXT,
    status INTEGER DEFAULT 0,  -- 0:未学习, 1:学习中, 2:已掌握
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(user_id, word)  -- 同一用户的单词不能重复
);

-- 创建查询历史表
CREATE TABLE IF NOT EXISTS query_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word VARCHAR(50) NOT NULL,
    result TEXT,  -- 缓存查询结果
    query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 创建索引以提高查询性能
CREATE INDEX IF NOT EXISTS idx_vocab_book_user_id ON vocabulary_book(user_id);
CREATE INDEX IF NOT EXISTS idx_vocab_book_word ON vocabulary_book(word);
CREATE INDEX IF NOT EXISTS idx_vocab_book_status ON vocabulary_book(status);
CREATE INDEX IF NOT EXISTS idx_query_history_user_id ON query_history(user_id);
CREATE INDEX IF NOT EXISTS idx_query_history_word ON query_history(word);
CREATE INDEX IF NOT EXISTS idx_query_history_time ON query_history(query_time);

-- 插入测试数据（可选）
-- INSERT INTO users (openid, nickname, avatar_url) VALUES 
-- ('test_openid_1', '测试用户', 'https://example.com/avatar.jpg');

-- 查看表结构
-- .schema

-- 查看索引
-- .indexes

-- 寰俊灏忕▼搴忚儗鍗曡瘝搴旂敤鏁版嵁搴撳垵濮嬪寲鑴氭湰
-- 鍩虹鐗堟湰锛氬寘鍚敤鎴疯〃銆佺敓璇嶆湰琛ㄣ€佹煡璇㈠巻鍙茶〃

-- 鍒犻櫎宸插瓨鍦ㄧ殑琛紙璋ㄦ厧浣跨敤锛?-- DROP TABLE IF EXISTS query_history;
-- DROP TABLE IF EXISTS vocabulary_book;
-- DROP TABLE IF EXISTS users;

-- 鍒涘缓鐢ㄦ埛琛?CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    openid VARCHAR(100) UNIQUE NOT NULL,
    nickname VARCHAR(50),
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 鍒涘缓鐢熻瘝鏈〃
CREATE TABLE IF NOT EXISTS vocabulary_book (
    vocab_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word VARCHAR(50) NOT NULL,
    phonetic VARCHAR(100),
    definition TEXT,
    english_definition TEXT,
    examples TEXT,  -- JSON鏍煎紡瀛樺偍渚嬪彞
    memory_tips TEXT,
    status INTEGER DEFAULT 0,  -- 0:鏈涔? 1:瀛︿範涓? 2:宸叉帉鎻?    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(user_id, word)  -- 鍚屼竴鐢ㄦ埛鐨勫崟璇嶄笉鑳介噸澶?);

-- 鍒涘缓鏌ヨ鍘嗗彶琛?CREATE TABLE IF NOT EXISTS query_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word VARCHAR(50) NOT NULL,
    result TEXT,  -- 缂撳瓨鏌ヨ缁撴灉
    query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 鍒涘缓绱㈠紩浠ユ彁楂樻煡璇㈡€ц兘
CREATE INDEX IF NOT EXISTS idx_vocab_book_user_id ON vocabulary_book(user_id);
CREATE INDEX IF NOT EXISTS idx_vocab_book_word ON vocabulary_book(word);
CREATE INDEX IF NOT EXISTS idx_vocab_book_status ON vocabulary_book(status);
CREATE INDEX IF NOT EXISTS idx_query_history_user_id ON query_history(user_id);
CREATE INDEX IF NOT EXISTS idx_query_history_word ON query_history(word);
CREATE INDEX IF NOT EXISTS idx_query_history_time ON query_history(query_time);

-- 鎻掑叆娴嬭瘯鏁版嵁锛堝彲閫夛級
-- INSERT INTO users (openid, nickname, avatar_url) VALUES 
-- ('test_openid_1', '娴嬭瘯鐢ㄦ埛', 'https://example.com/avatar.jpg');

-- 鏌ョ湅琛ㄧ粨鏋?-- .schema

-- 鏌ョ湅绱㈠紩
-- .indexes


-- V2.0 表
CREATE TABLE IF NOT EXISTS study_record (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    study_date DATE NOT NULL,
    query_count INTEGER DEFAULT 0,
    is_checked_in BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(user_id, study_date)
);

CREATE TABLE IF NOT EXISTS favorite_sentences (
    favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    vocab_id INTEGER NOT NULL,
    sentence TEXT NOT NULL,
    translation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (vocab_id) REFERENCES vocabulary_book(vocab_id)
);

-- V3.0 表
CREATE TABLE IF NOT EXISTS import_history (
    import_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    source_type VARCHAR(50),
    raw_text TEXT,
    word_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE INDEX IF NOT EXISTS idx_study_record_user_date ON study_record(user_id, study_date);
CREATE INDEX IF NOT EXISTS idx_favorite_user ON favorite_sentences(user_id);
CREATE INDEX IF NOT EXISTS idx_import_history_user_id ON import_history(user_id);

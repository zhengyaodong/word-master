-- 词库表（内置词库）
CREATE TABLE IF NOT EXISTS word_libraries (
    library_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,              -- 词库名称（如：CET-4, CET-6）
    description TEXT,                        -- 词库描述
    category VARCHAR(50),                    -- 分类：cet4/cet6/toefl/ielts/gre
    level VARCHAR(20),                       -- 难度等级：A1/A2/B1/B2/C1/C2
    total_words INTEGER DEFAULT 0,           -- 总单词数
    icon_url VARCHAR(255),                   -- 词库图标
    is_builtin BOOLEAN DEFAULT 1,            -- 是否内置词库
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 词库单词关联表
CREATE TABLE IF NOT EXISTS library_words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    library_id INTEGER NOT NULL,
    word VARCHAR(100) NOT NULL,
    phonetic VARCHAR(100),                   -- 音标
    definition TEXT,                         -- 中文释义
    english_definition TEXT,                 -- 英文释义
    examples TEXT,                           -- 例句(JSON)
    part_of_speech VARCHAR(50),              -- 词性
    frequency INTEGER DEFAULT 0,             -- 词频（在词库中的出现频率/重要性）
    difficulty INTEGER DEFAULT 1,            -- 难度：1-5
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (library_id) REFERENCES word_libraries(library_id),
    UNIQUE(library_id, word)
);

-- 用户词库学习进度表
CREATE TABLE IF NOT EXISTS user_library_progress (
    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    library_id INTEGER NOT NULL,
    word VARCHAR(100) NOT NULL,
    status INTEGER DEFAULT 0,                -- 0: 未学习, 1: 学习中, 2: 已掌握, 3: 需复习
    review_count INTEGER DEFAULT 0,          -- 复习次数
    correct_count INTEGER DEFAULT 0,         -- 正确次数
    wrong_count INTEGER DEFAULT 0,           -- 错误次数
    last_review_at TIMESTAMP,                -- 上次复习时间
    next_review_at TIMESTAMP,                -- 下次复习时间（间隔重复）
    easiness_factor REAL DEFAULT 2.5,        -- 简易度因子（SM-2算法）
    interval_days INTEGER DEFAULT 0,         -- 间隔天数
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (library_id) REFERENCES word_libraries(library_id),
    UNIQUE(user_id, library_id, word)
);

-- 索引
CREATE INDEX IF NOT EXISTS idx_library_words_library_id ON library_words(library_id);
CREATE INDEX IF NOT EXISTS idx_library_words_word ON library_words(word);
CREATE INDEX IF NOT EXISTS idx_user_progress_user_id ON user_library_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_library_id ON user_library_progress(library_id);
CREATE INDEX IF NOT EXISTS idx_user_progress_next_review ON user_library_progress(user_id, next_review_at);

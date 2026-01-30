# 微信小程序背单词项目需求文档（PRD）- 基础版本

## 1. 项目概述

### 1.1 项目背景
一款基于微信小程序的背单词应用，核心特色是利用本地Ollama大模型为用户提供智能单词解释，并支持建立个人生词本。

### 1.2 项目目标
- 提供便捷的单词查询功能，利用AI生成详细的单词解释
- 支持建立个人生词本，方便用户管理自定义学习的单词
- 实现简单的学习记录功能，帮助用户跟踪学习进度

### 1.3 技术栈
- **前端**：微信小程序（HTML + CSS + JavaScript）
- **后端**：Python + Flask
- **数据库**：SQLite3
- **AI模型**：Ollama本地服务（qwen3:0.6b）

---

## 2. 核心功能模块

### 2.1 用户系统

#### 2.1.1 功能描述
- 微信一键登录
- 自动创建用户账号
- 记录用户学习数据

#### 2.1.2 业务规则
- 首次使用自动创建用户
- 用户数据与微信openid绑定

---

### 2.2 单词查询模块

#### 2.2.1 功能描述
- 用户输入英文单词
- 调用本地Ollama大模型生成单词解释
- 展示单词的详细释义、例句、记忆技巧等
- 支持一键添加到生词本

#### 2.2.2 AI解释内容
Ollama模型返回以下信息：
- 音标
- 词性
- 中文释义
- 英文释义
- 2-3个例句（含中文翻译）
- 记忆技巧

#### 2.2.3 交互流程
1. 用户进入"查词"页面
2. 在搜索框输入英文单词
3. 点击"查询"按钮
4. 系统调用Ollama API获取解释
5. 展示查询结果
6. 用户可点击"加入生词本"

#### 2.2.4 业务规则
- 查询结果缓存24小时
- Ollama调用超时时间为30秒
- 查询失败时显示友好提示

---

### 2.3 生词本模块

#### 2.3.1 功能描述
- 查看已添加的单词列表
- 查看单词详情
- 删除单词
- 简单的学习状态标记（未学习/学习中/已掌握）

#### 2.3.2 交互流程
1. 用户进入"生词本"页面
2. 查看所有已添加的单词
3. 点击单词查看详情
4. 可标记学习状态或删除单词

#### 2.3.3 业务规则
- 生词本单词数量无上限
- 支持按添加时间排序
- 删除操作需确认

---

### 2.4 个人中心模块

#### 2.4.1 功能描述
- 显示用户基本信息
- 显示学习统计（生词本单词数、已掌握单词数）
- 显示查询历史

---

## 3. 用户界面设计

### 3.1 页面结构
- **底部导航栏**：查词 | 生词本 | 我的

### 3.2 查词页面
```
┌─────────────────────┐
│      查词           │
├─────────────────────┤
│ ┌─────────────────┐ │
│ │ 输入英文单词    │ │
│ └─────────────────┘ │
│      [查询按钮]      │
├─────────────────────┤
│ 最近查询：           │
│ apple, banana...    │
├─────────────────────┤
│ 查询结果：           │
│ ┌─────────────────┐ │
│ │ serendipity     │ │
│ │ /ˌserənˈdɪpəti/ │ │
│ │ n. 意外发现...   │ │
│ │                 │ │
│ │ 例句：           │ │
│ │ We found...     │ │
│ │                 │ │
│ │ 记忆技巧：       │ │
│ │ ...             │ │
│ └─────────────────┘ │
│ [加入生词本]        │
└─────────────────────┘
```

### 3.3 生词本页面
```
┌─────────────────────┐
│      生词本         │
├─────────────────────┤
│ 共50个单词          │
├─────────────────────┤
│ ┌─────────────────┐ │
│ │ serendipity     │ │
│ │ 意外发现...     │ │
│ │ [未学习]  [删除]│ │
│ └─────────────────┘ │
│ ┌─────────────────┐ │
│ │ ephemeral       │ │
│ │ 短暂的...       │ │
│ │ [已掌握]  [删除]│ │
│ └─────────────────┘ │
│ ...                 │
└─────────────────────┘
```

### 3.4 个人中心页面
```
┌─────────────────────┐
│       我的          │
├─────────────────────┤
│ 头像  用户名        │
├─────────────────────┤
│ 生词本：50个        │
│ 已掌握：20个        │
├─────────────────────┤
│ 查询历史 >          │
│ 关于我们 >          │
└─────────────────────┘
```

---

## 4. 数据结构设计

### 4.1 数据库表结构

#### users（用户表）
| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | INTEGER | 主键，自增 |
| openid | VARCHAR(100) | 微信openid，唯一 |
| nickname | VARCHAR(50) | 昵称 |
| avatar_url | VARCHAR(255) | 头像URL |
| created_at | TIMESTAMP | 创建时间 |

#### vocabulary_book（生词本表）
| 字段 | 类型 | 说明 |
|------|------|------|
| vocab_id | INTEGER | 主键，自增 |
| user_id | INTEGER | 用户ID，外键 |
| word | VARCHAR(50) | 单词 |
| phonetic | VARCHAR(100) | 音标 |
| definition | TEXT | 中文释义 |
| english_definition | TEXT | 英文释义 |
| examples | TEXT | 例句（JSON） |
| memory_tips | TEXT | 记忆技巧 |
| status | INTEGER | 状态：0-未学习，1-学习中，2-已掌握 |
| created_at | TIMESTAMP | 创建时间 |

#### query_history（查询历史表）
| 字段 | 类型 | 说明 |
|------|------|------|
| history_id | INTEGER | 主键，自增 |
| user_id | INTEGER | 用户ID |
| word | VARCHAR(50) | 查询的单词 |
| result | TEXT | 查询结果缓存 |
| query_time | TIMESTAMP | 查询时间 |

### 4.2 建表SQL
```sql
-- 用户表
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    openid VARCHAR(100) UNIQUE NOT NULL,
    nickname VARCHAR(50),
    avatar_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 生词本表
CREATE TABLE IF NOT EXISTS vocabulary_book (
    vocab_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word VARCHAR(50) NOT NULL,
    phonetic VARCHAR(100),
    definition TEXT,
    english_definition TEXT,
    examples TEXT,
    memory_tips TEXT,
    status INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(user_id, word)
);

-- 查询历史表
CREATE TABLE IF NOT EXISTS query_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word VARCHAR(50) NOT NULL,
    result TEXT,
    query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 索引
CREATE INDEX idx_vocab_book_user_id ON vocabulary_book(user_id);
CREATE INDEX idx_query_history_user_id ON query_history(user_id);
```

---

## 5. API接口设计

### 5.1 用户接口
| 接口 | 方法 | 功能 |
|------|------|------|
| /api/user/login | POST | 微信登录 |
| /api/user/info | GET | 获取用户信息 |

### 5.2 单词查询接口
| 接口 | 方法 | 功能 |
|------|------|------|
| /api/word/query | POST | 查询单词（调用Ollama） |
| /api/word/history | GET | 获取查询历史 |

### 5.3 生词本接口
| 接口 | 方法 | 功能 |
|------|------|------|
| /api/vocab-book/add | POST | 添加到生词本 |
| /api/vocab-book/list | GET | 获取生词本列表 |
| /api/vocab-book/detail | GET | 获取单词详情 |
| /api/vocab-book/update | PUT | 更新学习状态 |
| /api/vocab-book/delete | DELETE | 删除单词 |

### 5.4 接口详情

#### 查询单词
```
POST /api/word/query
请求：
{
    "word": "serendipity"
}

响应：
{
    "code": 0,
    "data": {
        "word": "serendipity",
        "phonetic": "/ˌserənˈdɪpəti/",
        "part_of_speech": "n.",
        "definition": "意外发现珍奇事物的本领",
        "english_definition": "The occurrence of events by chance in a happy way",
        "examples": [
            {"sentence": "We found it by pure serendipity.", "translation": "我们纯粹是机缘巧合找到了它。"}
        ],
        "memory_tips": "联想为宁静的seren + 小插曲dipity"
    }
}
```

#### 添加到生词本
```
POST /api/vocab-book/add
请求：
{
    "word": "serendipity",
    "phonetic": "/ˌserənˈdɪpəti/",
    "definition": "意外发现珍奇事物的本领",
    "english_definition": "The occurrence of events by chance",
    "examples": "[...]",
    "memory_tips": "联想记忆..."
}

响应：
{
    "code": 0,
    "data": {"vocab_id": 1},
    "message": "添加成功"
}
```

#### 获取生词本列表
```
GET /api/vocab-book/list?user_id=1

响应：
{
    "code": 0,
    "data": {
        "total": 50,
        "list": [
            {
                "vocab_id": 1,
                "word": "serendipity",
                "phonetic": "/ˌserənˈdɪpəti/",
                "definition": "意外发现...",
                "status": 0
            }
        ]
    }
}
```

---

## 6. Ollama集成

### 6.1 服务配置
```python
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",
    "model": "qwen3:0.6b",
    "timeout": 30
}
```

### 6.2 调用示例
```python
import requests
import json

def query_word(word):
    prompt = f"""解释单词'{word}'，以JSON格式返回：
{{
    "word": "单词",
    "phonetic": "音标",
    "part_of_speech": "词性",
    "definition": "中文释义",
    "english_definition": "英文释义",
    "examples": [{{"sentence": "例句", "translation": "翻译"}}],
    "memory_tips": "记忆技巧"
}}"""
    
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "qwen3:0.6b",
        "prompt": prompt,
        "stream": False
    })
    
    return json.loads(response.json()["response"])
```

---

## 7. 项目结构

```
word-master/
├── backend/              # Python后端
│   ├── app.py           # Flask应用入口
│   ├── models.py        # 数据库模型
│   ├── services/        # 业务逻辑
│   │   ├── ollama_service.py
│   │   └── vocab_service.py
│   ├── routes/          # API路由
│   │   ├── user.py
│   │   ├── word.py
│   │   └── vocab_book.py
│   └── utils/           # 工具函数
├── miniprogram/         # 微信小程序
│   ├── pages/           # 页面
│   │   ├── index/       # 查词页
│   │   ├── vocab-book/  # 生词本页
│   │   └── profile/     # 个人中心
│   ├── app.js
│   ├── app.json
│   └── app.wxss
├── database/            # 数据库
│   └── init.sql
└── PRD.md              # 需求文档
```

---

## 8. 开发计划

| 阶段 | 时间 | 任务 |
|------|------|------|
| 第1周 | 环境搭建 | 搭建Python环境、部署Ollama、创建数据库 |
| 第2周 | 后端开发 | 实现用户系统、单词查询、生词本API |
| 第3周 | 前端开发 | 开发小程序页面、对接API |
| 第4周 | 测试优化 | 功能测试、性能优化、Bug修复 |

---

## 9. 总结

基础版本聚焦核心功能：
1. **单词查询** - 调用Ollama AI解释单词
2. **生词本** - 管理个人单词库
3. **用户系统** - 微信登录，记录学习数据

后续可逐步添加：复习功能、测试功能、词库学习、记忆曲线等高级功能。

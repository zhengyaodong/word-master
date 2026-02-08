# 微信小程序背单词项目需求文档（PRD）- V2.0极简版

## 版本信息
- **版本号**: V2.0
- **更新日期**: 2026-01-31
- **更新说明**: 在V1.0基础上增加最基础的增强功能：学习统计、语音朗读、例句收藏、学习打卡

---

## 1. 项目概述

### 1.1 项目背景
V1.0已实现AI查词和生词本基础功能。V2.0增加4个简单实用的功能，提升用户体验。

### 1.2 V2.0目标
- 了解学习情况（统计）
- 帮助记忆发音（语音）
- 收藏好句子（收藏）
- 养成学习习惯（打卡）

### 1.3 技术栈
- **前端**: 微信小程序 + TypeScript
- **后端**: Python + Flask
- **数据库**: SQLite3
- **语音**: 微信小程序同声传译插件

---

## 2. V2.0功能模块（仅4个）

### 2.1 学习统计

#### 功能描述
展示基础学习数据。

#### 统计内容
- 总单词数、已掌握数、学习中数
- 今日查询次数
- 连续打卡天数
- 近7天每日查询次数（简单数字列表）

#### 页面设计
```
┌─────────────────────────┐
│       学习统计          │
├─────────────────────────┤
│ 总单词: 150             │
│ 已掌握: 80              │
│ 学习中: 45              │
├─────────────────────────┤
│ 今日查询: 12次          │
│ 连续打卡: 5天 🔥        │
├─────────────────────────┤
│ 近7天查询:              │
│ 今天: 12  昨天: 8       │
│ 前天: 15  大前天: 6     │
│ ...                     │
└─────────────────────────┘
```

---

### 2.2 语音朗读

#### 功能描述
点击播放按钮朗读单词和例句。

#### 功能点
- 单词详情页显示 🔊 按钮
- 点击播放单词发音
- 例句旁显示 🔊 按钮，点击朗读整句
- 使用微信小程序同声传译插件

---

### 2.3 例句收藏

#### 功能描述
收藏喜欢的例句，方便复习。

#### 功能点
- 单词详情页例句旁显示 ⭐ 按钮
- 点击收藏/取消收藏
- "我的"页面增加"收藏例句"入口
- 收藏列表页面显示所有收藏的例句

#### 页面设计
```
┌─────────────────────────┐
│       收藏例句          │
├─────────────────────────┤
│ ┌─────────────────────┐ │
│ │ serendipity         │ │
│ │ "We found it by..." │ │
│ │ 我们纯粹是机缘...   │ │
│ │              [删除] │ │
│ └─────────────────────┘ │
│ ┌─────────────────────┐ │
│ │ ephemeral           │ │
│ │ "Life is ephemeral" │ │
│ │ 生命是短暂的...     │ │
│ │              [删除] │ │
│ └─────────────────────┘ │
└─────────────────────────┘
```

---

### 2.4 学习打卡

#### 功能描述
记录每日学习，显示连续天数。

#### 功能点
- 当日查询过单词自动打卡
- 统计页面显示连续打卡天数
- 简单日历显示本月打卡情况

---

## 3. 数据库设计

### 3.1 新增表（仅2个）

#### study_record（学习记录表）
| 字段 | 类型 | 说明 |
|------|------|------|
| record_id | INTEGER | 主键 |
| user_id | INTEGER | 用户ID |
| study_date | DATE | 日期 |
| query_count | INTEGER | 查询次数 |
| is_checked_in | BOOLEAN | 是否打卡 |

#### favorite_sentences（收藏例句表）
| 字段 | 类型 | 说明 |
|------|------|------|
| favorite_id | INTEGER | 主键 |
| user_id | INTEGER | 用户ID |
| vocab_id | INTEGER | 单词ID |
| sentence | TEXT | 例句 |
| translation | TEXT | 翻译 |
| created_at | TIMESTAMP | 时间 |

### 3.2 建表SQL

```sql
-- 学习记录表
CREATE TABLE IF NOT EXISTS study_record (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    study_date DATE NOT NULL,
    query_count INTEGER DEFAULT 0,
    is_checked_in BOOLEAN DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(user_id, study_date)
);

-- 收藏例句表
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

-- 索引
CREATE INDEX idx_study_record_user_date ON study_record(user_id, study_date);
CREATE INDEX idx_favorite_user ON favorite_sentences(user_id);
```

---

## 4. API接口

### 4.1 统计接口

| 接口 | 方法 | 功能 |
|------|------|------|
| /api/stats/overview | GET | 学习概览 |
| /api/stats/trend | GET | 近7天数据 |

#### 响应示例
```json
{
    "code": 0,
    "data": {
        "total_words": 150,
        "mastered": 80,
        "learning": 45,
        "today_query": 12,
        "consecutive_days": 5,
        "last_7_days": [12, 8, 15, 6, 20, 10, 5]
    }
}
```

### 4.2 收藏接口

| 接口 | 方法 | 功能 |
|------|------|------|
| /api/favorites/add | POST | 收藏例句 |
| /api/favorites/list | GET | 收藏列表 |
| /api/favorites/delete | DELETE | 删除收藏 |

#### 收藏例句
```
POST /api/favorites/add
请求：
{
    "user_id": 1,
    "vocab_id": 10,
    "sentence": "We found it by pure serendipity.",
    "translation": "我们纯粹是机缘巧合找到了它。"
}
```

---

## 5. 页面修改

### 5.1 "我的"页面更新
```
┌─────────────────────────┐
│       我的              │
├─────────────────────────┤
│ 头像  用户名            │
├─────────────────────────┤
│ 生词本：50个    >       │
│ 已掌握：20个            │
│ 连续打卡：5天 🔥        │
├─────────────────────────┤
│ 学习统计    >           │
│ 收藏例句    >           │
│ 查询历史    >           │
├─────────────────────────┤
│ 关于我们    >           │
└─────────────────────────┘
```

### 5.2 单词详情页更新
```
┌─────────────────────────┐
│ < 返回                  │
├─────────────────────────┤
│                         │
│    serendipity    🔊   │
│   /ˌserənˈdɪpəti/      │
│                         │
├─────────────────────────┤
│ n. 意外发现珍奇事物的本领│
├─────────────────────────┤
│ 例句:                   │
│ 1. We found it...  🔊⭐ │
│    我们纯粹是...        │
│ 2. It was pure...  🔊⭐ │
│    这真是...            │
├─────────────────────────┤
│ 记忆技巧:               │
│ ...                     │
├─────────────────────────┤
│ [未学习] [学习中] [已掌握]│
└─────────────────────────┘
```

---

## 6. 开发计划（2周）

### 第1周
- [ ] 数据库表创建
- [ ] 学习记录API（查询时自动记录）
- [ ] 统计页面
- [ ] 打卡功能

### 第2周
- [ ] 语音朗读功能
- [ ] 收藏例句API
- [ ] 收藏页面
- [ ] 测试优化

---

## 7. 功能清单

### V1.0已有
- ✅ AI智能查词
- ✅ 生词本管理
- ✅ 学习状态标记
- ✅ 查询历史

### V2.0新增（仅4个）
1. ✅ 学习统计（数字+7天趋势）
2. ✅ 语音朗读（🔊按钮）
3. ✅ 例句收藏（⭐按钮）
4. ✅ 学习打卡（自动记录）

---

**文档版本**: V2.0极简版  
**最后更新**: 2026-01-31

# 微信小程序背单词项目需求文档（PRD）- V4.0 内置词库版

## 版本信息
- **版本号**: V4.0
- **更新日期**: 2026-02-08
- **更新说明**: 新增内置词库系统，支持四六级等考试词汇，实现基于SM-2算法的间隔重复复习

---

## 1. 项目概述

### 1.1 背景
V3.0已实现批量导入和AI助记功能。V4.0重点解决用户"不知道背什么单词"的问题，提供内置词库和科学的复习系统。

### 1.2 V4.0目标
- 提供常用考试词库（四六级、托福、雅思等）
- 实现科学的间隔重复复习算法（SM-2）
- 降低用户使用门槛，开箱即用
- 提高学习效率和单词留存率

### 1.3 技术栈
- **前端**: 微信小程序 + TypeScript + Less
- **后端**: Python + Flask + SQLAlchemy
- **数据库**: SQLite3
- **算法**: SM-2间隔重复算法

---

## 2. V4.0 功能模块

### 2.1 内置词库系统

#### 功能描述
提供常用英语考试词库，用户可以直接选择词库开始学习，无需手动添加单词。

#### 词库列表（V4.0首期）
| 词库 | 词汇量 | 难度 | 说明 |
|------|--------|------|------|
| CET-4 | 4434 | B1-B2 | 大学英语四级核心词汇（从官方考纲PDF提取） |
| CET-6 | 待添加 | B2-C1 | 大学英语六级核心词汇 |

#### 单词数据结构
```json
{
  "word": "abandon",
  "phonetic": "/əˈbændən/",
  "part_of_speech": "v.",
  "definition": "放弃，遗弃",
  "english_definition": "to leave behind, desert",
  "difficulty": 2,
  "examples": [...]
}
```

---

### 2.2 间隔重复复习系统（SM-2算法）

#### 功能描述
基于SuperMemo-2算法，根据用户对单词的掌握程度动态安排复习时间，提高记忆效率。

#### 算法原理
1. **简易度因子（EF）**: 初始值2.5，根据答题质量调整（1.3-2.5）
2. **间隔天数（I）**: 
   - 第1次复习：1天后
   - 第2次复习：6天后
   - 第N次复习：I(n-1) × EF
3. **质量评分（Q）**: 0-5分
   - 5分：完美回忆
   - 4分：正确回忆但有犹豫
   - 3分：正确回忆但困难
   - 0-2分：回忆失败，重置间隔

#### 学习状态流转
```
未学习 → 学习中 → 已掌握
   ↓          ↓
          需复习（复习失败）
```

---

### 2.3 学习进度追踪

#### 统计维度
- 总单词数、已掌握数、学习中数、需复习数
- 今日需复习单词数
- 连续学习天数
- 正确率统计

---

## 3. 数据库设计

### 3.1 词库表（word_libraries）
| 字段 | 类型 | 说明 |
|------|------|------|
| library_id | INTEGER | 主键 |
| name | VARCHAR(100) | 词库名称 |
| description | TEXT | 词库描述 |
| category | VARCHAR(50) | 分类标识（cet4/cet6等） |
| level | VARCHAR(20) | 难度等级（A1-C2） |
| total_words | INTEGER | 总单词数 |
| is_builtin | BOOLEAN | 是否内置词库 |

### 3.2 词库单词表（library_words）
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| library_id | INTEGER | 词库ID |
| word | VARCHAR(100) | 单词 |
| phonetic | VARCHAR(100) | 音标 |
| definition | TEXT | 中文释义 |
| english_definition | TEXT | 英文释义 |
| part_of_speech | VARCHAR(50) | 词性 |
| difficulty | INTEGER | 难度等级（1-5） |
| frequency | INTEGER | 词频/重要性 |

### 3.3 用户学习进度表（user_library_progress）
| 字段 | 类型 | 说明 |
|------|------|------|
| progress_id | INTEGER | 主键 |
| user_id | INTEGER | 用户ID |
| library_id | INTEGER | 词库ID |
| word | VARCHAR(100) | 单词 |
| status | INTEGER | 状态（0-3） |
| review_count | INTEGER | 复习次数 |
| correct_count | INTEGER | 正确次数 |
| wrong_count | INTEGER | 错误次数 |
| last_review_at | TIMESTAMP | 上次复习时间 |
| next_review_at | TIMESTAMP | 下次复习时间 |
| easiness_factor | INTEGER | 简易度因子（存储×100） |
| interval_days | INTEGER | 间隔天数 |

---

## 4. API设计

### 4.1 词库接口

| 接口 | 方法 | 功能 |
|------|------|------|
| /api/library/list | GET | 获取词库列表 |
| /api/library/words | GET | 获取词库单词列表（支持分页、筛选） |
| /api/library/random | GET | 获取随机单词（排除已掌握） |
| /api/library/start | POST | 开始学习词库（初始化进度） |
| /api/library/review | GET | 获取今日需复习单词 |
| /api/library/review | POST | 提交复习结果（SM-2算法） |
| /api/library/progress | GET | 获取学习进度统计 |
| /api/library/progress/update | POST | 更新单词学习状态 |
| /api/library/add-to-vocab | POST | 将词库单词添加到生词本 |

### 4.2 关键接口详情

#### 获取复习单词
```
GET /api/library/review?user_id=1&library_id=1&limit=20

响应：
{
  "code": 0,
  "data": {
    "total_due": 15,
    "words": [
      {
        "progress": {复习进度信息},
        "word_detail": {单词详情}
      }
    ]
  }
}
```

#### 提交复习结果
```
POST /api/library/review
请求：
{
  "user_id": 1,
  "library_id": 1,
  "word": "abandon",
  "quality": 4  // 0-5分
}

响应：
{
  "code": 0,
  "data": {
    "next_review": "2026-02-10",
    "interval_days": 3,
    "easiness_factor": 2.5,
    "status": 1
  }
}
```

#### 获取随机单词
```
GET /api/library/random?user_id=1&library_id=1&limit=20&exclude_mastered=true

响应：
{
  "code": 0,
  "data": {
    "library": {词库信息},
    "total": 4434,
    "words": [
      {
        "word": "abandon",
        "phonetic": "/əˈbændən/",
        "definition": "放弃，遗弃",
        "progress": {学习进度}
      }
    ]
  }
}
```

#### 更新学习状态
```
POST /api/library/progress/update
请求：
{
  "user_id": 1,
  "library_id": 1,
  "word": "abandon",
  "status": 1  // 0-未学习, 1-学习中, 2-已掌握, 3-需复习
}

响应：
{
  "code": 0,
  "data": {"status": 1},
  "message": "状态已更新"
}
```

---

## 5. 页面设计

### 5.1 新增页面

| 页面 | 路径 | 功能描述 |
|------|------|----------|
| **词库选择页** | `pages/library/list` | 展示所有可用词库，显示词汇量、学习进度和今日待复习数 |
| **单词列表页** | `pages/library/words` | 分页展示词库单词，支持按难度和状态筛选 |
| **单词学习页** | `pages/library/learn` | 随机展示未掌握的单词，支持查看详情和添加到生词本 |
| **复习模式页** | `pages/library/review` | 展示今日需复习单词，支持0-5分背诵质量评分 |

### 5.2 页面流程
```
查词页 → 词库选择 → 开始学习 → 单词列表
                        ↓
                   复习模式 ← 每日提醒
```

---

## 6. 使用流程

### 6.1 首次使用词库
1. 用户进入"词库"页面
2. 选择CET-4/CET-6词库
3. 点击"开始学习"
4. 系统初始化学习进度（所有单词设为未学习）
5. 用户从第一个单词开始背诵

### 6.2 每日复习流程
1. 系统计算今日需复习单词（next_review_at <= 今天）
2. 展示给用户复习
3. 用户选择背诵质量（0-5分）
4. 系统更新间隔天数和下次复习时间
5. 重复直到完成当日复习任务

### 6.3 添加到生词本
1. 在词库学习或复习时，遇到难词
2. 点击"加入生词本"
3. 单词同时进入个人生词本和词库进度
4. 可以在生词本中继续深度学习

---

## 7. 开发计划

### 第1周：数据库与后端 ✅
- [x] 创建词库表结构 (word_libraries, library_words, user_library_progress)
- [x] 导入CET-4词库数据 (4434词，从官方PDF提取)
- [x] 实现词库API接口 (/api/library/*)
- [x] 实现SM-2间隔重复算法

### 第2周：前端页面 ✅
- [x] 词库选择页面 (pages/library/list)
- [x] 词库单词列表页 (pages/library/words)
- [x] 单词学习页 (pages/library/learn)
- [x] 复习模式页面 (pages/library/review)
- [x] 学习进度统计

### 第3周：测试优化 ✅
- [x] SM-2算法准确性测试
- [x] 词库数据导入脚本
- [x] 性能优化 (数据库索引优化)

---

## 8. 功能清单

### V4.0 新增（已实现）
1. ✅ 内置词库系统（CET-4完整词库4434词）
2. ✅ 词库数据导入与管理系统
3. ✅ SM-2间隔重复算法实现
4. ✅ 学习进度追踪与统计
5. ✅ 词库与自定义生词本联动
6. ✅ 复习提醒与每日任务
7. ✅ 单词难度分级与筛选

### 后续可扩展
- [ ] CET-6词库添加
- [ ] 托福/雅思/GRE词库
- [ ] 主题词库（商务、旅游、学术）
- [ ] 拼写测试模式
- [ ] 学习提醒推送

---

## 9. 文件清单

### 后端文件
```
backend/
├── app.py                           # Flask应用入口（已注册library蓝图）
├── models.py                        # 数据库模型（已添加词库相关模型）
├── database/
│   ├── word_library_schema.sql      # 词库表结构定义
│   ├── cet4_words_from_pdf.json     # CET-4词库数据（4434词）
│   ├── import_libraries.py          # 词库导入脚本
│   ├── extract_cet4_from_pdf.py     # PDF词库提取工具
│   ├── generate_cet4_base.py        # 基础词库生成器
│   └── word_master.db               # SQLite数据库
└── routes/
    └── library.py                   # 词库API路由（完整实现）
```

### 前端文件
```
miniprogram/
├── app.json                         # 已添加词库tab页面
├── pages/
│   └── library/
│       ├── list.ts                  # 词库选择页面
│       ├── words.ts                 # 单词列表页面
│       ├── learn.ts                 # 单词学习页面
│       └── review.ts                # 复习模式页面
└── utils/
    └── api.js                       # 已添加libraryApi接口
```

---

## 10. 更新日志

### V4.0 (2026-02-08)
- ✅ 完成内置词库系统，集成CET-4完整词库（4434词）
- ✅ 实现SM-2间隔重复算法，支持科学的单词复习
- ✅ 添加词库学习进度追踪和统计
- ✅ 实现4个词库相关前端页面（选择、列表、学习、复习）
- ✅ 支持词库单词一键添加到生词本
- ✅ 添加随机单词学习模式，排除已掌握单词
- ✅ 实现单词难度分级和筛选功能
- ✅ 从官方CET-4 PDF考纲自动提取词库数据

---

**文档版本**: V4.0  
**最后更新**: 2026-02-08

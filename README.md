# AI智能背单词微信小程序

[![GitHub](https://img.shields.io/badge/GitHub-word--master-blue)](https://github.com/zhengyaodong/word-master)
[![Python](https://img.shields.io/badge/Python-3.12+-green)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green)](https://flask.palletsprojects.com/)
[![WeChat](https://img.shields.io/badge/WeChat-MiniProgram-brightgreen)](https://developers.weixin.qq.com/miniprogram/dev/framework/)
[![Ollama](https://img.shields.io/badge/Ollama-qwen3:0.6b-orange)](https://ollama.com/)

一个基于本地Ollama大模型的智能背单词微信小程序，支持AI单词解释、生词本管理、批量导入、语音朗读、AI助记、例句收藏、学习统计等功能。

## 功能特性

### V3.0 新增功能 (最新)
- **批量导入与一键洗词**: 粘贴长文本（文章、歌词等），AI自动提取核心词汇，一键加入生词本
- **AI语境助记**: 生成极短幽默故事或谐音联想，提升记忆效率
- **智能去重**: 自动过滤高频词和已存在的单词

### V2.0 功能
- **语音朗读**: 使用 Edge-TTS 实现高质量语音朗读，支持单词和例句朗读
- **例句收藏**: 收藏重要例句，方便重点复习
- **学习统计**: 学习数据可视化，包括查询趋势、掌握进度
- **每日打卡**: 自动记录学习打卡，支持连续打卡天数统计

### 核心功能
- **AI智能查词**: 调用本地Ollama大模型(qwen3:0.6b)提供智能单词解释
- **生词本管理**: 支持添加、删除、分类管理生词
- **学习状态跟踪**: 记录单词学习状态（未学习/学习中/已掌握）
- **查询历史**: 自动保存查询记录，方便复习

### 技术特点
- 本地AI模型，无需联网即可使用（除语音功能外）
- 查询结果缓存，提升响应速度
- 简洁美观的UI设计
- 完整的RESTful API接口
- Edge-TTS 语音合成，自然流畅
- 智能文本处理，支持长文本分词和关键词提取

## 技术架构

### 后端技术栈
- **Python 3.12+**
- **Flask**: Web框架
- **SQLAlchemy**: ORM数据库操作
- **SQLite3**: 数据存储
- **Ollama**: 本地大模型服务
- **Edge-TTS**: 微软Edge语音合成

### 前端技术栈
- **微信小程序原生开发**
- **TypeScript**: 类型安全
- **Less**: CSS预处理器

## 项目结构

```
word-master/
├── backend/                    # 后端服务
│   ├── app.py                 # Flask应用入口
│   ├── models.py              # 数据库模型
│   ├── init_database.py       # 数据库初始化
│   ├── requirements.txt       # Python依赖
│   ├── database/              # 数据库文件
│   │   └── word_master.db
│   ├── routes/                # API路由
│   │   ├── user.py           # 用户相关接口
│   │   ├── word.py           # 单词查询接口
│   │   ├── vocab_book.py     # 生词本接口
│   │   ├── tts.py           # 语音合成接口(Edge-TTS)
│   │   └── v2_features.py    # V2.0功能接口(统计、收藏)
│   ├── services/              # 业务服务
│   │   └── ollama_service.py # Ollama服务封装
│   └── audio_cache/           # 语音缓存目录
├── miniprogram/               # 微信小程序
│   ├── app.ts                # 应用入口
│   ├── app.json              # 全局配置
│   ├── pages/                # 页面
│   │   ├── index/           # 查词页面
│   │   ├── vocab-book/      # 生词本页面
│   │   ├── vocab-detail/    # 生词详情
│   │   ├── import/          # 批量导入(V3.0)
│   │   ├── stats/           # 学习统计(V2.0)
│   │   ├── favorites/       # 收藏例句(V2.0)
│   │   └── profile/         # 个人中心
│   └── utils/                # 工具类
│       └── api.js           # API请求封装
├── PRD.md                     # 产品需求文档
└── README.md                  # 项目说明
```

## 快速开始

### 环境要求
- Python 3.12+
- Node.js (用于前端测试)
- Ollama (本地大模型服务)
- 微信开发者工具

### 1. 安装Ollama

```bash
# 下载安装Ollama
# 官网: https://ollama.com/

# 拉取qwen3:0.6b模型
ollama pull qwen3:0.6b
```

### 2. 启动后端服务

```bash
# 进入后端目录
cd backend

# 安装依赖（推荐）
pip install -r requirements.txt

# 或者手动安装
pip install flask flask-cors sqlalchemy requests edge-tts

# 初始化数据库
python init_database.py

# 启动服务
python app.py
```

服务将在 `http://localhost:5000` 启动。

### 3. 运行微信小程序

1. 打开微信开发者工具
2. 导入项目，选择 `miniprogram` 目录
3. 在详情设置中勾选 **"不校验合法域名"**
4. 编译运行

**注意**: 语音朗读功能需要联网，因为 Edge-TTS 使用微软服务。

### 4. V3.0 批量导入使用说明

1. 进入"我的"页面，点击"批量导入"
2. 粘贴英语文章、歌词或其他长文本
3. 点击"一键洗词"，AI自动提取核心词汇
4. 选择要导入的单词（默认全选）
5. 点击"批量导入"加入生词本

**特点**:
- 自动过滤高频词（the, and, of等）
- 自动去重，跳过已存在的单词
- 支持最多200个单词批量导入

### 5. V3.0 AI助记使用说明

1. 在单词详情页点击"AI助记"按钮
2. 系统自动生成幽默故事或谐音联想
3. 助记内容会自动缓存，避免重复生成
4. 可随时刷新生成新的助记内容

**示例**:
- Ambition → "俺必胜（Am-bi-tion），因为我有野心。"

## API接口文档

### 基础信息
- **Base URL**: `http://localhost:5000`
- **Content-Type**: `application/json`

### 接口列表

#### 健康检查
```
GET /api/health
```

#### 用户接口
```
POST   /api/user/login          # 用户登录
GET    /api/user/info           # 获取用户信息
PUT    /api/user/update         # 更新用户信息
GET    /api/user/stats          # 获取用户统计
```

#### 单词查询接口
```
POST   /api/word/query          # 查询单词（调用AI）
GET    /api/word/history        # 获取查询历史
DELETE /api/word/history/clear  # 清空查询历史
```

#### 生词本接口
```
POST   /api/vocab-book/add              # 添加到生词本
GET    /api/vocab-book/list            # 获取生词列表
GET    /api/vocab-book/detail          # 获取生词详情
PUT    /api/vocab-book/update          # 更新生词状态
DELETE /api/vocab-book/delete          # 删除生词
DELETE /api/vocab-book/batch-delete    # 批量删除
GET    /api/vocab-book/stats           # 获取生词统计
GET    /api/vocab-book/check-exists    # 检查单词是否存在
```

#### 语音合成接口 (V2.0)
```
POST   /api/tts/speak           # 文本转语音
POST   /api/tts/stream          # 流式语音合成
GET    /api/tts/audio/<id>      # 获取音频文件
GET    /api/tts/voices          # 获取可用语音列表
DELETE /api/tts/clear-cache     # 清理音频缓存
```

#### 收藏例句接口 (V2.0)
```
POST   /api/favorites/add       # 收藏例句
GET    /api/favorites/list      # 获取收藏列表
DELETE /api/favorites/delete    # 删除收藏
GET    /api/favorites/check     # 检查是否已收藏
```

#### 学习统计接口 (V2.0)
```
GET    /api/stats/overview      # 获取学习概览
GET    /api/stats/trend         # 获取近7天趋势
POST   /api/stats/checkin       # 手动打卡
```

#### 批量导入接口 (V3.0)
```
POST   /api/vocab-book/clean            # 一键洗词（文本提取词汇）
POST   /api/vocab-book/import           # 批量导入单词到生词本
```

#### AI助记接口 (V3.0)
```
GET    /api/word/mnemonic         # 获取单词助记（优先缓存）
POST   /api/word/mnemonic         # 生成单词助记并缓存
```

## 配置说明

### 后端配置
编辑 `backend/services/ollama_service.py`:
```python
self.api_endpoint = "http://localhost:11434/api/generate"  # Ollama地址
self.model = "qwen3:0.6b"  # 使用的模型
```

### 前端配置
编辑 `miniprogram/utils/api.js`:
```javascript
// 开发环境
const BASE_URL = 'http://localhost:5000';

// 真机调试（改为实际IP）
const BASE_URL = 'http://192.168.x.x:5000';
```

## 测试

### 后端API测试
```bash
cd backend

# 基础API测试
python test_api.py

# V2.0功能测试
python test_v2_api.py
python test_v2_local.py

# V3.0功能测试
python test_v3_local.py
```

### 前端联调测试
```bash
cd miniprogram/utils
node test-node.js
```

## 数据库设计

### 用户表 (users)
| 字段 | 类型 | 说明 |
|------|------|------|
| user_id | INTEGER | 主键 |
| openid | VARCHAR(100) | 微信openid |
| nickname | VARCHAR(100) | 昵称 |
| avatar_url | VARCHAR(500) | 头像URL |
| created_at | TIMESTAMP | 创建时间 |

### 生词本表 (vocabulary_book)
| 字段 | 类型 | 说明 |
|------|------|------|
| vocab_id | INTEGER | 主键 |
| user_id | INTEGER | 用户ID |
| word | VARCHAR(100) | 单词 |
| phonetic | VARCHAR(100) | 音标 |
| definition | TEXT | 中文释义 |
| english_definition | TEXT | 英文释义 |
| examples | TEXT | 例句(JSON) |
| memory_tips | TEXT | 记忆技巧 |
| status | INTEGER | 状态(0未学习/1学习中/2已掌握) |
| created_at | TIMESTAMP | 创建时间 |

### 查询历史表 (query_history)
| 字段 | 类型 | 说明 |
|------|------|------|
| history_id | INTEGER | 主键 |
| user_id | INTEGER | 用户ID |
| word | VARCHAR(100) | 查询单词 |
| result | TEXT | 查询结果(JSON) |
| created_at | TIMESTAMP | 创建时间 |

### 收藏例句表 (favorite_sentences) - V2.0
| 字段 | 类型 | 说明 |
|------|------|------|
| favorite_id | INTEGER | 主键 |
| user_id | INTEGER | 用户ID |
| vocab_id | INTEGER | 生词ID |
| sentence | TEXT | 例句内容 |
| translation | TEXT | 中文翻译 |
| created_at | TIMESTAMP | 创建时间 |

### 学习记录表 (study_records) - V2.0
| 字段 | 类型 | 说明 |
|------|------|------|
| record_id | INTEGER | 主键 |
| user_id | INTEGER | 用户ID |
| study_date | DATE | 学习日期 |
| query_count | INTEGER | 查询次数 |
| is_checked_in | INTEGER | 是否打卡(0/1) |

### 导入记录表 (import_history) - V3.0
| 字段 | 类型 | 说明 |
|------|------|------|
| import_id | INTEGER | 主键 |
| user_id | INTEGER | 用户ID |
| source_type | VARCHAR(50) | 来源（paste/csv/json） |
| raw_text | TEXT | 原始文本 |
| word_count | INTEGER | 提取词数 |
| created_at | TIMESTAMP | 创建时间 |

#### 生词本表新增字段 (V3.0)
| 字段 | 类型 | 说明 |
|------|------|------|
| mnemonic | TEXT | AI助记内容（缓存） |
| mnemonic_updated_at | TIMESTAMP | 助记更新时间 |

## 开发计划

- [x] V1.0 基础版本
  - [x] 数据库设计
  - [x] 后端API开发
  - [x] 微信小程序前端
  - [x] Ollama AI集成
  - [x] 生词本管理
  - [x] 查询历史

- [x] V2.0 功能增强
  - [x] 语音朗读功能 (Edge-TTS)
  - [x] 例句收藏功能
  - [x] 学习统计图表
  - [x] 每日打卡功能
  - [x] 连续打卡统计

- [x] V3.0 功能升级 (2026-02-07)
  - [x] 批量导入与一键洗词
  - [x] AI语境辅助记忆（助记）
  - [x] 智能去重与高频词过滤

## 更新日志

### V3.0 (2026-02-07)
- 新增批量导入功能，支持粘贴长文本一键提取词汇
- 新增"一键洗词"功能，AI自动提取文章/歌词中的核心词汇
- 新增AI语境助记功能，生成幽默故事和谐音联想辅助记忆
- 新增导入历史记录表
- 优化生词本表结构，新增助记缓存字段
- 智能过滤高频词（the, and, of等）和已存在单词

### V2.0 (2026-01-31)
- 新增语音朗读功能，使用 Edge-TTS 替代微信小程序插件
- 新增例句收藏功能，支持收藏/取消收藏
- 新增学习统计页面，展示学习趋势和进度
- 新增每日打卡功能，自动记录学习天数
- 新增收藏例句页面，管理收藏的例句
- 优化收藏按钮状态显示
- 添加 requirements.txt 依赖管理

### V1.0 (基础版本)
- 实现AI智能查词功能
- 实现生词本管理
- 实现查询历史记录
- 集成Ollama本地大模型

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 作者: zhengyaodong
- GitHub: https://github.com/zhengyaodong/word-master

## 致谢

- [Ollama](https://ollama.com/) - 本地大模型服务
- [Flask](https://flask.palletsprojects.com/) - Python Web框架
- [Edge-TTS](https://github.com/rany2/edge-tts) - 微软Edge语音合成
- [微信小程序](https://developers.weixin.qq.com/miniprogram/dev/framework/) - 前端框架

# AI智能背单词微信小程序

[![GitHub](https://img.shields.io/badge/GitHub-word--master-blue)](https://github.com/zhengyaodong/word-master)
[![Python](https://img.shields.io/badge/Python-3.12+-green)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green)](https://flask.palletsprojects.com/)
[![WeChat](https://img.shields.io/badge/WeChat-MiniProgram-brightgreen)](https://developers.weixin.qq.com/miniprogram/dev/framework/)
[![Ollama](https://img.shields.io/badge/Ollama-qwen3:0.6b-orange)](https://ollama.com/)

一个基于本地Ollama大模型的智能背单词微信小程序，支持AI单词解释、生词本管理等功能。

## 功能特性

### 核心功能
- **AI智能查词**: 调用本地Ollama大模型(qwen3:0.6b)提供智能单词解释
- **生词本管理**: 支持添加、删除、分类管理生词
- **学习状态跟踪**: 记录单词学习状态（未学习/学习中/已掌握）
- **查询历史**: 自动保存查询记录，方便复习

### 技术特点
- 本地AI模型，无需联网即可使用
- 查询结果缓存，提升响应速度
- 简洁美观的UI设计
- 完整的RESTful API接口

## 技术架构

### 后端技术栈
- **Python 3.12+**
- **Flask**: Web框架
- **SQLAlchemy**: ORM数据库操作
- **SQLite3**: 数据存储
- **Ollama**: 本地大模型服务

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
│   ├── database/              # 数据库文件
│   │   └── word_master.db
│   ├── routes/                # API路由
│   │   ├── user.py           # 用户相关接口
│   │   ├── word.py           # 单词查询接口
│   │   └── vocab_book.py     # 生词本接口
│   └── services/              # 业务服务
│       └── ollama_service.py # Ollama服务封装
├── miniprogram/               # 微信小程序
│   ├── app.ts                # 应用入口
│   ├── app.json              # 全局配置
│   ├── pages/                # 页面
│   │   ├── index/           # 查词页面
│   │   ├── vocab-book/      # 生词本页面
│   │   ├── profile/         # 个人中心
│   │   └── vocab-detail/    # 生词详情
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

# 安装依赖
pip install flask flask-cors sqlalchemy requests

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
```

#### 生词本接口
```
POST   /api/vocab-book/add              # 添加到生词本
GET    /api/vocab-book/list            # 获取生词列表
GET    /api/vocab-book/detail          # 获取生词详情
PUT    /api/vocab-book/update          # 更新生词状态
DELETE /api/vocab-book/delete          # 删除生词
GET    /api/vocab-book/stats           # 获取生词统计
GET    /api/vocab-book/check-exists    # 检查单词是否存在
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
python test_api.py
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

## 开发计划

- [x] 基础版本开发
  - [x] 数据库设计
  - [x] 后端API开发
  - [x] 微信小程序前端
  - [x] Ollama AI集成
- [ ] 进阶功能
  - [ ] 单词复习模式
  - [ ] 学习统计图表
  - [ ] 单词导入导出
  - [ ] 语音朗读功能

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
- [微信小程序](https://developers.weixin.qq.com/miniprogram/dev/framework/) - 前端框架

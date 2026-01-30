# 微信小程序背单词项目需求文档（PRD）

## 1. 项目背景与目标

### 1.1 项目背景
随着全球化进程的加速和互联网技术的发展，英语作为国际通用语言的重要性日益凸显。越来越多的人意识到英语学习的重要性，尤其是单词积累作为英语学习的基础，受到了广泛关注。然而，传统的单词记忆方法存在效率低下、缺乏个性化、难以坚持等问题。

微信小程序作为一种轻量级应用，具有无需下载安装、使用便捷、用户基数大等优势，为单词学习提供了新的解决方案。本项目旨在开发一款基于微信小程序的背单词应用，结合现代教育理念和技术手段，为用户提供高效、个性化的单词学习体验。

### 1.2 项目目标
- 提供高效、科学的单词学习方法，帮助用户快速积累词汇量
- 结合记忆曲线算法，智能安排复习计划，提高记忆效果
- 支持多种学习模式和测试方式，满足不同用户的学习需求
- 提供个性化学习数据统计和分析，帮助用户了解学习进度
- 打造简洁、直观、易用的用户界面，提升用户体验
- 确保应用性能稳定、数据安全，保护用户隐私
- **新增：支持用户自定义查询单词，利用AI大模型提供智能解释**
- **新增：建立个人生词本，方便用户管理自定义学习的单词**

### 1.3 目标用户群体
- **学生群体**：包括中小学生、大学生等需要系统学习英语的学生
- **职场人士**：需要提升英语水平以适应工作需求的职场人员
- **英语爱好者**：对英语学习有兴趣，希望扩大词汇量的人群
- **备考人员**：准备各类英语考试（如四六级、考研、托福、雅思等）的考生
- **新增：自主学习者**：喜欢通过阅读、观影等方式自主学习英语，需要查询生词的用户

---

## 2. 核心功能模块

### 2.1 单词学习模块
#### 2.1.1 功能描述
- **词库选择**：支持多种词库（如小学、初中、高中、大学、考研、托福、雅思等）的选择
- **单词展示**：展示单词的拼写、发音、释义、例句、词性等信息
- **学习模式**：支持顺序学习、随机学习等多种学习模式
- **学习进度**：实时显示当前学习进度和剩余单词数量
- **标记功能**：支持标记难记单词，方便后续重点复习

#### 2.1.2 交互流程
1. 用户进入单词学习页面，选择要学习的词库
2. 系统展示单词信息，用户可点击发音按钮听单词发音
3. 用户可滑动或点击按钮切换到下一个单词
4. 系统自动记录学习进度，用户可随时退出，下次继续学习

#### 2.1.3 业务规则
- 每次学习默认展示20个单词，可根据用户设置调整
- 学习过程中，系统自动保存学习记录，确保进度不丢失
- 对于标记的难记单词，系统会在复习时优先展示

---

### 2.2 单词复习模块
#### 2.2.1 功能描述
- **智能复习**：基于艾宾浩斯记忆曲线算法，智能安排复习计划
- **复习提醒**：在适当的时间提醒用户进行复习
- **复习统计**：展示复习完成情况和记忆效果
- **重点复习**：针对标记的难记单词和易错单词进行重点复习

#### 2.2.2 交互流程
1. 用户进入单词复习页面，系统根据记忆曲线算法生成复习列表
2. 用户逐个复习单词，可选择"认识"或"不认识"
3. 系统根据用户的选择调整单词的下次复习时间
4. 复习完成后，系统展示复习统计数据

#### 2.2.3 业务规则
- 记忆曲线算法参数：首次学习后1天、2天、4天、7天、15天进行复习
- 对于标记为"不认识"的单词，缩短下次复习时间间隔
- 对于连续3次标记为"认识"的单词，延长下次复习时间间隔

---

### 2.3 单词测试模块
#### 2.3.1 功能描述
- **测试模式**：支持选择、填空、拼写等多种测试模式
- **测试范围**：可选择测试范围（如最近学习的单词、特定词库、**生词本**等）
- **测试难度**：支持调整测试难度
- **测试结果**：实时展示测试结果，包括正确率、用时等
- **错题收集**：自动收集错题，方便后续复习

#### 2.3.2 交互流程
1. 用户进入单词测试页面，选择测试模式、范围和难度
2. 系统生成测试题目，用户进行答题
3. 答题完成后，系统展示测试结果和错题解析
4. 用户可查看错题详情，选择重新测试或返回

#### 2.3.3 业务规则
- 测试题目数量默认为20题，可根据用户设置调整
- 测试完成后，系统自动将错题加入错题集
- 对于连续答错的单词，系统会增加其在后续测试中的出现频率

---

### 2.4 用户管理模块
#### 2.4.1 功能描述
- **用户注册/登录**：支持微信一键登录
- **个人信息管理**：支持修改头像、昵称等个人信息
- **学习数据统计**：展示学习天数、累计学习单词数、掌握单词数、**生词本单词数**等数据
- **学习计划设置**：支持设置每日学习目标、提醒时间等
- **账号安全**：支持修改密码、绑定手机等安全设置

#### 2.4.2 交互流程
1. 用户首次进入应用，系统引导用户进行微信登录
2. 登录后，用户可进入个人中心查看和管理个人信息
3. 用户可设置学习计划和提醒时间
4. 系统定期更新学习数据统计，用户可随时查看

#### 2.4.3 业务规则
- 必须通过微信登录才能使用应用的完整功能
- 学习数据统计每日更新，确保数据准确性
- 个人信息修改后，系统自动保存并更新

---

### 2.5 单词查询与生词本模块（新增）

#### 2.5.1 功能描述
- **单词查询**：用户输入英文单词，系统调用本地Ollama大模型进行智能解释
- **AI解释**：Ollama大模型提供单词的详细释义、音标、词性、例句、词根词缀分析、记忆技巧等
- **一键添加**：用户可将查询的单词一键添加到个人生词本
- **生词本管理**：支持查看、编辑、删除生词本中的单词
- **生词学习**：支持对生词本中的单词进行学习和复习
- **批量操作**：支持批量删除、批量标记等操作

#### 2.5.2 AI解释内容
Ollama大模型（qwen3:0.6b）将为每个单词提供以下信息：
- **基础信息**：单词拼写、音标、词性
- **中文释义**：详细的中文解释，包括常见含义和特殊含义
- **英文释义**：简洁的英文解释，帮助理解
- **例句**：2-3个实用例句，展示单词在不同语境下的用法
- **词根词缀**：分析单词的构词法，帮助记忆
- **同义词/反义词**：列出相关的同义词和反义词
- **记忆技巧**：提供记忆该单词的技巧和方法
- **常见搭配**：列出该单词的常用搭配短语

#### 2.5.3 交互流程

**单词查询流程：**
1. 用户进入"查词"页面，在搜索框输入要查询的英文单词
2. 点击"查询"按钮，系统显示加载状态
3. 后端调用本地Ollama大模型API获取单词解释
4. 系统展示AI生成的单词详细信息
5. 用户可点击"加入生词本"按钮将该单词添加到个人生词本
6. 用户可点击"发音"按钮听取单词发音（使用系统TTS或在线发音）

**生词本管理流程：**
1. 用户进入"生词本"页面，查看已添加的所有单词
2. 支持按添加时间、字母顺序、掌握程度等排序
3. 用户可点击单词查看详情，进行学习或复习
4. 支持左滑删除、批量选择删除等操作
5. 支持将生词本单词加入学习计划

#### 2.5.4 业务规则
- 单词查询功能需要设备能够连接到本地Ollama服务
- 查询结果缓存24小时，避免重复调用模型
- 生词本单词数量无上限，但建议保持在合理范围（500个以内）
- 生词本中的单词自动纳入复习计划，按照记忆曲线进行复习
- 生词本单词可参与测试，测试范围可选择"仅生词本"
- 支持将生词本导出为文本或PDF格式（可选功能）

#### 2.5.5 Ollama模型调用规范
- **模型名称**：qwen3:0.6b
- **调用方式**：本地HTTP API调用
- **请求格式**：
  ```json
  {
    "model": "qwen3:0.6b",
    "prompt": "请详细解释单词 '{word}'，包括：音标、词性、中文释义、英文释义、2-3个例句、词根词缀分析、同义词反义词、记忆技巧、常见搭配。请以JSON格式返回。",
    "stream": false
  }
  ```
- **响应解析**：解析模型返回的JSON格式数据，提取各字段信息
- **错误处理**：模型调用失败时，显示友好提示，建议用户检查Ollama服务状态
- **超时设置**：API调用超时时间为30秒

---

### 2.6 其他功能模块
#### 2.6.1 单词收藏
- 支持收藏重要或难记的单词
- 收藏的单词可在专门的收藏夹中查看和复习

#### 2.6.2 学习社区
- 支持用户分享学习成果和经验
- 提供学习排行榜，激励用户积极学习

#### 2.6.3 每日一词
- 每天推荐一个精选单词，帮助用户扩充词汇量
- 提供单词的详细解析和使用场景

---

## 3. 用户界面设计要求

### 3.1 整体风格
- **设计风格**：简洁、现代、清新，符合微信小程序的设计规范
- **色彩方案**：主色调采用蓝色系（代表知识、智慧），辅助色采用橙色（代表活力、热情），**AI功能使用紫色作为强调色**
- **图标设计**：使用简约、直观的线性图标，保持风格统一
- **字体设计**：采用无衬线字体，大小适中，确保可读性

### 3.2 页面布局
- **顶部导航栏**：显示当前页面标题，提供返回按钮
- **底部导航栏**：包含"首页"、"学习"、"**查词**"、"测试"、"个人中心"等核心功能入口
- **内容区域**：根据不同页面功能，合理安排内容布局，确保信息展示清晰
- **操作按钮**：位置明显，大小适中，便于点击操作

### 3.3 新增页面设计

#### 3.3.1 查词页面
- **搜索区域**：
  - 顶部搜索框，支持输入英文单词
  - 搜索按钮，点击触发查询
  - 历史记录展示，显示最近查询的单词
  
- **查询结果区域**：
  - 单词标题区：显示单词拼写、音标、发音按钮
  - AI解释卡片：
    - 中文释义（突出显示）
    - 英文释义
    - 例句列表（带中文翻译）
    - 词根词缀分析
    - 同义词/反义词
    - 记忆技巧
    - 常见搭配
  - 操作按钮区：
    - "加入生词本"按钮（醒目颜色）
    - "重新查询"按钮
    - "分享"按钮

- **加载状态**：
  - 查询时显示加载动画
  - 提示"AI正在思考中..."

- **空状态**：
  - 未查询时显示提示文字和示例单词
  - 查询失败时显示错误提示和重试按钮

#### 3.3.2 生词本页面
- **统计卡片**：
  - 生词总数
  - 今日新增
  - 已掌握数量
  - 待复习数量

- **单词列表**：
  - 卡片式布局，每个单词显示拼写、音标、简要释义
  - 左滑显示删除按钮
  - 长按进入批量选择模式
  - 点击卡片进入单词详情

- **筛选排序**：
  - 按添加时间排序（默认）
  - 按字母顺序排序
  - 按掌握程度筛选
  - 按复习状态筛选

- **操作栏**：
  - 批量选择按钮
  - 排序方式切换
  - 导出按钮（可选）

### 3.4 交互设计
- **动画效果**：添加适当的过渡动画，提升用户体验
- **反馈机制**：操作后给予清晰的视觉反馈，如按钮点击效果、加载状态等
- **手势操作**：支持常见的手势操作，如滑动切换单词、下拉刷新、左滑删除等
- **响应速度**：确保页面切换和操作响应迅速，减少用户等待时间
- **AI查询反馈**：查询过程中显示进度提示，查询完成后有成功提示音或动画

### 3.5 适配要求
- **设备适配**：适配不同尺寸的手机屏幕，确保在各种设备上都有良好的显示效果
- **系统适配**：兼容iOS和Android系统，确保功能正常运行

---

## 4. 数据结构设计

### 4.1 数据库表结构

#### 4.1.1 用户信息表（users）
| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `user_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 用户ID |
| `openid` | `VARCHAR(100)` | `UNIQUE NOT NULL` | 微信用户唯一标识 |
| `nickname` | `VARCHAR(50)` | `NOT NULL` | 用户昵称 |
| `avatar_url` | `VARCHAR(255)` | | 用户头像URL |
| `gender` | `INTEGER` | | 用户性别（0-未知，1-男，2-女） |
| `phone` | `VARCHAR(20)` | | 绑定手机号 |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 注册时间 |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 更新时间 |

#### 4.1.2 词库表（vocabulary_sets）
| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `set_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 词库ID |
| `set_name` | `VARCHAR(50)` | `NOT NULL` | 词库名称 |
| `description` | `TEXT` | | 词库描述 |
| `level` | `INTEGER` | | 词库难度级别 |
| `word_count` | `INTEGER` | | 单词数量 |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 创建时间 |

#### 4.1.3 单词库表（word_library）
| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `word_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 单词ID |
| `word` | `VARCHAR(50)` | `NOT NULL` | 单词拼写 |
| `phonetic` | `VARCHAR(100)` | | 音标 |
| `definition` | `TEXT` | `NOT NULL` | 释义 |
| `example` | `TEXT` | | 例句 |
| `audio_url` | `VARCHAR(255)` | | 发音URL |
| `set_id` | `INTEGER` | `REFERENCES vocabulary_sets(set_id)` | 所属词库ID |
| `difficulty` | `INTEGER` | | 单词难度 |

#### 4.1.4 学习记录表（learning_records）
| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `record_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 记录ID |
| `user_id` | `INTEGER` | `REFERENCES users(user_id)` | 用户ID |
| `word_id` | `INTEGER` | `REFERENCES word_library(word_id)` | 单词ID |
| `first_learned_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 首次学习时间 |
| `last_reviewed_at` | `TIMESTAMP` | | 最后复习时间 |
| `next_review_at` | `TIMESTAMP` | | 下次复习时间 |
| `review_count` | `INTEGER` | `DEFAULT 0` | 复习次数 |
| `mastery_level` | `INTEGER` | `DEFAULT 0` | 掌握程度（0-未掌握，1-熟悉，2-掌握） |
| `is_marked` | `BOOLEAN` | `DEFAULT FALSE` | 是否标记为重点 |

#### 4.1.5 测试记录表（test_records）
| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `test_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 测试ID |
| `user_id` | `INTEGER` | `REFERENCES users(user_id)` | 用户ID |
| `test_type` | `VARCHAR(20)` | `NOT NULL` | 测试类型 |
| `test_scope` | `VARCHAR(100)` | | 测试范围 |
| `difficulty` | `INTEGER` | | 测试难度 |
| `total_questions` | `INTEGER` | `NOT NULL` | 总题目数 |
| `correct_count` | `INTEGER` | `NOT NULL` | 正确题目数 |
| `wrong_count` | `INTEGER` | `NOT NULL` | 错误题目数 |
| `time_used` | `INTEGER` | | 用时（秒） |
| `test_date` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 测试时间 |

#### 4.1.6 测试题目表（test_questions）
| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `question_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 题目ID |
| `test_id` | `INTEGER` | `REFERENCES test_records(test_id)` | 所属测试ID |
| `word_id` | `INTEGER` | `REFERENCES word_library(word_id)` | 单词ID |
| `question_type` | `VARCHAR(20)` | `NOT NULL` | 题目类型 |
| `question_content` | `TEXT` | `NOT NULL` | 题目内容 |
| `options` | `TEXT` | | 选项（JSON格式） |
| `correct_answer` | `TEXT` | `NOT NULL` | 正确答案 |
| `user_answer` | `TEXT` | | 用户答案 |
| `is_correct` | `BOOLEAN` | | 是否正确 |

#### 4.1.7 用户词库关联表（user_vocabulary_sets）
| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 关联ID |
| `user_id` | `INTEGER` | `REFERENCES users(user_id)` | 用户ID |
| `set_id` | `INTEGER` | `REFERENCES vocabulary_sets(set_id)` | 词库ID |
| `progress` | `INTEGER` | `DEFAULT 0` | 学习进度（百分比） |
| `joined_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 加入时间 |

#### 4.1.8 用户设置表（user_settings）
| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `setting_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 设置ID |
| `user_id` | `INTEGER` | `REFERENCES users(user_id)` | 用户ID |
| `daily_target` | `INTEGER` | `DEFAULT 20` | 每日学习目标（单词数） |
| `review_reminder` | `BOOLEAN` | `DEFAULT TRUE` | 是否开启复习提醒 |
| `reminder_time` | `TIME` | | 提醒时间 |
| `theme` | `VARCHAR(20)` | `DEFAULT 'light'` | 主题（light/dark） |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 更新时间 |

#### 4.1.9 生词本表（user_vocabulary_book）- 新增
| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `vocab_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 生词ID |
| `user_id` | `INTEGER` | `REFERENCES users(user_id)` | 用户ID |
| `word` | `VARCHAR(50)` | `NOT NULL` | 单词拼写 |
| `phonetic` | `VARCHAR(100)` | | 音标 |
| `definition` | `TEXT` | `NOT NULL` | 中文释义 |
| `english_definition` | `TEXT` | | 英文释义 |
| `examples` | `TEXT` | | 例句（JSON格式） |
| `word_formation` | `TEXT` | | 词根词缀分析 |
| `synonyms` | `TEXT` | | 同义词（JSON格式） |
| `antonyms` | `TEXT` | | 反义词（JSON格式） |
| `memory_tips` | `TEXT` | | 记忆技巧 |
| `collocations` | `TEXT` | | 常见搭配（JSON格式） |
| `source` | `VARCHAR(20)` | `DEFAULT 'ollama'` | 来源（ollama/manual） |
| `ai_raw_response` | `TEXT` | | Ollama原始响应（用于调试） |
| `mastery_level` | `INTEGER` | `DEFAULT 0` | 掌握程度（0-未掌握，1-熟悉，2-掌握） |
| `review_count` | `INTEGER` | `DEFAULT 0` | 复习次数 |
| `last_reviewed_at` | `TIMESTAMP` | | 最后复习时间 |
| `next_review_at` | `TIMESTAMP` | | 下次复习时间 |
| `is_in_plan` | `BOOLEAN` | `DEFAULT TRUE` | 是否加入学习计划 |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 添加时间 |
| `updated_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 更新时间 |

#### 4.1.10 查询历史表（query_history）- 新增
| 字段名 | 数据类型 | 约束 | 描述 |
| :--- | :--- | :--- | :--- |
| `history_id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | 历史记录ID |
| `user_id` | `INTEGER` | `REFERENCES users(user_id)` | 用户ID |
| `word` | `VARCHAR(50)` | `NOT NULL` | 查询的单词 |
| `query_result` | `TEXT` | | 查询结果缓存 |
| `is_added_to_book` | `BOOLEAN` | `DEFAULT FALSE` | 是否已加入生词本 |
| `vocab_id` | `INTEGER` | `REFERENCES user_vocabulary_book(vocab_id)` | 关联的生词本ID |
| `query_time` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | 查询时间 |

### 4.2 数据传输对象（DTOs）

#### 4.2.1 用户信息DTO
```json
{
  "user_id": 1,
  "nickname": "张三",
  "avatar_url": "https://example.com/avatar.jpg",
  "phone": "13800138000",
  "created_at": "2023-01-01 12:00:00"
}
```

#### 4.2.2 单词信息DTO
```json
{
  "word_id": 1,
  "word": "apple",
  "phonetic": "/ˈæpl/",
  "definition": "n. 苹果",
  "example": "I ate an apple this morning.",
  "audio_url": "https://example.com/audio/apple.mp3",
  "set_id": 1,
  "difficulty": 1
}
```

#### 4.2.3 学习记录DTO
```json
{
  "record_id": 1,
  "user_id": 1,
  "word_id": 1,
  "word": "apple",
  "first_learned_at": "2023-01-01 12:00:00",
  "last_reviewed_at": "2023-01-02 12:00:00",
  "next_review_at": "2023-01-04 12:00:00",
  "review_count": 1,
  "mastery_level": 1,
  "is_marked": false
}
```

#### 4.2.4 测试结果DTO
```json
{
  "test_id": 1,
  "test_type": "choice",
  "test_scope": "最近学习",
  "difficulty": 2,
  "total_questions": 20,
  "correct_count": 15,
  "wrong_count": 5,
  "accuracy": 75,
  "time_used": 300,
  "test_date": "2023-01-01 12:00:00",
  "wrong_words": [
    {
      "word_id": 5,
      "word": "banana",
      "definition": "n. 香蕉"
    }
  ]
}
```

#### 4.2.5 AI单词解释DTO（新增）
```json
{
  "word": "serendipity",
  "phonetic": "/ˌserənˈdɪpəti/",
  "part_of_speech": "n.",
  "definition": "意外发现珍奇事物的本领；机缘凑巧",
  "english_definition": "The occurrence and development of events by chance in a happy or beneficial way",
  "examples": [
    {
      "sentence": "We found the restaurant by pure serendipity.",
      "translation": "我们纯粹是机缘巧合找到了这家餐厅。"
    },
    {
      "sentence": "Many scientific discoveries are the result of serendipity.",
      "translation": "许多科学发现都是机缘巧合的结果。"
    }
  ],
  "word_formation": "源自波斯童话《Serendip》（锡兰三王子），由英国作家Horace Walpole于1754年创造",
  "synonyms": ["chance", "luck", "fortune", "accident"],
  "antonyms": ["misfortune", "bad luck"],
  "memory_tips": "可以联想为'seren'(宁静的) + 'dipity'(小插曲)，在宁静中发生的小插曲就是意外之喜",
  "collocations": ["pure serendipity", "by serendipity", "a moment of serendipity"]
}
```

#### 4.2.6 生词本单词DTO（新增）
```json
{
  "vocab_id": 1,
  "user_id": 1,
  "word": "serendipity",
  "phonetic": "/ˌserənˈdɪpəti/",
  "definition": "意外发现珍奇事物的本领；机缘凑巧",
  "english_definition": "The occurrence and development of events by chance in a happy or beneficial way",
  "examples": [
    {
      "sentence": "We found the restaurant by pure serendipity.",
      "translation": "我们纯粹是机缘巧合找到了这家餐厅。"
    }
  ],
  "word_formation": "源自波斯童话《Serendip》",
  "synonyms": ["chance", "luck"],
  "antonyms": ["misfortune"],
  "memory_tips": "联想为'seren'(宁静的) + 'dipity'(小插曲)",
  "collocations": ["pure serendipity", "by serendipity"],
  "source": "ollama",
  "mastery_level": 0,
  "review_count": 0,
  "is_in_plan": true,
  "created_at": "2023-01-01 12:00:00"
}
```

---

## 5. 技术架构说明

### 5.1 技术栈
- **前端**：HTML + CSS + JavaScript（微信小程序原生开发）
- **后端**：Python（Flask/FastAPI框架）
- **数据库**：SQLite3
- **AI模型**：Ollama（本地部署，模型：qwen3:0.6b）
- **部署**：微信小程序云开发或传统服务器部署

### 5.2 架构设计
#### 5.2.1 前后端分离架构
- **前端**：微信小程序客户端，负责用户界面展示和用户交互
- **后端**：Python服务端，负责业务逻辑处理、数据存储和AI模型调用
- **API接口**：RESTful风格，JSON格式数据传输
- **AI服务**：本地Ollama服务，提供单词智能解释功能

#### 5.2.2 核心流程图
```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   微信小程序    │────▶│   Python后端     │────▶│   SQLite3数据库 │
│    客户端       │◀────│    服务器        │◀────│                 │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                │
                                │ HTTP API
                                ▼
                        ┌──────────────────┐
                        │   Ollama本地服务  │
                        │  (qwen3:0.6b)    │
                        └──────────────────┘
```

#### 5.2.3 单词查询流程（新增）
```
用户输入单词
    │
    ▼
微信小程序发送查询请求
    │
    ▼
Python后端接收请求
    │
    ▼
检查缓存（24小时内查询过？）
    │
    ├── 是 ──▶ 直接返回缓存结果
    │
    └── 否 ──▶ 调用Ollama API
                  │
                  ▼
            构造Prompt请求
                  │
                  ▼
            Ollama生成解释
                  │
                  ▼
            解析JSON响应
                  │
                  ▼
            保存到缓存
                  │
                  ▼
            返回查询结果
```

### 5.3 API接口设计

#### 5.3.1 用户相关接口
| API路径 | 方法 | 功能描述 | 请求参数 | 成功响应 |
| :--- | :--- | :--- | :--- | :--- |
| `/api/user/login` | `POST` | 微信登录 | `code: string`（微信登录凭证） | `{"code": 0, "data": {"user_id": 1, "nickname": "张三", "avatar_url": "..."}, "message": "登录成功"}` |
| `/api/user/info` | `GET` | 获取用户信息 | `user_id: int` | `{"code": 0, "data": {"user_id": 1, "nickname": "张三", "avatar_url": "...", "phone": "..."}, "message": "获取成功"}` |
| `/api/user/update` | `PUT` | 更新用户信息 | `user_id: int, nickname: string, avatar_url: string, phone: string` | `{"code": 0, "data": {}, "message": "更新成功"}` |
| `/api/user/settings` | `GET` | 获取用户设置 | `user_id: int` | `{"code": 0, "data": {"daily_target": 20, "review_reminder": true, "reminder_time": "08:00", "theme": "light"}, "message": "获取成功"}` |
| `/api/user/settings/update` | `PUT` | 更新用户设置 | `user_id: int, daily_target: int, review_reminder: boolean, reminder_time: string, theme: string` | `{"code": 0, "data": {}, "message": "更新成功"}` |
| `/api/user/stats` | `GET` | 获取用户学习统计 | `user_id: int` | `{"code": 0, "data": {"learn_days": 30, "total_words": 500, "mastered_words": 300, "vocab_book_count": 50}, "message": "获取成功"}` |

#### 5.3.2 词库相关接口
| API路径 | 方法 | 功能描述 | 请求参数 | 成功响应 |
| :--- | :--- | :--- | :--- | :--- |
| `/api/vocabulary/sets` | `GET` | 获取词库列表 | 无 | `{"code": 0, "data": [{"set_id": 1, "set_name": "小学英语", "description": "...", "level": 1, "word_count": 1000}], "message": "获取成功"}` |
| `/api/vocabulary/words` | `GET` | 获取单词列表 | `set_id: int, page: int, page_size: int` | `{"code": 0, "data": {"total": 1000, "words": [{"word_id": 1, "word": "apple", "phonetic": "/ˈæpl/", "definition": "n. 苹果", "example": "...", "audio_url": "..."}]}, "message": "获取成功"}` |
| `/api/vocabulary/join` | `POST` | 加入词库 | `user_id: int, set_id: int` | `{"code": 0, "data": {}, "message": "加入成功"}` |
| `/api/vocabulary/progress` | `GET` | 获取词库学习进度 | `user_id: int, set_id: int` | `{"code": 0, "data": {"progress": 20, "learned_count": 200, "total_count": 1000}, "message": "获取成功"}` |

#### 5.3.3 学习相关接口
| API路径 | 方法 | 功能描述 | 请求参数 | 成功响应 |
| :--- | :--- | :--- | :--- | :--- |
| `/api/learning/start` | `POST` | 开始学习 | `user_id: int, set_id: int, count: int` | `{"code": 0, "data": {"words": [{"word_id": 1, "word": "apple", "phonetic": "/ˈæpl/", "definition": "n. 苹果", "example": "...", "audio_url": "..."}]}, "message": "获取成功"}` |
| `/api/learning/record` | `POST` | 提交学习记录 | `user_id: int, word_id: int, mastery_level: int, is_marked: boolean` | `{"code": 0, "data": {}, "message": "提交成功"}` |
| `/api/learning/records` | `GET` | 获取学习记录 | `user_id: int, page: int, page_size: int` | `{"code": 0, "data": {"total": 100, "records": [{"record_id": 1, "word_id": 1, "word": "apple", "first_learned_at": "...", "last_reviewed_at": "...", "review_count": 1, "mastery_level": 1}]}, "message": "获取成功"}` |

#### 5.3.4 复习相关接口
| API路径 | 方法 | 功能描述 | 请求参数 | 成功响应 |
| :--- | :--- | :--- | :--- | :--- |
| `/api/review/list` | `GET` | 获取复习列表 | `user_id: int, count: int` | `{"code": 0, "data": {"words": [{"word_id": 1, "word": "apple", "phonetic": "/ˈæpl/", "definition": "n. 苹果", "example": "...", "audio_url": "...", "review_count": 1, "mastery_level": 1}]}, "message": "获取成功"}` |
| `/api/review/record` | `POST` | 提交复习记录 | `user_id: int, word_id: int, mastery_level: int` | `{"code": 0, "data": {"next_review_at": "2023-01-04 12:00:00"}, "message": "提交成功"}` |
| `/api/review/stats` | `GET` | 获取复习统计 | `user_id: int` | `{"code": 0, "data": {"total_reviews": 100, "today_reviews": 20, "mastered_count": 80, "learning_count": 20}, "message": "获取成功"}` |

#### 5.3.5 测试相关接口
| API路径 | 方法 | 功能描述 | 请求参数 | 成功响应 |
| :--- | :--- | :--- | :--- | :--- |
| `/api/test/start` | `POST` | 开始测试 | `user_id: int, test_type: string, set_id: int, difficulty: int, count: int` | `{"code": 0, "data": {"test_id": 1, "questions": [{"question_id": 1, "word_id": 1, "question_type": "choice", "question_content": "Choose the correct meaning of 'apple':", "options": ["苹果", "香蕉", "橙子", "梨"], "correct_answer": "苹果"}]}, "message": "获取成功"}` |
| `/api/test/submit` | `POST` | 提交测试结果 | `user_id: int, test_id: int, answers: array` | `{"code": 0, "data": {"total_questions": 20, "correct_count": 15, "wrong_count": 5, "accuracy": 75, "time_used": 300, "wrong_words": [{"word_id": 5, "word": "banana", "definition": "n. 香蕉"}]}, "message": "提交成功"}` |
| `/api/test/records` | `GET` | 获取测试记录 | `user_id: int, page: int, page_size: int` | `{"code": 0, "data": {"total": 10, "records": [{"test_id": 1, "test_type": "choice", "test_date": "...", "total_questions": 20, "correct_count": 15, "accuracy": 75, "time_used": 300}]}, "message": "获取成功"}` |
| `/api/test/errors` | `GET` | 获取错题集 | `user_id: int, page: int, page_size: int` | `{"code": 0, "data": {"total": 20, "errors": [{"word_id": 5, "word": "banana", "definition": "n. 香蕉", "error_count": 2, "last_error_at": "..."}]}, "message": "获取成功"}` |

#### 5.3.6 单词查询与生词本接口（新增）
| API路径 | 方法 | 功能描述 | 请求参数 | 成功响应 |
| :--- | :--- | :--- | :--- | :--- |
| `/api/word/query` | `POST` | 查询单词（调用Ollama） | `user_id: int, word: string` | `{"code": 0, "data": {"word": "serendipity", "phonetic": "/ˌserənˈdɪpəti/", "definition": "意外发现珍奇事物的本领", "examples": [...], "word_formation": "...", "synonyms": [...], "antonyms": [...], "memory_tips": "...", "collocations": [...]}, "message": "查询成功"}` |
| `/api/word/query/cache` | `GET` | 获取查询缓存 | `user_id: int, word: string` | `{"code": 0, "data": {...}, "message": "获取成功"}` 或 `{"code": 404, "message": "缓存不存在"}` |
| `/api/word/history` | `GET` | 获取查询历史 | `user_id: int, page: int, page_size: int` | `{"code": 0, "data": {"total": 50, "history": [{"history_id": 1, "word": "serendipity", "is_added_to_book": true, "query_time": "..."}]}, "message": "获取成功"}` |
| `/api/word/history/clear` | `DELETE` | 清空查询历史 | `user_id: int` | `{"code": 0, "data": {}, "message": "清空成功"}` |
| `/api/vocab-book/add` | `POST` | 添加到生词本 | `user_id: int, word: string, phonetic: string, definition: string, english_definition: string, examples: array, word_formation: string, synonyms: array, antonyms: array, memory_tips: string, collocations: array` | `{"code": 0, "data": {"vocab_id": 1}, "message": "添加成功"}` |
| `/api/vocab-book/list` | `GET` | 获取生词本列表 | `user_id: int, page: int, page_size: int, sort_by: string, filter: string` | `{"code": 0, "data": {"total": 50, "words": [{"vocab_id": 1, "word": "serendipity", "phonetic": "/ˌserənˈdɪpəti/", "definition": "...", "mastery_level": 0, "review_count": 0, "created_at": "..."}]}, "message": "获取成功"}` |
| `/api/vocab-book/detail` | `GET` | 获取生词详情 | `user_id: int, vocab_id: int` | `{"code": 0, "data": {"vocab_id": 1, "word": "serendipity", ...}, "message": "获取成功"}` |
| `/api/vocab-book/update` | `PUT` | 更新生词信息 | `user_id: int, vocab_id: int, mastery_level: int, is_in_plan: boolean` | `{"code": 0, "data": {}, "message": "更新成功"}` |
| `/api/vocab-book/delete` | `DELETE` | 删除生词 | `user_id: int, vocab_id: int` | `{"code": 0, "data": {}, "message": "删除成功"}` |
| `/api/vocab-book/batch-delete` | `DELETE` | 批量删除生词 | `user_id: int, vocab_ids: array` | `{"code": 0, "data": {"deleted_count": 5}, "message": "批量删除成功"}` |
| `/api/vocab-book/stats` | `GET` | 获取生词本统计 | `user_id: int` | `{"code": 0, "data": {"total_count": 50, "today_added": 3, "mastered_count": 20, "review_due_count": 10}, "message": "获取成功"}` |
| `/api/vocab-book/review/list` | `GET` | 获取生词本复习列表 | `user_id: int, count: int` | `{"code": 0, "data": {"words": [{"vocab_id": 1, "word": "serendipity", ...}]}, "message": "获取成功"}` |
| `/api/vocab-book/review/record` | `POST` | 提交生词复习记录 | `user_id: int, vocab_id: int, mastery_level: int` | `{"code": 0, "data": {"next_review_at": "2023-01-04 12:00:00"}, "message": "提交成功"}` |

### 5.4 Ollama服务集成

#### 5.4.1 Ollama服务配置
```python
# config.py
OLLAMA_CONFIG = {
    "base_url": "http://localhost:11434",  # Ollama服务地址
    "model": "qwen3:0.6b",  # 使用的模型
    "timeout": 30,  # 请求超时时间（秒）
    "max_retries": 3,  # 最大重试次数
    "temperature": 0.7,  # 生成文本的随机性
}

# 查询缓存配置
QUERY_CACHE_CONFIG = {
    "enabled": True,
    "ttl": 86400,  # 缓存有效期（秒），24小时
    "max_size": 1000  # 最大缓存条目数
}
```

#### 5.4.2 Ollama调用示例
```python
import requests
import json
from typing import Dict, Any

class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen3:0.6b"):
        self.base_url = base_url
        self.model = model
        self.api_endpoint = f"{base_url}/api/generate"
    
    def query_word(self, word: str) -> Dict[str, Any]:
        """
        查询单词解释
        
        Args:
            word: 要查询的英文单词
            
        Returns:
            包含单词详细信息的字典
        """
        prompt = self._build_prompt(word)
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 500
            }
        }
        
        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return self._parse_response(result["response"])
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama服务调用失败: {str(e)}")
    
    def _build_prompt(self, word: str) -> str:
        """构建查询Prompt"""
        return f"""请详细解释英文单词'{word}'，请以JSON格式返回以下信息：
{{
    "word": "单词拼写",
    "phonetic": "音标",
    "part_of_speech": "词性",
    "definition": "中文释义（详细）",
    "english_definition": "英文释义（简洁）",
    "examples": [
        {{"sentence": "例句1", "translation": "翻译1"}},
        {{"sentence": "例句2", "translation": "翻译2"}},
        {{"sentence": "例句3", "translation": "翻译3"}}
    ],
    "word_formation": "词根词缀分析",
    "synonyms": ["同义词1", "同义词2"],
    "antonyms": ["反义词1", "反义词2"],
    "memory_tips": "记忆技巧",
    "collocations": ["搭配1", "搭配2", "搭配3"]
}}
请确保返回的是有效的JSON格式。"""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """解析Ollama响应"""
        try:
            # 尝试直接解析JSON
            return json.loads(response_text)
        except json.JSONDecodeError:
            # 如果直接解析失败，尝试提取JSON部分
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise Exception("无法解析Ollama响应")
```

### 5.5 数据库设计
#### 5.5.1 数据库初始化脚本（包含新增表）
```sql
-- 创建用户信息表
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    openid VARCHAR(100) UNIQUE NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    avatar_url VARCHAR(255),
    gender INTEGER,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建词库表
CREATE TABLE IF NOT EXISTS vocabulary_sets (
    set_id INTEGER PRIMARY KEY AUTOINCREMENT,
    set_name VARCHAR(50) NOT NULL,
    description TEXT,
    level INTEGER,
    word_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 创建单词库表
CREATE TABLE IF NOT EXISTS word_library (
    word_id INTEGER PRIMARY KEY AUTOINCREMENT,
    word VARCHAR(50) NOT NULL,
    phonetic VARCHAR(100),
    definition TEXT NOT NULL,
    example TEXT,
    audio_url VARCHAR(255),
    set_id INTEGER,
    difficulty INTEGER,
    FOREIGN KEY (set_id) REFERENCES vocabulary_sets(set_id)
);

-- 创建学习记录表
CREATE TABLE IF NOT EXISTS learning_records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    word_id INTEGER,
    first_learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_reviewed_at TIMESTAMP,
    next_review_at TIMESTAMP,
    review_count INTEGER DEFAULT 0,
    mastery_level INTEGER DEFAULT 0,
    is_marked BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (word_id) REFERENCES word_library(word_id)
);

-- 创建测试记录表
CREATE TABLE IF NOT EXISTS test_records (
    test_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    test_type VARCHAR(20) NOT NULL,
    test_scope VARCHAR(100),
    difficulty INTEGER,
    total_questions INTEGER NOT NULL,
    correct_count INTEGER NOT NULL,
    wrong_count INTEGER NOT NULL,
    time_used INTEGER,
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 创建测试题目表
CREATE TABLE IF NOT EXISTS test_questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER,
    word_id INTEGER,
    question_type VARCHAR(20) NOT NULL,
    question_content TEXT NOT NULL,
    options TEXT,
    correct_answer TEXT NOT NULL,
    user_answer TEXT,
    is_correct BOOLEAN,
    FOREIGN KEY (test_id) REFERENCES test_records(test_id),
    FOREIGN KEY (word_id) REFERENCES word_library(word_id)
);

-- 创建用户词库关联表
CREATE TABLE IF NOT EXISTS user_vocabulary_sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    set_id INTEGER,
    progress INTEGER DEFAULT 0,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (set_id) REFERENCES vocabulary_sets(set_id)
);

-- 创建用户设置表
CREATE TABLE IF NOT EXISTS user_settings (
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    daily_target INTEGER DEFAULT 20,
    review_reminder BOOLEAN DEFAULT TRUE,
    reminder_time TIME,
    theme VARCHAR(20) DEFAULT 'light',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 创建生词本表（新增）
CREATE TABLE IF NOT EXISTS user_vocabulary_book (
    vocab_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word VARCHAR(50) NOT NULL,
    phonetic VARCHAR(100),
    definition TEXT NOT NULL,
    english_definition TEXT,
    examples TEXT,  -- JSON格式
    word_formation TEXT,
    synonyms TEXT,  -- JSON格式
    antonyms TEXT,  -- JSON格式
    memory_tips TEXT,
    collocations TEXT,  -- JSON格式
    source VARCHAR(20) DEFAULT 'ollama',
    ai_raw_response TEXT,
    mastery_level INTEGER DEFAULT 0,
    review_count INTEGER DEFAULT 0,
    last_reviewed_at TIMESTAMP,
    next_review_at TIMESTAMP,
    is_in_plan BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(user_id, word)
);

-- 创建查询历史表（新增）
CREATE TABLE IF NOT EXISTS query_history (
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word VARCHAR(50) NOT NULL,
    query_result TEXT,
    is_added_to_book BOOLEAN DEFAULT FALSE,
    vocab_id INTEGER,
    query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (vocab_id) REFERENCES user_vocabulary_book(vocab_id)
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_learning_records_user_id ON learning_records(user_id);
CREATE INDEX IF NOT EXISTS idx_learning_records_word_id ON learning_records(word_id);
CREATE INDEX IF NOT EXISTS idx_learning_records_next_review ON learning_records(next_review_at);
CREATE INDEX IF NOT EXISTS idx_test_records_user_id ON test_records(user_id);
CREATE INDEX IF NOT EXISTS idx_user_vocabulary_sets_user_id ON user_vocabulary_sets(user_id);
CREATE INDEX IF NOT EXISTS idx_user_vocabulary_sets_set_id ON user_vocabulary_sets(set_id);
CREATE INDEX IF NOT EXISTS idx_word_library_set_id ON word_library(set_id);

-- 新增索引
CREATE INDEX IF NOT EXISTS idx_user_vocabulary_book_user_id ON user_vocabulary_book(user_id);
CREATE INDEX IF NOT EXISTS idx_user_vocabulary_book_word ON user_vocabulary_book(word);
CREATE INDEX IF NOT EXISTS idx_user_vocabulary_book_next_review ON user_vocabulary_book(next_review_at);
CREATE INDEX IF NOT EXISTS idx_query_history_user_id ON query_history(user_id);
CREATE INDEX IF NOT EXISTS idx_query_history_word ON query_history(word);
```

---

## 6. 性能与安全要求

### 6.1 性能要求
- **响应速度**：页面加载时间不超过2秒，API接口响应时间不超过500毫秒，**Ollama查询响应时间不超过30秒**
- **并发处理**：支持至少1000个并发用户同时使用，**Ollama服务支持至少10个并发查询**
- **数据缓存**：对常用数据（如词库列表、单词信息）进行缓存，减少数据库查询；**Ollama查询结果缓存24小时**
- **离线功能**：支持基本的离线学习功能，在无网络情况下仍可进行单词学习和复习
- **AI查询优化**：实现查询队列和限流机制，防止Ollama服务过载

### 6.2 安全要求
- **数据加密**：用户敏感数据（如手机号）进行加密存储
- **API安全**：API接口采用token认证机制，防止未授权访问
- **防SQL注入**：所有数据库操作使用参数化查询，防止SQL注入攻击
- **防XSS攻击**：对用户输入进行过滤和转义，防止XSS攻击
- **用户隐私保护**：严格遵守微信小程序用户隐私保护规范，不收集和存储不必要的用户信息
- **数据备份**：定期对数据库进行备份，防止数据丢失
- **AI服务安全**：Ollama服务仅允许本地访问，不暴露到公网

### 6.3 可靠性要求
- **错误处理**：完善的错误处理机制，确保系统在遇到异常时能够正常运行
- **日志记录**：详细的日志记录，便于问题排查和系统监控
- **容灾方案**：制定容灾方案，确保系统在遇到故障时能够快速恢复
- **AI服务降级**：Ollama服务不可用时，提供友好的错误提示，并允许用户手动添加单词到生词本

---

## 7. 开发与测试环境规范

### 7.1 开发环境
- **操作系统**：Windows 10/11
- **开发工具**：
  - 微信开发者工具（最新版本）
  - Python IDE（如PyCharm、VS Code）
  - SQLite3数据库工具（如DB Browser for SQLite）
- **Python版本**：3.8+
- **Ollama环境**：
  - Ollama版本：最新版
  - 模型：qwen3:0.6b
  - 安装命令：`ollama pull qwen3:0.6b`
- **依赖包**：
  - Flask/FastAPI
  - SQLAlchemy
  - PyJWT
  - WeChatpy
  - Requests
  - 其他必要的Python包

### 7.2 Ollama服务部署
```bash
# 1. 安装Ollama
# Windows: 下载安装包从 https://ollama.com/download

# 2. 拉取模型
ollama pull qwen3:0.6b

# 3. 启动服务（默认监听11434端口）
ollama serve

# 4. 测试服务
curl http://localhost:11434/api/generate -d '{
  "model": "qwen3:0.6b",
  "prompt": "解释单词hello",
  "stream": false
}'
```

### 7.3 测试环境
- **测试设备**：
  - iOS设备（至少2台，不同版本）
  - Android设备（至少2台，不同版本）
  - 微信开发者工具模拟器
- **测试网络**：
  - WiFi网络
  - 4G/5G移动网络
  - 弱网络环境
- **测试工具**：
  - 微信开发者工具调试工具
  - Postman（API接口测试）
  - 性能测试工具（如JMeter）
- **AI功能测试**：
  - 测试Ollama服务的可用性
  - 测试各种类型单词的查询（简单词、复杂词、专业词）
  - 测试查询结果的准确性和完整性
  - 测试缓存机制
  - 测试错误处理和降级方案

### 7.4 部署环境
- **服务器**：
  - 云服务器（如腾讯云、阿里云）
  - 配置：至少2核4G内存，50G存储空间
- **操作系统**：Linux（Ubuntu 20.04+）
- **Web服务器**：Nginx
- **应用服务器**：Gunicorn/uWSGI
- **数据库**：SQLite3（生产环境可考虑升级为PostgreSQL）
- **Ollama部署**：
  - 与后端服务部署在同一服务器
  - 配置防火墙，仅允许本地访问
  - 设置服务自启动

### 7.5 代码规范
- **前端代码**：
  - 遵循微信小程序代码规范
  - 使用ES6+语法
  - 代码缩进统一为2空格
  - 变量命名采用驼峰命名法
- **后端代码**：
  - 遵循PEP 8代码规范
  - 使用Type Hints
  - 代码缩进统一为4空格
  - 函数命名采用小写字母加下划线
- **数据库规范**：
  - 表名和字段名采用小写字母加下划线
  - 使用索引优化查询性能
  - 避免使用复杂的SQL语句

---

## 8. 项目实施计划及里程碑

### 8.1 项目实施计划
| 阶段 | 时间 | 任务内容 | 负责人 |
| :--- | :--- | :--- | :--- |
| **需求分析与设计** | 第1-2周 | 需求分析、系统设计、数据库设计、UI设计 | 产品经理、UI设计师、后端开发 |
| **Ollama环境搭建** | 第2周 | 部署Ollama服务、测试模型效果、优化Prompt | 后端开发 |
| **前端开发** | 第3-6周 | 微信小程序框架搭建、页面开发、交互实现、接口对接 | 前端开发 |
| **后端开发** | 第3-6周 | 后端服务搭建、API接口开发、数据库实现、业务逻辑实现、**Ollama集成** | 后端开发 |
| **测试阶段** | 第7-8周 | 单元测试、集成测试、功能测试、性能测试、安全测试、**AI功能测试** | 测试工程师 |
| **上线准备** | 第9周 | 应用审核、服务器部署、数据初始化、运营准备 | 全团队 |
| **正式上线** | 第10周 | 应用发布、用户反馈收集、问题修复 | 全团队 |
| **运营与迭代** | 持续进行 | 用户数据分析、功能优化、新功能开发 | 全团队 |

### 8.2 里程碑
- **里程碑1**：需求分析与设计完成（第2周末）
  - 完成需求文档
  - 完成系统设计文档
  - 完成数据库设计文档
  - 完成UI设计稿

- **里程碑2**：Ollama环境搭建完成（第2周末）
  - Ollama服务部署成功
  - qwen3:0.6b模型下载完成
  - 单词查询功能测试通过
  - Prompt优化完成

- **里程碑3**：前端开发完成（第6周末）
  - 完成微信小程序所有页面开发
  - 完成所有交互功能实现
  - 完成与后端API的对接

- **里程碑4**：后端开发完成（第6周末）
  - 完成后端服务搭建
  - 完成所有API接口开发
  - 完成数据库实现
  - 完成业务逻辑实现
  - **完成Ollama服务集成**

- **里程碑5**：测试完成（第8周末）
  - 完成所有测试用例
  - 修复所有测试发现的问题
  - 性能测试通过
  - 安全测试通过
  - **AI功能测试通过**

- **里程碑6**：应用上线（第10周末）
  - 微信小程序审核通过
  - 服务器部署完成
  - Ollama服务部署完成
  - 应用正式发布
  - 运营活动准备就绪

---

## 9. 总结

本需求文档详细描述了微信小程序背单词项目的背景、目标、功能模块、用户界面设计、数据结构设计、技术架构、性能与安全要求、开发与测试环境规范以及项目实施计划。文档明确了各功能模块的详细需求、交互流程、数据字段定义及业务规则，为后续开发工作提供了清晰、可执行的指导依据。

### 9.1 核心亮点
1. **智能单词查询**：集成本地Ollama大模型，为用户提供详细的单词解释，包括词根词缀、记忆技巧等
2. **个人生词本**：支持用户自定义添加单词，建立个人化的学习词库
3. **AI辅助学习**：利用AI技术提供更丰富、更个性化的单词学习体验
4. **完整的复习体系**：结合记忆曲线算法，确保学习效果

### 9.2 技术特色
1. **本地AI部署**：使用Ollama本地部署大模型，保护用户隐私，降低使用成本
2. **缓存机制**：智能缓存AI查询结果，提高响应速度，减少模型调用
3. **离线支持**：支持基本的离线学习功能，提升用户体验

### 9.3 后续优化方向
1. 支持更多AI模型选择
2. 增加AI生成个性化学习计划功能
3. 增加AI智能纠错功能
4. 支持生词本导入导出
5. 增加学习社区功能，支持用户分享生词本

项目团队应严格按照本需求文档的要求进行开发，确保项目按时、按质、按量完成。同时，在开发过程中，应根据实际情况对需求进行合理的调整和优化，以确保最终产品能够满足用户的需求和期望。

通过本项目的实施，我们将为用户提供一款高效、科学、个性化的背单词工具，结合AI技术为用户提供更智能、更便捷的单词学习体验，帮助用户快速积累词汇量，提高英语水平。

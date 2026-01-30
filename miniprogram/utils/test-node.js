/**
 * 前端API测试脚本 (Node.js原生版本)
 * 用于验证前后端联调
 */

const http = require('http');

const BASE_URL = 'localhost';
const PORT = 5000;

// 封装请求方法
const request = (method, path, data = null) => {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: BASE_URL,
      port: PORT,
      path: path,
      method: method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const req = http.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        try {
          const parsedData = JSON.parse(responseData);
          resolve(parsedData);
        } catch (e) {
          reject(new Error('解析响应失败'));
        }
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    if (data) {
      req.write(JSON.stringify(data));
    }

    req.end();
  });
};

// API方法
const api = {
  healthCheck: () => request('GET', '/api/health'),
  login: (openid, nickname, avatarUrl) => request('POST', '/api/user/login', {
    openid, nickname, avatar_url: avatarUrl
  }),
  getUserInfo: (userId) => request('GET', `/api/user/info?user_id=${userId}`),
  getUserStats: (userId) => request('GET', `/api/user/stats?user_id=${userId}`),
  queryWord: (userId, word, useCache = true) => request('POST', '/api/word/query', {
    user_id: userId, word, use_cache: useCache
  }),
  getHistory: (userId) => request('GET', `/api/word/history?user_id=${userId}`),
  addToVocabBook: (userId, wordData) => request('POST', '/api/vocab-book/add', {
    user_id: userId, ...wordData
  }),
  getVocabList: (userId) => request('GET', `/api/vocab-book/list?user_id=${userId}`),
  getVocabDetail: (userId, vocabId) => request('GET', `/api/vocab-book/detail?user_id=${userId}&vocab_id=${vocabId}`),
  updateVocab: (userId, vocabId, data) => request('PUT', '/api/vocab-book/update', {
    user_id: userId, vocab_id: vocabId, ...data
  }),
  deleteVocab: (userId, vocabId) => request('DELETE', '/api/vocab-book/delete', {
    user_id: userId, vocab_id: vocabId
  }),
  getVocabStats: (userId) => request('GET', `/api/vocab-book/stats?user_id=${userId}`),
  checkWordExists: (userId, word) => request('GET', `/api/vocab-book/check-exists?user_id=${userId}&word=${encodeURIComponent(word)}`)
};

/**
 * 测试函数
 */
const runTests = async () => {
  console.log('=== 微信小程序前端API测试 (Node.js) ===\n');

  let userId = null;
  let vocabId = null;

  // 1. 健康检查
  console.log('1. 测试健康检查...');
  try {
    const result = await api.healthCheck();
    console.log('✓ 健康检查通过');
    console.log('  服务状态:', result.data.status);
    console.log('  Ollama状态:', result.data.ollama_available ? '在线' : '离线');
  } catch (error) {
    console.log('✗ 健康检查失败');
    console.log('  请确保后端服务已启动: python app.py');
    console.log('  错误:', error.message);
    return;
  }

  // 2. 用户登录
  console.log('\n2. 测试用户登录...');
  try {
    const result = await api.login('test_openid_frontend', '前端测试用户', '');
    userId = result.data.user_id;
    console.log('✓ 登录成功');
    console.log('  用户ID:', userId);
    console.log('  昵称:', result.data.nickname);
  } catch (error) {
    console.log('✗ 登录失败:', error.message);
    return;
  }

  // 3. 获取用户信息
  console.log('\n3. 测试获取用户信息...');
  try {
    const result = await api.getUserInfo(userId);
    console.log('✓ 获取用户信息成功');
    console.log('  用户:', result.data.nickname);
  } catch (error) {
    console.log('✗ 获取用户信息失败:', error.message);
  }

  // 4. 查询单词
  console.log('\n4. 测试查询单词...');
  try {
    const result = await api.queryWord(userId, 'hello', true);
    console.log('✓ 查询成功');
    console.log('  单词:', result.data.word);
    console.log('  音标:', result.data.phonetic);
    console.log('  释义:', result.data.definition.substring(0, 30) + '...');
    console.log('  来自缓存:', result.data.from_cache);
  } catch (error) {
    console.log('✗ 查询失败:', error.message);
  }

  // 5. 获取查询历史
  console.log('\n5. 测试获取查询历史...');
  try {
    const result = await api.getHistory(userId);
    console.log('✓ 获取历史成功');
    console.log('  历史记录数:', result.data.total);
  } catch (error) {
    console.log('✗ 获取历史失败:', error.message);
  }

  // 6. 添加到生词本
  console.log('\n6. 测试添加到生词本...');
  try {
    const wordData = {
      word: 'frontend',
      phonetic: '/ˈfrʌntend/',
      definition: '前端，用户界面',
      english_definition: 'The part of a software system that users interact with',
      examples: [
        { sentence: 'He works as a frontend developer.', translation: '他是一名前端开发工程师。' }
      ],
      memory_tips: 'front(前面) + end(端) = 前端'
    };
    const result = await api.addToVocabBook(userId, wordData);
    vocabId = result.data.vocab_id;
    console.log('✓ 添加成功');
    console.log('  生词ID:', vocabId);
  } catch (error) {
    console.log('✗ 添加失败:', error.message);
  }

  // 7. 获取生词本列表
  console.log('\n7. 测试获取生词本列表...');
  try {
    const result = await api.getVocabList(userId);
    console.log('✓ 获取列表成功');
    console.log('  生词数量:', result.data.total);
  } catch (error) {
    console.log('✗ 获取列表失败:', error.message);
  }

  // 8. 获取生词详情
  console.log('\n8. 测试获取生词详情...');
  if (vocabId) {
    try {
      const result = await api.getVocabDetail(userId, vocabId);
      console.log('✓ 获取详情成功');
      console.log('  单词:', result.data.word);
      console.log('  状态:', result.data.status_text);
    } catch (error) {
      console.log('✗ 获取详情失败:', error.message);
    }
  }

  // 9. 更新生词状态
  console.log('\n9. 测试更新生词状态...');
  if (vocabId) {
    try {
      await api.updateVocab(userId, vocabId, { status: 1 });
      console.log('✓ 更新状态成功');
    } catch (error) {
      console.log('✗ 更新状态失败:', error.message);
    }
  }

  // 10. 获取生词本统计
  console.log('\n10. 测试获取生词本统计...');
  try {
    const result = await api.getVocabStats(userId);
    console.log('✓ 获取统计成功');
    console.log('  总数:', result.data.total_count);
    console.log('  未学习:', result.data.new_count);
    console.log('  学习中:', result.data.learning_count);
    console.log('  已掌握:', result.data.mastered_count);
  } catch (error) {
    console.log('✗ 获取统计失败:', error.message);
  }

  // 11. 检查单词是否存在
  console.log('\n11. 测试检查单词是否存在...');
  try {
    const result = await api.checkWordExists(userId, 'frontend');
    console.log('✓ 检查成功');
    console.log('  是否存在:', result.data.exists);
  } catch (error) {
    console.log('✗ 检查失败:', error.message);
  }

  // 12. 删除生词
  console.log('\n12. 测试删除生词...');
  if (vocabId) {
    try {
      await api.deleteVocab(userId, vocabId);
      console.log('✓ 删除成功');
    } catch (error) {
      console.log('✗ 删除失败:', error.message);
    }
  }

  // 13. 获取用户统计
  console.log('\n13. 测试获取用户统计...');
  try {
    const result = await api.getUserStats(userId);
    console.log('✓ 获取统计成功');
    console.log('  总查询:', result.data.total_queries);
    console.log('  生词数:', result.data.vocab_count);
    console.log('  今日查询:', result.data.today_queries);
  } catch (error) {
    console.log('✗ 获取统计失败:', error.message);
  }

  console.log('\n========================================');
  console.log('✅ 前后端联调测试完成！');
  console.log('========================================');
  console.log('\n前端页面文件已创建:');
  console.log('  📄 pages/index/index (查词页面)');
  console.log('  📄 pages/vocab-book/vocab-book (生词本页面)');
  console.log('  📄 pages/profile/profile (个人中心)');
  console.log('  📄 pages/vocab-detail/vocab-detail (生词详情)');
  console.log('\n请使用微信开发者工具打开 miniprogram 目录进行预览');
  console.log('\n使用说明:');
  console.log('  1. 确保后端服务已启动: python app.py');
  console.log('  2. 打开微信开发者工具');
  console.log('  3. 导入项目: miniprogram 目录');
  console.log('  4. 在详情设置中勾选 "不校验合法域名"');
  console.log('  5. 编译预览');
};

// 运行测试
runTests().catch(console.error);

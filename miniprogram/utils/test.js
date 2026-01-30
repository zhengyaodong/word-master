/**
 * 前端API测试脚本
 * 用于验证前后端联调
 */

const { userApi, wordApi, vocabBookApi, healthCheck } = require('./api');

/**
 * 测试函数
 */
const runTests = async () => {
  console.log('=== 微信小程序前端API测试 ===\n');

  let userId = null;
  let vocabId = null;

  // 1. 健康检查
  console.log('1. 测试健康检查...');
  try {
    const result = await healthCheck();
    console.log('✓ 健康检查通过');
    console.log('  Ollama状态:', result.data.ollama_available ? '在线' : '离线');
  } catch (error) {
    console.log('✗ 健康检查失败:', error);
    return;
  }

  // 2. 用户登录
  console.log('\n2. 测试用户登录...');
  try {
    const result = await userApi.login('test_openid_frontend', '前端测试用户', '');
    userId = result.data.user_id;
    console.log('✓ 登录成功');
    console.log('  用户ID:', userId);
    console.log('  昵称:', result.data.nickname);
  } catch (error) {
    console.log('✗ 登录失败:', error);
    return;
  }

  // 3. 获取用户信息
  console.log('\n3. 测试获取用户信息...');
  try {
    const result = await userApi.getInfo(userId);
    console.log('✓ 获取用户信息成功');
    console.log('  用户:', result.data.nickname);
  } catch (error) {
    console.log('✗ 获取用户信息失败:', error);
  }

  // 4. 查询单词
  console.log('\n4. 测试查询单词...');
  try {
    const result = await wordApi.query(userId, 'hello', true);
    console.log('✓ 查询成功');
    console.log('  单词:', result.data.word);
    console.log('  音标:', result.data.phonetic);
    console.log('  释义:', result.data.definition.substring(0, 30) + '...');
  } catch (error) {
    console.log('✗ 查询失败:', error.message || error);
  }

  // 5. 获取查询历史
  console.log('\n5. 测试获取查询历史...');
  try {
    const result = await wordApi.getHistory(userId);
    console.log('✓ 获取历史成功');
    console.log('  历史记录数:', result.data.total);
  } catch (error) {
    console.log('✗ 获取历史失败:', error);
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
    const result = await vocabBookApi.add(userId, wordData);
    vocabId = result.data.vocab_id;
    console.log('✓ 添加成功');
    console.log('  生词ID:', vocabId);
  } catch (error) {
    console.log('✗ 添加失败:', error);
  }

  // 7. 获取生词本列表
  console.log('\n7. 测试获取生词本列表...');
  try {
    const result = await vocabBookApi.getList(userId);
    console.log('✓ 获取列表成功');
    console.log('  生词数量:', result.data.total);
  } catch (error) {
    console.log('✗ 获取列表失败:', error);
  }

  // 8. 获取生词详情
  console.log('\n8. 测试获取生词详情...');
  if (vocabId) {
    try {
      const result = await vocabBookApi.getDetail(userId, vocabId);
      console.log('✓ 获取详情成功');
      console.log('  单词:', result.data.word);
    } catch (error) {
      console.log('✗ 获取详情失败:', error);
    }
  }

  // 9. 更新生词状态
  console.log('\n9. 测试更新生词状态...');
  if (vocabId) {
    try {
      await vocabBookApi.update(userId, vocabId, { status: 1 });
      console.log('✓ 更新状态成功');
    } catch (error) {
      console.log('✗ 更新状态失败:', error);
    }
  }

  // 10. 获取生词本统计
  console.log('\n10. 测试获取生词本统计...');
  try {
    const result = await vocabBookApi.getStats(userId);
    console.log('✓ 获取统计成功');
    console.log('  总数:', result.data.total_count);
    console.log('  已掌握:', result.data.mastered_count);
  } catch (error) {
    console.log('✗ 获取统计失败:', error);
  }

  // 11. 检查单词是否存在
  console.log('\n11. 测试检查单词是否存在...');
  try {
    const result = await vocabBookApi.checkExists(userId, 'frontend');
    console.log('✓ 检查成功');
    console.log('  是否存在:', result.data.exists);
  } catch (error) {
    console.log('✗ 检查失败:', error);
  }

  // 12. 删除生词
  console.log('\n12. 测试删除生词...');
  if (vocabId) {
    try {
      await vocabBookApi.delete(userId, vocabId);
      console.log('✓ 删除成功');
    } catch (error) {
      console.log('✗ 删除失败:', error);
    }
  }

  // 13. 获取用户统计
  console.log('\n13. 测试获取用户统计...');
  try {
    const result = await userApi.getStats(userId);
    console.log('✓ 获取统计成功');
    console.log('  总查询:', result.data.total_queries);
    console.log('  生词数:', result.data.vocab_count);
  } catch (error) {
    console.log('✗ 获取统计失败:', error);
  }

  console.log('\n=== 测试完成 ===');
};

// 运行测试
runTests().catch(console.error);

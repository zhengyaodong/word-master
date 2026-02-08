// 个人中心页面
import { userApi, healthCheck } from '../../utils/api';

const app = getApp<IAppOption>();

Page({
  data: {
    userInfo: {
      userId: 0,
      nickname: '',
      avatarUrl: '',
      createdAt: ''
    },
    stats: {
      total_queries: 0,
      vocab_count: 0,
      today_queries: 0,
      consecutive_days: 0  // V2.0: 连续打卡天数
    },
    ollamaStatus: false,
    loading: false
  },

  onLoad() {
    this.loadUserInfo();
  },

  onShow() {
    if (this.data.userInfo.userId) {
      this.loadStats();
      this.checkService();
    }
  },

  // 加载用户信息
  loadUserInfo() {
    const userInfo = app.globalData.userInfo;
    if (userInfo && userInfo.userId) {
      this.setData({ userInfo });
      this.loadStats();
      this.checkService();
    } else {
      // 模拟登录（实际应该调用微信登录）
      this.mockLogin();
    }
  },

  // 模拟登录（开发测试用）
  async mockLogin() {
    try {
      console.log('[DEBUG] 开始登录...');
      // 使用测试openid
      const result = await userApi.login('test_openid_123', '测试用户', '');
      console.log('[DEBUG] 登录返回结果:', result);
      
      const data = result.data;
      // 将后端字段映射到前端字段（后端返回驼峰命名）
      const userInfo = {
        userId: data.userId,
        nickname: data.nickname,
        avatarUrl: data.avatarUrl,
        createdAt: data.createdAt
      };
      console.log('[DEBUG] 转换后的 userInfo:', userInfo);
      
      app.globalData.userInfo = userInfo;
      
      // 使用回调确保setData完成
      this.setData({ userInfo }, () => {
        console.log('[DEBUG] setData 完成, 当前 userInfo:', this.data.userInfo);
        this.loadStats();
        this.checkService();
      });
      
      wx.showToast({
        title: '登录成功',
        icon: 'success'
      });
    } catch (error) {
      console.error('登录失败:', error);
    }
  },

  // 加载统计
  async loadStats() {
    console.log('[DEBUG] loadStats 被调用, userInfo:', this.data.userInfo);
    try {
      const userId = this.data.userInfo.userId;
      console.log('[DEBUG] 准备获取统计, userId:', userId);
      if (!userId) {
        console.error('[DEBUG] userId 为空，跳过获取统计');
        return;
      }
      console.log('[DEBUG] 即将调用 userApi.getStats...');
      const result = await userApi.getStats(userId);
      console.log('[DEBUG] 获取统计成功, 结果:', result);
      this.setData({ stats: result.data });
    } catch (error) {
      console.error('[DEBUG] 加载统计失败:', error);
    }
  },

  // 检查服务状态
  async checkService() {
    try {
      const result = await healthCheck();
      this.setData({ ollamaStatus: result.data.ollama_available });
    } catch (error) {
      this.setData({ ollamaStatus: false });
    }
  },

  // 获取用户信息（微信授权）
  getUserProfile() {
    wx.getUserProfile({
      desc: '用于完善用户资料',
      success: (res) => {
        const { nickName, avatarUrl } = res.userInfo;
        this.updateUserInfo(nickName, avatarUrl);
      }
    });
  },

  // 更新用户信息
  async updateUserInfo(nickname: string, avatarUrl: string) {
    try {
      await userApi.update(this.data.userInfo.userId, {
        nickname,
        avatar_url: avatarUrl
      });
      
      const userInfo = { ...this.data.userInfo, nickname, avatarUrl };
      this.setData({ userInfo });
      app.globalData.userInfo = userInfo;
      
      wx.showToast({
        title: '更新成功',
        icon: 'success'
      });
    } catch (error) {
      console.error('更新失败:', error);
    }
  },

  // 跳转到生词本
  goToVocabBook() {
    wx.switchTab({
      url: '/pages/vocab-book/vocab-book'
    });
  },

  // 关于页面
  showAbout() {
    const content = [
      'AI智能背单词 v4.0.0',
      '',
      '使用本地Ollama大模型提供智能单词解释',
      '',
      'V2.0新增功能：',
      '- 学习统计',
      '- 语音朗读',
      '- 例句收藏',
      '- 学习打卡',
      '',
      'V3.0新增功能：',
      '- 批量导入与一键洗词',
      '- AI语境助记',
      '- 智能去重',
      '',
      'V4.0新增功能：',
      '- 内置词库（CET-4/CET-6）',
      '- 词库学习与进度追踪',
      '- SM-2间隔重复复习'
    ].join('\n');

    wx.showModal({
      title: '关于',
      content,
      showCancel: false
    });
  }
});

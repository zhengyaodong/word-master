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
      today_queries: 0
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
    if (userInfo) {
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
      // 使用测试openid
      const result = await userApi.login('test_openid_123', '测试用户', '');
      const userInfo = result.data;
      
      app.globalData.userInfo = userInfo;
      this.setData({ userInfo });
      
      this.loadStats();
      this.checkService();
      
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
    try {
      const result = await userApi.getStats(this.data.userInfo.userId);
      this.setData({ stats: result.data });
    } catch (error) {
      console.error('加载统计失败:', error);
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
    wx.showModal({
      title: '关于',
      content: 'AI智能背单词 v1.0.0\n\n使用本地Ollama大模型提供智能单词解释',
      showCancel: false
    });
  }
});

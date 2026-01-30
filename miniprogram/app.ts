// app.ts
import { userApi } from './utils/api';

App<IAppOption>({
  globalData: {
    userInfo: null as any
  },
  
  onLaunch() {
    // 展示本地存储能力
    const logs = wx.getStorageSync('logs') || [];
    logs.unshift(Date.now());
    wx.setStorageSync('logs', logs);

    // 尝试自动登录
    this.autoLogin();
  },

  // 自动登录
  async autoLogin() {
    try {
      // 开发环境使用测试账号
      // 生产环境应该使用 wx.login 获取 code，然后调用后端登录
      const result = await userApi.login('test_openid_123', '测试用户', '');
      this.globalData.userInfo = result.data;
      console.log('自动登录成功:', result.data);
    } catch (error) {
      console.error('自动登录失败:', error);
    }
  }
});

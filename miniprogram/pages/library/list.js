const { libraryApi } = require('../../utils/api');

const app = getApp();

Page({
  data: {
    libraries: [],
    loading: false,
    userId: 0
  },

  onLoad() {
    const userInfo = app.globalData.userInfo;
    if (userInfo && userInfo.userId) {
      this.setData({ userId: userInfo.userId });
      this.loadLibraries();
      return;
    }

    const checkLogin = setInterval(() => {
      const info = app.globalData.userInfo;
      if (info && info.userId) {
        this.setData({ userId: info.userId });
        this.loadLibraries();
        clearInterval(checkLogin);
      }
    }, 100);

    setTimeout(() => {
      clearInterval(checkLogin);
      if (!this.data.userId) {
        this.loadLibraries();
      }
    }, 10000);
  },

  async loadLibraries() {
    this.setData({ loading: true });
    try {
      const res = await libraryApi.list(this.data.userId);
      this.setData({ libraries: res.data.libraries || [] });
    } catch (error) {
      console.error('加载词库失败:', error);
      wx.showToast({ title: '加载失败', icon: 'none' });
    } finally {
      this.setData({ loading: false });
    }
  },

  async startLearning(e) {
    const libraryId = e.currentTarget.dataset.libraryId;
    const name = e.currentTarget.dataset.name || '';
    if (!this.data.userId) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    try {
      await libraryApi.start(this.data.userId, libraryId);
      wx.showToast({ title: '初始化完成', icon: 'success' });
      this.loadLibraries();
      wx.navigateTo({
        url: `/pages/library/learn?libraryId=${libraryId}&name=${encodeURIComponent(name)}`
      });
    } catch (error) {
      console.error('开始学习失败:', error);
    }
  },

  viewWords(e) {
    const libraryId = e.currentTarget.dataset.libraryId;
    const name = e.currentTarget.dataset.name || '';
    wx.navigateTo({
      url: `/pages/library/words?libraryId=${libraryId}&name=${encodeURIComponent(name)}`
    });
  },

  goReview(e) {
    const libraryId = e.currentTarget.dataset.libraryId;
    const name = e.currentTarget.dataset.name || '';
    wx.navigateTo({
      url: `/pages/library/review?libraryId=${libraryId}&name=${encodeURIComponent(name)}`
    });
  }
});

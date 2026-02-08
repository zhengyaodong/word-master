import { libraryApi } from '../../utils/api';

const app = getApp<IAppOption>();

Page({
  data: {
    libraryId: 0,
    libraryName: '',
    userId: 0,
    loading: false,
    words: [] as any[],
    currentIndex: 0,
    totalDue: 0,
    currentWord: null as any
  },

  onLoad(options: any) {
    const libraryId = parseInt(options.libraryId, 10);
    const name = options.name ? decodeURIComponent(options.name) : '';
    this.setData({ libraryId, libraryName: name });

    const userInfo = app.globalData.userInfo;
    if (userInfo && userInfo.userId) {
      this.setData({ userId: userInfo.userId });
      this.loadReview();
      return;
    }

    const checkLogin = setInterval(() => {
      const info = app.globalData.userInfo;
      if (info && info.userId) {
        this.setData({ userId: info.userId });
        this.loadReview();
        clearInterval(checkLogin);
      }
    }, 100);

    setTimeout(() => {
      clearInterval(checkLogin);
      if (!this.data.userId) {
        this.loadReview();
      }
    }, 10000);
  },

  async loadReview() {
    if (!this.data.userId) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    this.setData({ loading: true });
    try {
      const res = await libraryApi.getReview(this.data.userId, this.data.libraryId, 20);
      const words = res.data.words || [];
      this.setData({
        words,
        currentIndex: 0,
        totalDue: res.data.total_due || words.length,
        currentWord: words.length ? words[0] : null
      });
    } catch (error) {
      console.error('加载复习失败:', error);
      wx.showToast({ title: '加载失败', icon: 'none' });
    } finally {
      this.setData({ loading: false });
    }
  },

  async submitReview(e: any) {
    const quality = parseInt(e.currentTarget.dataset.quality, 10);
    const current = this.data.currentWord;
    if (!current) return;

    try {
      await libraryApi.submitReview(
        this.data.userId,
        this.data.libraryId,
        current.word_detail.word,
        quality
      );

      const nextIndex = this.data.currentIndex + 1;
      if (nextIndex >= this.data.words.length) {
        this.setData({ currentIndex: nextIndex, currentWord: null });
        wx.showToast({ title: '今日完成', icon: 'success' });
      } else {
        this.setData({
          currentIndex: nextIndex,
          currentWord: this.data.words[nextIndex]
        });
      }
    } catch (error) {
      console.error('提交复习失败:', error);
      wx.showToast({ title: '提交失败', icon: 'none' });
    }
  }
});

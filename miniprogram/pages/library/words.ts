import { libraryApi } from '../../utils/api';

const app = getApp<IAppOption>();

Page({
  data: {
    libraryId: 0,
    libraryName: '',
    userId: 0,
    words: [] as any[],
    total: 0,
    page: 1,
    pageSize: 50,
    loading: false,
    hasMore: true,
    statusFilter: 'all' as any
  },

  onLoad(options: any) {
    const libraryId = parseInt(options.libraryId, 10);
    const name = options.name ? decodeURIComponent(options.name) : '';
    this.setData({ libraryId, libraryName: name });

    const userInfo = app.globalData.userInfo;
    if (userInfo && userInfo.userId) {
      this.setData({ userId: userInfo.userId });
      this.loadWords(true);
      return;
    }

    const checkLogin = setInterval(() => {
      const info = app.globalData.userInfo;
      if (info && info.userId) {
        this.setData({ userId: info.userId });
        this.loadWords(true);
        clearInterval(checkLogin);
      }
    }, 100);

    setTimeout(() => {
      clearInterval(checkLogin);
      if (!this.data.userId) {
        this.loadWords(true);
      }
    }, 10000);
  },

  async loadWords(reset = false) {
    if (this.data.loading) return;
    if (!this.data.hasMore && !reset) return;

    this.setData({ loading: true });
    const page = reset ? 1 : this.data.page;
    const status =
      this.data.statusFilter === 'all' ? undefined : this.data.statusFilter;

    try {
      const res = await libraryApi.getWords({
        libraryId: this.data.libraryId,
        userId: this.data.userId,
        page,
        pageSize: this.data.pageSize,
        status
      });

      const data = res.data || {};
      const list = data.words || [];
      const total = data.total || 0;
      const merged = reset ? list : this.data.words.concat(list);
      const hasMore = merged.length < total;

      this.setData({
        words: merged,
        total,
        page: page + 1,
        hasMore
      });
    } catch (error) {
      console.error('加载词库单词失败:', error);
      wx.showToast({ title: '加载失败', icon: 'none' });
    } finally {
      this.setData({ loading: false });
    }
  },

  onReachBottom() {
    this.loadWords(false);
  },

  changeFilter(e: any) {
    const status = e.currentTarget.dataset.status;
    const parsed = status === 'all' ? 'all' : parseInt(status, 10);
    this.setData({ statusFilter: parsed, page: 1, hasMore: true, words: [] });
    this.loadWords(true);
  },

  async initLearning() {
    if (!this.data.userId) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    try {
      await libraryApi.start(this.data.userId, this.data.libraryId);
      wx.showToast({ title: '初始化完成', icon: 'success' });
      this.setData({ page: 1, hasMore: true, words: [] });
      this.loadWords(true);
    } catch (error) {
      console.error('初始化失败:', error);
    }
  },

  goReview() {
    const name = this.data.libraryName || '';
    wx.navigateTo({
      url: `/pages/library/review?libraryId=${this.data.libraryId}&name=${encodeURIComponent(name)}`
    });
  },

  async addToVocab(e: any) {
    if (!this.data.userId) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    const word = e.currentTarget.dataset.word;
    try {
      await libraryApi.addToVocab(this.data.userId, this.data.libraryId, word);
      wx.showToast({ title: '已加入生词本', icon: 'success' });
    } catch (error) {
      console.error('加入生词本失败:', error);
    }
  },

  async updateStatus(e: any) {
    if (!this.data.userId) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    const word = e.currentTarget.dataset.word;
    const status = parseInt(e.currentTarget.dataset.status, 10);
    try {
      await libraryApi.updateProgress(this.data.userId, this.data.libraryId, word, status);
      const words = this.data.words.map((item) => {
        if (item.word === word) {
          const progress = item.progress || {};
          const statusText = ['未学习', '学习中', '已掌握', '需复习'][status] || '未知';
          return { ...item, progress: { ...progress, status, status_text: statusText } };
        }
        return item;
      });
      this.setData({ words });
      wx.showToast({ title: '状态已更新', icon: 'success' });
    } catch (error) {
      console.error('更新状态失败:', error);
    }
  }
});

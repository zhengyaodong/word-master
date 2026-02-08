const { libraryApi } = require('../../utils/api');

const app = getApp();

Page({
  data: {
    libraryId: 0,
    libraryName: '',
    userId: 0,
    loading: false,
    words: [],
    total: 0,
    currentIndex: 0,
    currentWord: null,
    batchSize: 20
  },

  onLoad(options) {
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
    this.setData({ loading: true });

    try {
      const res = await libraryApi.getRandomWords(
        this.data.libraryId,
        this.data.userId,
        this.data.batchSize,
        true
      );

      const data = res.data || {};
      const list = data.words || [];
      const total = list.length;

      this.setData({
        words: list,
        total,
        currentIndex: 0,
        currentWord: list.length ? list[0] : null
      });
    } catch (error) {
      console.error('加载学习单词失败:', error);
      wx.showToast({ title: '加载失败', icon: 'none' });
    } finally {
      this.setData({ loading: false });
    }
  },

  async setStatus(e) {
    if (!this.data.userId || !this.data.currentWord) return;
    const status = parseInt(e.currentTarget.dataset.status, 10);
    const word = this.data.currentWord.word;
    try {
      await libraryApi.updateProgress(this.data.userId, this.data.libraryId, word, status);
      const statusText = ['未学习', '学习中', '已掌握', '需复习'][status] || '未知';
      const currentWord = {
        ...this.data.currentWord,
        progress: { ...(this.data.currentWord.progress || {}), status, status_text: statusText }
      };
      this.setData({ currentWord });
      wx.showToast({ title: '状态已更新', icon: 'success' });
    } catch (error) {
      console.error('更新状态失败:', error);
    }
  },

  async addToVocab() {
    if (!this.data.userId || !this.data.currentWord) return;
    try {
      await libraryApi.addToVocab(this.data.userId, this.data.libraryId, this.data.currentWord.word);
      wx.showToast({ title: '已加入生词本', icon: 'success' });
    } catch (error) {
      console.error('加入生词本失败:', error);
    }
  },

  async nextWord() {
    let nextIndex = this.data.currentIndex + 1;
    if (nextIndex < this.data.words.length) {
      this.setData({
        currentIndex: nextIndex,
        currentWord: this.data.words[nextIndex]
      });
    } else {
      this.setData({ currentWord: null });
    }
  }
});

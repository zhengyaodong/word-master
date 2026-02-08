// 批量导入页面
import { vocabBookApi } from '../../utils/api';

const app = getApp<IAppOption>();

Page({
  data: {
    inputText: '',
    useAi: true,
    maxWords: 50,
    cleaning: false,
    importing: false,
    words: [] as string[],
    selectedWords: [] as string[],
    selectedMap: {} as Record<string, boolean>,
    userId: 0
  },

  onLoad() {
    const userInfo = app.globalData.userInfo;
    if (userInfo && userInfo.userId) {
      this.setData({ userId: userInfo.userId });
      return;
    }

    const checkLogin = setInterval(() => {
      const info = app.globalData.userInfo;
      if (info && info.userId) {
        this.setData({ userId: info.userId });
        clearInterval(checkLogin);
      }
    }, 100);

    setTimeout(() => {
      clearInterval(checkLogin);
    }, 10000);
  },

  onInput(e: any) {
    this.setData({ inputText: e.detail.value });
  },

  onMaxChange(e: any) {
    const value = parseInt(e.detail.value, 10);
    this.setData({ maxWords: isNaN(value) ? 50 : value });
  },

  toggleAi(e: any) {
    this.setData({ useAi: e.detail.value });
  },

  clearInput() {
    this.setData({ inputText: '' });
  },

  async cleanWords() {
    const { inputText, useAi, maxWords, userId } = this.data;
    if (!userId) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    if (!inputText.trim()) {
      wx.showToast({ title: '请输入文本', icon: 'none' });
      return;
    }

    this.setData({ cleaning: true });
    try {
      const res = await vocabBookApi.cleanText(userId, inputText, maxWords, useAi);
      const words = res.data.words || [];
      const selectedMap: Record<string, boolean> = {};
      words.forEach((w) => { selectedMap[w] = true; });
      this.setData({ words, selectedWords: words, selectedMap });
      wx.showToast({ title: `提取 ${words.length} 个`, icon: 'success' });
    } catch (error) {
      console.error('洗词失败:', error);
    } finally {
      this.setData({ cleaning: false });
    }
  },

  toggleWord(e: any) {
    const word = e.currentTarget.dataset.word;
    const selectedMap = { ...this.data.selectedMap };
    selectedMap[word] = !selectedMap[word];
    const selectedWords = Object.keys(selectedMap).filter((w) => selectedMap[w]);
    this.setData({ selectedMap, selectedWords });
  },

  selectAll() {
    const selectedMap: Record<string, boolean> = {};
    this.data.words.forEach((w) => { selectedMap[w] = true; });
    this.setData({ selectedWords: [...this.data.words], selectedMap });
  },

  clearSelection() {
    this.setData({ selectedWords: [], selectedMap: {} });
  },

  async importWords() {
    const { userId, selectedWords, inputText } = this.data;
    if (!userId) {
      wx.showToast({ title: '请先登录', icon: 'none' });
      return;
    }
    if (!selectedWords.length) {
      wx.showToast({ title: '请选择单词', icon: 'none' });
      return;
    }

    this.setData({ importing: true });
    try {
      const res = await vocabBookApi.importBatch(userId, selectedWords, 'paste', inputText);
      const data = res.data || {};
      wx.showToast({
        title: `导入${data.added_count || 0}个`,
        icon: 'success'
      });
    } catch (error) {
      console.error('导入失败:', error);
    } finally {
      this.setData({ importing: false });
    }
  }
});

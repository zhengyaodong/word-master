// 查词页面逻辑
import { wordApi, vocabBookApi } from '../../utils/api';

// 获取全局app实例
const app = getApp<IAppOption>();

Page({
  data: {
    inputWord: '',
    isLoading: false,
    queryResult: null as any,
    history: [] as any[],
    isInVocabBook: false,
    userId: 0
  },

  onLoad() {
    // 从全局获取用户信息
    const userInfo = app.globalData.userInfo;
    if (userInfo && userInfo.userId) {
      this.setData({ userId: userInfo.userId });
      this.loadHistory();
    } else {
      // 等待自动登录完成
      const checkLogin = setInterval(() => {
        const userInfo = app.globalData.userInfo;
        if (userInfo && userInfo.userId) {
          this.setData({ userId: userInfo.userId });
          this.loadHistory();
          clearInterval(checkLogin);
        }
      }, 100);
      
      // 5秒后停止检查
      setTimeout(() => {
        clearInterval(checkLogin);
      }, 5000);
    }
  },

  onShow() {
    // 页面显示时刷新历史记录
    if (this.data.userId) {
      this.loadHistory();
    }
  },

  // 输入框变化
  onInputChange(e: any) {
    this.setData({
      inputWord: e.detail.value
    });
  },

  // 执行查询
  async onSearch() {
    const word = this.data.inputWord.trim();
    
    if (!word) {
      wx.showToast({
        title: '请输入单词',
        icon: 'none'
      });
      return;
    }

    // 验证单词格式
    if (!/^[a-zA-Z]+$/.test(word)) {
      wx.showToast({
        title: '只能输入英文字母',
        icon: 'none'
      });
      return;
    }

    this.setData({ isLoading: true });

    try {
      const result = await wordApi.query(this.data.userId, word.toLowerCase());
      
      this.setData({
        queryResult: result.data,
        isLoading: false
      });

      // 检查是否已在生词本
      this.checkIfInVocabBook(word);

      // 刷新历史记录
      this.loadHistory();

    } catch (error) {
      this.setData({ isLoading: false });
      console.error('查询失败:', error);
    }
  },

  // 检查单词是否已在生词本
  async checkIfInVocabBook(word: string) {
    try {
      const result = await vocabBookApi.checkExists(this.data.userId, word);
      this.setData({
        isInVocabBook: result.data.exists
      });
    } catch (error) {
      console.error('检查失败:', error);
    }
  },

  // 加载查询历史
  async loadHistory() {
    try {
      const result = await wordApi.getHistory(this.data.userId, 1, 10);
      this.setData({
        history: result.data.list || []
      });
    } catch (error) {
      console.error('加载历史失败:', error);
    }
  },

  // 点击历史记录
  onHistoryTap(e: any) {
    const word = e.currentTarget.dataset.word;
    this.setData({ inputWord: word });
    this.onSearch();
  },

  // 清空历史
  async clearHistory() {
    wx.showModal({
      title: '确认清空',
      content: '确定要清空查询历史吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await wordApi.clearHistory(this.data.userId);
            this.setData({ history: [] });
            wx.showToast({
              title: '已清空',
              icon: 'success'
            });
          } catch (error) {
            console.error('清空失败:', error);
          }
        }
      }
    });
  },

  // 添加到生词本
  async addToVocabBook() {
    if (this.data.isInVocabBook || !this.data.queryResult) {
      return;
    }

    const result = this.data.queryResult;
    const userId = this.data.userId;
    
    console.log('添加生词 - userId:', userId);
    console.log('添加生词 - result:', result);
    
    if (!userId || userId === 0) {
      wx.showToast({
        title: '请先登录',
        icon: 'none'
      });
      return;
    }
    
    wx.showLoading({ title: '添加中...' });

    try {
      const addResult = await vocabBookApi.add(userId, {
        word: result.word,
        phonetic: result.phonetic,
        definition: result.definition,
        english_definition: result.english_definition,
        examples: result.examples,
        memory_tips: result.memory_tips
      });
      
      console.log('添加生词结果:', addResult);

      this.setData({ isInVocabBook: true });

      wx.showToast({
        title: '添加成功',
        icon: 'success'
      });
    } catch (error) {
      console.error('添加失败:', error);
      wx.showToast({
        title: '添加失败',
        icon: 'none'
      });
    } finally {
      wx.hideLoading();
    }
  },

  // 分享功能
  onShareAppMessage() {
    if (this.data.queryResult) {
      return {
        title: `单词：${this.data.queryResult.word}`,
        path: `/pages/index/index?word=${this.data.queryResult.word}`
      };
    }
    return {
      title: 'AI智能背单词',
      path: '/pages/index/index'
    };
  }
});

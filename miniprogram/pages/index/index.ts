// 查词页面逻辑
import { wordApi, vocabBookApi, voiceApi, favoritesApi } from '../../utils/api';

// 获取全局app实例
const app = getApp<IAppOption>();

Page({
  data: {
    inputWord: '',
    isLoading: false,
    queryResult: null as any,
    history: [] as any[],
    isInVocabBook: false,
    userId: 0,
    favoriteStatus: [] as boolean[], // V2.0: 例句收藏状态
    currentVocabId: 0 // V2.0: 当前单词在生词本中的ID
  },

  onLoad() {
    console.log('[DEBUG] Index页面加载，全局用户信息:', app.globalData.userInfo);
    
    // 从全局获取用户信息
    const userInfo = app.globalData.userInfo;
    if (userInfo && userInfo.userId) {
      console.log('[DEBUG] 用户已登录，设置userId:', userInfo.userId);
      this.setData({ userId: userInfo.userId });
      this.loadHistory();
    } else {
      console.log('[DEBUG] 用户未登录，等待登录完成');
      // 等待自动登录完成
      const checkLogin = setInterval(() => {
        const userInfo = app.globalData.userInfo;
        console.log('[DEBUG] 检查登录状态:', userInfo);
        if (userInfo && userInfo.userId) {
          console.log('[DEBUG] 登录完成，设置userId:', userInfo.userId);
          this.setData({ userId: userInfo.userId });
          this.loadHistory();
          clearInterval(checkLogin);
        }
      }, 100);
      
      // 10秒后停止检查
      setTimeout(() => {
        clearInterval(checkLogin);
        console.log('[DEBUG] 登录检查超时');
      }, 10000);
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
    console.log('[DEBUG] 输入框内容变化:', e.detail.value);
    this.setData({
      inputWord: e.detail.value
    });
  },

  // 清空输入框
  clearInput() {
    console.log('[DEBUG] 清空输入框');
    this.setData({
      inputWord: ''
    });
  },

  // 执行查询
  async onSearch() {
    console.log('[DEBUG] 开始查询，当前输入:', this.data.inputWord);
    const word = this.data.inputWord.trim();
    console.log('[DEBUG] 处理后的单词:', word);
    
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
      const vocabId = result.data.exists ? result.data.vocab_id : 0;
      this.setData({
        isInVocabBook: result.data.exists,
        currentVocabId: vocabId
      });

      // 如果单词在生词本中，检查每个例句的收藏状态
      if (result.data.exists && this.data.queryResult && this.data.queryResult.examples) {
        await this.initFavoriteStatus(vocabId);
      }
    } catch (error) {
      console.error('检查失败:', error);
    }
  },

  // V2.0: 初始化例句收藏状态
  async initFavoriteStatus(vocabId: number) {
    if (!this.data.queryResult || !this.data.queryResult.examples) return;

    const favoriteStatus: boolean[] = [];
    const examples = this.data.queryResult.examples;

    for (let i = 0; i < examples.length; i++) {
      try {
        const checkResult = await favoritesApi.check(
          this.data.userId,
          vocabId,
          examples[i].sentence
        );
        favoriteStatus.push(checkResult.data.is_favorite);
        // 保存favoriteId到例句数据中
        examples[i].favoriteId = checkResult.data.favorite_id;
        examples[i].isFavorite = checkResult.data.is_favorite;
      } catch (error) {
        favoriteStatus.push(false);
        examples[i].isFavorite = false;
      }
    }

    this.setData({
      favoriteStatus,
      queryResult: { ...this.data.queryResult, examples }
    });
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
  },

  // V2.0: 朗读单词
  speakWord() {
    if (!this.data.queryResult) return;
    
    const word = this.data.queryResult.word;
    voiceApi.speak(word, 'en_US');
  },

  // V2.0: 朗读例句
  speakExample(e: any) {
    const index = e.currentTarget.dataset.index;
    const example = this.data.queryResult.examples[index];
    
    if (example && example.sentence) {
      voiceApi.speak(example.sentence, 'en_US');
    }
  },

  // V2.0: 收藏/取消收藏例句
  async addFavorite(e: any) {
    const index = e.currentTarget.dataset.index;
    const example = this.data.queryResult.examples[index];

    if (!example) return;

    try {
      let vocabId = this.data.currentVocabId;

      // 如果单词不在生词本，先添加单词
      if (!this.data.isInVocabBook) {
        const addResult = await vocabBookApi.add(this.data.userId, {
          word: this.data.queryResult.word,
          phonetic: this.data.queryResult.phonetic,
          definition: this.data.queryResult.definition,
          english_definition: this.data.queryResult.english_definition,
          examples: this.data.queryResult.examples,
          memory_tips: this.data.queryResult.memory_tips
        });
        vocabId = addResult.data.vocab_id;
        this.setData({
          isInVocabBook: true,
          currentVocabId: vocabId
        });
      }

      const isFavorite = this.data.favoriteStatus[index] || false;

      if (isFavorite) {
        // 取消收藏
        const favoriteId = example.favoriteId;
        if (favoriteId) {
          await favoritesApi.delete(this.data.userId, favoriteId);
        }
        wx.showToast({
          title: '已取消收藏',
          icon: 'success'
        });
      } else {
        // 添加收藏
        const result = await favoritesApi.add(
          this.data.userId,
          vocabId,
          example.sentence,
          example.translation
        );

        // 保存favoriteId
        if (result.data && result.data.favorite_id) {
          const queryResult = { ...this.data.queryResult };
          queryResult.examples[index].favoriteId = result.data.favorite_id;
          this.setData({ queryResult });
        }

        wx.showToast({
          title: '收藏成功',
          icon: 'success'
        });
      }

      // 更新收藏状态
      const favoriteStatus = [...this.data.favoriteStatus];
      favoriteStatus[index] = !isFavorite;

      // 更新例句的收藏状态
      const queryResult = { ...this.data.queryResult };
      queryResult.examples[index].isFavorite = !isFavorite;

      this.setData({
        favoriteStatus,
        queryResult
      });
    } catch (error) {
      console.error('收藏操作失败:', error);
      wx.showToast({
        title: '操作失败',
        icon: 'none'
      });
    }
  }
});

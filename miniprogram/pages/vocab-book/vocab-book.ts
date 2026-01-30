// 生词本页面
import { vocabBookApi } from '../../utils/api';

const app = getApp<IAppOption>();

Page({
  data: {
    vocabList: [] as any[],
    stats: {
      total_count: 0,
      mastered_count: 0,
      learning_count: 0,
      new_count: 0
    },
    userId: 0,
    loading: false,
    currentFilter: 'all' // all, new, learning, mastered
  },

  onLoad() {
    const userInfo = app.globalData.userInfo;
    if (userInfo && userInfo.userId) {
      this.setData({ userId: userInfo.userId });
    }
  },

  onShow() {
    if (this.data.userId) {
      this.loadVocabList();
      this.loadStats();
    }
  },

  // 加载生词本列表
  async loadVocabList() {
    this.setData({ loading: true });
    
    try {
      const params: any = {};
      if (this.data.currentFilter !== 'all') {
        const statusMap: { [key: string]: number } = {
          'new': 0,
          'learning': 1,
          'mastered': 2
        };
        params.status = statusMap[this.data.currentFilter];
      }

      const result = await vocabBookApi.getList(this.data.userId, params);
      this.setData({
        vocabList: result.data.list || []
      });
    } catch (error) {
      console.error('加载生词本失败:', error);
    } finally {
      this.setData({ loading: false });
    }
  },

  // 加载统计
  async loadStats() {
    try {
      const result = await vocabBookApi.getStats(this.data.userId);
      this.setData({ stats: result.data });
    } catch (error) {
      console.error('加载统计失败:', error);
    }
  },

  // 筛选切换
  onFilterChange(e: any) {
    const filter = e.currentTarget.dataset.filter;
    this.setData({ currentFilter: filter });
    this.loadVocabList();
  },

  // 更新状态
  async updateStatus(e: any) {
    const { vocabId, status } = e.currentTarget.dataset;
    
    try {
      await vocabBookApi.update(this.data.userId, vocabId, { status });
      this.loadVocabList();
      this.loadStats();
      
      wx.showToast({
        title: '更新成功',
        icon: 'success'
      });
    } catch (error) {
      console.error('更新失败:', error);
    }
  },

  // 删除单词
  async deleteVocab(e: any) {
    const vocabId = e.currentTarget.dataset.vocabId;
    
    wx.showModal({
      title: '确认删除',
      content: '确定要删除这个单词吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await vocabBookApi.delete(this.data.userId, vocabId);
            this.loadVocabList();
            this.loadStats();
            
            wx.showToast({
              title: '删除成功',
              icon: 'success'
            });
          } catch (error) {
            console.error('删除失败:', error);
          }
        }
      }
    });
  },

  // 查看详情
  viewDetail(e: any) {
    const vocabId = e.currentTarget.dataset.vocabId;
    wx.navigateTo({
      url: `/pages/vocab-detail/vocab-detail?vocabId=${vocabId}`
    });
  }
});

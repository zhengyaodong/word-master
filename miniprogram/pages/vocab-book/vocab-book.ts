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
    currentFilter: 'all', // all, new, learning, mastered
    selectedVocabIds: [] as number[],
    hasMore: true,
    page: 1,
    pageSize: 20
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

  // 更新单个单词状态
  async updateSingleStatus(e: any) {
    const { vocabId, status } = e.currentTarget.dataset;
    
    // 调试输出
    console.log('updateSingleStatus 调试信息:', {
      vocabId: vocabId,
      status: status,
      statusType: typeof status,
      dataset: e.currentTarget.dataset
    });
    
    // 确保status是有效的数字
    if (status === null || status === undefined || status === '') {
      console.error('status参数无效:', status);
      wx.showToast({
        title: '参数错误：状态值无效',
        icon: 'none'
      });
      return;
    }
    
    const numericStatus = parseInt(status);
    if (isNaN(numericStatus) || ![0, 1, 2].includes(numericStatus)) {
      console.error('status参数不是有效值:', status, 'parsed:', numericStatus);
      wx.showToast({
        title: '参数错误：状态值必须是0、1或2',
        icon: 'none'
      });
      return;
    }
    
    try {
      await vocabBookApi.update(this.data.userId, vocabId, { status: numericStatus });
      this.loadVocabList();
      this.loadStats();
      
      const statusText = numericStatus === 1 ? '学习中' : (numericStatus === 2 ? '已掌握' : '重新学习');
      wx.showToast({
        title: `已标记为${statusText}`,
        icon: 'success',
        duration: 1500
      });
    } catch (error) {
      console.error('更新状态失败:', error);
      wx.showToast({
        title: '更新失败，请重试',
        icon: 'none'
      });
    }
  },

  // 更新状态（批量操作）
  async updateStatus(e: any) {
    const { vocabId, status } = e.currentTarget.dataset;
    
    // 调试输出
    console.log('批量更新状态:', {
      vocabId: vocabId,
      status: status,
      statusType: typeof status,
      dataset: e.currentTarget.dataset
    });
    
    // 确保status是有效的数字
    if (status === null || status === undefined || status === '') {
      console.error('批量status参数无效:', status);
      wx.showToast({
        title: '参数错误：状态值无效',
        icon: 'none'
      });
      return;
    }
    
    const numericStatus = parseInt(status);
    if (isNaN(numericStatus) || ![0, 1, 2].includes(numericStatus)) {
      console.error('批量status参数不是有效值:', status, 'parsed:', numericStatus);
      wx.showToast({
        title: '参数错误：状态值必须是0、1或2',
        icon: 'none'
      });
      return;
    }
    
    try {
      await vocabBookApi.update(this.data.userId, vocabId, { status: numericStatus });
      this.loadVocabList();
      this.loadStats();
      
      wx.showToast({
        title: '批量更新成功',
        icon: 'success'
      });
    } catch (error) {
      console.error('批量更新失败:', error);
      wx.showToast({
        title: '批量更新失败，请重试',
        icon: 'none'
      });
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
  },

  // 批量更新状态
  async batchUpdateStatus(e: any) {
    const status = e.currentTarget.dataset.status;
    
    wx.showModal({
      title: '确认操作',
      content: `确定要将选中的单词标记为${status === 1 ? '学习中' : '已掌握'}吗？`,
      success: async (res) => {
        if (res.confirm && this.data.selectedVocabIds.length > 0) {
          try {
            // 逐个更新状态
            for (const vocabId of this.data.selectedVocabIds) {
              await vocabBookApi.update(this.data.userId, vocabId, { status });
            }
            
            this.setData({ selectedVocabIds: [] });
            this.loadVocabList();
            this.loadStats();
            
            wx.showToast({
              title: '批量更新成功',
              icon: 'success'
            });
          } catch (error) {
            console.error('批量更新失败:', error);
          }
        }
      }
    });
  },

  // 批量删除
  async batchDelete() {
    wx.showModal({
      title: '确认删除',
      content: `确定要删除选中的${this.data.selectedVocabIds.length}个单词吗？`,
      success: async (res) => {
        if (res.confirm && this.data.selectedVocabIds.length > 0) {
          try {
            await vocabBookApi.batchDelete(this.data.userId, this.data.selectedVocabIds);
            
            this.setData({ selectedVocabIds: [] });
            this.loadVocabList();
            this.loadStats();
            
            wx.showToast({
              title: '批量删除成功',
              icon: 'success'
            });
          } catch (error) {
            console.error('批量删除失败:', error);
          }
        }
      }
    });
  },

  // 跳转到查词页面
  goToSearch() {
    wx.switchTab({
      url: '/pages/index/index'
    });
  }
});

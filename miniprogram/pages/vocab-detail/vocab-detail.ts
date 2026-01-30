// 生词详情页面
import { vocabBookApi } from '../../utils/api';

const app = getApp<IAppOption>();

Page({
  data: {
    vocabId: 0,
    vocabDetail: null as any,
    userId: 0,
    loading: false
  },

  onLoad(options: any) {
    const vocabId = parseInt(options.vocabId);
    this.setData({ vocabId });

    const userInfo = app.globalData.userInfo;
    if (userInfo && userInfo.userId) {
      this.setData({ userId: userInfo.userId });
      this.loadVocabDetail();
    }
  },

  // 加载生词详情
  async loadVocabDetail() {
    this.setData({ loading: true });
    
    try {
      const result = await vocabBookApi.getDetail(this.data.userId, this.data.vocabId);
      this.setData({
        vocabDetail: result.data,
        loading: false
      });
    } catch (error) {
      this.setData({ loading: false });
      console.error('加载详情失败:', error);
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    }
  },

  // 更新状态
  async updateStatus(e: any) {
    const status = e.currentTarget.dataset.status;
    
    try {
      await vocabBookApi.update(this.data.userId, this.data.vocabId, { status });
      this.loadVocabDetail();
      
      wx.showToast({
        title: '更新成功',
        icon: 'success'
      });
    } catch (error) {
      console.error('更新失败:', error);
    }
  },

  // 删除生词
  async deleteVocab() {
    wx.showModal({
      title: '确认删除',
      content: '确定要删除这个单词吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await vocabBookApi.delete(this.data.userId, this.data.vocabId);
            
            wx.showToast({
              title: '删除成功',
              icon: 'success'
            });

            // 返回上一页
            setTimeout(() => {
              wx.navigateBack();
            }, 1000);
          } catch (error) {
            console.error('删除失败:', error);
          }
        }
      }
    });
  }
});

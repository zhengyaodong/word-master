// 收藏例句页面
import { favoritesApi } from '../../utils/api';

const app = getApp<IAppOption>();

Page({
  data: {
    loading: true,
    favorites: []
  },

  onLoad() {
    this.loadFavorites();
  },

  onShow() {
    this.loadFavorites();
  },

  // 加载收藏列表
  async loadFavorites() {
    const userInfo = app.globalData.userInfo;
    if (!userInfo || !userInfo.userId) {
      this.setData({ loading: false });
      return;
    }

    try {
      this.setData({ loading: true });
      
      const result = await favoritesApi.getList(userInfo.userId);
      
      this.setData({
        favorites: result.data.list || [],
        loading: false
      });
    } catch (error) {
      console.error('加载收藏失败:', error);
      this.setData({ loading: false });
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    }
  },

  // 删除收藏
  async deleteFavorite(e: any) {
    const favoriteId = e.currentTarget.dataset.id;
    const userInfo = app.globalData.userInfo;
    
    if (!userInfo || !userInfo.userId) {
      return;
    }

    // 确认删除
    const confirm = await wx.showModal({
      title: '确认删除',
      content: '确定要删除这条收藏吗？',
      confirmColor: '#ff4d4f'
    });

    if (!confirm.confirm) {
      return;
    }

    try {
      wx.showLoading({ title: '删除中...' });
      
      await favoritesApi.delete(userInfo.userId, favoriteId);
      
      wx.hideLoading();
      wx.showToast({
        title: '删除成功',
        icon: 'success'
      });
      
      // 重新加载列表
      this.loadFavorites();
    } catch (error) {
      wx.hideLoading();
      console.error('删除失败:', error);
      wx.showToast({
        title: '删除失败',
        icon: 'none'
      });
    }
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadFavorites().then(() => {
      wx.stopPullDownRefresh();
    });
  }
});

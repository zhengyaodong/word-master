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
    currentFilter: 'all',
    selectedVocabIds: [] as number[],
    selectedMap: {} as Record<number, boolean>,
    editMode: false,
    hasMore: true,
    total: 0,
    loadedCount: 0,
    showBackTop: false,
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
      this.refreshList();
      this.loadStats();
    }
  },

  onPullDownRefresh() {
    this.refreshList().then(() => {
      wx.stopPullDownRefresh();
    });
  },

  onReachBottom() {
    if (this.data.loading || !this.data.hasMore) return;
    this.loadMore();
  },

  onPageScroll(e: any) {
    if (e.scrollTop > 600 && !this.data.showBackTop) {
      this.setData({ showBackTop: true });
    } else if (e.scrollTop <= 600 && this.data.showBackTop) {
      this.setData({ showBackTop: false });
    }
  },

  async refreshList() {
    this.setData({
      page: 1,
      hasMore: true,
      vocabList: [],
      selectedVocabIds: [],
      selectedMap: {},
      loadedCount: 0
    });
    await this.loadVocabList();
  },

  async loadMore() {
    if (!this.data.hasMore) return;
    this.setData({ page: this.data.page + 1 });
    await this.loadVocabList(true);
  },

  async loadVocabList(append = false) {
    if (!this.data.userId) return;
    this.setData({ loading: true });

    try {
      const params: any = {
        page: this.data.page,
        pageSize: this.data.pageSize
      };
      if (this.data.currentFilter !== 'all') {
        const statusMap: { [key: string]: number } = {
          new: 0,
          learning: 1,
          mastered: 2
        };
        params.status = statusMap[this.data.currentFilter];
      }

      const result = await vocabBookApi.getList(this.data.userId, params);
      const list = (result.data.list || []).map((item: any) => ({
        ...item,
        vocab_id: Number(item.vocab_id)
      }));
      const nextList = append ? [...this.data.vocabList, ...list] : list;
      const hasMore = list.length >= this.data.pageSize;

      this.setData({
        vocabList: nextList,
        hasMore,
        total: result.data.total || nextList.length,
        loadedCount: nextList.length
      });
    } catch (error) {
      console.error('加载生词本失败:', error);
    } finally {
      this.setData({ loading: false });
    }
  },

  async loadStats() {
    try {
      const result = await vocabBookApi.getStats(this.data.userId);
      this.setData({ stats: result.data });
    } catch (error) {
      console.error('加载统计失败:', error);
    }
  },

  onFilterChange(e: any) {
    const filter = e.currentTarget.dataset.filter;
    this.setData({ currentFilter: filter, page: 1, vocabList: [], hasMore: true });
    this.loadVocabList();
  },

  toggleEdit() {
    const editMode = !this.data.editMode;
    this.setData({ editMode, selectedVocabIds: [], selectedMap: {} });
  },

  toggleSelect(e: any) {
    const vocabId = Number(e.currentTarget.dataset.vocabId);
    const selectedMap = { ...this.data.selectedMap };
    selectedMap[vocabId] = !selectedMap[vocabId];
    const selectedVocabIds = Object.keys(selectedMap)
      .filter((k) => selectedMap[Number(k)])
      .map((k) => Number(k));
    this.setData({ selectedMap, selectedVocabIds });
  },

  selectAll() {
    const selectedMap: Record<number, boolean> = {};
    const allIds = this.data.vocabList.map((v) => Number(v.vocab_id));
    allIds.forEach((id) => {
      selectedMap[id] = true;
    });
    this.setData({ selectedVocabIds: allIds, selectedMap });
  },

  clearSelection() {
    this.setData({ selectedVocabIds: [], selectedMap: {} });
  },

  async updateSingleStatus(e: any) {
    const { vocabId, status } = e.currentTarget.dataset;

    try {
      await vocabBookApi.update(this.data.userId, vocabId, { status: parseInt(status, 10) });
      this.refreshList();
      this.loadStats();
      wx.showToast({ title: '更新成功', icon: 'success' });
    } catch (error) {
      console.error('更新状态失败:', error);
      wx.showToast({ title: '更新失败', icon: 'none' });
    }
  },

  async batchUpdateStatus(e: any) {
    const status = parseInt(e.currentTarget.dataset.status, 10);
    if (!this.data.selectedVocabIds.length) return;

    wx.showModal({
      title: '确认操作',
      content: '确定更新选中单词的状态吗？',
      success: async (res) => {
        if (!res.confirm) return;
        try {
          for (const vocabId of this.data.selectedVocabIds) {
            await vocabBookApi.update(this.data.userId, vocabId, { status });
          }
          this.setData({ selectedVocabIds: [] });
          this.refreshList();
          this.loadStats();
          wx.showToast({ title: '批量更新成功', icon: 'success' });
        } catch (error) {
          console.error('批量更新失败:', error);
        }
      }
    });
  },

  async batchDelete() {
    if (!this.data.selectedVocabIds.length) return;

    wx.showModal({
      title: '确认删除',
      content: `确定要删除选中的 ${this.data.selectedVocabIds.length} 个单词吗？`,
      success: async (res) => {
        if (!res.confirm) return;
        try {
          await vocabBookApi.batchDelete(this.data.userId, this.data.selectedVocabIds);
          this.setData({ selectedVocabIds: [] });
          this.refreshList();
          this.loadStats();
          wx.showToast({ title: '批量删除成功', icon: 'success' });
        } catch (error) {
          console.error('批量删除失败:', error);
        }
      }
    });
  },

  viewDetail(e: any) {
    if (this.data.editMode) {
      this.toggleSelect(e);
      return;
    }
    const vocabId = e.currentTarget.dataset.vocabId;
    wx.navigateTo({
      url: `/pages/vocab-detail/vocab-detail?vocabId=${vocabId}`
    });
  },

  goToSearch() {
    wx.switchTab({
      url: '/pages/index/index'
    });
  },

  backToTop() {
    wx.pageScrollTo({
      scrollTop: 0,
      duration: 300
    });
  }
});

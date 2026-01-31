// 生词详情页面
import { vocabBookApi, voiceApi, favoritesApi } from '../../utils/api';

const app = getApp<IAppOption>();

Page({
  data: {
    vocabId: 0,
    vocabDetail: null as any,
    userId: 0,
    loading: false,
    favoriteStatus: [] as boolean[] // V2.0: 例句收藏状态
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
      const vocabDetail = result.data;

      // 初始化收藏状态数组
      const favoriteStatus: boolean[] = [];
      if (vocabDetail.examples && vocabDetail.examples.length > 0) {
        // 检查每个例句的收藏状态
        for (let i = 0; i < vocabDetail.examples.length; i++) {
          const example = vocabDetail.examples[i];
          try {
            const checkResult = await favoritesApi.check(
              this.data.userId,
              this.data.vocabId,
              example.sentence
            );
            // 设置收藏状态和favoriteId
            const isFavorite = checkResult.data.is_favorite;
            favoriteStatus.push(isFavorite);
            vocabDetail.examples[i].isFavorite = isFavorite;
            vocabDetail.examples[i].favoriteId = checkResult.data.favorite_id;
          } catch (error) {
            favoriteStatus.push(false);
            vocabDetail.examples[i].isFavorite = false;
          }
        }
      }

      this.setData({
        vocabDetail,
        favoriteStatus,
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
  },

  // V2.0: 朗读单词
  speakWord() {
    if (!this.data.vocabDetail) return;
    
    const word = this.data.vocabDetail.word;
    voiceApi.speak(word, 'en_US');
  },

  // V2.0: 朗读例句
  speakExample(e: any) {
    const index = e.currentTarget.dataset.index;
    const example = this.data.vocabDetail.examples[index];
    
    if (example && example.sentence) {
      voiceApi.speak(example.sentence, 'en_US');
    }
  },

  // V2.0: 切换收藏状态
  async toggleFavorite(e: any) {
    const index = e.currentTarget.dataset.index;
    const example = this.data.vocabDetail.examples[index];

    if (!example) return;

    try {
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
          this.data.vocabId,
          example.sentence,
          example.translation
        );

        // 保存返回的favoriteId，用于后续取消收藏
        if (result.data && result.data.favorite_id) {
          const vocabDetail = { ...this.data.vocabDetail };
          vocabDetail.examples[index].favoriteId = result.data.favorite_id;
          this.setData({ vocabDetail });
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
      const vocabDetail = { ...this.data.vocabDetail };
      vocabDetail.examples[index].isFavorite = !isFavorite;

      this.setData({
        favoriteStatus,
        vocabDetail
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

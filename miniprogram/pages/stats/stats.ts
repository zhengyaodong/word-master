// 学习统计页面
import { statsApi } from '../../utils/api';

const app = getApp<IAppOption>();

Page({
  data: {
    loading: true,
    stats: {
      total_words: 0,
      mastered: 0,
      learning: 0,
      new: 0,
      today_query: 0,
      consecutive_days: 0
    },
    trendData: [],
    calendarDays: [],
    weekdays: ['日', '一', '二', '三', '四', '五', '六'],
    currentMonth: ''
  },

  onLoad() {
    this.loadStats();
  },

  onShow() {
    this.loadStats();
  },

  // 加载统计数据
  async loadStats() {
    const userInfo = app.globalData.userInfo;
    if (!userInfo || !userInfo.userId) {
      this.setData({ loading: false });
      return;
    }

    try {
      this.setData({ loading: true });
      
      // 并行获取概览和趋势
      const [overviewRes, trendRes] = await Promise.all([
        statsApi.getOverview(userInfo.userId),
        statsApi.getTrend(userInfo.userId)
      ]);

      // 处理概览数据
      const stats = overviewRes.data;
      
      // 处理趋势数据，计算柱状图高度
      const maxCount = Math.max(...trendRes.data.last_7_days.map(d => d.query_count), 1);
      const trendData = trendRes.data.last_7_days.map(day => ({
        ...day,
        barHeight: Math.max((day.query_count / maxCount) * 120, 10) // 最小10rpx，最大120rpx
      }));

      // 生成日历数据
      const calendarDays = this.generateCalendarDays(trendRes.data.last_7_days);
      const currentMonth = new Date().getFullYear() + '年' + (new Date().getMonth() + 1) + '月';

      this.setData({
        stats,
        trendData,
        calendarDays,
        currentMonth,
        loading: false
      });
    } catch (error) {
      console.error('加载统计失败:', error);
      this.setData({ loading: false });
      wx.showToast({
        title: '加载失败',
        icon: 'none'
      });
    }
  },

  // 生成日历数据
  generateCalendarDays(last7Days) {
    const days = [];
    const today = new Date();
    const currentYear = today.getFullYear();
    const currentMonth = today.getMonth();
    
    // 获取本月第一天是星期几
    const firstDayOfMonth = new Date(currentYear, currentMonth, 1);
    const firstDayWeekday = firstDayOfMonth.getDay();
    
    // 获取本月天数
    const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    
    // 填充空白（上月）
    for (let i = 0; i < firstDayWeekday; i++) {
      days.push({ isEmpty: true });
    }
    
    // 填充本月日期
    const checkedDates = new Set(last7Days.filter(d => d.is_checked_in).map(d => {
      const date = new Date();
      date.setDate(parseInt(d.date.split('-')[1]));
      return date.getDate();
    }));
    
    for (let day = 1; day <= daysInMonth; day++) {
      const date = new Date(currentYear, currentMonth, day);
      const isToday = day === today.getDate();
      
      // 检查是否已打卡（简化处理：只看最近7天数据）
      const isCheckedIn = checkedDates.has(day) || (isToday && this.data.stats.today_query > 0);
      
      days.push({
        day: day,
        date: `${currentMonth + 1}-${day}`,
        isToday,
        isCheckedIn
      });
    }
    
    return days;
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadStats().then(() => {
      wx.stopPullDownRefresh();
    });
  }
});

/**
 * API请求工具
 * 封装微信小程序的wx.request，统一处理后端API调用
 */

// 后端API基础地址
// 开发环境使用本地地址，生产环境需要修改为服务器地址
// 注意：微信小程序真机调试时不能使用 localhost，需要使用实际IP地址
// 模拟器使用 localhost，真机调试需要改为实际 IP

// 自动检测运行环境
const isSimulator = typeof wx !== 'undefined' && wx.getSystemInfoSync().platform === 'devtools';
const isDevtool = typeof wx !== 'undefined' && wx.getSystemInfoSync().platform === 'devtools';

// 基础URL配置
let BASE_URL = 'http://localhost:5000';

// 根据环境自动切换
if (isDevtool) {
  // 开发者工具/模拟器环境
  BASE_URL = 'http://localhost:5000';
} else {
  // 真机环境，使用局域网IP
  // 这里可以手动配置你的电脑局域网IP
  const LOCAL_IP = '192.168.0.104'; // 请根据实际情况修改
  BASE_URL = `http://${LOCAL_IP}:5000`;
}

/**
 * 封装请求方法
 * @param {string} method - 请求方法 GET/POST/PUT/DELETE
 * @param {string} url - 请求路径
 * @param {object} data - 请求数据
 * @returns {Promise} 返回Promise对象
 */
const request = (method, url, data = {}, options = {}) => {
  return new Promise((resolve, reject) => {
    // 检查网络状态
    wx.getNetworkType({
      success: (netRes) => {
        if (netRes.networkType === 'none') {
          wx.showToast({
            title: '网络不可用，请检查网络连接',
            icon: 'none',
            duration: 2000
          });
          reject(new Error('网络不可用'));
          return;
        }

        wx.request({
          url: `${BASE_URL}${url}`,
          method: method,
          data: data,
          timeout: options.timeout || 30000,
          header: {
            'Content-Type': 'application/json',
            ...options.header
          },
          success: (res) => {
            if (res.statusCode === 200) {
              const result = res.data;
              if (result.code === 0) {
                resolve(result);
              } else {
                // 业务错误，根据错误码提供更友好的提示
                const errorMessage = getErrorMessage(result);
                if (!options.hideErrorToast) {
                  wx.showToast({
                    title: errorMessage,
                    icon: 'none',
                    duration: 3000
                  });
                }
                reject(new Error(errorMessage));
              }
            } else if (res.statusCode === 404) {
              if (!options.hideErrorToast) {
                wx.showToast({
                  title: '请求的接口不存在',
                  icon: 'none'
                });
              }
              reject(new Error('接口不存在'));
            } else if (res.statusCode === 500) {
              if (!options.hideErrorToast) {
                wx.showToast({
                  title: '服务器内部错误，请稍后重试',
                  icon: 'none'
                });
              }
              reject(new Error('服务器内部错误'));
            } else {
              // 其他HTTP错误
              if (!options.hideErrorToast) {
                wx.showToast({
                  title: `请求失败 (${res.statusCode})`,
                  icon: 'none'
                });
              }
              reject(new Error(`HTTP ${res.statusCode}`));
            }
          },
          fail: (err) => {
            // 网络错误或超时
            let errorMessage = '网络请求失败，请检查网络';
            if (err.errMsg && err.errMsg.includes('timeout')) {
              errorMessage = '请求超时，请检查网络连接';
            } else if (err.errMsg && err.errMsg.includes('fail')) {
              errorMessage = '网络连接失败，请检查后端服务是否启动';
            }
            
            if (!options.hideErrorToast) {
              wx.showToast({
                title: errorMessage,
                icon: 'none',
                duration: 3000
              });
            }
            reject(new Error(errorMessage));
          }
        });
      },
      fail: () => {
        // 获取网络类型失败
        wx.showToast({
          title: '无法获取网络状态，请检查网络',
          icon: 'none'
        });
        reject(new Error('网络状态未知'));
      }
    });
  });
};

// 获取友好的错误信息
const getErrorMessage = (result) => {
  const code = result.code;
  const message = result.message;
  
  // 根据错误码返回更友好的提示
  switch (code) {
    case 1:
      return message || '操作失败';
    case 404:
      return '请求的资源不存在';
    case 409:
      return '数据冲突，该单词可能已存在';
    case 503:
      return 'AI服务暂时不可用，请稍后重试';
    default:
      return message || '未知错误，请稍后重试';
  }
};

/**
 * 用户相关API
 */
const userApi = {
  /**
   * 用户登录
   * @param {string} openid - 微信openid
   * @param {string} nickname - 昵称
   * @param {string} avatarUrl - 头像URL
   */
  login: (openid, nickname = '', avatarUrl = '') => {
    return request('POST', '/api/user/login', {
      openid,
      nickname,
      avatar_url: avatarUrl
    });
  },

  /**
   * 获取用户信息
   * @param {number} userId - 用户ID
   */
  getInfo: (userId) => {
    return request('GET', `/api/user/info?userId=${userId}`);
  },

  /**
   * 更新用户信息
   * @param {number} userId - 用户ID
   * @param {object} data - 更新数据
   */
  update: (userId, data) => {
    return request('PUT', '/api/user/update', {
      userId,
      ...data
    });
  },

  /**
   * 获取用户统计
   * @param {number} userId - 用户ID
   */
  getStats: (userId) => {
    return request('GET', `/api/user/stats?userId=${userId}`);
  }
};

/**
 * 单词查询相关API
 */
const wordApi = {
  /**
   * 查询单词
   * @param {number} userId - 用户ID
   * @param {string} word - 要查询的单词
   * @param {boolean} useCache - 是否使用缓存
   */
  query: (userId, word, useCache = true) => {
    return request('POST', '/api/word/query', {
      userId,
      word,
      use_cache: useCache
    });
  },

  /**
   * 获取查询历史
   * @param {number} userId - 用户ID
   * @param {number} page - 页码
   * @param {number} pageSize - 每页数量
   */
  getHistory: (userId, page = 1, pageSize = 20) => {
    return request('GET', `/api/word/history?userId=${userId}&page=${page}&page_size=${pageSize}`);
  },

  /**
   * 清空查询历史
   * @param {number} userId - 用户ID
   */
  clearHistory: (userId) => {
    return request('DELETE', '/api/word/history/clear', {
      userId
    });
  },

  /**
   * 检查Ollama服务状态
   */
  checkService: () => {
    return request('GET', '/api/word/check');
  }
};

/**
 * 生词本相关API
 */
const vocabBookApi = {
  /**
   * 添加单词到生词本
   * @param {number} userId - 用户ID
   * @param {object} wordData - 单词数据
   */
  add: (userId, wordData) => {
    return request('POST', '/api/vocab-book/add', {
      userId,
      ...wordData
    });
  },

  /**
   * 获取生词本列表
   * @param {number} userId - 用户ID
   * @param {object} params - 查询参数
   */
  getList: (userId, params = {}) => {
    const { page = 1, pageSize = 20, status, sortBy, order } = params;
    let url = `/api/vocab-book/list?userId=${userId}&page=${page}&page_size=${pageSize}`;
    if (status !== undefined) url += `&status=${status}`;
    if (sortBy) url += `&sort_by=${sortBy}`;
    if (order) url += `&order=${order}`;
    return request('GET', url);
  },

  /**
   * 获取生词详情
   * @param {number} userId - 用户ID
   * @param {number} vocabId - 生词ID
   */
  getDetail: (userId, vocabId) => {
    return request('GET', `/api/vocab-book/detail?userId=${userId}&vocab_id=${vocabId}`);
  },

  /**
   * 更新生词信息
   * @param {number} userId - 用户ID
   * @param {number} vocabId - 生词ID
   * @param {object} data - 更新数据
   */
  update: (userId, vocabId, data) => {
    return request('PUT', '/api/vocab-book/update', {
      userId,
      vocab_id: vocabId,
      ...data
    });
  },

  /**
   * 删除生词
   * @param {number} userId - 用户ID
   * @param {number} vocabId - 生词ID
   */
  delete: (userId, vocabId) => {
    return request('DELETE', '/api/vocab-book/delete', {
      userId,
      vocab_id: vocabId
    });
  },

  /**
   * 批量删除生词
   * @param {number} userId - 用户ID
   * @param {array} vocabIds - 生词ID列表
   */
  batchDelete: (userId, vocabIds) => {
    return request('DELETE', '/api/vocab-book/batch-delete', {
      userId,
      vocab_ids: vocabIds
    });
  },

  /**
   * 获取生词本统计
   * @param {number} userId - 用户ID
   */
  getStats: (userId) => {
    return request('GET', `/api/vocab-book/stats?userId=${userId}`);
  },

  /**
   * 检查单词是否已存在
   * @param {number} userId - 用户ID
   * @param {string} word - 单词
   */
  checkExists: (userId, word) => {
    return request('GET', `/api/vocab-book/check-exists?userId=${userId}&word=${word}`);
  }
};

/**
 * V2.0 统计相关API
 */
const statsApi = {
  /**
   * 获取学习概览统计
   * @param {number} userId - 用户ID
   */
  getOverview: (userId) => {
    return request('GET', `/api/stats/overview?user_id=${userId}`);
  },

  /**
   * 获取近7天趋势
   * @param {number} userId - 用户ID
   */
  getTrend: (userId) => {
    return request('GET', `/api/stats/trend?user_id=${userId}`);
  },

  /**
   * 手动打卡
   * @param {number} userId - 用户ID
   */
  checkIn: (userId) => {
    return request('POST', '/api/stats/checkin', {
      user_id: userId
    });
  }
};

/**
 * V2.0 收藏例句相关API
 */
const favoritesApi = {
  /**
   * 收藏例句
   * @param {number} userId - 用户ID
   * @param {number} vocabId - 单词ID
   * @param {string} sentence - 例句
   * @param {string} translation - 翻译
   */
  add: (userId, vocabId, sentence, translation) => {
    return request('POST', '/api/favorites/add', {
      user_id: userId,
      vocab_id: vocabId,
      sentence,
      translation
    });
  },

  /**
   * 获取收藏列表
   * @param {number} userId - 用户ID
   */
  getList: (userId) => {
    return request('GET', `/api/favorites/list?user_id=${userId}`);
  },

  /**
   * 删除收藏
   * @param {number} userId - 用户ID
   * @param {number} favoriteId - 收藏ID
   */
  delete: (userId, favoriteId) => {
    return request('DELETE', '/api/favorites/delete', {
      user_id: userId,
      favorite_id: favoriteId
    });
  },

  /**
   * 检查是否已收藏
   * @param {number} userId - 用户ID
   * @param {number} vocabId - 单词ID
   * @param {string} sentence - 例句
   */
  check: (userId, vocabId, sentence) => {
    return request('GET', `/api/favorites/check?user_id=${userId}&vocab_id=${vocabId}&sentence=${encodeURIComponent(sentence)}`);
  }
};

/**
 * 语音朗读（使用 Edge-TTS 后端服务）
 */
const voiceApi = {
  /**
   * 朗读文本
   * @param {string} text - 要朗读的文本
   * @param {string} lang - 语言，默认英语
   */
  speak: (text, lang = 'en_US') => {
    return new Promise((resolve, reject) => {
      // 检查网络状态
      wx.getNetworkType({
        success: (netRes) => {
          if (netRes.networkType === 'none') {
            wx.showToast({
              title: '网络不可用，请检查网络连接',
              icon: 'none',
              duration: 2000
            });
            reject(new Error('网络不可用'));
            return;
          }

          // 调用后端 TTS API
          wx.request({
            url: `${BASE_URL}/api/tts/speak`,
            method: 'POST',
            data: {
              text: text,
              lang: lang
            },
            header: {
              'Content-Type': 'application/json'
            },
            timeout: 30000,
            success: (res) => {
              if (res.statusCode === 200 && res.data.code === 0) {
                const audioUrl = res.data.data.audio_url;
                const fullUrl = `${BASE_URL}${audioUrl}`;
                
                // 创建音频上下文并播放
                const audio = wx.createInnerAudioContext();
                audio.src = fullUrl;
                
                audio.onPlay(() => {
                  console.log('开始播放语音:', text);
                });
                
                audio.onError((err) => {
                  console.error('语音播放失败:', err);
                  wx.showToast({
                    title: '语音播放失败',
                    icon: 'none'
                  });
                  reject(err);
                });
                
                audio.onEnded(() => {
                  console.log('语音播放完成:', text);
                  audio.destroy();
                });
                
                audio.play();
                resolve(res.data);
              } else {
                const errorMsg = res.data?.message || '语音合成失败';
                console.error('TTS API 错误:', errorMsg);
                wx.showToast({
                  title: errorMsg,
                  icon: 'none',
                  duration: 2000
                });
                reject(new Error(errorMsg));
              }
            },
            fail: (err) => {
              console.error('TTS 请求失败:', err);
              let errorMessage = '语音服务请求失败';
              if (err.errMsg && err.errMsg.includes('timeout')) {
                errorMessage = '语音合成超时，请稍后重试';
              }
              wx.showToast({
                title: errorMessage,
                icon: 'none',
                duration: 2000
              });
              reject(new Error(errorMessage));
            }
          });
        },
        fail: () => {
          wx.showToast({
            title: '无法获取网络状态',
            icon: 'none'
          });
          reject(new Error('网络状态未知'));
        }
      });
    });
  },

  /**
   * 获取可用的语音列表
   */
  getVoices: () => {
    return request('GET', '/api/tts/voices');
  },

  /**
   * 清理音频缓存（管理员功能）
   */
  clearCache: () => {
    return request('DELETE', '/api/tts/clear-cache');
  }
};

/**
 * 健康检查
 */
const healthCheck = () => {
  return request('GET', '/api/health');
};

module.exports = {
  BASE_URL,
  userApi,
  wordApi,
  vocabBookApi,
  statsApi,
  favoritesApi,
  voiceApi,
  healthCheck
};

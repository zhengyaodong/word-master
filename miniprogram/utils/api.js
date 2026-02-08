/**
 * API请求工具
 * 封装微信小程序的wx.request，统一处理后端API调用
 */

// 后端API基础地址
// 开发环境使用本地地址，生产环境需要修改为服务器地址
// 注意：微信小程序真机调试时不能使用localhost，需要使用实际IP地址
// 模拟器使用localhost，真机调试需要改为实际IP

// 自动检测运行环境
const isSimulator = typeof wx !== 'undefined' && wx.getSystemInfoSync().platform === 'devtools';
const isDevtool = typeof wx !== 'undefined' && wx.getSystemInfoSync().platform === 'devtools';

// 基础URL配置
let BASE_URL = 'http://localhost:5000';

// 根据环境自动切换
if (isDevtool) {
  // 开发者工具模拟器环境
  BASE_URL = 'http://localhost:5000';
} else {
  // 真机环境，使用局域网IP
  const LOCAL_IP = '192.168.0.102'; // 根据实际情况修改
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
  login: (openid, nickname = '', avatarUrl = '') => {
    return request('POST', '/api/user/login', {
      openid,
      nickname,
      avatar_url: avatarUrl
    });
  },

  getInfo: (userId) => {
    return request('GET', `/api/user/info?userId=${userId}`);
  },

  update: (userId, data) => {
    return request('PUT', '/api/user/update', {
      userId,
      ...data
    });
  },

  getStats: (userId) => {
    return request('GET', `/api/user/stats?userId=${userId}`);
  }
};

/**
 * 单词查询相关API
 */
const wordApi = {
  query: (userId, word, useCache = true) => {
    return request('POST', '/api/word/query', {
      userId,
      word,
      use_cache: useCache
    });
  },

  getHistory: (userId, page = 1, pageSize = 20) => {
    return request('GET', `/api/word/history?userId=${userId}&page=${page}&page_size=${pageSize}`);
  },

  clearHistory: (userId) => {
    return request('DELETE', '/api/word/history/clear', {
      userId
    });
  },

  checkService: () => {
    return request('GET', '/api/word/check');
  }
};

/**
 * 生词本相关API
 */
const vocabBookApi = {
  add: (userId, wordData) => {
    return request('POST', '/api/vocab-book/add', {
      userId,
      ...wordData
    });
  },

  getList: (userId, params = {}) => {
    const { page = 1, pageSize = 20, status, sortBy, order } = params;
    let url = `/api/vocab-book/list?userId=${userId}&page=${page}&page_size=${pageSize}`;
    if (status !== undefined) url += `&status=${status}`;
    if (sortBy) url += `&sort_by=${sortBy}`;
    if (order) url += `&order=${order}`;
    return request('GET', url);
  },

  getDetail: (userId, vocabId) => {
    return request('GET', `/api/vocab-book/detail?userId=${userId}&vocab_id=${vocabId}`);
  },

  update: (userId, vocabId, data) => {
    return request('PUT', '/api/vocab-book/update', {
      userId,
      vocab_id: vocabId,
      ...data
    });
  },

  delete: (userId, vocabId) => {
    return request('DELETE', '/api/vocab-book/delete', {
      userId,
      vocab_id: vocabId
    });
  },

  batchDelete: (userId, vocabIds) => {
    return request('DELETE', '/api/vocab-book/batch-delete', {
      userId,
      vocab_ids: vocabIds
    });
  },

  getStats: (userId) => {
    return request('GET', `/api/vocab-book/stats?userId=${userId}`);
  },

  checkExists: (userId, word) => {
    return request('GET', `/api/vocab-book/check-exists?userId=${userId}&word=${word}`);
  },

  cleanText: (userId, text, maxWords = 50, useAi = true) => {
    return request('POST', '/api/vocab-book/clean', {
      user_id: userId,
      text,
      max_words: maxWords,
      use_ai: useAi
    });
  },

  importBatch: (userId, words, sourceType = 'paste', rawText = '') => {
    return request('POST', '/api/vocab-book/import', {
      user_id: userId,
      words,
      source_type: sourceType,
      raw_text: rawText
    });
  }
};

/**
 * V2.0 统计相关API
 */
const statsApi = {
  getOverview: (userId) => {
    return request('GET', `/api/stats/overview?user_id=${userId}`);
  },

  getTrend: (userId) => {
    return request('GET', `/api/stats/trend?user_id=${userId}`);
  },

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
  add: (userId, vocabId, sentence, translation) => {
    return request('POST', '/api/favorites/add', {
      user_id: userId,
      vocab_id: vocabId,
      sentence,
      translation
    });
  },

  getList: (userId) => {
    return request('GET', `/api/favorites/list?user_id=${userId}`);
  },

  delete: (userId, favoriteId) => {
    return request('DELETE', '/api/favorites/delete', {
      user_id: userId,
      favorite_id: favoriteId
    });
  },

  check: (userId, vocabId, sentence) => {
    return request('GET', `/api/favorites/check?user_id=${userId}&vocab_id=${vocabId}&sentence=${encodeURIComponent(sentence)}`);
  }
};

/**
 * 语音朗读
 */
const voiceApi = {
  speak: (text, lang = 'en_US') => {
    return new Promise((resolve, reject) => {
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

  getVoices: () => {
    return request('GET', '/api/tts/voices');
  },

  clearCache: () => {
    return request('DELETE', '/api/tts/clear-cache');
  }
};

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

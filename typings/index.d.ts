/// <reference path="./types/index.d.ts" />

// 自定义用户信息类型，包含后端返回的userId
interface CustomUserInfo {
  userId: number;
  nickname: string;
  avatarUrl: string;
  createdAt: string;
  updatedAt?: string;
}

interface IAppOption {
  globalData: {
    userInfo?: CustomUserInfo | null,
  }
  userInfoReadyCallback?: WechatMiniprogram.GetUserInfoSuccessCallback,
}
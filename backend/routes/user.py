#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户相关API路由
"""

from flask import Blueprint, request, jsonify
from models import get_db_session, User
from datetime import datetime

user_bp = Blueprint("user", __name__, url_prefix="/api/user")


def success_response(data=None, message="操作成功"):
    """成功响应"""
    return jsonify({"code": 0, "data": data or {}, "message": message})


def error_response(message="操作失败", code=1):
    """错误响应"""
    return jsonify({"code": code, "data": {}, "message": message})


@user_bp.route("/login", methods=["POST"])
def login():
    """
    用户登录（模拟微信登录）

    请求参数:
        - openid: 用户微信openid（实际应从微信获取）
        - nickname: 昵称（可选）
        - avatar_url: 头像URL（可选）

    返回:
        - user_id: 用户ID
        - nickname: 昵称
        - avatar_url: 头像
    """
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    openid = data.get("openid")
    if not openid:
        return error_response("openid不能为空")

    session = get_db_session()
    try:
        # 查找或创建用户
        user = session.query(User).filter_by(openid=openid).first()

        if user:
            # 更新用户信息
            if data.get("nickname"):
                user.nickname = data["nickname"]
            if data.get("avatar_url"):
                user.avatar_url = data["avatar_url"]
            session.commit()
            message = "登录成功"
        else:
            # 创建新用户
            user = User(
                openid=openid,
                nickname=data.get("nickname", "微信用户"),
                avatar_url=data.get("avatar_url", ""),
            )
            session.add(user)
            session.commit()
            message = "注册并登录成功"

        return success_response(data=user.to_dict(), message=message)

    except Exception as e:
        session.rollback()
        # 记录详细错误日志
        print(f"[ERROR] 用户登录失败 - openid: {openid}, error: {str(e)}")
        return error_response("登录失败，请稍后重试")
    finally:
        session.close()


@user_bp.route("/info", methods=["GET"])
def get_user_info():
    """
    获取用户信息

    请求参数:
        - userId 或 user_id: 用户ID

    返回:
        - 用户信息详情
    """
    # 支持两种命名方式
    user_id = request.args.get("userId", type=int) or request.args.get(
        "user_id", type=int
    )

    if not user_id:
        return error_response("user_id不能为空")

    session = get_db_session()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()

        if not user:
            return error_response("用户不存在", code=404)

        return success_response(data=user.to_dict())

    except Exception as e:
        return error_response(f"获取用户信息失败: {str(e)}")
    finally:
        session.close()


@user_bp.route("/update", methods=["PUT"])
def update_user():
    """
    更新用户信息

    请求参数:
        - user_id: 用户ID
        - nickname: 新昵称（可选）
        - avatar_url: 新头像（可选）

    返回:
        - 更新后的用户信息
    """
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    # 支持两种命名方式
    user_id = data.get("userId") or data.get("user_id")
    if not user_id:
        return error_response("user_id不能为空")

    session = get_db_session()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()

        if not user:
            return error_response("用户不存在", code=404)

        # 更新字段
        if "nickname" in data:
            user.nickname = data["nickname"]
        if "avatar_url" in data:
            user.avatar_url = data["avatar_url"]

        # updated_at 字段会自动更新（onupdate=datetime.now）
        session.commit()

        return success_response(data=user.to_dict(), message="更新成功")

    except Exception as e:
        session.rollback()
        return error_response(f"更新失败: {str(e)}")
    finally:
        session.close()


@user_bp.route("/stats", methods=["GET"])
def get_user_stats():
    """
    获取用户学习统计

    请求参数:
        - userId 或 user_id: 用户ID

    返回:
        - vocab_count: 生词本单词数
        - mastered_count: 已掌握单词数
        - learning_count: 学习中单词数
    """
    # 首先打印所有请求参数
    print(f"[DEBUG] /stats 收到请求，所有参数: {dict(request.args)}")

    # 支持两种命名方式：userId（驼峰）和 user_id（下划线）
    user_id = request.args.get("userId", type=int) or request.args.get(
        "user_id", type=int
    )

    print(
        f"[DEBUG] /stats 解析结果: userId={request.args.get('userId')}, user_id={request.args.get('user_id')}, 解析后={user_id}"
    )

    if not user_id:
        return error_response("user_id不能为空")

    session = get_db_session()
    try:
        from models import VocabularyBook

        # 统计生词本数据
        vocab_count = session.query(VocabularyBook).filter_by(user_id=user_id).count()
        mastered_count = (
            session.query(VocabularyBook).filter_by(user_id=user_id, status=2).count()
        )
        learning_count = (
            session.query(VocabularyBook).filter_by(user_id=user_id, status=1).count()
        )

        stats = {
            "vocab_count": vocab_count,
            "mastered_count": mastered_count,
            "learning_count": learning_count,
            "new_count": vocab_count - mastered_count - learning_count,
        }

        return success_response(data=stats)

    except Exception as e:
        return error_response(f"获取统计失败: {str(e)}")
    finally:
        session.close()

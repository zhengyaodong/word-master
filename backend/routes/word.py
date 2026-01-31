#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单词查询相关API路由
"""

from flask import Blueprint, request, jsonify
from models import get_db_session, QueryHistory, User
from services.ollama_service import query_word_with_cache, ollama_service
from routes.v2_features import record_study
from datetime import datetime

word_bp = Blueprint("word", __name__, url_prefix="/api/word")


def success_response(data=None, message="操作成功"):
    """成功响应"""
    return jsonify({"code": 0, "data": data or {}, "message": message})


def error_response(message="操作失败", code=1):
    """错误响应"""
    return jsonify({"code": code, "data": {}, "message": message})


@word_bp.route("/query", methods=["POST"])
def query_word():
    """
    查询单词（调用Ollama AI）

    请求参数:
        - user_id: 用户ID（可选，用于记录查询历史）
        - word: 要查询的英文单词
        - use_cache: 是否使用缓存（可选，默认true）

    返回:
        - word: 单词
        - phonetic: 音标
        - part_of_speech: 词性
        - definition: 中文释义
        - english_definition: 英文释义
        - examples: 例句列表
        - memory_tips: 记忆技巧
        - from_cache: 是否来自缓存
    """
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    word = data.get("word", "").strip()
    if not word:
        return error_response("单词不能为空")

    # 验证单词格式（只允许英文字母）
    if not word.isalpha():
        return error_response("单词只能包含英文字母")

    # 支持两种命名方式：userId（驼峰）和 user_id（下划线）
    user_id = data.get("userId") or data.get("user_id")
    use_cache = data.get("use_cache", True)

    session = get_db_session()
    try:
        # 检查Ollama服务是否可用
        if not ollama_service.is_available():
            return error_response(
                "Ollama服务不可用，请确保:\n1. Ollama已启动\n2. 模型qwen3:0.6b已下载",
                code=503,
            )

        # 调用Ollama查询单词
        result = query_word_with_cache(word, use_cache)

        # 记录查询历史（如果提供了user_id）
        if user_id:
            try:
                history = QueryHistory(
                    user_id=user_id,
                    word=word.lower(),
                )
                history.set_result(result)
                session.add(history)
                session.commit()

                # V2.0: 记录学习统计和打卡
                record_study(user_id, query_increment=1)
            except Exception as e:
                session.rollback()
                print(f"[ERROR] 记录查询历史失败: {e}")
                import traceback

                traceback.print_exc()

        return success_response(
            data=result,
            message="查询成功" if not result.get("from_cache") else "来自缓存",
        )

    except Exception as e:
        return error_response(f"查询失败: {str(e)}")
    finally:
        session.close()


@word_bp.route("/history", methods=["GET"])
def get_query_history():
    """
    获取查询历史

    请求参数:
        - user_id: 用户ID
        - page: 页码（默认1）
        - page_size: 每页数量（默认20）

    返回:
        - total: 总记录数
        - list: 历史记录列表
    """
    # 支持两种命名方式：userId（驼峰）和 user_id（下划线）
    user_id = request.args.get("userId", type=int) or request.args.get(
        "user_id", type=int
    )
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 20, type=int)

    if not user_id:
        return error_response("user_id不能为空")

    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 20

    session = get_db_session()
    try:
        # 查询总数
        total = session.query(QueryHistory).filter_by(user_id=user_id).count()

        # 分页查询
        histories = (
            session.query(QueryHistory)
            .filter_by(user_id=user_id)
            .order_by(QueryHistory.query_time.desc())
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        result = {
            "total": total,
            "page": page,
            "page_size": page_size,
            "list": [h.to_dict() for h in histories],
        }

        return success_response(data=result)

    except Exception as e:
        return error_response(f"获取历史记录失败: {str(e)}")
    finally:
        session.close()


@word_bp.route("/history/clear", methods=["DELETE"])
def clear_query_history():
    """
    清空查询历史

    请求参数:
        - user_id: 用户ID

    返回:
        - deleted_count: 删除的记录数
    """
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    # 支持两种命名方式：userId（驼峰）和 user_id（下划线）
    user_id = data.get("userId") or data.get("user_id")
    if not user_id:
        return error_response("user_id不能为空")

    session = get_db_session()
    try:
        # 删除该用户的所有查询历史
        deleted = session.query(QueryHistory).filter_by(user_id=user_id).delete()
        session.commit()

        return success_response(
            data={"deleted_count": deleted}, message=f"成功清空{deleted}条历史记录"
        )

    except Exception as e:
        session.rollback()
        return error_response(f"清空历史记录失败: {str(e)}")
    finally:
        session.close()


@word_bp.route("/check", methods=["GET"])
def check_service():
    """
    检查Ollama服务状态

    返回:
        - available: 是否可用
        - model: 使用的模型
        - message: 状态信息
    """
    available = ollama_service.is_available()

    return success_response(
        data={
            "available": available,
            "model": ollama_service.model,
            "base_url": ollama_service.base_url,
        },
        message="服务正常" if available else "服务不可用",
    )

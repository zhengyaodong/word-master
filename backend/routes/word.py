#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word query related API routes.
"""

from flask import Blueprint, request, jsonify
from models import get_db_session, QueryHistory, User, VocabularyBook
from services.ollama_service import query_word_with_cache, ollama_service
from routes.v2_features import record_study

word_bp = Blueprint("word", __name__, url_prefix="/api/word")


def success_response(data=None, message="操作成功"):
    return jsonify({"code": 0, "data": data or {}, "message": message})


def error_response(message="操作失败", code=1):
    return jsonify({"code": code, "data": {}, "message": message})


@word_bp.route("/query", methods=["POST"])
def query_word():
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    word = data.get("word", "").strip()
    if not word:
        return error_response("单词不能为空")

    if not word.isalpha():
        return error_response("单词只能包含英文字母")

    user_id = data.get("userId") or data.get("user_id")
    use_cache = data.get("use_cache", True)

    session = get_db_session()
    try:
        if not ollama_service.is_available():
            return error_response(
                "Ollama服务不可用，请确认：\n1. Ollama已启动\n2. 模型 qwen3:0.6b 已下载",
                code=503,
            )

        result = query_word_with_cache(word, use_cache)

        if user_id:
            try:
                history = QueryHistory(user_id=user_id, word=word.lower())
                history.set_result(result)
                session.add(history)
                session.commit()

                record_study(user_id, query_increment=1)
            except Exception as e:
                session.rollback()
                print(f"[ERROR] 记录查询历史失败: {e}")

            # 如果该词已在生词本中，更新其详情以便后续查看
            try:
                vocab = (
                    session.query(VocabularyBook)
                    .filter_by(user_id=user_id, word=word.lower())
                    .first()
                )
                if vocab:
                    vocab.phonetic = result.get("phonetic", vocab.phonetic)
                    vocab.definition = result.get("definition", vocab.definition)
                    vocab.english_definition = result.get(
                        "english_definition", vocab.english_definition
                    )
                    if result.get("examples"):
                        vocab.set_examples(result.get("examples"))
                    vocab.memory_tips = result.get("memory_tips", vocab.memory_tips)
                    session.commit()
            except Exception:
                session.rollback()

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
        total = session.query(QueryHistory).filter_by(user_id=user_id).count()

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
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    user_id = data.get("userId") or data.get("user_id")
    if not user_id:
        return error_response("user_id不能为空")

    session = get_db_session()
    try:
        deleted = session.query(QueryHistory).filter_by(user_id=user_id).delete()
        session.commit()

        return success_response(
            data={"deleted_count": deleted}, message=f"成功清空{deleted}条记录"
        )

    except Exception as e:
        session.rollback()
        return error_response(f"清空历史记录失败: {str(e)}")
    finally:
        session.close()


@word_bp.route("/check", methods=["GET"])
def check_service():
    available = ollama_service.is_available()

    return success_response(
        data={
            "available": available,
            "model": ollama_service.model,
            "base_url": ollama_service.base_url,
        },
        message="服务正常" if available else "服务不可用",
    )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生词本相关API路由
"""

from flask import Blueprint, request, jsonify
from models import get_db_session, VocabularyBook, User
from datetime import datetime
import json

vocab_book_bp = Blueprint("vocab_book", __name__, url_prefix="/api/vocab-book")


def success_response(data=None, message="操作成功"):
    """成功响应"""
    return jsonify({"code": 0, "data": data or {}, "message": message})


def error_response(message="操作失败", code=1):
    """错误响应"""
    return jsonify({"code": code, "data": {}, "message": message})


@vocab_book_bp.route("/add", methods=["POST"])
def add_to_vocab_book():
    """
    添加单词到生词本

    请求参数:
        - user_id: 用户ID
        - word: 单词
        - phonetic: 音标（可选）
        - definition: 中文释义
        - english_definition: 英文释义（可选）
        - examples: 例句列表（可选）
        - memory_tips: 记忆技巧（可选）

    返回:
        - vocab_id: 生词ID
    """
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    # 支持两种命名方式：userId（驼峰）和 user_id（下划线）
    user_id = data.get("userId") or data.get("user_id")
    word = data.get("word", "").strip()

    if not user_id:
        return error_response("user_id不能为空")
    if not word:
        return error_response("单词不能为空")

    session = get_db_session()
    try:
        # 检查用户是否存在
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            return error_response("用户不存在", code=404)

        # 检查单词是否已存在
        existing = (
            session.query(VocabularyBook)
            .filter_by(user_id=user_id, word=word.lower())
            .first()
        )

        if existing:
            return error_response("该单词已在生词本中", code=409)

        # 处理 memory_tips，如果是列表则转换为字符串
        memory_tips = data.get("memory_tips", "")
        if isinstance(memory_tips, list):
            memory_tips = " ".join(memory_tips)

        # 创建生词记录
        vocab = VocabularyBook(
            user_id=user_id,
            word=word.lower(),
            phonetic=data.get("phonetic", ""),
            definition=data.get("definition", ""),
            english_definition=data.get("english_definition", ""),
            memory_tips=memory_tips,
            status=0,  # 默认未学习
        )

        # 设置例句
        if data.get("examples"):
            vocab.set_examples(data["examples"])

        session.add(vocab)
        session.commit()

        return success_response(data={"vocab_id": vocab.vocab_id}, message="添加成功")

    except Exception as e:
        session.rollback()
        return error_response(f"添加失败: {str(e)}")
    finally:
        session.close()


@vocab_book_bp.route("/list", methods=["GET"])
def get_vocab_list():
    """
    获取生词本列表

    请求参数:
        - user_id: 用户ID
        - page: 页码（默认1）
        - page_size: 每页数量（默认20）
        - status: 状态筛选（可选：0-未学习, 1-学习中, 2-已掌握）
        - sort_by: 排序方式（默认created_at，可选：word, status）
        - order: 排序顺序（默认desc，可选：asc）

    返回:
        - total: 总记录数
        - list: 生词列表
    """
    # 支持两种命名方式：userId（驼峰）和 user_id（下划线）
    user_id = request.args.get("userId", type=int) or request.args.get(
        "user_id", type=int
    )
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 20, type=int)
    status = request.args.get("status", type=int)
    sort_by = request.args.get("sort_by", "created_at")
    order = request.args.get("order", "desc")

    if not user_id:
        return error_response("user_id不能为空")

    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 20

    session = get_db_session()
    try:
        # 构建查询
        query = session.query(VocabularyBook).filter_by(user_id=user_id)

        # 状态筛选
        if status is not None:
            query = query.filter_by(status=status)

        # 排序
        if sort_by == "word":
            order_column = VocabularyBook.word
        elif sort_by == "status":
            order_column = VocabularyBook.status
        else:
            order_column = VocabularyBook.created_at

        if order == "asc":
            query = query.order_by(order_column.asc())
        else:
            query = query.order_by(order_column.desc())

        # 查询总数
        total = query.count()

        # 分页
        vocabs = query.offset((page - 1) * page_size).limit(page_size).all()

        result = {
            "total": total,
            "page": page,
            "page_size": page_size,
            "list": [v.to_dict() for v in vocabs],
        }

        return success_response(data=result)

    except Exception as e:
        return error_response(f"获取生词本失败: {str(e)}")
    finally:
        session.close()


@vocab_book_bp.route("/detail", methods=["GET"])
def get_vocab_detail():
    """
    获取生词详情

    请求参数:
        - user_id: 用户ID
        - vocab_id: 生词ID

    返回:
        - 生词详细信息
    """
    # 支持两种命名方式：userId（驼峰）和 user_id（下划线）
    user_id = request.args.get("userId", type=int) or request.args.get(
        "user_id", type=int
    )
    vocab_id = request.args.get("vocab_id", type=int)

    if not user_id:
        return error_response("user_id不能为空")
    if not vocab_id:
        return error_response("vocab_id不能为空")

    session = get_db_session()
    try:
        vocab = (
            session.query(VocabularyBook)
            .filter_by(user_id=user_id, vocab_id=vocab_id)
            .first()
        )

        if not vocab:
            return error_response("生词不存在", code=404)

        return success_response(data=vocab.to_dict())

    except Exception as e:
        return error_response(f"获取详情失败: {str(e)}")
    finally:
        session.close()


@vocab_book_bp.route("/update", methods=["PUT"])
def update_vocab():
    """
    更新生词信息

    请求参数:
        - user_id: 用户ID
        - vocab_id: 生词ID
        - status: 学习状态（可选：0-未学习, 1-学习中, 2-已掌握）
        - phonetic: 音标（可选）
        - definition: 中文释义（可选）
        - memory_tips: 记忆技巧（可选）

    返回:
        - 更新后的生词信息
    """
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    # 支持两种命名方式：userId（驼峰）和 user_id（下划线）
    user_id = data.get("userId") or data.get("user_id")
    vocab_id = data.get("vocab_id")

    if not user_id:
        return error_response("user_id不能为空")
    if not vocab_id:
        return error_response("vocab_id不能为空")

    session = get_db_session()
    try:
        vocab = (
            session.query(VocabularyBook)
            .filter_by(user_id=user_id, vocab_id=vocab_id)
            .first()
        )

        if not vocab:
            return error_response("生词不存在", code=404)

        # 更新字段
        if "status" in data:
            status = data["status"]
            # 确保status是整数类型
            try:
                status = int(status)
            except (ValueError, TypeError):
                return error_response("状态值必须为整数(0,1,2)")
            if status not in [0, 1, 2]:
                return error_response("状态值必须为0、1或2")
            vocab.status = status

        if "phonetic" in data:
            vocab.phonetic = data["phonetic"]
        if "definition" in data:
            vocab.definition = data["definition"]
        if "english_definition" in data:
            vocab.english_definition = data["english_definition"]
        if "memory_tips" in data:
            vocab.memory_tips = data["memory_tips"]
        if "examples" in data:
            vocab.set_examples(data["examples"])

        session.commit()

        return success_response(data=vocab.to_dict(), message="更新成功")

    except Exception as e:
        session.rollback()
        return error_response(f"更新失败: {str(e)}")
    finally:
        session.close()


@vocab_book_bp.route("/delete", methods=["DELETE"])
def delete_vocab():
    """
    删除生词

    请求参数:
        - user_id: 用户ID
        - vocab_id: 生词ID

    返回:
        - 删除结果
    """
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    # 支持两种命名方式：userId（驼峰）和 user_id（下划线）
    user_id = data.get("userId") or data.get("user_id")
    vocab_id = data.get("vocab_id")

    if not user_id:
        return error_response("user_id不能为空")
    if not vocab_id:
        return error_response("vocab_id不能为空")

    session = get_db_session()
    try:
        vocab = (
            session.query(VocabularyBook)
            .filter_by(user_id=user_id, vocab_id=vocab_id)
            .first()
        )

        if not vocab:
            return error_response("生词不存在", code=404)

        word = vocab.word
        session.delete(vocab)
        session.commit()

        return success_response(
            data={"deleted_word": word}, message=f"已删除单词: {word}"
        )

    except Exception as e:
        session.rollback()
        return error_response(f"删除失败: {str(e)}")
    finally:
        session.close()


@vocab_book_bp.route("/batch-delete", methods=["DELETE"])
def batch_delete_vocab():
    """
    批量删除生词

    请求参数:
        - user_id: 用户ID
        - vocab_ids: 生词ID列表

    返回:
        - deleted_count: 删除的数量
    """
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    # 支持两种命名方式：userId（驼峰）和 user_id（下划线）
    user_id = data.get("userId") or data.get("user_id")
    vocab_ids = data.get("vocab_ids", [])

    if not user_id:
        return error_response("user_id不能为空")
    if not vocab_ids or not isinstance(vocab_ids, list):
        return error_response("vocab_ids必须是列表")

    session = get_db_session()
    try:
        # 批量删除
        deleted = (
            session.query(VocabularyBook)
            .filter(
                VocabularyBook.user_id == user_id,
                VocabularyBook.vocab_id.in_(vocab_ids),
            )
            .delete(synchronize_session=False)
        )

        session.commit()

        return success_response(
            data={"deleted_count": deleted}, message=f"成功删除{deleted}个单词"
        )

    except Exception as e:
        session.rollback()
        return error_response(f"批量删除失败: {str(e)}")
    finally:
        session.close()


@vocab_book_bp.route("/stats", methods=["GET"])
def get_vocab_stats():
    """
    获取生词本统计

    请求参数:
        - user_id: 用户ID

    返回:
        - total_count: 总单词数
        - mastered_count: 已掌握数
        - learning_count: 学习中数
        - new_count: 未学习数
    """
    # 支持两种命名方式：userId（驼峰）和 user_id（下划线）
    user_id = request.args.get("userId", type=int) or request.args.get(
        "user_id", type=int
    )

    if not user_id:
        return error_response("user_id不能为空")

    session = get_db_session()
    try:
        total = session.query(VocabularyBook).filter_by(user_id=user_id).count()
        mastered = (
            session.query(VocabularyBook).filter_by(user_id=user_id, status=2).count()
        )
        learning = (
            session.query(VocabularyBook).filter_by(user_id=user_id, status=1).count()
        )
        new_count = (
            session.query(VocabularyBook).filter_by(user_id=user_id, status=0).count()
        )

        stats = {
            "total_count": total,
            "mastered_count": mastered,
            "learning_count": learning,
            "new_count": new_count,
        }

        return success_response(data=stats)

    except Exception as e:
        return error_response(f"获取统计失败: {str(e)}")
    finally:
        session.close()


@vocab_book_bp.route("/check-exists", methods=["GET"])
def check_word_exists():
    """
    检查单词是否已在生词本中

    请求参数:
        - user_id: 用户ID
        - word: 单词

    返回:
        - exists: 是否存在
        - vocab_id: 如果存在，返回生词ID
    """
    # 支持两种命名方式：userId（驼峰）和 user_id（下划线）
    user_id = request.args.get("userId", type=int) or request.args.get(
        "user_id", type=int
    )
    word = request.args.get("word", "").strip()

    if not user_id:
        return error_response("user_id不能为空")
    if not word:
        return error_response("单词不能为空")

    session = get_db_session()
    try:
        vocab = (
            session.query(VocabularyBook)
            .filter_by(user_id=user_id, word=word.lower())
            .first()
        )

        result = {
            "exists": vocab is not None,
            "vocab_id": vocab.vocab_id if vocab else None,
        }

        return success_response(data=result)

    except Exception as e:
        return error_response(f"检查失败: {str(e)}")
    finally:
        session.close()

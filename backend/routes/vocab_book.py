#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vocabulary book related API routes.
"""

from flask import Blueprint, request, jsonify
from models import get_db_session, VocabularyBook, User, ImportHistory
from services.ollama_service import ollama_service, query_word_with_cache
import re

vocab_book_bp = Blueprint("vocab_book", __name__, url_prefix="/api/vocab-book")


def success_response(data=None, message="操作成功"):
    return jsonify({"code": 0, "data": data or {}, "message": message})


def error_response(message="操作失败", code=1):
    return jsonify({"code": code, "data": {}, "message": message})


def normalize_words(words):
    normalized = []
    seen = set()
    for w in words:
        if not isinstance(w, str):
            continue
        word = w.strip().lower()
        if not word:
            continue
        if not re.match(r"^[a-zA-Z]+$", word):
            continue
        if word in seen:
            continue
        seen.add(word)
        normalized.append(word)
    return normalized


@vocab_book_bp.route("/add", methods=["POST"])
def add_to_vocab_book():
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    user_id = data.get("userId") or data.get("user_id")
    word = data.get("word", "").strip()

    if not user_id:
        return error_response("user_id不能为空")
    if not word:
        return error_response("单词不能为空")

    session = get_db_session()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            return error_response("用户不存在", code=404)

        existing = (
            session.query(VocabularyBook)
            .filter_by(user_id=user_id, word=word.lower())
            .first()
        )

        if existing:
            return error_response("该单词已在生词本中", code=409)

        memory_tips = data.get("memory_tips", "")
        if isinstance(memory_tips, list):
            memory_tips = " ".join(memory_tips)

        vocab = VocabularyBook(
            user_id=user_id,
            word=word.lower(),
            phonetic=data.get("phonetic", ""),
            definition=data.get("definition", ""),
            english_definition=data.get("english_definition", ""),
            memory_tips=memory_tips,
            status=0,
        )

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
        query = session.query(VocabularyBook).filter_by(user_id=user_id)

        if status is not None:
            query = query.filter_by(status=status)

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

        total = query.count()
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

        # V3.0: 如果详情为空，尝试自动填充
        auto_fill = request.args.get("auto_fill", "true").lower() != "false"
        if auto_fill and (not vocab.definition or not vocab.examples):
            try:
                if ollama_service.is_available():
                    result = query_word_with_cache(vocab.word, use_cache=True)
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

        return success_response(data=vocab.to_dict())

    except Exception as e:
        return error_response(f"获取详情失败: {str(e)}")
    finally:
        session.close()


@vocab_book_bp.route("/update", methods=["PUT"])
def update_vocab():
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

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

        if "status" in data:
            try:
                status = int(data["status"])
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
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

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
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    user_id = data.get("userId") or data.get("user_id")
    vocab_ids = data.get("vocab_ids", [])

    if not user_id:
        return error_response("user_id不能为空")
    if not vocab_ids or not isinstance(vocab_ids, list):
        return error_response("vocab_ids必须是列表")

    session = get_db_session()
    try:
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


@vocab_book_bp.route("/clean", methods=["POST"])
def clean_text():
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    user_id = data.get("userId") or data.get("user_id")
    text = data.get("text") or data.get("content") or ""
    max_words = data.get("max_words", 50)
    use_ai = data.get("use_ai", True)

    if not user_id:
        return error_response("user_id不能为空")
    if not text.strip():
        return error_response("文本不能为空")

    try:
        max_words = int(max_words)
    except (ValueError, TypeError):
        max_words = 50
    if max_words < 1:
        max_words = 50
    if max_words > 200:
        max_words = 200

    try:
        words = ollama_service.extract_keywords(text, max_words=max_words, use_ai=use_ai)
        words = normalize_words(words)
        return success_response(data={"words": words, "count": len(words)})
    except Exception as e:
        return error_response(f"洗词失败: {str(e)}")


@vocab_book_bp.route("/import", methods=["POST"])
def import_words():
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    user_id = data.get("userId") or data.get("user_id")
    words = data.get("words")
    source_type = data.get("source_type", "paste")
    raw_text = data.get("raw_text", "")

    if not user_id:
        return error_response("user_id不能为空")
    if not isinstance(words, list) or not words:
        return error_response("words必须为非空列表")

    normalized = normalize_words(words)
    if not normalized:
        return error_response("没有可导入的单词")

    session = get_db_session()
    try:
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            return error_response("用户不存在", code=404)

        existing = (
            session.query(VocabularyBook.word)
            .filter(VocabularyBook.user_id == user_id, VocabularyBook.word.in_(normalized))
            .all()
        )
        existing_set = {w[0] for w in existing}

        to_add = [w for w in normalized if w not in existing_set]

        for word in to_add:
            session.add(
                VocabularyBook(
                    user_id=user_id,
                    word=word,
                    status=0,
                )
            )

        session.commit()

        try:
            history = ImportHistory(
                user_id=user_id,
                source_type=source_type,
                raw_text=raw_text if raw_text else None,
                word_count=len(normalized),
            )
            session.add(history)
            session.commit()
        except Exception:
            session.rollback()

        return success_response(
            data={
                "total": len(normalized),
                "added_count": len(to_add),
                "skipped_count": len(normalized) - len(to_add),
                "added_words": to_add,
            },
            message="导入完成",
        )

    except Exception as e:
        session.rollback()
        return error_response(f"导入失败: {str(e)}")
    finally:
        session.close()

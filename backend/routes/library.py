#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内置词库API路由
提供词库列表、单词学习、复习计划等功能
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import func
from models import (
    get_db_session,
    WordLibrary,
    LibraryWord,
    UserLibraryProgress,
    User,
    VocabularyBook,
)

library_bp = Blueprint("library", __name__, url_prefix="/api/library")


def success_response(data=None, message="操作成功"):
    return jsonify({"code": 0, "data": data or {}, "message": message})


def error_response(message="操作失败", code=1):
    return jsonify({"code": code, "data": {}, "message": message})


@library_bp.route("/list", methods=["GET"])
def get_libraries():
    """获取所有可用词库"""
    session = get_db_session()
    try:
        libraries = session.query(WordLibrary).filter_by(is_builtin=1).all()

        result = []
        for lib in libraries:
            lib_dict = lib.to_dict()
            # 统计用户学习进度（如果有user_id参数）
            user_id = request.args.get("user_id", type=int)
            if user_id:
                status_counts = (
                    session.query(UserLibraryProgress.status, func.count())
                    .filter_by(user_id=user_id, library_id=lib.library_id)
                    .group_by(UserLibraryProgress.status)
                    .all()
                )

                counts = {s: c for s, c in status_counts}
                total_progress = sum(counts.values())

                if total_progress == 0:
                    not_started = lib.total_words
                    learning = 0
                    mastered = 0
                    need_review = 0
                else:
                    not_started = counts.get(0, 0) + max(
                        lib.total_words - total_progress, 0
                    )
                    learning = counts.get(1, 0)
                    mastered = counts.get(2, 0)
                    need_review = counts.get(3, 0)

                lib_dict["user_learned"] = mastered
                lib_dict["progress_stats"] = {
                    "total": lib.total_words,
                    "not_started": not_started,
                    "learning": learning,
                    "mastered": mastered,
                    "need_review": need_review,
                }
            result.append(lib_dict)

        return success_response(data={"libraries": result})
    except Exception as e:
        return error_response(f"获取词库失败: {str(e)}")
    finally:
        session.close()


@library_bp.route("/words", methods=["GET"])
def get_library_words():
    """获取词库中的单词列表"""
    library_id = request.args.get("library_id", type=int)
    user_id = request.args.get("user_id", type=int)
    page = request.args.get("page", 1, type=int)
    page_size = request.args.get("page_size", 50, type=int)
    difficulty = request.args.get("difficulty", type=int)
    status = request.args.get("status", type=int)  # 筛选学习状态

    if not library_id:
        return error_response("library_id不能为空")

    if page < 1:
        page = 1
    if page_size < 1 or page_size > 100:
        page_size = 50

    session = get_db_session()
    try:
        # 检查词库是否存在
        library = session.query(WordLibrary).filter_by(library_id=library_id).first()
        if not library:
            return error_response("词库不存在", code=404)

        # 若按状态筛选，直接关联进度表查询，保证分页与总数准确
        if status is not None and user_id:
            query = (
                session.query(LibraryWord, UserLibraryProgress)
                .join(
                    UserLibraryProgress,
                    (UserLibraryProgress.library_id == LibraryWord.library_id)
                    & (UserLibraryProgress.word == LibraryWord.word),
                )
                .filter(
                    UserLibraryProgress.user_id == user_id,
                    LibraryWord.library_id == library_id,
                    UserLibraryProgress.status == status,
                )
            )

            if difficulty:
                query = query.filter(LibraryWord.difficulty == difficulty)

            total = query.count()
            rows = query.offset((page - 1) * page_size).limit(page_size).all()

            result = []
            for word, progress in rows:
                word_dict = word.to_dict()
                word_dict["progress"] = progress.to_dict() if progress else None
                result.append(word_dict)

            return success_response(
                data={
                    "library": library.to_dict(),
                    "total": total,
                    "page": page,
                    "page_size": page_size,
                    "words": result,
                }
            )

        # 基础查询（不按状态筛选）
        query = session.query(LibraryWord).filter_by(library_id=library_id)

        if difficulty:
            query = query.filter_by(difficulty=difficulty)

        total = query.count()
        words = query.offset((page - 1) * page_size).limit(page_size).all()

        # 获取用户学习进度（批量）
        progress_map = {}
        if user_id and words:
            word_list = [w.word for w in words]
            progresses = (
                session.query(UserLibraryProgress)
                .filter(
                    UserLibraryProgress.user_id == user_id,
                    UserLibraryProgress.library_id == library_id,
                    UserLibraryProgress.word.in_(word_list),
                )
                .all()
            )
            progress_map = {p.word: p for p in progresses}

        result = []
        for word in words:
            word_dict = word.to_dict()
            if user_id:
                progress = progress_map.get(word.word)
                word_dict["progress"] = progress.to_dict() if progress else None
            result.append(word_dict)

        return success_response(
            data={
                "library": library.to_dict(),
                "total": total,
                "page": page,
                "page_size": page_size,
                "words": result,
            }
        )
    except Exception as e:
        return error_response(f"获取单词失败: {str(e)}")
    finally:
        session.close()


@library_bp.route("/random", methods=["GET"])
def get_random_words():
    """获取词库随机单词"""
    library_id = request.args.get("library_id", type=int)
    user_id = request.args.get("user_id", type=int)
    limit = request.args.get("limit", 20, type=int)
    exclude_mastered = request.args.get("exclude_mastered", "true").lower() != "false"

    if not library_id:
        return error_response("library_id不能为空")

    if limit < 1:
        limit = 20
    if limit > 100:
        limit = 100

    session = get_db_session()
    try:
        library = session.query(WordLibrary).filter_by(library_id=library_id).first()
        if not library:
            return error_response("词库不存在", code=404)

        query = session.query(LibraryWord).filter_by(library_id=library_id)
        if user_id and exclude_mastered:
            # Exclude mastered words (status=2) for this user/library.
            subq = (
                session.query(UserLibraryProgress.word)
                .filter_by(user_id=user_id, library_id=library_id, status=2)
                .subquery()
            )
            query = query.filter(~LibraryWord.word.in_(subq))

        words = query.order_by(func.random()).limit(limit).all()

        progress_map = {}
        if user_id and words:
            word_list = [w.word for w in words]
            progresses = (
                session.query(UserLibraryProgress)
                .filter(
                    UserLibraryProgress.user_id == user_id,
                    UserLibraryProgress.library_id == library_id,
                    UserLibraryProgress.word.in_(word_list),
                )
                .all()
            )
            progress_map = {p.word: p for p in progresses}

        result = []
        for word in words:
            word_dict = word.to_dict()
            if user_id:
                progress = progress_map.get(word.word)
                word_dict["progress"] = progress.to_dict() if progress else None
            result.append(word_dict)

        return success_response(
            data={
                "library": library.to_dict(),
                "total": library.total_words,
                "words": result,
            }
        )
    except Exception as e:
        return error_response(f"获取随机单词失败: {str(e)}")
    finally:
        session.close()


@library_bp.route("/start", methods=["POST"])
def start_learning():
    """开始学习某个词库"""
    data = request.get_json()
    user_id = data.get("user_id")
    library_id = data.get("library_id")

    if not user_id or not library_id:
        return error_response("user_id和library_id不能为空")

    session = get_db_session()
    try:
        # 检查用户和词库
        user = session.query(User).filter_by(user_id=user_id).first()
        if not user:
            return error_response("用户不存在", code=404)

        library = session.query(WordLibrary).filter_by(library_id=library_id).first()
        if not library:
            return error_response("词库不存在", code=404)

        # 获取词库所有单词
        words = session.query(LibraryWord).filter_by(library_id=library_id).all()

        # 初始化学习进度（如果不存在）
        initialized = 0
        for word in words:
            existing = (
                session.query(UserLibraryProgress)
                .filter_by(user_id=user_id, library_id=library_id, word=word.word)
                .first()
            )

            if not existing:
                progress = UserLibraryProgress(
                    user_id=user_id,
                    library_id=library_id,
                    word=word.word,
                    status=0,
                    next_review_at=datetime.now() + timedelta(days=1),
                )
                session.add(progress)
                initialized += 1

        session.commit()

        return success_response(
            data={"initialized_count": initialized, "total_words": len(words)},
            message=f"开始学习词库: {library.name}",
        )
    except Exception as e:
        session.rollback()
        return error_response(f"开始学习失败: {str(e)}")
    finally:
        session.close()


@library_bp.route("/review", methods=["GET"])
def get_review_words():
    """获取今日需要复习的单词（SM-2间隔重复算法）"""
    user_id = request.args.get("user_id", type=int)
    library_id = request.args.get("library_id", type=int)
    limit = request.args.get("limit", 20, type=int)

    if not user_id:
        return error_response("user_id不能为空")

    session = get_db_session()
    try:
        now = datetime.now()

        # 查询需要复习的单词
        query = session.query(UserLibraryProgress).filter(
            UserLibraryProgress.user_id == user_id,
            UserLibraryProgress.status.in_([1, 2, 3]),  # 学习中、已掌握、需复习
            UserLibraryProgress.next_review_at <= now,
        )

        if library_id:
            query = query.filter_by(library_id=library_id)

        progresses = (
            query.order_by(UserLibraryProgress.next_review_at).limit(limit).all()
        )

        result = []
        for progress in progresses:
            # 获取单词详情
            word = (
                session.query(LibraryWord)
                .filter_by(library_id=progress.library_id, word=progress.word)
                .first()
            )

            if word:
                result.append(
                    {"progress": progress.to_dict(), "word_detail": word.to_dict()}
                )

        return success_response(data={"total_due": len(result), "words": result})
    except Exception as e:
        return error_response(f"获取复习单词失败: {str(e)}")
    finally:
        session.close()


@library_bp.route("/review", methods=["POST"])
def submit_review():
    """提交复习结果，更新学习进度（SM-2算法）"""
    data = request.get_json()
    user_id = data.get("user_id")
    library_id = data.get("library_id")
    word = data.get("word")
    quality = data.get("quality")  # 0-5: 背诵质量评分

    if not all([user_id, library_id, word]):
        return error_response("参数不完整")

    if quality is None or not (0 <= quality <= 5):
        return error_response("quality评分必须是0-5之间的整数")

    session = get_db_session()
    try:
        progress = (
            session.query(UserLibraryProgress)
            .filter_by(user_id=user_id, library_id=library_id, word=word)
            .first()
        )

        if not progress:
            return error_response("学习记录不存在", code=404)

        # SM-2算法更新
        old_easiness = progress.get_easiness_factor()
        old_interval = progress.interval_days

        # 更新简易度因子
        new_easiness = old_easiness + (
            0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
        )
        new_easiness = max(1.3, new_easiness)  # 最小值1.3

        # 更新间隔天数
        if quality < 3:
            # 背诵失败，重置间隔
            new_interval = 1
            progress.status = 3  # 标记为需要复习
        else:
            # 背诵成功
            if progress.review_count == 0:
                new_interval = 1
            elif progress.review_count == 1:
                new_interval = 6
            else:
                new_interval = int(old_interval * new_easiness)

            # 更新状态
            if progress.review_count >= 3:
                progress.status = 2  # 已掌握
            else:
                progress.status = 1  # 学习中

        # 更新进度
        progress.set_easiness_factor(new_easiness)
        progress.interval_days = new_interval
        progress.next_review_at = datetime.now() + timedelta(days=new_interval)
        progress.last_review_at = datetime.now()
        progress.review_count += 1

        if quality >= 3:
            progress.correct_count += 1
        else:
            progress.wrong_count += 1

        session.commit()

        return success_response(
            data={
                "next_review": progress.next_review_at.strftime("%Y-%m-%d"),
                "interval_days": new_interval,
                "easiness_factor": new_easiness,
                "status": progress.status,
            },
            message="复习记录已更新",
        )
    except Exception as e:
        session.rollback()
        return error_response(f"更新失败: {str(e)}")
    finally:
        session.close()


@library_bp.route("/progress", methods=["GET"])
def get_progress():
    """获取用户在词库的学习进度统计"""
    user_id = request.args.get("user_id", type=int)
    library_id = request.args.get("library_id", type=int)

    if not user_id:
        return error_response("user_id不能为空")

    session = get_db_session()
    try:
        # 查询进度
        query = session.query(UserLibraryProgress).filter_by(user_id=user_id)
        if library_id:
            query = query.filter_by(library_id=library_id)

        progresses = query.all()

        # 统计
        stats = {
            "total": len(progresses),
            "not_started": sum(1 for p in progresses if p.status == 0),
            "learning": sum(1 for p in progresses if p.status == 1),
            "mastered": sum(1 for p in progresses if p.status == 2),
            "need_review": sum(1 for p in progresses if p.status == 3),
            "due_today": sum(
                1
                for p in progresses
                if p.next_review_at and p.next_review_at <= datetime.now()
            ),
        }

        # 按词库分组
        if not library_id:
            library_stats = {}
            for p in progresses:
                lib_id = p.library_id
                if lib_id not in library_stats:
                    library = (
                        session.query(WordLibrary).filter_by(library_id=lib_id).first()
                    )
                    library_stats[lib_id] = {
                        "library_name": library.name if library else "未知",
                        "total": 0,
                        "mastered": 0,
                    }
                library_stats[lib_id]["total"] += 1
                if p.status == 2:
                    library_stats[lib_id]["mastered"] += 1

            stats["by_library"] = library_stats

        return success_response(data=stats)
    except Exception as e:
        return error_response(f"获取进度失败: {str(e)}")
    finally:
        session.close()


@library_bp.route("/progress/update", methods=["POST"])
def update_progress():
    """更新单词学习状态"""
    data = request.get_json()
    user_id = data.get("user_id")
    library_id = data.get("library_id")
    word = data.get("word")
    status = data.get("status")

    if not all([user_id, library_id, word]) or status is None:
        return error_response("参数不完整")

    try:
        status = int(status)
    except (ValueError, TypeError):
        return error_response("status必须为整数")

    if status not in [0, 1, 2, 3]:
        return error_response("status必须为0-3")

    session = get_db_session()
    try:
        progress = (
            session.query(UserLibraryProgress)
            .filter_by(user_id=user_id, library_id=library_id, word=word)
            .first()
        )

        if not progress:
            progress = UserLibraryProgress(
                user_id=user_id,
                library_id=library_id,
                word=word,
                status=status,
                next_review_at=datetime.now() + timedelta(days=1),
            )
            session.add(progress)
        else:
            progress.status = status
            if status == 3:
                progress.next_review_at = datetime.now()
            elif not progress.next_review_at:
                progress.next_review_at = datetime.now() + timedelta(days=1)

        session.commit()

        return success_response(data={"status": status}, message="状态已更新")
    except Exception as e:
        session.rollback()
        return error_response(f"更新失败: {str(e)}")
    finally:
        session.close()


@library_bp.route("/add-to-vocab", methods=["POST"])
def add_to_vocab_book():
    """将词库单词添加到用户生词本"""
    data = request.get_json()
    user_id = data.get("user_id")
    library_id = data.get("library_id")
    word_text = data.get("word")

    if not all([user_id, library_id, word_text]):
        return error_response("参数不完整")

    session = get_db_session()
    try:
        # 获取单词详情
        word = (
            session.query(LibraryWord)
            .filter_by(library_id=library_id, word=word_text)
            .first()
        )

        if not word:
            return error_response("单词不存在", code=404)

        # 检查是否已存在
        existing = (
            session.query(VocabularyBook)
            .filter_by(user_id=user_id, word=word_text.lower())
            .first()
        )

        if existing:
            return error_response("该单词已在生词本中", code=409)

        # 添加到生词本
        vocab = VocabularyBook(
            user_id=user_id,
            word=word_text.lower(),
            phonetic=word.phonetic,
            definition=word.definition,
            english_definition=word.english_definition,
            status=0,
        )

        if word.examples:
            vocab.examples = word.examples

        session.add(vocab)

        # 更新学习进度状态
        progress = (
            session.query(UserLibraryProgress)
            .filter_by(user_id=user_id, library_id=library_id, word=word_text)
            .first()
        )

        if progress:
            progress.status = 1  # 标记为学习中

        session.commit()

        return success_response(
            data={"vocab_id": vocab.vocab_id}, message="已添加到生词本"
        )
    except Exception as e:
        session.rollback()
        return error_response(f"添加失败: {str(e)}")
    finally:
        session.close()

"""
V2.0 功能API路由
包含：学习统计、收藏例句
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import func
from models import get_db_session, StudyRecord, FavoriteSentence, VocabularyBook, User

stats_bp = Blueprint("stats", __name__, url_prefix="/api")
favorites_bp = Blueprint("favorites", __name__, url_prefix="/api")


@stats_bp.route("/stats/overview", methods=["GET"])
def get_stats_overview():
    """获取学习概览统计"""
    user_id = request.args.get("user_id", type=int)

    if not user_id:
        return jsonify({"code": 400, "message": "缺少user_id参数"})

    session = get_db_session()
    try:
        # 基础统计
        total_words = session.query(VocabularyBook).filter_by(user_id=user_id).count()
        mastered = (
            session.query(VocabularyBook).filter_by(user_id=user_id, status=2).count()
        )
        learning = (
            session.query(VocabularyBook).filter_by(user_id=user_id, status=1).count()
        )
        new_words = total_words - mastered - learning

        # 今日查询次数
        today = datetime.now().date()
        today_record = (
            session.query(StudyRecord)
            .filter_by(user_id=user_id, study_date=today)
            .first()
        )
        today_query = today_record.query_count if today_record else 0

        # 连续打卡天数
        consecutive_days = calculate_consecutive_days(session, user_id)

        return jsonify(
            {
                "code": 0,
                "data": {
                    "total_words": total_words,
                    "mastered": mastered,
                    "learning": learning,
                    "new": new_words,
                    "today_query": today_query,
                    "consecutive_days": consecutive_days,
                },
            }
        )
    except Exception as e:
        return jsonify({"code": 500, "message": f"统计失败: {str(e)}"})
    finally:
        session.close()


@stats_bp.route("/stats/trend", methods=["GET"])
def get_stats_trend():
    """获取近7天查询趋势"""
    user_id = request.args.get("user_id", type=int)

    if not user_id:
        return jsonify({"code": 400, "message": "缺少user_id参数"})

    session = get_db_session()
    try:
        # 获取近7天数据
        today = datetime.now().date()
        last_7_days = []

        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            record = (
                session.query(StudyRecord)
                .filter_by(user_id=user_id, study_date=date)
                .first()
            )

            last_7_days.append(
                {
                    "date": date.strftime("%m-%d"),
                    "query_count": record.query_count if record else 0,
                    "is_checked_in": bool(record.is_checked_in) if record else False,
                }
            )

        return jsonify({"code": 0, "data": {"last_7_days": last_7_days}})
    except Exception as e:
        return jsonify({"code": 500, "message": f"获取趋势失败: {str(e)}"})
    finally:
        session.close()


@stats_bp.route("/stats/checkin", methods=["POST"])
def check_in():
    """手动打卡（备用接口）"""
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"code": 400, "message": "缺少user_id"})

    session = get_db_session()
    try:
        today = datetime.now().date()
        record = (
            session.query(StudyRecord)
            .filter_by(user_id=user_id, study_date=today)
            .first()
        )

        if not record:
            record = StudyRecord(
                user_id=user_id, study_date=today, query_count=0, is_checked_in=1
            )
            session.add(record)
        else:
            record.is_checked_in = 1

        session.commit()

        return jsonify(
            {
                "code": 0,
                "message": "打卡成功",
                "data": {"is_checked_in": True, "date": today.strftime("%Y-%m-%d")},
            }
        )
    except Exception as e:
        session.rollback()
        return jsonify({"code": 500, "message": f"打卡失败: {str(e)}"})
    finally:
        session.close()


def record_study(user_id, query_increment=1):
    """记录学习（供其他接口调用）"""
    session = get_db_session()
    try:
        from datetime import datetime, date

        today = datetime.now().date()

        record = (
            session.query(StudyRecord)
            .filter_by(user_id=user_id, study_date=today)
            .first()
        )

        if not record:
            record = StudyRecord(
                user_id=user_id,
                study_date=today,
                query_count=query_increment,
                is_checked_in=True,  # 首次查询自动打卡
            )
            session.add(record)
        else:
            record.query_count = record.query_count + query_increment
            record.is_checked_in = 1  # 确保已打卡

        session.commit()
        return True
    except Exception as e:
        session.rollback()
        print(f"记录学习失败: {e}")
        return False
    finally:
        session.close()


def calculate_consecutive_days(session, user_id):
    """计算连续打卡天数"""
    today = datetime.now().date()
    consecutive = 0

    # 从昨天开始往前数
    for i in range(1, 365):  # 最多查一年
        date = today - timedelta(days=i)
        record = (
            session.query(StudyRecord)
            .filter_by(user_id=user_id, study_date=date, is_checked_in=1)
            .first()
        )

        if record:
            consecutive += 1
        else:
            break

    # 检查今天是否已打卡
    today_record = (
        session.query(StudyRecord)
        .filter_by(user_id=user_id, study_date=today, is_checked_in=1)
        .first()
    )

    if today_record:
        consecutive += 1

    return consecutive


# ==================== 收藏例句API ====================


@favorites_bp.route("/favorites/add", methods=["POST"])
def add_favorite():
    """收藏例句"""
    data = request.get_json()
    user_id = data.get("user_id")
    vocab_id = data.get("vocab_id")
    sentence = data.get("sentence")
    translation = data.get("translation", "")

    if not all([user_id, vocab_id, sentence]):
        return jsonify({"code": 400, "message": "缺少必要参数"})

    session = get_db_session()
    try:
        # 检查是否已收藏
        existing = (
            session.query(FavoriteSentence)
            .filter_by(user_id=user_id, vocab_id=vocab_id, sentence=sentence)
            .first()
        )

        if existing:
            return jsonify({"code": 400, "message": "该例句已收藏"})

        favorite = FavoriteSentence(
            user_id=user_id,
            vocab_id=vocab_id,
            sentence=sentence,
            translation=translation,
        )
        session.add(favorite)
        session.commit()

        return jsonify(
            {
                "code": 0,
                "message": "收藏成功",
                "data": {"favorite_id": favorite.favorite_id},
            }
        )
    except Exception as e:
        session.rollback()
        return jsonify({"code": 500, "message": f"收藏失败: {str(e)}"})
    finally:
        session.close()


@favorites_bp.route("/favorites/list", methods=["GET"])
def get_favorites():
    """获取收藏列表"""
    user_id = request.args.get("user_id", type=int)

    if not user_id:
        return jsonify({"code": 400, "message": "缺少user_id参数"})

    session = get_db_session()
    try:
        favorites = (
            session.query(FavoriteSentence)
            .filter_by(user_id=user_id)
            .order_by(FavoriteSentence.created_at.desc())
            .all()
        )

        # 获取单词信息
        result = []
        for fav in favorites:
            vocab = (
                session.query(VocabularyBook).filter_by(vocab_id=fav.vocab_id).first()
            )

            result.append(
                {
                    "favorite_id": fav.favorite_id,
                    "vocab_id": fav.vocab_id,
                    "word": vocab.word if vocab else "未知",
                    "sentence": fav.sentence,
                    "translation": fav.translation,
                    "created_at": fav.created_at.strftime("%Y-%m-%d %H:%M:%S")
                    if fav.created_at
                    else None,
                }
            )

        return jsonify({"code": 0, "data": {"total": len(result), "list": result}})
    except Exception as e:
        return jsonify({"code": 500, "message": f"获取失败: {str(e)}"})
    finally:
        session.close()


@favorites_bp.route("/favorites/delete", methods=["DELETE"])
def delete_favorite():
    """删除收藏"""
    data = request.get_json()
    user_id = data.get("user_id")
    favorite_id = data.get("favorite_id")

    if not all([user_id, favorite_id]):
        return jsonify({"code": 400, "message": "缺少必要参数"})

    session = get_db_session()
    try:
        favorite = (
            session.query(FavoriteSentence)
            .filter_by(favorite_id=favorite_id, user_id=user_id)
            .first()
        )

        if not favorite:
            return jsonify({"code": 404, "message": "收藏记录不存在"})

        session.delete(favorite)
        session.commit()

        return jsonify({"code": 0, "message": "删除成功"})
    except Exception as e:
        session.rollback()
        return jsonify({"code": 500, "message": f"删除失败: {str(e)}"})
    finally:
        session.close()


@favorites_bp.route("/favorites/check", methods=["GET"])
def check_favorite():
    """检查例句是否已收藏"""
    user_id = request.args.get("user_id", type=int)
    vocab_id = request.args.get("vocab_id", type=int)
    sentence = request.args.get("sentence")

    if not all([user_id, vocab_id, sentence]):
        return jsonify({"code": 400, "message": "缺少必要参数"})

    session = get_db_session()
    try:
        favorite = (
            session.query(FavoriteSentence)
            .filter_by(user_id=user_id, vocab_id=vocab_id, sentence=sentence)
            .first()
        )

        return jsonify(
            {
                "code": 0,
                "data": {
                    "is_favorite": favorite is not None,
                    "favorite_id": favorite.favorite_id if favorite else None,
                },
            }
        )
    except Exception as e:
        return jsonify({"code": 500, "message": f"查询失败: {str(e)}"})
    finally:
        session.close()

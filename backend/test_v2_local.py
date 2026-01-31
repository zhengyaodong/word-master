#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2.0 API 本地测试（无需启动服务）
直接测试数据库模型和API函数
"""

import sys
import os

# 添加backend到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models import get_db_session, StudyRecord, FavoriteSentence, User, VocabularyBook
from routes.v2_features import calculate_consecutive_days, record_study
from datetime import datetime, timedelta


def test_database_tables():
    """测试数据库表是否存在"""
    print("\n" + "=" * 50)
    print("【测试1: 数据库表检查】")
    print("=" * 50)

    session = get_db_session()
    try:
        # 检查表是否存在
        from sqlalchemy import inspect

        inspector = inspect(session.bind)
        tables = inspector.get_table_names()

        print(f"数据库中的表: {tables}")

        required_tables = [
            "users",
            "vocabulary_book",
            "query_history",
            "study_record",
            "favorite_sentences",
        ]

        for table in required_tables:
            if table in tables:
                print(f"  [OK] {table} 表存在")
            else:
                print(f"  [FAIL] {table} 表缺失")

        return True
    except Exception as e:
        print(f"  [FAIL] 检查失败: {e}")
        return False
    finally:
        session.close()


def test_create_user():
    """创建测试用户"""
    print("\n" + "=" * 50)
    print("【测试2: 创建测试用户】")
    print("=" * 50)

    session = get_db_session()
    try:
        # 检查是否已有测试用户
        user = session.query(User).filter_by(openid="test_v2_user").first()

        if user:
            print(f"  [OK] 测试用户已存在: ID={user.user_id}")
            return user.user_id

        # 创建新用户
        new_user = User(openid="test_v2_user", nickname="V2测试用户")
        session.add(new_user)
        session.commit()

        print(f"  [OK] 创建测试用户成功: ID={new_user.user_id}")
        return new_user.user_id

    except Exception as e:
        session.rollback()
        print(f"  [FAIL] 创建用户失败: {e}")
        return None
    finally:
        session.close()


def test_study_record(user_id):
    """测试学习记录功能"""
    print("\n" + "=" * 50)
    print("【测试3: 学习记录功能】")
    print("=" * 50)

    # 测试记录学习
    print("  记录今日学习...")
    result = record_study(user_id, query_increment=5)

    if result:
        print("  [OK] 记录学习成功")
    else:
        print("  [FAIL] 记录学习失败")

    # 查询记录
    session = get_db_session()
    try:
        today = datetime.now().date()
        record = (
            session.query(StudyRecord)
            .filter_by(user_id=user_id, study_date=today)
            .first()
        )

        if record:
            print(f"  [OK] 查询到今日记录:")
            print(f"    - 查询次数: {record.query_count}")
            print(f"    - 是否打卡: {bool(record.is_checked_in)}")
        else:
            print("  [FAIL] 未找到今日记录")

        # 测试连续天数计算
        days = calculate_consecutive_days(session, user_id)
        print(f"  [OK] 连续打卡天数: {days}天")

    except Exception as e:
        print(f"  [FAIL] 查询失败: {e}")
    finally:
        session.close()


def test_favorite_sentences(user_id):
    """测试收藏例句功能"""
    print("\n" + "=" * 50)
    print("【测试4: 收藏例句功能】")
    print("=" * 50)

    session = get_db_session()
    try:
        # 先创建一个测试单词（如果不存在）
        vocab = (
            session.query(VocabularyBook)
            .filter_by(user_id=user_id, word="test_word")
            .first()
        )

        if not vocab:
            vocab = VocabularyBook(
                user_id=user_id, word="test_word", definition="测试单词", status=0
            )
            session.add(vocab)
            session.commit()
            print(f"  [OK] 创建测试单词: ID={vocab.vocab_id}")
        else:
            print(f"  [OK] 使用已有测试单词: ID={vocab.vocab_id}")

        # 添加收藏
        favorite = FavoriteSentence(
            user_id=user_id,
            vocab_id=vocab.vocab_id,
            sentence="This is a test sentence.",
            translation="这是一个测试例句。",
        )
        session.add(favorite)
        session.commit()

        print(f"  [OK] 添加收藏成功: ID={favorite.favorite_id}")

        # 查询收藏列表
        favorites = session.query(FavoriteSentence).filter_by(user_id=user_id).all()

        print(f"  [OK] 用户共有 {len(favorites)} 条收藏")

        for fav in favorites:
            print(f"    - {fav.sentence[:30]}...")

        # 删除测试收藏
        session.delete(favorite)
        session.commit()
        print("  [OK] 删除测试收藏成功")

        # 删除测试单词
        session.delete(vocab)
        session.commit()
        print("  [OK] 删除测试单词成功")

    except Exception as e:
        session.rollback()
        print(f"  [FAIL] 测试失败: {e}")
    finally:
        session.close()


def test_stats_calculation(user_id):
    """测试统计计算"""
    print("\n" + "=" * 50)
    print("【测试5: 统计计算】")
    print("=" * 50)

    session = get_db_session()
    try:
        # 统计单词数量
        total = session.query(VocabularyBook).filter_by(user_id=user_id).count()
        mastered = (
            session.query(VocabularyBook).filter_by(user_id=user_id, status=2).count()
        )
        learning = (
            session.query(VocabularyBook).filter_by(user_id=user_id, status=1).count()
        )

        print(f"  [OK] 单词统计:")
        print(f"    - 总数: {total}")
        print(f"    - 已掌握: {mastered}")
        print(f"    - 学习中: {learning}")

        # 近7天数据
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

        print(f"  [OK] 近7天学习记录:")
        for day in last_7_days:
            status = "[OK]" if day["is_checked_in"] else "[FAIL]"
            print(f"    - {day['date']}: {day['query_count']}次查询 [{status}]")

    except Exception as e:
        print(f"  [FAIL] 统计失败: {e}")
    finally:
        session.close()


def cleanup_test_data(user_id):
    """清理测试数据"""
    print("\n" + "=" * 50)
    print("【清理测试数据】")
    print("=" * 50)

    session = get_db_session()
    try:
        # 删除学习记录
        deleted_records = session.query(StudyRecord).filter_by(user_id=user_id).delete()
        print(f"  [OK] 删除 {deleted_records} 条学习记录")

        # 删除用户（测试用户）
        user = session.query(User).filter_by(user_id=user_id).first()
        if user and user.openid == "test_v2_user":
            session.delete(user)
            print(f"  [OK] 删除测试用户")

        session.commit()
        print("  [OK] 清理完成")

    except Exception as e:
        session.rollback()
        print(f"  [FAIL] 清理失败: {e}")
    finally:
        session.close()


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("V2.0 API 本地测试")
    print("=" * 50)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 1. 检查数据库表
    if not test_database_tables():
        print("\n[FAIL] 数据库检查失败，停止测试")
        return

    # 2. 创建测试用户
    user_id = test_create_user()
    if not user_id:
        print("\n[FAIL] 无法创建测试用户，停止测试")
        return

    # 3. 测试学习记录
    test_study_record(user_id)

    # 4. 测试收藏例句
    test_favorite_sentences(user_id)

    # 5. 测试统计计算
    test_stats_calculation(user_id)

    # 6. 清理测试数据
    cleanup_test_data(user_id)

    print("\n" + "=" * 50)
    print("[OK] 所有测试完成!")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()

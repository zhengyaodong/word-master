#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
词库导入脚本
将JSON词库文件导入到SQLite数据库
"""

import json
import os
import sys

# 添加父目录到路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from models import get_db_session, init_db
from sqlalchemy import text


def init_library_tables():
    """初始化词库表结构"""
    sql_file = os.path.join(os.path.dirname(__file__), "word_library_schema.sql")

    if not os.path.exists(sql_file):
        print(f"错误: 找不到SQL文件 {sql_file}")
        return False

    with open(sql_file, "r", encoding="utf-8") as f:
        sql = f.read()

    session = get_db_session()
    try:
        # 执行SQL创建表
        for statement in sql.split(";"):
            if statement.strip():
                session.execute(text(statement))
        session.commit()
        print("[OK] 词库表结构初始化完成")
        return True
    except Exception as e:
        session.rollback()
        print(f"[ERROR] 初始化表结构失败: {e}")
        return False
    finally:
        session.close()


def import_libraries():
    """导入词库数据"""
    json_file = os.path.join(os.path.dirname(__file__), "word_libraries.json")

    if not os.path.exists(json_file):
        print(f"错误: 找不到词库文件 {json_file}")
        return False

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    session = get_db_session()
    try:
        # 清空现有数据
        session.execute(text("DELETE FROM library_words"))
        session.execute(text("DELETE FROM word_libraries"))
        session.commit()

        # 导入词库基本信息
        library_map = {}
        for lib in data.get("libraries", []):
            result = session.execute(
                text("""
                INSERT INTO word_libraries 
                (library_id, name, description, category, level, total_words, icon_url, is_builtin)
                VALUES (:library_id, :name, :description, :category, :level, :total_words, :icon_url, :is_builtin)
                """),
                {
                    "library_id": lib["library_id"],
                    "name": lib["name"],
                    "description": lib["description"],
                    "category": lib["category"],
                    "level": lib["level"],
                    "total_words": lib["total_words"],
                    "icon_url": lib.get("icon_url", ""),
                    "is_builtin": 1 if lib.get("is_builtin", True) else 0,
                },
            )
            library_map[lib["category"]] = lib["library_id"]
            print(f"[OK] 导入词库: {lib['name']} ({lib['category']})")

        # 导入单词
        total_words = 0
        for category, words in data.get("words", {}).items():
            library_id = library_map.get(category)
            if not library_id:
                continue

            for word_data in words:
                session.execute(
                    text("""
                    INSERT INTO library_words 
                    (library_id, word, phonetic, part_of_speech, definition, english_definition, difficulty)
                    VALUES (:library_id, :word, :phonetic, :part_of_speech, :definition, :english_definition, :difficulty)
                    """),
                    {
                        "library_id": library_id,
                        "word": word_data["word"],
                        "phonetic": word_data.get("phonetic", ""),
                        "part_of_speech": word_data.get("part_of_speech", ""),
                        "definition": word_data.get("definition", ""),
                        "english_definition": word_data.get("english_definition", ""),
                        "difficulty": word_data.get("difficulty", 1),
                    },
                )
                total_words += 1

            print(f"[OK] 导入 {category} 词汇: {len(words)} 个")

        # 更新词库单词数量
        for category, library_id in library_map.items():
            count = session.execute(
                text(
                    "SELECT COUNT(*) FROM library_words WHERE library_id = :library_id"
                ),
                {"library_id": library_id},
            ).scalar()

            session.execute(
                text(
                    "UPDATE word_libraries SET total_words = :count WHERE library_id = :library_id"
                ),
                {"count": count, "library_id": library_id},
            )

        session.commit()
        print(f"\n[OK] 词库导入完成！共导入 {total_words} 个单词")
        return True

    except Exception as e:
        session.rollback()
        print(f"[ERROR] 导入失败: {e}")
        import traceback

        traceback.print_exc()
        return False
    finally:
        session.close()


def verify_import():
    """验证导入结果"""
    session = get_db_session()
    try:
        # 检查词库
        libraries = session.execute(
            text("SELECT library_id, name, category, total_words FROM word_libraries")
        ).fetchall()

        print("\n=== 词库统计 ===")
        for lib in libraries:
            print(f"  {lib.name} ({lib.category}): {lib.total_words} 词")

        # 检查示例单词
        print("\n=== 示例单词 ===")
        samples = session.execute(
            text("""
            SELECT w.word, w.phonetic, w.definition, l.name as library_name
            FROM library_words w
            JOIN word_libraries l ON w.library_id = l.library_id
            LIMIT 5
            """)
        ).fetchall()

        for s in samples:
            print(f"  {s.word} {s.phonetic} - {s.definition} [{s.library_name}]")

    except Exception as e:
        print(f"验证失败: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    print("=== 词库导入工具 ===\n")

    # 初始化数据库连接
    init_db()

    # 初始化表结构
    if init_library_tables():
        # 导入数据
        if import_libraries():
            # 验证
            verify_import()

    print("\n完成!")

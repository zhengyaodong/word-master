#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据库初始化脚本
创建数据库文件和所有表结构
"""

import os
import sys

# 添加backend目录到路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from models import init_db, engine, Base


def check_database():
    """检查数据库状态"""
    from sqlalchemy import inspect
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("\n=== 数据库状态检查 ===")
    print(f"数据库文件: {engine.url}")
    print(f"已存在的表: {tables if tables else '无'}")
    
    if tables:
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"\n表 '{table}' 的列:")
            for col in columns:
                print(f"  - {col['name']}: {col['type']}")
            
            # 显示索引
            indexes = inspector.get_indexes(table)
            if indexes:
                print(f"  索引:")
                for idx in indexes:
                    print(f"    - {idx['name']}: {idx['column_names']}")
    
    return tables


def main():
    """主函数"""
    print("=" * 50)
    print("微信小程序背单词应用 - 数据库初始化")
    print("=" * 50)
    
    # 检查数据库目录
    db_dir = os.path.join(BASE_DIR, 'database')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"\n创建数据库目录: {db_dir}")
    
    # 检查现有表
    existing_tables = check_database()
    
    if existing_tables:
        print(f"\n数据库已存在 {len(existing_tables)} 个表")
        response = input("是否重新初始化数据库？(这将删除所有数据) [y/N]: ")
        if response.lower() == 'y':
            print("\n删除现有表...")
            Base.metadata.drop_all(bind=engine)
            print("现有表已删除")
        else:
            print("\n跳过初始化，保持现有数据库")
            return
    
    # 创建所有表
    print("\n创建数据库表...")
    init_db()
    
    # 验证创建结果
    print("\n验证数据库结构...")
    tables = check_database()
    
    expected_tables = ['users', 'vocabulary_book', 'query_history']
    missing_tables = set(expected_tables) - set(tables)
    
    if missing_tables:
        print(f"\n错误: 以下表未成功创建: {missing_tables}")
        sys.exit(1)
    else:
        print(f"\n成功创建 {len(tables)} 个表:")
        for table in tables:
            print(f"  ✓ {table}")
    
    print("\n" + "=" * 50)
    print("数据库初始化完成！")
    print("=" * 50)


if __name__ == '__main__':
    main()

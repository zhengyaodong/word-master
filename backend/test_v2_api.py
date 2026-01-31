#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2.0 API 测试脚本
测试统计和收藏功能
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

# 测试用户ID（需要先创建或已存在）
TEST_USER_ID = 1


def print_response(title, response):
    """打印响应结果"""
    print(f"\n{'=' * 50}")
    print(f"【{title}】")
    print(f"{'=' * 50}")
    print(f"状态码: {response.status_code}")
    try:
        data = response.json()
        print(f"响应内容:\n{json.dumps(data, ensure_ascii=False, indent=2)}")
        return data
    except:
        print(f"响应内容: {response.text}")
        return None


def test_stats_overview():
    """测试学习概览统计"""
    url = f"{BASE_URL}/api/stats/overview"
    params = {"user_id": TEST_USER_ID}

    response = requests.get(url, params=params)
    return print_response("学习概览统计", response)


def test_stats_trend():
    """测试近7天趋势"""
    url = f"{BASE_URL}/api/stats/trend"
    params = {"user_id": TEST_USER_ID}

    response = requests.get(url, params=params)
    return print_response("近7天趋势", response)


def test_check_in():
    """测试打卡功能"""
    url = f"{BASE_URL}/api/stats/checkin"
    data = {"user_id": TEST_USER_ID}

    response = requests.post(url, json=data)
    return print_response("手动打卡", response)


def test_add_favorite():
    """测试收藏例句"""
    url = f"{BASE_URL}/api/favorites/add"
    data = {
        "user_id": TEST_USER_ID,
        "vocab_id": 1,  # 假设存在vocab_id=1
        "sentence": "This is a test sentence for favorite feature.",
        "translation": "这是收藏功能的测试例句。",
    }

    response = requests.post(url, json=data)
    return print_response("收藏例句", response)


def test_get_favorites():
    """测试获取收藏列表"""
    url = f"{BASE_URL}/api/favorites/list"
    params = {"user_id": TEST_USER_ID}

    response = requests.get(url, params=params)
    return print_response("收藏列表", response)


def test_check_favorite():
    """测试检查收藏状态"""
    url = f"{BASE_URL}/api/favorites/check"
    params = {
        "user_id": TEST_USER_ID,
        "vocab_id": 1,
        "sentence": "This is a test sentence for favorite feature.",
    }

    response = requests.get(url, params=params)
    return print_response("检查收藏状态", response)


def test_delete_favorite(favorite_id):
    """测试删除收藏"""
    url = f"{BASE_URL}/api/favorites/delete"
    data = {"user_id": TEST_USER_ID, "favorite_id": favorite_id}

    response = requests.delete(url, json=data)
    return print_response("删除收藏", response)


def test_query_word_and_record():
    """测试查询单词并自动记录学习"""
    url = f"{BASE_URL}/api/word/query"
    data = {"user_id": TEST_USER_ID, "word": "hello"}

    response = requests.post(url, json=data)
    return print_response("查询单词(自动记录学习)", response)


def test_health():
    """测试服务健康状态"""
    url = f"{BASE_URL}/api/health"

    response = requests.get(url)
    return print_response("服务健康检查", response)


def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("V2.0 API 测试开始")
    print("=" * 50)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"基础URL: {BASE_URL}")
    print(f"测试用户ID: {TEST_USER_ID}")

    # 1. 健康检查
    test_health()

    # 2. 统计相关测试
    print("\n" + "=" * 50)
    print("【统计功能测试】")
    print("=" * 50)

    test_stats_overview()
    test_stats_trend()
    test_check_in()

    # 3. 查询单词（自动记录学习）
    print("\n" + "=" * 50)
    print("【学习记录测试】")
    print("=" * 50)

    # 查询几次以产生学习记录
    for i in range(3):
        test_query_word_and_record()

    # 再次查看统计
    test_stats_overview()
    test_stats_trend()

    # 4. 收藏功能测试
    print("\n" + "=" * 50)
    print("【收藏功能测试】")
    print("=" * 50)

    # 添加收藏
    result = test_add_favorite()
    favorite_id = None
    if result and result.get("code") == 0:
        favorite_id = result.get("data", {}).get("favorite_id")

    # 获取收藏列表
    test_get_favorites()

    # 检查收藏状态
    test_check_favorite()

    # 删除收藏（如果添加成功）
    if favorite_id:
        test_delete_favorite(favorite_id)
        # 再次查看列表确认删除
        test_get_favorites()

    print("\n" + "=" * 50)
    print("V2.0 API 测试完成")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()

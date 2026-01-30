#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API测试脚本
测试所有后端API接口
"""

import requests
import json
import sys

# 服务地址
BASE_URL = "http://localhost:5000"

# 测试数据
TEST_OPENID = "test_openid_12345"
TEST_USER_ID = None
TEST_VOCAB_ID = None


def print_separator(title):
    """打印分隔线"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def test_health_check():
    """测试健康检查"""
    print_separator("测试1: 健康检查")
    
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            print("✓ 健康检查通过")
            return True
        else:
            print("✗ 健康检查失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_user_login():
    """测试用户登录"""
    print_separator("测试2: 用户登录")
    global TEST_USER_ID
    
    data = {
        "openid": TEST_OPENID,
        "nickname": "测试用户",
        "avatar_url": "https://example.com/avatar.jpg"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/user/login",
            json=data,
            timeout=10
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            TEST_USER_ID = result["data"]["user_id"]
            print(f"✓ 登录成功，用户ID: {TEST_USER_ID}")
            return True
        else:
            print("✗ 登录失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_get_user_info():
    """测试获取用户信息"""
    print_separator("测试3: 获取用户信息")
    
    if not TEST_USER_ID:
        print("✗ 跳过测试：没有用户ID")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/user/info?user_id={TEST_USER_ID}",
            timeout=10
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            print("✓ 获取用户信息成功")
            return True
        else:
            print("✗ 获取用户信息失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_get_user_stats():
    """测试获取用户统计"""
    print_separator("测试4: 获取用户统计")
    
    if not TEST_USER_ID:
        print("✗ 跳过测试：没有用户ID")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/user/stats?user_id={TEST_USER_ID}",
            timeout=10
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            print("✓ 获取用户统计成功")
            return True
        else:
            print("✗ 获取用户统计失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_check_ollama():
    """测试Ollama服务状态"""
    print_separator("测试5: 检查Ollama服务")
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/word/check",
            timeout=10
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            available = result["data"]["available"]
            if available:
                print("✓ Ollama服务可用")
            else:
                print("⚠ Ollama服务不可用，后续测试可能失败")
            return available
        else:
            print("✗ 检查失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_query_word():
    """测试查询单词"""
    print_separator("测试6: 查询单词")
    
    if not TEST_USER_ID:
        print("✗ 跳过测试：没有用户ID")
        return False
    
    data = {
        "user_id": TEST_USER_ID,
        "word": "hello",
        "use_cache": True
    }
    
    print("正在查询单词 'hello'，请稍候...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/word/query",
            json=data,
            timeout=60  # Ollama可能需要较长时间
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            print("✓ 单词查询成功")
            return True
        else:
            print("✗ 单词查询失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_get_query_history():
    """测试获取查询历史"""
    print_separator("测试7: 获取查询历史")
    
    if not TEST_USER_ID:
        print("✗ 跳过测试：没有用户ID")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/word/history?user_id={TEST_USER_ID}",
            timeout=10
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            print("✓ 获取查询历史成功")
            return True
        else:
            print("✗ 获取查询历史失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_add_to_vocab_book():
    """测试添加到生词本"""
    print_separator("测试8: 添加到生词本")
    global TEST_VOCAB_ID
    
    if not TEST_USER_ID:
        print("✗ 跳过测试：没有用户ID")
        return False
    
    data = {
        "user_id": TEST_USER_ID,
        "word": "serendipity",
        "phonetic": "/ˌserənˈdɪpəti/",
        "definition": "意外发现珍奇事物的本领",
        "english_definition": "The occurrence of events by chance in a happy way",
        "examples": [
            {"sentence": "We found it by pure serendipity.", "translation": "我们纯粹是机缘巧合找到了它。"}
        ],
        "memory_tips": "联想为宁静的seren + 小插曲dipity"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/vocab-book/add",
            json=data,
            timeout=10
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            TEST_VOCAB_ID = result["data"]["vocab_id"]
            print(f"✓ 添加成功，生词ID: {TEST_VOCAB_ID}")
            return True
        else:
            print("✗ 添加失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_get_vocab_list():
    """测试获取生词本列表"""
    print_separator("测试9: 获取生词本列表")
    
    if not TEST_USER_ID:
        print("✗ 跳过测试：没有用户ID")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/vocab-book/list?user_id={TEST_USER_ID}",
            timeout=10
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            print("✓ 获取生词本列表成功")
            return True
        else:
            print("✗ 获取生词本列表失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_get_vocab_detail():
    """测试获取生词详情"""
    print_separator("测试10: 获取生词详情")
    
    if not TEST_USER_ID or not TEST_VOCAB_ID:
        print("✗ 跳过测试：没有用户ID或生词ID")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/vocab-book/detail?user_id={TEST_USER_ID}&vocab_id={TEST_VOCAB_ID}",
            timeout=10
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            print("✓ 获取生词详情成功")
            return True
        else:
            print("✗ 获取生词详情失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_update_vocab_status():
    """测试更新生词状态"""
    print_separator("测试11: 更新生词状态")
    
    if not TEST_USER_ID or not TEST_VOCAB_ID:
        print("✗ 跳过测试：没有用户ID或生词ID")
        return False
    
    data = {
        "user_id": TEST_USER_ID,
        "vocab_id": TEST_VOCAB_ID,
        "status": 2  # 标记为已掌握
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/vocab-book/update",
            json=data,
            timeout=10
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            print("✓ 更新生词状态成功")
            return True
        else:
            print("✗ 更新生词状态失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_get_vocab_stats():
    """测试获取生词本统计"""
    print_separator("测试12: 获取生词本统计")
    
    if not TEST_USER_ID:
        print("✗ 跳过测试：没有用户ID")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/vocab-book/stats?user_id={TEST_USER_ID}",
            timeout=10
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            print("✓ 获取生词本统计成功")
            return True
        else:
            print("✗ 获取生词本统计失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_check_word_exists():
    """测试检查单词是否存在"""
    print_separator("测试13: 检查单词是否存在")
    
    if not TEST_USER_ID:
        print("✗ 跳过测试：没有用户ID")
        return False
    
    try:
        response = requests.get(
            f"{BASE_URL}/api/vocab-book/check-exists?user_id={TEST_USER_ID}&word=serendipity",
            timeout=10
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            print("✓ 检查单词是否存在成功")
            return True
        else:
            print("✗ 检查单词是否存在失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def test_delete_vocab():
    """测试删除生词"""
    print_separator("测试14: 删除生词")
    
    if not TEST_USER_ID or not TEST_VOCAB_ID:
        print("✗ 跳过测试：没有用户ID或生词ID")
        return False
    
    data = {
        "user_id": TEST_USER_ID,
        "vocab_id": TEST_VOCAB_ID
    }
    
    try:
        response = requests.delete(
            f"{BASE_URL}/api/vocab-book/delete",
            json=data,
            timeout=10
        )
        result = response.json()
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        
        if result.get("code") == 0:
            print("✓ 删除生词成功")
            return True
        else:
            print("✗ 删除生词失败")
            return False
    except Exception as e:
        print(f"✗ 请求失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print(" 微信小程序背单词应用 - API测试")
    print("=" * 60)
    print(f"\n服务地址: {BASE_URL}")
    print("请确保服务已启动: python app.py")
    print("\n")
    
    # 检查服务是否运行
    try:
        requests.get(f"{BASE_URL}/api/health", timeout=2)
    except:
        print("✗ 无法连接到服务，请确保服务已启动")
        print(f"  运行命令: cd {BASE_URL.replace('http://localhost:5000', 'backend')} && python app.py")
        sys.exit(1)
    
    # 运行测试
    results = []
    
    # 基础测试
    results.append(("健康检查", test_health_check()))
    results.append(("用户登录", test_user_login()))
    results.append(("获取用户信息", test_get_user_info()))
    results.append(("获取用户统计", test_get_user_stats()))
    
    # Ollama相关测试
    ollama_available = test_check_ollama()
    results.append(("检查Ollama服务", ollama_available))
    
    if ollama_available:
        results.append(("查询单词", test_query_word()))
    else:
        print("\n⚠ 跳过Ollama相关测试（服务不可用）")
    
    results.append(("获取查询历史", test_get_query_history()))
    
    # 生词本测试
    results.append(("添加到生词本", test_add_to_vocab_book()))
    results.append(("获取生词本列表", test_get_vocab_list()))
    results.append(("获取生词详情", test_get_vocab_detail()))
    results.append(("更新生词状态", test_update_vocab_status()))
    results.append(("获取生词本统计", test_get_vocab_stats()))
    results.append(("检查单词是否存在", test_check_word_exists()))
    results.append(("删除生词", test_delete_vocab()))
    
    # 打印测试总结
    print_separator("测试总结")
    
    passed = sum(1 for _, result in results if result)
    failed = sum(1 for _, result in results if not result)
    
    for name, result in results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"{status}: {name}")
    
    print(f"\n总计: {len(results)} 个测试")
    print(f"通过: {passed} 个")
    print(f"失败: {failed} 个")
    
    if failed == 0:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠ {failed} 个测试失败，请检查日志")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

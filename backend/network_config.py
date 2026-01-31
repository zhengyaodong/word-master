#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络配置工具
用于获取本地网络IP地址，方便真机调试
"""

import socket
import requests
import json


def get_local_ip():
    """获取本地网络IP地址"""
    try:
        # 创建一个UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 连接到一个公共DNS服务器（不实际发送数据）
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"获取本地IP失败: {e}")
        return "127.0.0.1"


def check_ollama_service(host="localhost", port=11434):
    """检查Ollama服务是否可访问"""
    try:
        url = f"http://{host}:{port}/api/tags"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "models" in data and data["models"]:
                model_names = [model["name"] for model in data["models"]]
                return True, model_names
            return True, []
        return False, []
    except requests.exceptions.ConnectionError:
        return False, "连接被拒绝"
    except requests.exceptions.Timeout:
        return False, "连接超时"
    except Exception as e:
        return False, f"未知错误: {str(e)}"


def test_connectivity():
    """测试各种连接方式"""
    print("=== 网络连接测试 ===")
    print(f"本地IP: {get_local_ip()}")

    # 测试各种连接方式
    test_hosts = [
        ("localhost", "本地localhost"),
        ("127.0.0.1", "本地127.0.0.1"),
        (get_local_ip(), f"局域网IP {get_local_ip()}"),
    ]

    for host, description in test_hosts:
        print(f"\n--- 测试 {description} ---")
        is_available, result = check_ollama_service(host)
        if is_available:
            print(f"✅ Ollama服务可用")
            if result:
                print(f"可用模型: {', '.join(result)}")
        else:
            print(f"❌ Ollama服务不可用")
            print(f"错误信息: {result}")


def print_network_config():
    """打印网络配置建议"""
    local_ip = get_local_ip()
    print("\n=== 网络配置建议 ===")
    print(f"电脑局域网IP: {local_ip}")
    print(f"手机应访问: http://{local_ip}:11434")
    print(f"微信开发者工具设置: http://{local_ip}:5000")

    # 检查Ollama服务状态
    print("\n=== Ollama服务状态 ===")
    for host in ["localhost", "127.0.0.1", local_ip]:
        is_available, result = check_ollama_service(host)
        if is_available:
            print(f"✅ {host}:11434 - 服务正常")
            break
        else:
            print(f"❌ {host}:11434 - {result}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="网络配置工具")
    parser.add_argument("--test", action="store_true", help="测试网络连接")
    args = parser.parse_args()

    if args.test:
        test_connectivity()
    else:
        print_network_config()

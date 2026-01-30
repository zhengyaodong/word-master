#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama服务模块
用于调用本地Ollama大模型查询单词解释
"""

import requests
import json
import re
from typing import Dict, Any, Optional
from datetime import datetime, timedelta


class OllamaService:
    """Ollama服务类"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen3:0.6b"):
        """
        初始化Ollama服务
        
        Args:
            base_url: Ollama服务地址
            model: 使用的模型名称
        """
        self.base_url = base_url
        self.model = model
        self.api_endpoint = f"{base_url}/api/generate"
        self.timeout = 30
        
    def is_available(self) -> bool:
        """
        检查Ollama服务是否可用
        
        Returns:
            bool: 服务是否可用
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def query_word(self, word: str) -> Dict[str, Any]:
        """
        查询单词解释
        
        Args:
            word: 要查询的英文单词
            
        Returns:
            包含单词详细信息的字典
            
        Raises:
            Exception: 当Ollama服务调用失败时
        """
        prompt = self._build_prompt(word)
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "num_predict": 800
            }
        }
        
        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            return self._parse_response(result["response"], word)
            
        except requests.exceptions.Timeout:
            raise Exception("Ollama服务响应超时，请检查服务是否正常运行")
        except requests.exceptions.ConnectionError:
            raise Exception("无法连接到Ollama服务，请确保服务已启动")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama服务调用失败: {str(e)}")
    
    def _build_prompt(self, word: str) -> str:
        """
        构建查询Prompt
        
        Args:
            word: 要查询的单词
            
        Returns:
            完整的Prompt字符串
        """
        return f"""请详细解释英文单词'{word}'，请以JSON格式返回以下信息：
{{
    "word": "单词拼写",
    "phonetic": "音标（使用IPA格式）",
    "part_of_speech": "词性（如n./v./adj./adv.等）",
    "definition": "中文释义（简洁准确）",
    "english_definition": "英文释义（简洁）",
    "examples": [
        {{"sentence": "英文例句1", "translation": "中文翻译1"}},
        {{"sentence": "英文例句2", "translation": "中文翻译2"}},
        {{"sentence": "英文例句3", "translation": "中文翻译3"}}
    ],
    "memory_tips": "记忆技巧（提供一个简单有趣的记忆方法）"
}}

要求：
1. 必须返回有效的JSON格式
2. 例句要实用、地道
3. 记忆技巧要简单易懂
4. 如果单词有多种含义，选择最常用的1-2种
"""
    
    def _parse_response(self, response_text: str, word: str) -> Dict[str, Any]:
        """
        解析Ollama响应
        
        Args:
            response_text: Ollama返回的文本
            word: 原始查询的单词
            
        Returns:
            解析后的字典
        """
        # 清理响应文本
        response_text = response_text.strip()
        
        # 尝试直接解析JSON
        try:
            result = json.loads(response_text)
            return self._validate_and_normalize(result, word)
        except json.JSONDecodeError:
            pass
        
        # 尝试提取JSON部分（处理可能的markdown代码块）
        json_patterns = [
            r'```json\s*(.*?)\s*```',  # Markdown JSON代码块
            r'```\s*(.*?)\s*```',       # 普通代码块
            r'\{.*\}',                   # 纯JSON对象
        ]
        
        for pattern in json_patterns:
            match = re.search(pattern, response_text, re.DOTALL)
            if match:
                try:
                    json_str = match.group(1) if pattern != r'\{.*\}' else match.group(0)
                    result = json.loads(json_str.strip())
                    return self._validate_and_normalize(result, word)
                except json.JSONDecodeError:
                    continue
        
        # 如果都无法解析，返回一个基本结构
        return {
            "word": word,
            "phonetic": "",
            "part_of_speech": "",
            "definition": "解析失败，请重试",
            "english_definition": "",
            "examples": [],
            "memory_tips": "",
            "raw_response": response_text
        }
    
    def _validate_and_normalize(self, result: Dict[str, Any], word: str) -> Dict[str, Any]:
        """
        验证并规范化结果
        
        Args:
            result: 解析后的字典
            word: 原始查询的单词
            
        Returns:
            规范化后的字典
        """
        # 确保必要字段存在
        normalized = {
            "word": result.get("word", word),
            "phonetic": result.get("phonetic", ""),
            "part_of_speech": result.get("part_of_speech", ""),
            "definition": result.get("definition", ""),
            "english_definition": result.get("english_definition", ""),
            "examples": result.get("examples", []),
            "memory_tips": result.get("memory_tips", "")
        }
        
        # 规范化examples格式
        if isinstance(normalized["examples"], list):
            normalized["examples"] = [
                {
                    "sentence": ex.get("sentence", "") if isinstance(ex, dict) else str(ex),
                    "translation": ex.get("translation", "") if isinstance(ex, dict) else ""
                }
                for ex in normalized["examples"][:3]  # 最多保留3个例句
            ]
        else:
            normalized["examples"] = []
        
        return normalized


class QueryCache:
    """查询缓存类"""
    
    def __init__(self, ttl_hours: int = 24):
        """
        初始化缓存
        
        Args:
            ttl_hours: 缓存有效期（小时）
        """
        self.ttl = timedelta(hours=ttl_hours)
        self._cache = {}
    
    def get(self, word: str) -> Optional[Dict[str, Any]]:
        """
        获取缓存
        
        Args:
            word: 查询的单词
            
        Returns:
            缓存的结果或None
        """
        word = word.lower()
        if word in self._cache:
            data, timestamp = self._cache[word]
            if datetime.now() - timestamp < self.ttl:
                return data
            else:
                del self._cache[word]
        return None
    
    def set(self, word: str, data: Dict[str, Any]):
        """
        设置缓存
        
        Args:
            word: 查询的单词
            data: 查询结果
        """
        self._cache[word.lower()] = (data, datetime.now())
    
    def clear(self):
        """清空缓存"""
        self._cache.clear()


# 全局服务实例
ollama_service = OllamaService()
query_cache = QueryCache()


def query_word_with_cache(word: str, use_cache: bool = True) -> Dict[str, Any]:
    """
    带缓存的单词查询
    
    Args:
        word: 要查询的单词
        use_cache: 是否使用缓存
        
    Returns:
        单词解释
    """
    word = word.strip().lower()
    
    # 检查缓存
    if use_cache:
        cached = query_cache.get(word)
        if cached:
            cached["from_cache"] = True
            return cached
    
    # 调用Ollama服务
    result = ollama_service.query_word(word)
    result["from_cache"] = False
    
    # 存入缓存
    if use_cache:
        query_cache.set(word, result)
    
    return result


if __name__ == "__main__":
    # 测试代码
    print("测试Ollama服务...")
    
    service = OllamaService()
    
    # 检查服务可用性
    print(f"服务可用性检查: {service.is_available()}")
    
    if service.is_available():
        # 测试查询
        test_word = "serendipity"
        print(f"\n查询单词: {test_word}")
        
        try:
            result = query_word_with_cache(test_word)
            print(f"\n查询结果:")
            print(json.dumps(result, ensure_ascii=False, indent=2))
            
            # 测试缓存
            print("\n测试缓存...")
            result2 = query_word_with_cache(test_word)
            print(f"来自缓存: {result2.get('from_cache', False)}")
            
        except Exception as e:
            print(f"查询失败: {e}")
    else:
        print("Ollama服务不可用，请确保:")
        print("1. Ollama已安装并运行")
        print("2. 模型 qwen3:0.6b 已下载")
        print("3. 服务地址正确: http://localhost:11434")

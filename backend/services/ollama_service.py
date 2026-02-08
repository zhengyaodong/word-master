#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama service helpers.
"""

import requests
import json
import re
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from collections import Counter


class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "qwen3:0.6b"):
        self.base_url = base_url
        self.model = model
        self.api_endpoint = f"{base_url}/api/generate"
        self.timeout = 30

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def query_word(self, word: str) -> Dict[str, Any]:
        prompt = self._build_prompt(word)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.7, "num_predict": 800},
        }

        try:
            response = requests.post(self.api_endpoint, json=payload, timeout=self.timeout)
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
        return f"""请详细解释英文单词 '{word}'，请以 JSON 格式返回以下信息：
{{
    "word": "单词拼写",
    "phonetic": "音标（使用IPA格式）",
    "part_of_speech": "词性（如n./v./adj./adv.等）",
    "definition": "中文释义（必须是中文，简洁准确）",
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
5. definition 字段必须是中文，不要用英文
"""

    def _build_extract_prompt(self, text: str, max_words: int) -> str:
        return f"""请从下面文本中提取核心英文词汇，过滤常见高频词（如 the, and, of 等），输出 JSON 数组：
要求：
1. 只返回小写英文单词
2. 去重
3. 最多 {max_words} 个
4. 只输出 JSON 数组，不要解释

文本：
{text}
"""

    def _strip_think(self, text: str) -> str:
        if not text:
            return text
        text = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.IGNORECASE)
        text = re.sub(r"</?think>", "", text, flags=re.IGNORECASE)
        return text.strip()

    def _parse_response(self, response_text: str, word: str) -> Dict[str, Any]:
        response_text = self._strip_think(response_text.strip())

        try:
            result = json.loads(response_text)
            return self._validate_and_normalize(result, word)
        except json.JSONDecodeError:
            pass

        json_patterns = [
            r"```json\s*(.*?)\s*```",
            r"```\s*(.*?)\s*```",
            r"\{.*\}",
        ]

        for pattern in json_patterns:
            match = re.search(pattern, response_text, re.DOTALL)
            if match:
                try:
                    json_str = match.group(1) if pattern != r"\{.*\}" else match.group(0)
                    json_str = self._strip_think(json_str)
                    result = json.loads(json_str.strip())
                    return self._validate_and_normalize(result, word)
                except json.JSONDecodeError:
                    continue

        return {
            "word": word,
            "phonetic": "",
            "part_of_speech": "",
            "definition": "解析失败，请重试",
            "english_definition": "",
            "examples": [],
            "memory_tips": "",
            "raw_response": response_text,
        }

    def _validate_and_normalize(self, result: Dict[str, Any], word: str) -> Dict[str, Any]:
        normalized = {
            "word": result.get("word", word),
            "phonetic": result.get("phonetic", ""),
            "part_of_speech": result.get("part_of_speech", ""),
            "definition": result.get("definition", ""),
            "english_definition": result.get("english_definition", ""),
            "examples": result.get("examples", []),
            "memory_tips": result.get("memory_tips", ""),
        }

        if isinstance(normalized["examples"], list):
            normalized["examples"] = [
                {
                    "sentence": ex.get("sentence", "") if isinstance(ex, dict) else str(ex),
                    "translation": ex.get("translation", "") if isinstance(ex, dict) else "",
                }
                for ex in normalized["examples"][:3]
            ]
        else:
            normalized["examples"] = []

        return normalized

    def _parse_word_list(self, response_text: str) -> List[str]:
        response_text = self._strip_think(response_text.strip())
        try:
            data = json.loads(response_text)
            if isinstance(data, list):
                return [str(x).strip().lower() for x in data if str(x).strip()]
            if isinstance(data, dict) and isinstance(data.get("words"), list):
                return [str(x).strip().lower() for x in data["words"] if str(x).strip()]
        except json.JSONDecodeError:
            pass

        match = re.search(r"\[(.*?)\]", response_text, re.DOTALL)
        if match:
            try:
                data = json.loads(f"[{match.group(1)}]")
                if isinstance(data, list):
                    return [str(x).strip().lower() for x in data if str(x).strip()]
            except json.JSONDecodeError:
                pass

        return [w.lower() for w in re.findall(r"[A-Za-z]{2,}", response_text)]

    def _basic_extract_words(self, text: str, max_words: int) -> List[str]:
        words = re.findall(r"[A-Za-z]{2,}", text)
        words = [w.lower() for w in words]
        filtered = [w for w in words if w not in STOP_WORDS]
        counts = Counter(filtered)
        sorted_words = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        return [w for w, _ in sorted_words[:max_words]]

    def extract_keywords(self, text: str, max_words: int = 50, use_ai: bool = True) -> List[str]:
        if not text or not text.strip():
            return []

        text = text.strip()
        words: List[str] = []

        if use_ai and self.is_available():
            try:
                chunks = [text]
                if len(text) > 2000:
                    chunks = [text[i : i + 2000] for i in range(0, len(text), 2000)]
                    chunks = chunks[:3]

                for chunk in chunks:
                    prompt = self._build_extract_prompt(chunk, max_words)
                    payload = {
                        "model": self.model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {"temperature": 0.2, "num_predict": 400},
                    }
                    response = requests.post(
                        self.api_endpoint, json=payload, timeout=self.timeout
                    )
                    response.raise_for_status()
                    result = response.json()
                    extracted = self._parse_word_list(result.get("response", ""))
                    words.extend(extracted)

                words = [w.lower() for w in words if w and w.isalpha()]
                words = [w for w in words if w not in STOP_WORDS]
                seen = set()
                deduped = []
                for w in words:
                    if w not in seen:
                        seen.add(w)
                        deduped.append(w)
                return deduped[:max_words]
            except Exception:
                pass

        return self._basic_extract_words(text, max_words)

class QueryCache:
    def __init__(self, ttl_hours: int = 24):
        self.ttl = timedelta(hours=ttl_hours)
        self._cache = {}

    def get(self, word: str) -> Optional[Dict[str, Any]]:
        word = word.lower()
        if word in self._cache:
            data, timestamp = self._cache[word]
            if datetime.now() - timestamp < self.ttl:
                return data
            else:
                del self._cache[word]
        return None

    def set(self, word: str, data: Dict[str, Any]):
        self._cache[word.lower()] = (data, datetime.now())

    def clear(self):
        self._cache.clear()


ollama_service = OllamaService()
query_cache = QueryCache()

# Basic English stop words for filtering
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "has",
    "have",
    "he",
    "her",
    "his",
    "i",
    "in",
    "is",
    "it",
    "its",
    "me",
    "my",
    "not",
    "of",
    "on",
    "or",
    "our",
    "she",
    "that",
    "the",
    "their",
    "them",
    "they",
    "this",
    "to",
    "was",
    "we",
    "were",
    "with",
    "you",
    "your",
}


def query_word_with_cache(word: str, use_cache: bool = True) -> Dict[str, Any]:
    word = word.strip().lower()

    if use_cache:
        cached = query_cache.get(word)
        if cached:
            cached["from_cache"] = True
            return cached

    result = ollama_service.query_word(word)
    result["from_cache"] = False

    if use_cache:
        query_cache.set(word, result)

    return result


if __name__ == "__main__":
    print("Testing Ollama service...")
    service = OllamaService()
    print(f"Available: {service.is_available()}")

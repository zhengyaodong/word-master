#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音合成(TTS)相关API路由 - 使用 Edge-TTS
"""

import os
import uuid
import asyncio
from flask import Blueprint, request, jsonify, send_file
import edge_tts

# 创建蓝图
tts_bp = Blueprint("tts", __name__, url_prefix="/api/tts")

# 音频文件存储目录
AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio_cache")

# 确保音频缓存目录存在
if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR)

# 默认语音配置
DEFAULT_VOICE = "en-US-GuyNeural"  # 英语男声
DEFAULT_RATE = "+0%"
DEFAULT_VOLUME = "+0%"

# 语言到语音的映射
VOICE_MAP = {
    "en_US": "en-US-GuyNeural",  # 英语（美国）
    "en_GB": "en-GB-RyanNeural",  # 英语（英国）
    "zh_CN": "zh-CN-YunxiNeural",  # 中文（普通话）
    "zh_TW": "zh-TW-HsiaoChenNeural",  # 中文（台湾）
    "ja_JP": "ja-JP-KeitaNeural",  # 日语
    "ko_KR": "ko-KR-InJoonNeural",  # 韩语
    "fr_FR": "fr-FR-HenriNeural",  # 法语
    "de_DE": "de-DE-ConradNeural",  # 德语
    "es_ES": "es-ES-AlvaroNeural",  # 西班牙语
    "ru_RU": "ru-RU-DmitryNeural",  # 俄语
}


def success_response(data=None, message="操作成功"):
    """成功响应"""
    return jsonify({"code": 0, "data": data or {}, "message": message})


def error_response(message="操作失败", code=1):
    """错误响应"""
    return jsonify({"code": code, "data": {}, "message": message})


async def generate_speech_async(text, voice, rate, volume, output_file):
    """
    异步生成语音文件

    参数:
        text: 要合成的文本
        voice: 语音ID
        rate: 语速（如 +0%, -50%, +50%）
        volume: 音量（如 +0%, -50%, +50%）
        output_file: 输出文件路径
    """
    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume)
    await communicate.save(output_file)


@tts_bp.route("/speak", methods=["POST"])
def speak():
    """
    文本转语音 - 生成音频文件并返回URL

    请求参数:
        - text: 要朗读的文本（必填）
        - lang: 语言代码，默认 en_US（可选）
        - voice: 语音ID（可选，默认根据lang选择）
        - rate: 语速调整（可选，默认 +0%）
        - volume: 音量调整（可选，默认 +0%）

    返回:
        - audio_url: 音频文件URL
        - text: 原文本
        - lang: 语言
        - duration: 预估时长（秒）
    """
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    text = data.get("text", "").strip()
    if not text:
        return error_response("文本不能为空")

    # 获取参数
    lang = data.get("lang", "en_US")
    voice = data.get("voice", VOICE_MAP.get(lang, DEFAULT_VOICE))
    rate = data.get("rate", DEFAULT_RATE)
    volume = data.get("volume", DEFAULT_VOLUME)

    try:
        # 生成唯一文件名
        file_id = str(uuid.uuid4())
        output_file = os.path.join(AUDIO_DIR, f"{file_id}.mp3")

        # 异步生成语音
        asyncio.run(generate_speech_async(text, voice, rate, volume, output_file))

        # 计算预估时长（粗略估计：每秒约15个字符）
        estimated_duration = len(text) / 15.0

        # 构建音频URL
        audio_url = f"/api/tts/audio/{file_id}.mp3"

        return success_response(
            data={
                "audio_url": audio_url,
                "text": text,
                "lang": lang,
                "voice": voice,
                "duration": round(estimated_duration, 1),
            },
            message="语音合成成功",
        )

    except Exception as e:
        return error_response(f"语音合成失败: {str(e)}", code=503)


@tts_bp.route("/stream", methods=["POST"])
def stream_speak():
    """
    文本转语音 - 流式返回音频数据

    请求参数:
        - text: 要朗读的文本（必填）
        - lang: 语言代码，默认 en_US（可选）
        - voice: 语音ID（可选）
        - rate: 语速调整（可选）
        - volume: 音量调整（可选）

    返回:
        - 音频文件流（MP3格式）
    """
    data = request.get_json()

    if not data:
        return error_response("请求参数不能为空")

    text = data.get("text", "").strip()
    if not text:
        return error_response("文本不能为空")

    # 获取参数
    lang = data.get("lang", "en_US")
    voice = data.get("voice", VOICE_MAP.get(lang, DEFAULT_VOICE))
    rate = data.get("rate", DEFAULT_RATE)
    volume = data.get("volume", DEFAULT_VOLUME)

    try:
        # 生成临时文件
        file_id = str(uuid.uuid4())
        output_file = os.path.join(AUDIO_DIR, f"stream_{file_id}.mp3")

        # 异步生成语音
        asyncio.run(generate_speech_async(text, voice, rate, volume, output_file))

        # 返回音频文件
        response = send_file(
            output_file,
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="speech.mp3",
        )

        # 添加响应头，允许微信小程序访问
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response

    except Exception as e:
        return error_response(f"语音合成失败: {str(e)}", code=503)


@tts_bp.route("/audio/<filename>", methods=["GET"])
def get_audio(filename):
    """
    获取音频文件

    参数:
        - filename: 音频文件名（如 xxx.mp3）

    返回:
        - 音频文件流
    """
    try:
        file_path = os.path.join(AUDIO_DIR, filename)

        if not os.path.exists(file_path):
            return error_response("音频文件不存在", code=404)

        response = send_file(file_path, mimetype="audio/mpeg", as_attachment=False)

        # 添加响应头，允许微信小程序访问
        response.headers.add("Access-Control-Allow-Origin", "*")

        return response

    except Exception as e:
        return error_response(f"获取音频失败: {str(e)}")


@tts_bp.route("/voices", methods=["GET"])
def list_voices():
    """
    获取可用的语音列表

    返回:
        - voices: 语音列表
    """
    try:
        # 返回常用的语音列表
        voices = [
            {
                "name": "en-US-GuyNeural",
                "lang": "en_US",
                "gender": "Male",
                "desc": "英语（美国）- 男声",
            },
            {
                "name": "en-US-JennyNeural",
                "lang": "en_US",
                "gender": "Female",
                "desc": "英语（美国）- 女声",
            },
            {
                "name": "en-GB-RyanNeural",
                "lang": "en_GB",
                "gender": "Male",
                "desc": "英语（英国）- 男声",
            },
            {
                "name": "en-GB-SoniaNeural",
                "lang": "en_GB",
                "gender": "Female",
                "desc": "英语（英国）- 女声",
            },
            {
                "name": "zh-CN-YunxiNeural",
                "lang": "zh_CN",
                "gender": "Male",
                "desc": "中文（普通话）- 男声",
            },
            {
                "name": "zh-CN-XiaoxiaoNeural",
                "lang": "zh_CN",
                "gender": "Female",
                "desc": "中文（普通话）- 女声",
            },
            {
                "name": "ja-JP-KeitaNeural",
                "lang": "ja_JP",
                "gender": "Male",
                "desc": "日语 - 男声",
            },
            {
                "name": "ja-JP-NanamiNeural",
                "lang": "ja_JP",
                "gender": "Female",
                "desc": "日语 - 女声",
            },
        ]

        return success_response(data={"voices": voices}, message="获取语音列表成功")

    except Exception as e:
        return error_response(f"获取语音列表失败: {str(e)}")


@tts_bp.route("/clear-cache", methods=["DELETE"])
def clear_cache():
    """
    清理音频缓存文件

    返回:
        - deleted_count: 删除的文件数量
    """
    try:
        deleted_count = 0

        # 遍历音频目录，删除所有mp3文件
        for filename in os.listdir(AUDIO_DIR):
            if filename.endswith(".mp3"):
                file_path = os.path.join(AUDIO_DIR, filename)
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except:
                    pass

        return success_response(
            data={"deleted_count": deleted_count},
            message=f"成功清理{deleted_count}个缓存文件",
        )

    except Exception as e:
        return error_response(f"清理缓存失败: {str(e)}")

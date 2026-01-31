#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信小程序背单词应用 - Flask后端服务
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys

# 添加当前目录到路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

# 导入路由
from routes.user import user_bp
from routes.word import word_bp
from routes.vocab_book import vocab_book_bp
from routes.v2_features import stats_bp, favorites_bp
from routes.tts import tts_bp

# 创建Flask应用
app = Flask(__name__)

# 启用CORS（允许微信小程序访问）
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    },
)

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(word_bp)
app.register_blueprint(vocab_book_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(favorites_bp)
app.register_blueprint(tts_bp)


@app.route("/")
def index():
    """首页"""
    return jsonify(
        {
            "code": 0,
            "message": "微信小程序背单词应用后端服务",
            "version": "1.0.0",
            "status": "running",
        }
    )


@app.route("/api/health")
def health_check():
    """健康检查"""
    from services.ollama_service import ollama_service

    ollama_available = ollama_service.is_available()

    return jsonify(
        {
            "code": 0,
            "data": {
                "status": "healthy",
                "ollama_available": ollama_available,
                "service": "word-master-backend",
            },
            "message": "服务正常运行" if ollama_available else "Ollama服务不可用",
        }
    )


@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({"code": 404, "data": {}, "message": "接口不存在"}), 404


@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    return jsonify({"code": 500, "data": {}, "message": "服务器内部错误"}), 500


def init_app():
    """初始化应用"""
    # 确保数据库目录存在
    db_dir = os.path.join(BASE_DIR, "database")
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"创建数据库目录: {db_dir}")

    # 检查数据库文件
    db_file = os.path.join(db_dir, "word_master.db")
    if not os.path.exists(db_file):
        print("数据库文件不存在，正在初始化...")
        from models import init_db

        init_db()
        print("数据库初始化完成")

    print("\n=== 服务配置 ===")
    print(f"数据库: {db_file}")
    print(f"Ollama: http://localhost:11434")
    print(f"模型: qwen3:0.6b")


if __name__ == "__main__":
    # 初始化
    init_app()

    # 启动服务
    print("\n=== 启动服务 ===")
    print("服务地址: http://localhost:5000")
    print("API文档: http://localhost:5000/api/health")
    print("\n按 Ctrl+C 停止服务\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False,  # 避免重复初始化
    )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask backend for word-master mini program.
"""

from flask import Flask, jsonify
from flask_cors import CORS
import os
import sys

# Add backend dir to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from routes.user import user_bp
from routes.word import word_bp
from routes.vocab_book import vocab_book_bp
from routes.v2_features import stats_bp, favorites_bp
from routes.tts import tts_bp
from routes.library import library_bp

app = Flask(__name__)

# Enable CORS
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

# Register blueprints
app.register_blueprint(user_bp)
app.register_blueprint(word_bp)
app.register_blueprint(vocab_book_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(favorites_bp)
app.register_blueprint(tts_bp)
app.register_blueprint(library_bp)


@app.route("/")
def index():
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
    return jsonify({"code": 404, "data": {}, "message": "接口不存在"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"code": 500, "data": {}, "message": "服务器内部错误"}), 500


def init_app():
    """Initialize database and ensure schema."""
    db_dir = os.path.join(BASE_DIR, "database")
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"创建数据库目录: {db_dir}")

    db_file = os.path.join(db_dir, "word_master.db")
    if not os.path.exists(db_file):
        print("数据库文件不存在，正在初始化...")
        from models import init_db, ensure_schema

        init_db()
        ensure_schema()
        print("数据库初始化完成")
    else:
        from models import init_db, ensure_schema

        init_db()
        ensure_schema()

    print("\n=== 服务配置 ===")
    print(f"数据库: {db_file}")
    print("Ollama: http://localhost:11434")
    print("模型: qwen3:0.6b")


if __name__ == "__main__":
    init_app()

    print("\n=== 启动服务 ===")
    print("服务地址: http://localhost:5000")
    print("API 文档: http://localhost:5000/api/health")
    print("\n按 Ctrl+C 停止服务\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False,
    )

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V3.0 backend local tests (no external server required).
"""

from app import app, init_app
from models import get_db_session, ImportHistory


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def run_tests():
    init_app()
    client = app.test_client()

    # 1) login
    resp = client.post(
        "/api/user/login",
        json={"openid": "test_openid_v3", "nickname": "v3_test", "avatar_url": ""},
    )
    data = resp.get_json()
    assert_true(data["code"] == 0, "login failed")
    user_id = data["data"]["userId"]

    # 2) clean text (use rule-based to avoid ollama dependency)
    text = "Ambition and determination drive success. The quick brown fox jumps over the lazy dog."
    resp = client.post(
        "/api/vocab-book/clean",
        json={"user_id": user_id, "text": text, "max_words": 10, "use_ai": False},
    )
    data = resp.get_json()
    assert_true(data["code"] == 0, "clean failed")
    words = data["data"]["words"]
    assert_true(isinstance(words, list) and len(words) > 0, "clean words empty")

    # 3) import words
    resp = client.post(
        "/api/vocab-book/import",
        json={
            "user_id": user_id,
            "words": words,
            "source_type": "paste",
            "raw_text": text,
        },
    )
    data = resp.get_json()
    assert_true(data["code"] == 0, "import failed")
    assert_true(data["data"]["total"] >= 1, "import total invalid")

    # 4) ensure import history record
    session = get_db_session()
    try:
        history_count = session.query(ImportHistory).filter_by(user_id=user_id).count()
        assert_true(history_count >= 1, "import history not recorded")
    finally:
        session.close()

    print("V3 local tests passed")


if __name__ == "__main__":
    run_tests()

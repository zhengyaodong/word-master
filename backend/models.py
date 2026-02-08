"""
SQLAlchemy models for word-master backend.
"""

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Date,
    ForeignKey,
    Index,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import inspect
from datetime import datetime
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database", "word_master.db")

engine = create_engine(f"sqlite:///{DATABASE_PATH}", echo=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(100), unique=True, nullable=False)
    nickname = Column(String(50))
    avatar_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    vocabulary_books = relationship(
        "VocabularyBook", back_populates="user", cascade="all, delete-orphan"
    )
    query_histories = relationship(
        "QueryHistory", back_populates="user", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "userId": self.user_id,
            "openid": self.openid,
            "nickname": self.nickname,
            "avatarUrl": self.avatar_url,
            "createdAt": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.created_at
            else None,
            "updatedAt": self.updated_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.updated_at
            else None,
        }


class VocabularyBook(Base):
    __tablename__ = "vocabulary_book"

    vocab_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    word = Column(String(50), nullable=False)
    phonetic = Column(String(100))
    definition = Column(Text)
    english_definition = Column(Text)
    examples = Column(Text)
    memory_tips = Column(Text)
    status = Column(Integer, default=0)  # 0:未学习 1:学习中 2:已掌握
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="vocabulary_books")

    __table_args__ = (
        Index("idx_user_word", "user_id", "word", unique=True),
        Index("idx_vocab_book_user_id", "user_id"),
        Index("idx_vocab_book_word", "word"),
        Index("idx_vocab_book_status", "status"),
    )

    def get_examples(self):
        if self.examples:
            try:
                return json.loads(self.examples)
            except json.JSONDecodeError:
                return []
        return []

    def set_examples(self, examples_list):
        self.examples = json.dumps(examples_list, ensure_ascii=False)

    def get_status_text(self):
        status_map = {0: "未学习", 1: "学习中", 2: "已掌握"}
        return status_map.get(self.status, "未知")

    def to_dict(self):
        return {
            "vocab_id": self.vocab_id,
            "userId": self.user_id,
            "word": self.word,
            "phonetic": self.phonetic,
            "definition": self.definition,
            "english_definition": self.english_definition,
            "examples": self.get_examples(),
            "memory_tips": self.memory_tips,
            "status": self.status,
            "status_text": self.get_status_text(),
            "createdAt": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.created_at
            else None,
        }


class QueryHistory(Base):
    __tablename__ = "query_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    word = Column(String(50), nullable=False)
    result = Column(Text)
    query_time = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="query_histories")

    __table_args__ = (
        Index("idx_query_history_user_id", "user_id"),
        Index("idx_query_history_word", "word"),
        Index("idx_query_history_time", "query_time"),
    )

    def get_result(self):
        if self.result:
            try:
                return json.loads(self.result)
            except json.JSONDecodeError:
                return None
        return None

    def set_result(self, result_dict):
        self.result = json.dumps(result_dict, ensure_ascii=False)

    def to_dict(self):
        return {
            "history_id": self.history_id,
            "userId": self.user_id,
            "word": self.word,
            "result": self.get_result(),
            "query_time": self.query_time.strftime("%Y-%m-%d %H:%M:%S")
            if self.query_time
            else None,
        }


class StudyRecord(Base):
    __tablename__ = "study_record"

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    study_date = Column(Date, nullable=False)
    query_count = Column(Integer, default=0)
    is_checked_in = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User")

    __table_args__ = (
        Index("idx_study_record_user_date", "user_id", "study_date", unique=True),
        Index("idx_study_record_user_id", "user_id"),
    )

    def to_dict(self):
        return {
            "record_id": self.record_id,
            "user_id": self.user_id,
            "study_date": self.study_date.strftime("%Y-%m-%d")
            if self.study_date
            else None,
            "query_count": self.query_count,
            "is_checked_in": bool(self.is_checked_in),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.created_at
            else None,
        }


class FavoriteSentence(Base):
    __tablename__ = "favorite_sentences"

    favorite_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    vocab_id = Column(
        Integer,
        ForeignKey("vocabulary_book.vocab_id", ondelete="CASCADE"),
        nullable=False,
    )
    sentence = Column(Text, nullable=False)
    translation = Column(Text)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User")
    vocab = relationship("VocabularyBook")

    __table_args__ = (
        Index("idx_favorite_user_id", "user_id"),
        Index("idx_favorite_vocab_id", "vocab_id"),
    )

    def to_dict(self):
        return {
            "favorite_id": self.favorite_id,
            "user_id": self.user_id,
            "vocab_id": self.vocab_id,
            "sentence": self.sentence,
            "translation": self.translation,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.created_at
            else None,
        }


class ImportHistory(Base):
    __tablename__ = "import_history"

    import_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    source_type = Column(String(50))
    raw_text = Column(Text)
    word_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User")

    __table_args__ = (Index("idx_import_history_user_id", "user_id"),)

    def to_dict(self):
        return {
            "import_id": self.import_id,
            "user_id": self.user_id,
            "source_type": self.source_type,
            "word_count": self.word_count,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.created_at
            else None,
        }


class WordLibrary(Base):
    __tablename__ = "word_libraries"

    library_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50))
    level = Column(String(20))
    total_words = Column(Integer, default=0)
    icon_url = Column(String(255))
    is_builtin = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)

    library_words = relationship(
        "LibraryWord", back_populates="library", cascade="all, delete-orphan"
    )
    user_progress = relationship(
        "UserLibraryProgress", back_populates="library", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "library_id": self.library_id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "level": self.level,
            "total_words": self.total_words,
            "icon_url": self.icon_url,
            "is_builtin": bool(self.is_builtin),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.created_at
            else None,
        }


class LibraryWord(Base):
    __tablename__ = "library_words"

    id = Column(Integer, primary_key=True, autoincrement=True)
    library_id = Column(
        Integer,
        ForeignKey("word_libraries.library_id", ondelete="CASCADE"),
        nullable=False,
    )
    word = Column(String(100), nullable=False)
    phonetic = Column(String(100))
    definition = Column(Text)
    english_definition = Column(Text)
    examples = Column(Text)
    part_of_speech = Column(String(50))
    frequency = Column(Integer, default=0)
    difficulty = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)

    library = relationship("WordLibrary", back_populates="library_words")

    __table_args__ = (
        Index("idx_library_words_library_id", "library_id"),
        Index("idx_library_words_word", "word"),
        Index("idx_library_words_difficulty", "difficulty"),
    )

    def get_examples(self):
        if self.examples:
            try:
                return json.loads(self.examples)
            except json.JSONDecodeError:
                return []
        return []

    def set_examples(self, examples_list):
        self.examples = json.dumps(examples_list, ensure_ascii=False)

    def to_dict(self):
        return {
            "id": self.id,
            "library_id": self.library_id,
            "word": self.word,
            "phonetic": self.phonetic,
            "definition": self.definition,
            "english_definition": self.english_definition,
            "examples": self.get_examples(),
            "part_of_speech": self.part_of_speech,
            "frequency": self.frequency,
            "difficulty": self.difficulty,
        }


class UserLibraryProgress(Base):
    __tablename__ = "user_library_progress"

    progress_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    library_id = Column(
        Integer,
        ForeignKey("word_libraries.library_id", ondelete="CASCADE"),
        nullable=False,
    )
    word = Column(String(100), nullable=False)
    status = Column(Integer, default=0)  # 0: 未学习, 1: 学习中, 2: 已掌握, 3: 需复习
    review_count = Column(Integer, default=0)
    correct_count = Column(Integer, default=0)
    wrong_count = Column(Integer, default=0)
    last_review_at = Column(DateTime)
    next_review_at = Column(DateTime)
    easiness_factor = Column(Integer, default=250)  # 存储为整数(2.5 * 100)
    interval_days = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User")
    library = relationship("WordLibrary", back_populates="user_progress")

    __table_args__ = (
        Index(
            "idx_user_progress_user_library_word",
            "user_id",
            "library_id",
            "word",
            unique=True,
        ),
        Index("idx_user_progress_user_id", "user_id"),
        Index("idx_user_progress_library_id", "library_id"),
        Index("idx_user_progress_next_review", "user_id", "next_review_at"),
    )

    def get_easiness_factor(self):
        return self.easiness_factor / 100.0

    def set_easiness_factor(self, value):
        self.easiness_factor = int(value * 100)

    def to_dict(self):
        return {
            "progress_id": self.progress_id,
            "user_id": self.user_id,
            "library_id": self.library_id,
            "word": self.word,
            "status": self.status,
            "status_text": ["未学习", "学习中", "已掌握", "需复习"][self.status]
            if 0 <= self.status <= 3
            else "未知",
            "review_count": self.review_count,
            "correct_count": self.correct_count,
            "wrong_count": self.wrong_count,
            "last_review_at": self.last_review_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.last_review_at
            else None,
            "next_review_at": self.next_review_at.strftime("%Y-%m-%d %H:%M:%S")
            if self.next_review_at
            else None,
            "easiness_factor": self.get_easiness_factor(),
            "interval_days": self.interval_days,
        }


SessionLocal = sessionmaker(bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
    print(f"数据库初始化完成: {DATABASE_PATH}")


def ensure_schema():
    inspector = inspect(engine)
    if "vocabulary_book" in inspector.get_table_names():
        _ = {col["name"] for col in inspector.get_columns("vocabulary_book")}
        # Reserved for future schema migrations.
        return


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session():
    return SessionLocal()


if __name__ == "__main__":
    init_db()
    ensure_schema()

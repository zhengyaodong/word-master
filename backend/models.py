"""
微信小程序背单词应用 - 数据库模型
使用SQLAlchemy ORM
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import json
import os

# 获取数据库文件路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'database', 'word_master.db')

# 创建数据库引擎
engine = create_engine(f'sqlite:///{DATABASE_PATH}', echo=False)
Base = declarative_base()


class User(Base):
    """用户表"""
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    openid = Column(String(100), unique=True, nullable=False)
    nickname = Column(String(50))
    avatar_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联关系
    vocabulary_books = relationship("VocabularyBook", back_populates="user", cascade="all, delete-orphan")
    query_histories = relationship("QueryHistory", back_populates="user", cascade="all, delete-orphan")
    
    def to_dict(self):
        """转换为字典"""
        return {
            'userId': self.user_id,
            'openid': self.openid,
            'nickname': self.nickname,
            'avatarUrl': self.avatar_url,
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def __repr__(self):
        return f"<User(user_id={self.user_id}, nickname={self.nickname})>"


class VocabularyBook(Base):
    """生词本表"""
    __tablename__ = 'vocabulary_book'
    
    vocab_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    word = Column(String(50), nullable=False)
    phonetic = Column(String(100))
    definition = Column(Text)
    english_definition = Column(Text)
    examples = Column(Text)  # JSON格式存储
    memory_tips = Column(Text)
    status = Column(Integer, default=0)  # 0:未学习, 1:学习中, 2:已掌握
    created_at = Column(DateTime, default=datetime.now)
    
    # 关联关系
    user = relationship("User", back_populates="vocabulary_books")
    
    # 联合唯一约束：同一用户的单词不能重复
    __table_args__ = (
        Index('idx_user_word', 'user_id', 'word', unique=True),
        Index('idx_vocab_book_user_id', 'user_id'),
        Index('idx_vocab_book_word', 'word'),
        Index('idx_vocab_book_status', 'status'),
    )
    
    def get_examples(self):
        """获取例句列表"""
        if self.examples:
            try:
                return json.loads(self.examples)
            except json.JSONDecodeError:
                return []
        return []
    
    def set_examples(self, examples_list):
        """设置例句列表"""
        self.examples = json.dumps(examples_list, ensure_ascii=False)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'vocab_id': self.vocab_id,
            'userId': self.user_id,
            'word': self.word,
            'phonetic': self.phonetic,
            'definition': self.definition,
            'english_definition': self.english_definition,
            'examples': self.get_examples(),
            'memory_tips': self.memory_tips,
            'status': self.status,
            'status_text': self.get_status_text(),
            'createdAt': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def get_status_text(self):
        """获取状态文本"""
        status_map = {0: '未学习', 1: '学习中', 2: '已掌握'}
        return status_map.get(self.status, '未知')
    
    def __repr__(self):
        return f"<VocabularyBook(vocab_id={self.vocab_id}, word={self.word})>"


class QueryHistory(Base):
    """查询历史表"""
    __tablename__ = 'query_history'
    
    history_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    word = Column(String(50), nullable=False)
    result = Column(Text)  # 缓存查询结果
    query_time = Column(DateTime, default=datetime.now)
    
    # 关联关系
    user = relationship("User", back_populates="query_histories")
    
    # 索引
    __table_args__ = (
        Index('idx_query_history_user_id', 'user_id'),
        Index('idx_query_history_word', 'word'),
        Index('idx_query_history_time', 'query_time'),
    )
    
    def get_result(self):
        """获取查询结果"""
        if self.result:
            try:
                return json.loads(self.result)
            except json.JSONDecodeError:
                return None
        return None
    
    def set_result(self, result_dict):
        """设置查询结果"""
        self.result = json.dumps(result_dict, ensure_ascii=False)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'history_id': self.history_id,
            'userId': self.user_id,
            'word': self.word,
            'result': self.get_result(),
            'query_time': self.query_time.strftime('%Y-%m-%d %H:%M:%S') if self.query_time else None
        }
    
    def __repr__(self):
        return f"<QueryHistory(history_id={self.history_id}, word={self.word})>"


# 创建会话工厂
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """初始化数据库，创建所有表"""
    Base.metadata.create_all(bind=engine)
    print(f"数据库初始化完成: {DATABASE_PATH}")


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session():
    """获取数据库会话（直接返回）"""
    return SessionLocal()


if __name__ == '__main__':
    # 直接运行此文件时初始化数据库
    init_db()
    print("数据库表创建成功！")
    
    # 测试数据库连接
    session = get_db_session()
    try:
        # 测试插入用户
        test_user = User(openid='test_openid', nickname='测试用户')
        session.add(test_user)
        session.commit()
        print(f"测试用户创建成功: {test_user.user_id}")
        
        # 测试插入生词
        test_vocab = VocabularyBook(
            user_id=test_user.user_id,
            word='hello',
            phonetic='/həˈloʊ/',
            definition='int. 你好',
            english_definition='used as a greeting',
            memory_tips='想象两个人见面时说嗨喽'
        )
        test_vocab.set_examples([
            {'sentence': 'Hello, how are you?', 'translation': '你好，你好吗？'},
            {'sentence': 'Say hello to your parents.', 'translation': '代我向你的父母问好。'}
        ])
        session.add(test_vocab)
        session.commit()
        print(f"测试生词创建成功: {test_vocab.vocab_id}")
        
        # 查询测试
        user = session.query(User).first()
        print(f"查询用户: {user.to_dict()}")
        
        vocab = session.query(VocabularyBook).first()
        print(f"查询生词: {vocab.to_dict()}")
        
        # 清理测试数据
        session.delete(test_vocab)
        session.delete(test_user)
        session.commit()
        print("测试数据清理完成")
        
    except Exception as e:
        print(f"测试失败: {e}")
        session.rollback()
    finally:
        session.close()

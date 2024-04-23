import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, TEXT

# 创建基类
Base = declarative_base()


# 定义问题数据表模型
class Questions(Base):
    __tablename__ = 'question'
    question_id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(TEXT)
    samples = Column(TEXT)
    language = Column(String(20))

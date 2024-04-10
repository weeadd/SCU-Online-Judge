import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime

# 创建基类
Base = declarative_base()

# 定义不良坐姿数据表模型
class Students(Base):
    __tablename__ = 'students'
    student_id = Column(String(20), primary_key=True)
    name = Column(String(100))
    class_id = Column(String(50))
    username = Column(String(50))
    password = Column(String(100))
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime

# 创建基类
Base = declarative_base()

# 定义不良坐姿数据表模型
class AbnormalPoseRecord(Base):
    __tablename__ = 'abnormal_pose_records'

    record_id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime)
    head_left = Column(String(255))
    head_right = Column(String(255))
    hunchback = Column(String(255))
    chin_in_hands = Column(String(255))
    body_left = Column(String(255))
    body_right = Column(String(255))
    neck_forward = Column(String(255))
    shoulder_left = Column(String(255))
    shoulder_right = Column(String(255))
    twisted_head = Column(String(255))
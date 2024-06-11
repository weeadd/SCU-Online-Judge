# 由sqlacodegen自动生成，用于定义数据库表的模型
# 控制台执行 sqlacodegen --outfile models.py mysql+pymysql://root:123456@47.236.92.108:3306/scu_online_judge 自动生成
import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, Float, String, Table, Text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Classes(Base):
    __tablename__ = 'classes'

    class_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    class_name: Mapped[Optional[str]] = mapped_column(String(50))
    teacher_id: Mapped[Optional[str]] = mapped_column(String(20))


class ExamSubmissions(Base):
    __tablename__ = 'exam_submissions'

    submission_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    exam_id: Mapped[int] = mapped_column(INTEGER(11))
    student_id: Mapped[Optional[str]] = mapped_column(String(20))
    submit_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class Exams(Base):
    __tablename__ = 'exams'

    exam_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    class_id: Mapped[int] = mapped_column(INTEGER(11))
    name: Mapped[Optional[str]] = mapped_column(String(100))
    release_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deadline: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    problem_ids: Mapped[Optional[str]] = mapped_column(String(255))
    context: Mapped[Optional[str]] = mapped_column(Text)


class HomeworkSubmissions(Base):
    __tablename__ = 'homework_submissions'

    submission_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    homework_id: Mapped[int] = mapped_column(INTEGER(11))
    student_id: Mapped[Optional[str]] = mapped_column(String(20))
    submit_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)


class Homeworks(Base):
    __tablename__ = 'homeworks'

    homework_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    class_id: Mapped[int] = mapped_column(INTEGER(11))
    name: Mapped[Optional[str]] = mapped_column(String(100))
    release_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    deadline: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    problem_ids: Mapped[Optional[str]] = mapped_column(String(255))
    context: Mapped[Optional[str]] = mapped_column(Text)


class Questions(Base):
    __tablename__ = 'questions'

    question_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String(100))
    content: Mapped[Optional[str]] = mapped_column(Text)
    samples: Mapped[Optional[str]] = mapped_column(Text)
    language: Mapped[Optional[str]] = mapped_column(String(20))
    is_public: Mapped[bool] = mapped_column()


class Students(Base):
    __tablename__ = 'students'

    student_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    class_id: Mapped[Optional[str]] = mapped_column(String(10))
    password: Mapped[Optional[str]] = mapped_column(String(20))


t_submit_records = Table(
    'submit_records', Base.metadata,
    Column('submission_id', INTEGER(11)),
    Column('student_id', String(20)),
    Column('question_id', INTEGER(11)),
    Column('submit_time', DateTime),
    Column('submitted_code', Text),
    Column('judge_result', String(50)),
    Column('execution_time', Float)
)


class Teachers(Base):
    __tablename__ = 'teachers'

    teacher_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(20))
    password: Mapped[Optional[str]] = mapped_column(String(20))

from sqlalchemy import Column, Integer, String, Text, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SubmitRecords(Base):
    __tablename__ = 'submit_records'

    submission_id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    student_id = Column(String(20))
    submitter = Column(String(20))
    code = Column(Text)
    memory = Column(String(10))
    execution_time = Column(Float)
    status = Column(String(20))
    ast_status = Column(String(20))
    ast_advice = Column(String(50))
    output = Column(Text)
    submit_time = Column(DateTime)

    def __repr__(self):
        return f"<SubmitRecords(submission_id={self.submission_id}, question_id={self.question_id}, student_id={self.student_id}, submitter={self.submitter}, code={self.code}, memory={self.memory}, execution_time={self.execution_time}, status={self.status},ast_status={self.ast_status} ast_analysis={self.ast_advice}, output={self.output}, submit_time={self.submit_time})>"

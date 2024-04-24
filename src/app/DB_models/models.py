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


class Question(Base):
    __tablename__ = 'question'

    question_id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    title: Mapped[Optional[str]] = mapped_column(String(100))
    content: Mapped[Optional[str]] = mapped_column(Text)
    samples: Mapped[Optional[str]] = mapped_column(Text)
    language: Mapped[Optional[str]] = mapped_column(String(20))


class Students(Base):
    __tablename__ = 'students'

    student_id: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(100))
    class_id: Mapped[Optional[int]] = mapped_column(INTEGER(11))
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

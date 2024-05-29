from flask import g
from sqlalchemy import text
from .FormatConversion import toDataFrame
from . import toJSON


def get_all_exams():
    with g.sql_session.create_session() as session:
        query = text("select * from exams")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


def get_exam_by_id(exam_id):
    with g.sql_session.create_session() as session:
        query = text("select * from exams where exam_id = :exam_id")
        res = session.execute(query, {"exam_id": exam_id})
        json_res = toJSON(res)
        return json_res

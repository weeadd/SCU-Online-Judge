from flask import g
from sqlalchemy import text
from .FormatConversion import toDataFrame


def get_all_exams():
    with g.sql_session.create_session() as session:
        query = text("select * from exams")
        res = session.execute(query)
        df_res = toDataFrame(res)
        return df_res


def get_exam_by_id(exam_id):
    with g.sql_session.create_session() as session:
        query = text("select * from exams where exam_id = :exam_id")
        res = session.execute(query, {"exam_id": exam_id})
        df_res = toDataFrame(res)
        return df_res
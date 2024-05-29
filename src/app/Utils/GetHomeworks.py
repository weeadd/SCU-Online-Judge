from flask import g
from sqlalchemy import text
from .FormatConversion import toDataFrame
from . import toJSON


def get_all_homeworks():
    with g.sql_session.create_session() as session:
        query = text("select * from homeworks")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


def get_homework_by_id(homework_id):
    with g.sql_session.create_session() as session:
        query = text("select * from homeworks where homework_id = :homework_id")
        res = session.execute(query, {"homework_id": homework_id})
        json_res = toJSON(res)
        return json_res



def get_homework_by_class_id(class_id):
    with g.sql_session.create_session() as session:
        query = text("select * from homeworks where class_id = :class_id")
        res = session.execute(query, {"class_id": class_id})
        df_res = toDataFrame(res)
        return df_res

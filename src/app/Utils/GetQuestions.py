from flask import g
from sqlalchemy import text
from .FormatConversion import toDataFrame


def get_all_questions():
    with g.sql_session.create_session() as session:
        query = text("select question_id,title,language from questions")
        res = session.execute(query)
        df_res = toDataFrame(res)
        return df_res

def get_questions_by_id(question_id):
    with g.sql_session.create_session() as session:
        query = text("select * from questions where question_id = :question_id")
        res = session.execute(query, {"question_id": question_id})
        df_res = toDataFrame(res)
        return df_res
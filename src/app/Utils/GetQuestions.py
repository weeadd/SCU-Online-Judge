from sqlalchemy import text
from ..DataAnalyse.SQLSession import get_session, toDataFrame


def get_all_questions():
    with get_session() as session:
        query = text("select * from question")
        res = session.execute(query)
        df_res = toDataFrame(res)
        return df_res

def get_questions_by_id(question_id):
    with get_session() as session:
        query = text("select * from questions where question_id = :question_id")
        res = session.execute(query, {"question_id": question_id})
        df_res = toDataFrame(res)
        return df_res
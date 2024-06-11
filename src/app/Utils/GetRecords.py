from flask import g
from sqlalchemy import text
from .FormatConversion import toDataFrame


def get_all_records():
    with g.sql_session.create_session() as session:
        query = text("select * from submit_records")
        res = session.execute(query)
        df_res = toDataFrame(res)
        return df_res

def get_submission_stats():
    with g.sql_session.create_session() as session:
        query = text("""SELECT question_id,
        COUNT(*) AS submit_count,
        SUM(CASE WHEN status = 'accepted' THEN 1 ELSE 0 END) / COUNT(*) AS accepted_rate
    FROM
        submit_records
    GROUP BY
        question_id""")


        res = session.execute(query)
        df_res = toDataFrame(res)
        return df_res
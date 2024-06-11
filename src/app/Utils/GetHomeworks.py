import json

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
        query = text("select name, problem_ids, context from homeworks where homework_id = :homework_id")
        res = session.execute(query, {"homework_id": homework_id})
        json_res = toJSON(res)
        return json_res


def get_homework_by_id_with_questionList(homework_id):
    with g.sql_session.create_session() as session:
        query = text("select name, problem_ids, context from homeworks where homework_id = :homework_id")
        res = session.execute(query, {"homework_id": homework_id})

        json_res = toJSON(res)
        homework_data = json.loads(json_res)[0]  # Assuming only one homework is fetched
        print(homework_data)

        # Splitting problem_ids and extracting information for each problem
        problem_ids = homework_data['problem_ids'].split(', ')
        problem_info_list = []
        for problem_id in problem_ids:
            problem_query = text("select question_id, title, is_public from questions where question_id = :problem_id")
            problem_res = session.execute(problem_query, {"problem_id": problem_id})
            problem_data = toJSON(problem_res)
            problem_data = json.loads(problem_data)

            # Count submit records
            submit_query = text("select count(*) from submit_records where question_id = :question_id")
            submit_res = session.execute(submit_query, {"question_id": problem_data['question_id']})
            submit_count = submit_res.scalar()

            # Calculate accepted rate
            accepted_query = text(
                "select count(*) from submit_records where question_id = :question_id and is_accepted = 1")
            accepted_res = session.execute(accepted_query, {"question_id": problem_data[0]['question_id']})
            accepted_count = accepted_res.scalar()
            total_submissions = submit_count if submit_count > 0 else 1  # to avoid division by zero
            accepted_rate = accepted_count / total_submissions

            problem_info = {
                'question_id': problem_data[0]['question_id'],
                'title': problem_data[0]['title'],
                'is_public': problem_data[0]['is_public'],
                'submit_count': submit_count,
                'accepted_rate': accepted_rate
            }
            problem_info_list.append(problem_info)

        homework_data['problem_info_list'] = problem_info_list
        return json_res


def get_homework_by_class_id(class_id):
    with g.sql_session.create_session() as session:
        query = text("select * from homeworks where class_id = :class_id")
        res = session.execute(query, {"class_id": class_id})
        df_res = toDataFrame(res)
        return df_res

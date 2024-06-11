import json

from flask import g
from sqlalchemy import text
from .FormatConversion import toDataFrame
from . import toJSON


def get_all_homeworks():
    with g.sql_session.create_session() as session:
        query = text("select homework_id, name, problem_ids from homeworks")
        res = session.execute(query)

        json_res = toJSON(res)
        homework_data = json.loads(json_res)[0]  # Assuming only one homework is fetched
        print(homework_data)

        # Splitting problem_ids and extracting information for each problem
        problem_ids = homework_data['problem_ids'].split(',')
        print(problem_ids)
        problem_info_list = []
        for question_id in problem_ids:
            problem_query = text("select title, is_public from questions where question_id = :question_id")
            problem_res = session.execute(problem_query, {"question_id": question_id})
            df_res = toDataFrame(problem_res)
            title = df_res['title'].values[0]

            # Count submit records
            submit_query = text("select count(*) from submit_records where question_id = :question_id")
            submit_res = session.execute(submit_query, {"question_id": question_id})
            submit_count = submit_res.scalar()

            # Calculate accepted rate
            accepted_query = text(
                "select count(*) from submit_records where question_id = :question_id and status = 'Accepted'")
            accepted_res = session.execute(accepted_query, {"question_id": question_id})
            accepted_count = accepted_res.scalar()
            total_submissions = submit_count if submit_count > 0 else 1  # to avoid division by zero
            accepted_rate = accepted_count / total_submissions

            problem_info = {
                'question_id': question_id,
                'title': title,
                'submit_count': submit_count,
                'accepted_rate': accepted_rate
            }
            problem_info_list.append(problem_info)

        homework_data['problem_info_list'] = problem_info_list
        del homework_data['problem_ids']
        print(homework_data)

    return homework_data
    # with g.sql_session.create_session() as session:
    #     query = text("select * from homeworks")
    #     res = session.execute(query)
    #     json_res = toJSON(res)
    #     return json_res


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
        problem_ids = homework_data['problem_ids'].split(',')
        print(problem_ids)
        problem_info_list = []
        for question_id in problem_ids:
            problem_query = text("select title, is_public from questions where question_id = :question_id")
            problem_res = session.execute(problem_query, {"question_id": question_id})
            df_res = toDataFrame(problem_res)
            title = df_res['title'].values[0]

            # Count submit records
            submit_query = text("select count(*) from submit_records where question_id = :question_id")
            submit_res = session.execute(submit_query, {"question_id": question_id})
            submit_count = submit_res.scalar()

            # Calculate accepted rate
            accepted_query = text(
                "select count(*) from submit_records where question_id = :question_id and status = 'Accepted'")
            accepted_res = session.execute(accepted_query, {"question_id": question_id})
            accepted_count = accepted_res.scalar()
            total_submissions = submit_count if submit_count > 0 else 1  # to avoid division by zero
            accepted_rate = accepted_count / total_submissions

            problem_info = {
                'question_id': question_id,
                'title': title,
                'submit_count': submit_count,
                'accepted_rate': accepted_rate
            }
            problem_info_list.append(problem_info)

        homework_data['problem_info_list'] = problem_info_list

    print(problem_info_list)
    return problem_info_list


def get_homework_by_class_id(class_id):
    with g.sql_session.create_session() as session:
        query = text("select * from homeworks where class_id = :class_id")
        res = session.execute(query, {"class_id": class_id})
        df_res = toDataFrame(res)
        return df_res

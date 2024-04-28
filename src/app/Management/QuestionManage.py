from flask import request, Blueprint, g
from sqlalchemy import text
from ..Utils import get_questions_by_id,get_all_questions,toJSON
from ..DB_models.models import Questions

# 创建路由蓝图
question_manage_blue = Blueprint('question_manage', __name__)


@question_manage_blue.route('/question_manage', methods=['GET', 'PUT', 'POST', 'DELETE'])
def question_manage():
    # 查询题目
    if request.method == 'GET':  # 处理 GET 请求
        question_id = request.args.get('question_id')  # 必选参数
        language = request.args.get('language')  # 可选参数

        # 有题目id参数则返回question_id为该id的题目信息，无参数则返回全部题目
        if question_id is not None and question_id != '':
            results = get_questions_by_id(question_id)
        else:
            results = get_all_questions()
        return results.to_json(orient='records')

    # 更新题目信息
    elif request.method == 'PUT':  # 处理 PUT 请求
        data = request.json
        question_id = data.get('question_id')
        if question_id is not None:
            update_question_info(data)
            return "Question information updated successfully", 200
        else:
            return "Question ID is missing", 400

    # 增加题目
    elif request.method == 'POST':  # 处理 POST 请求
        add_question_to_question_bank(request.json)
        return "Question added successfully", 201

    # 删除题目
    elif request.method == 'DELETE':  # 处理 DELETE 请求
        question_id = request.args.get('question_id')  # 获取要删除的学生的ID
        if question_id is not None and question_id != '':
            delete_question(question_id)
            return "Question deleted successfully", 200
        else:
            return "Question ID is missing", 400


def get_classes_by_language(language):
    with g.sql_session.create_session() as session:
        query = text("select * from questions where language = :language")
        res = session.execute(query, {"language": language})
        json_res = toJSON(res)
        return json_res


# 更新题目信息
def update_question_info(data):
    with g.sql_session.create_session() as session:
        question_id = data.get('question_id')
        question = session.query(Questions).filter_by(question_id=question_id).first()
        if question:
            # 更新学生信息
            question.title = data.get('title')
            question.content = data.get('content')
            question.samples = data.get('samples')
            question.language = data.get('language')
            session.commit()
        else:
            raise ValueError("Question not found")


# 将题目数据加入题库写入数据库
def add_question_to_question_bank(data):
    with g.sql_session.create_session() as session:
        # 从请求的数据中获取题目信息
        title = data.get('title')
        content = data.get('content')
        samples = data.get('samples')
        language = data.get('language')

        # 创建一个新的 Question 对象，并添加到数据库会话中
        question_record = Questions(
            title=title,
            content=content,
            samples=samples,
            language=language
        )
        session.add(question_record)
        session.commit()


# 从数据库中删除指定题目
def delete_question(question_id):
    with g.sql_session.create_session() as session:
        question = session.query(Questions).filter_by(question_id=question_id).first()  # 查询要删除的学生
        if question:
            session.delete(question)  # 删除题目记录
            session.commit()
        else:
            raise ValueError("Question not found")

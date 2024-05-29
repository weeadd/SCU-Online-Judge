from flask import request, Blueprint, g
from sqlalchemy import text
from ..Utils import get_exam_by_id,get_all_exams,toJSON
from ..DB_models.models import Exams

# 创建路由蓝图
exam_manage_blue = Blueprint('exam_manage', __name__)


@exam_manage_blue.route('/exam_manage', methods=['GET', 'PUT', 'POST', 'DELETE'])
def exam_manage():
    # 查询考试
    if request.method == 'GET':  # 处理 GET 请求
        exam_id = request.args.get('exam_id')  # 必选参数

        # 有考试id参数则返回question_id为该id的题目信息，无参数则返回全部题目
        if exam_id is not None and exam_id != '':
            results = get_exam_by_id(exam_id)
        else:
            results = get_all_exams()
        return results.to_json(orient='records')

    # 更新考试信息
    elif request.method == 'PUT':  # 处理 PUT 请求
        data = request.json
        exam_id = data.get('exam_id')
        if exam_id is not None:
            update_exam_info(data)
            return "Exam information updated successfully", 200
        else:
            return "Exam ID is missing", 400

    # 增加考试
    elif request.method == 'POST':  # 处理 POST 请求
        add_exam(request.json)
        return "Exam added successfully", 201

    # 删除考试
    elif request.method == 'DELETE':  # 处理 DELETE 请求
        exam_id = request.args.get('exam_id')  # 获取要删除的考试的ID
        if exam_id is not None and exam_id != '':
            delete_exam(exam_id)
            return "Exam deleted successfully", 200
        else:
            return "Exam ID is missing", 400


# 更新考试信息
def update_exam_info(data):
    with g.sql_session.create_session() as session:
        exam_id = data.get('exam_id')
        exam = session.query(Exams).filter_by(exam_id=exam_id).first()
        if exam:
            # 更新考试信息
            exam.name = data.get('name')
            exam.class_id = data.get('class_id')
            exam.release_time = data.get('release_time')
            exam.deadline = data.get('deadline')
            exam.problem_ids = data.get('problem_ids')
            exam.context = data.get('context')
            session.commit()
        else:
            raise ValueError("Exam not found")


# 将考试数据写入数据库
def add_exam(data):
    with g.sql_session.create_session() as session:
        # 从请求的数据中获取考试信息
        name = data.get('name')
        class_id = data.get('class_id')
        release_time = data.get('release_time')
        deadline = data.get('deadline')
        problem_ids = data.get('problem_ids')
        context = data.get('context')

        # 创建一个新的 Homeworks 对象，并添加到数据库会话中
        exam_record = Exams(
            name=name,
            class_id=class_id,
            release_time=release_time,
            deadline=deadline,
            problem_ids=problem_ids,
            context=context,
        )
        session.add(exam_record)
        session.commit()


# 从数据库中删除指定考试
def delete_exam(exam_id):
    with g.sql_session.create_session() as session:
        exam = session.query(Exams).filter_by(exam_id=exam_id).first()  # 查询要删除的考试
        if exam:
            session.delete(exam)  # 删除考试记录
            session.commit()
        else:
            raise ValueError("Exam not found")

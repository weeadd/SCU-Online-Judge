from flask import request, Blueprint, g
from sqlalchemy import text
from ..Utils import get_homework_by_id,get_all_homeworks,toJSON
from ..DB_models.models import Homeworks
import datetime

# 创建路由蓝图
homework_manage_blue = Blueprint('homework_manage', __name__)


@homework_manage_blue.route('/homework_manage', methods=['GET', 'PUT', 'POST', 'DELETE'])
def homework_manage():
    # 查询作业
    if request.method == 'GET':  # 处理 GET 请求
        homework_id = request.args.get('homework_id')  # 必选参数

        # 有题目id参数则返回question_id为该id的题目信息，无参数则返回全部题目
        if homework_id is not None and homework_id != '':
            results = get_homework_by_id(homework_id)
        else:
            results = get_all_homeworks()
        return results

    # 更新作业信息
    elif request.method == 'PUT':  # 处理 PUT 请求
        data = request.json
        homework_id = data.get('homework_id')
        if homework_id is not None:
            update_homework_info(data)
            return "Homework information updated successfully", 200
        else:
            return "Homework ID is missing", 400

    # 增加作业
    elif request.method == 'POST':  # 处理 POST 请求
        add_homework(request.json)
        return "Homework added successfully", 201

    # 删除作业
    elif request.method == 'DELETE':  # 处理 DELETE 请求
        homework_id = request.args.get('homework_id')  # 获取要删除的学生的ID
        if homework_id is not None and homework_id != '':
            delete_homework(homework_id)
            return "Homework deleted successfully", 200
        else:
            return "Homework ID is missing", 400


# 更新作业信息
def update_homework_info(data):
    with g.sql_session.create_session() as session:
        homework_id = data.get('homework_id')
        homework = session.query(Homeworks).filter_by(homework_id=homework_id).first()
        if homework:
            # 更新作业信息
            if data.get('name'):
                homework.name = data.get('name')
            if data.get('class_id'):
                homework.class_id = data.get('class_id')
            if data.get('deadline'):
                homework.deadline = data.get('deadline')
            if data.get('problem_ids'):
                homework.problem_ids = data.get('problem_ids')
            if data.get('content'):
                homework.content = data.get('content')
            session.commit()
        else:
            raise ValueError("Homework not found")


# 将作业数据写入数据库
def add_homework(data):
    current_time = datetime.datetime.now()
    release_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    with g.sql_session.create_session() as session:
        # 从请求的数据中获取作业信息
        name = data.get('name')
        class_id = data.get('class_id')
        # release_time = data.get('release_time')
        deadline = data.get('deadline')
        problem_ids = data.get('problem_ids')
        content = data.get('content')

        # 创建一个新的 Homeworks 对象，并添加到数据库会话中
        homework_record = Homeworks(
            name=name,
            class_id=class_id,
            release_time=release_time,
            deadline=deadline,
            problem_ids=problem_ids,
            content=content,
        )
        session.add(homework_record)
        session.commit()


# 从数据库中删除指定作业
def delete_homework(homework_id):
    with g.sql_session.create_session() as session:
        homework = session.query(Homeworks).filter_by(homework_id=homework_id).first()  # 查询要删除的学生
        if homework:
            session.delete(homework)  # 删除作业记录
            session.commit()
        else:
            raise ValueError("Homework not found")

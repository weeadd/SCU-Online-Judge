from flask import request, Blueprint, g
from sqlalchemy import text

from ..DB_connect.SQLSession import toJSON
from ..DB_models.models import Students

# 创建路由蓝图
class_manage_blue = Blueprint('class_manage', __name__)


@class_manage_blue.route('/')
def All():
    return get_all_students()


@class_manage_blue.route('/class_manage')
def class_manage():
    # 查询学生
    if request.method == 'GET':
        teacher_id = request.args.get('teacher_id')  # 必选参数
        class_id = request.args.get('class_id')  # 可选参数

        # 有班级id参数则返回某一个班级的学生列表，无参数则返回班级列表供老师选择需要管理的班级
        if class_id is not None and class_id != '':
            results = get_students_by_class(class_id)
        else:
            results = get_classes_by_teacher(teacher_id)
        return results

    # 更新学生信息
    elif request.method == 'PUT':
        data = request.json
        student_id = data.get('student_id')
        if student_id is not None:
            update_student_info(data)
            return "Student information updated successfully", 200
        else:
            return "Student ID is missing", 400

    # 增加学生
    elif request.method == 'POST':
        add_student_to_class(request.json)
        return "Student added successfully", 201

    # 删除学生
    elif request.method == 'DELETE':  # 处理 DELETE 请求
        student_id = request.args.get('student_id')  # 获取要删除的学生的ID
        if student_id is not None and student_id != '':
            delete_student(student_id)
            return "Student deleted successfully", 200
        else:
            return "Student ID is missing", 400


# 将学生数据加入班级写入数据库
def add_student_to_class(data, class_id):
    with g.sql_session.create_session() as session:
        # 从请求的数据中获取学生信息
        student_id = data.get('student_id')
        name = data.get('name')
        password = data.get('password')

        # 创建一个新的 Students 对象，并添加到数据库会话中
        student_record = Students(
            student_id=student_id,
            name=name,
            class_id=class_id,
            password=password
        )
        session.add(student_record)
        session.commit()


# 查询所有学生数据
def get_all_students():
    with g.sql_session.create_session() as session:
        query = text("select * from students")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


# 根据班级id查询学生数据
def get_students_by_class(class_id):
    with g.sql_session.create_session() as session:
        query = text("select * from students where class_id = :class_id")
        res = session.execute(query, {"class_id": class_id})
        json_res = toJSON(res)
        return json_res


# 查询当前老师所教班级
def get_classes_by_teacher(teacher_id):
    with g.sql_session.create_session() as session:
        query = text("select * from classes where teacher_id = :teacher_id")
        res = session.execute(query, {"teacher_id": teacher_id})
        json_res = toJSON(res)
        return json_res


# 从数据库中删除指定学生
def delete_student(student_id):
    with g.sql_session.create_session() as session:
        student = session.query(Students).filter_by(student_id=student_id).first()  # 查询要删除的学生
        if student:
            session.delete(student)  # 删除学生记录
            session.commit()
        else:
            raise ValueError("Student not found")


# 更新学生信息
def update_student_info(data):
    with g.sql_session.create_session() as session:
        student_id = data.get('student_id')
        student = session.query(Students).filter_by(student_id=student_id).first()
        if student:
            # 更新学生信息
            student.name = data.get('name')
            student.class_id = data.get('class_id')
            student.username = data.get('username')
            student.password = data.get('password')
            session.commit()
        else:
            raise ValueError("Student not found")

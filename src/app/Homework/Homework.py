from flask import request, Blueprint, g
from sqlalchemy import text
from ..Utils import get_homework_by_id_with_questionList,get_all_homeworks,get_homework_by_class_id,toJSON
from ..DB_models.models import Homeworks,HomeworkSubmissions
import datetime

# 创建路由蓝图
homework_blue = Blueprint('homework', __name__)


@homework_blue.route('/get_homework')
def get_homework():
    homework_id = request.args.get('homework_id')  # 必选参数
    class_id = request.args.get('class_id')  # 必选参数

    # 有题目id参数则返回question_id为该id的题目信息，无参数则返回全部题目
    if class_id is not None and class_id != '':
        results = get_homework_by_class_id(class_id)
    else:
        if homework_id is not None and homework_id != '':
            results = get_homework_by_id_with_questionList(homework_id)
        else:
            return '参数错误'
    return toJSON(results)


@homework_blue.route('/get_homework_by_student_in_class')
def get_homework_by_student_in_class():
    student_id = request.args.get('student_id')  # 必选参数
    with g.sql_session.create_session() as session:
        query = text("select homework_id, name, deadline, problem_ids from homeworks where class_id in "
                     "(select class_id from students where student_id = :student_id)")
        res = session.execute(query, {"student_id": student_id})
        json_res = toJSON(res)
        return json_res


    # return toJSON(results)


@homework_blue.route('/submit_homework')
def submit_homework():
    homework_id = request.args.get('homework_id')  # 必选参数
    student_id = request.args.get('student_id')  # 必选参数

    # 有题目id参数则返回question_id为该id的题目信息，无参数则返回全部题目
    if student_id is not None and student_id != '' and \
            homework_id is not None and homework_id != '':
        submit_one_homework(student_id, homework_id)
        return '提交成功'
    else:
        return '参数错误'


def submit_one_homework(student_id, homework_id):
    current_time = datetime.datetime.now()
    submit_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    with g.sql_session.create_session() as session:
        # 创建一个新的 Homeworks 对象，并添加到数据库会话中
        homeworksubmissions_record = HomeworkSubmissions(
            student_id=student_id,
            homework_id=homework_id,
            submit_time=submit_time
        )
        session.add(homeworksubmissions_record)
        session.commit()

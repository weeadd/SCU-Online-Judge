from flask import Blueprint, g
from sqlalchemy import text

from ..Utils import toJSON

# 创建路由蓝图
submit_record_blue = Blueprint('submit_record', __name__)


@submit_record_blue.route('/', methods=['GET'])
def get_all_submit_record():
    with g.sql_session.create_session() as session:
        query = text("select * from submit_records")
        res = session.execute(query)
        json_res = toJSON(res)
        return json_res


@submit_record_blue.route('/<student_id>', methods=['GET'])
def get_submit_record_by_student(student_id):
    with g.sql_session.create_session() as session:
        query = text("select * from submit_records where student_id = :student_id")
        res = session.execute(query, {"student_id": student_id})
        json_res = toJSON(res)
        return json_res

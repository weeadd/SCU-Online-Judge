from flask import request, Blueprint, jsonify

from ..DB_models import Students
from ..DataAnalyse.SQLSession import get_session

# 创建路由蓝图
login_manage_blue = Blueprint('login', __name__)


@login_manage_blue.route('/login', methods=['POST'])
def login():
    # 学生登录功能
    data = request.json
    student_id = data.get('student_id')
    password = data.get('password')

    with get_session() as session:
        student = session.query(Students).filter_by(student_id=student_id).first()
        if student and student.password == password:
            return jsonify({"message": "Login successful"}), 200
        else:
            return jsonify({"message": "Invalid student ID or password"}), 401

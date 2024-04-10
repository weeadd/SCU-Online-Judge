from flask import request, Blueprint
from sqlalchemy import text
from ..DataAnalyse.SQLSession import get_session, toJSON, toDataFrame

# 创建路由蓝图
question_manage_blue = Blueprint('question_manage', __name__)


@question_manage_blue.route('/question_manage')
def question_manage():
    return "Hello World!"

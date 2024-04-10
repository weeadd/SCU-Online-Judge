from flask import request
from sqlalchemy import text
from ..DataAnalyse.SQLSession import get_session, toJSON, toDataFrame
from . import management_blue


@management_blue.route('/question_manage')
def question_manage():
    pass

from flask import request, Blueprint, jsonify

from ..DB_models.models import Students


# 创建路由蓝图
login_manage_blue = Blueprint('login', __name__)


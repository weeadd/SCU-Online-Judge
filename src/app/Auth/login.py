from flask import request, Blueprint, g
from flask_jwt_extended import create_access_token
from sqlalchemy import text

from ..Utils import toJSON

# 创建路由蓝图
auth_blue = Blueprint('auth', __name__)


@auth_blue.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    if username == 'admin' or username == 'yang':
        gid = '2'
    else:
        gid = '1'
    # role = data['role']
    # # 验证用户是否存在
    # with g.sql_session.create_session() as session:
    #     if role == 'teacher':
    #         query = text("select * from teachers where name = :username")
    #     else:
    #         query = text("select * from students where name = :username")
    #     res = session.execute(query, {"username": username})
    #     # 获取查询结果的列名
    #     keys = res.keys()
    #     # 将 ResultProxy 对象转换为字典列表
    #     results = [dict(zip(keys, row)) for row in res]
    #     if not res:
    #         return {'message': '用户不存在！', 'code': 400}
    #     # 验证密码是否正确
    #     if results[0]['password'] != data['password']:
    #         return {'message': '密码错误！', 'code': 400}
    # 用户登录成功，生成 JWT
    access_token = create_access_token(identity=username)
    # 将 JWT 发送给前端
    return {'access_token': access_token, 'gid': gid,'code': 200}


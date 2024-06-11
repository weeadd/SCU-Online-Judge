from flask import Flask, g
from flask_cors import CORS

from .Auth import auth_blue
from .DB_connect import SQLSession
from .Judge import judge_blue
from .Management import class_manage_blue, question_manage_blue
from .Management import class_manage_blue, question_manage_blue, homework_manage_blue, exam_manage_blue
from .QuestionBank import questionbank_blue
from .SubmitRecord import submit_record_blue
from .Homework import homework_blue
from .Rank import rank_blue
from flask_jwt_extended import JWTManager


def create_app(config):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    @app.before_request
    def before_request():
        g.sql_session = SQLSession(db_url=config.DATABASE_URL)

    app.register_blueprint(class_manage_blue, url_prefix='/class_manage')
    app.register_blueprint(question_manage_blue, url_prefix='/question_manage')
    app.register_blueprint(questionbank_blue, url_prefix='/questionlist')
    app.register_blueprint(homework_manage_blue, url_prefix='/homework_manage')
    app.register_blueprint(exam_manage_blue, url_prefix='/exam')
    app.register_blueprint(judge_blue, url_prefix='/judge')
    app.register_blueprint(submit_record_blue, url_prefix='/submit_record')
    app.register_blueprint(auth_blue, url_prefix='/auth')
    app.register_blueprint(rank_blue, url_prefix='/rank')
    app.register_blueprint(homework_blue, url_prefix='/student_homework')

    app.config['JWT_SECRET_KEY'] = 'lihua'  # 设置JWT的加密密钥
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False  # 设置ACCESS_TOKEN的永不过期
    JWTManager(app)  # 创建 JWTManager 实例

    return app

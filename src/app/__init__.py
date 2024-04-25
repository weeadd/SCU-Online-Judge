from flask import Flask, g
from flask_cors import CORS

from .DB_connect import SQLSession
from .Management import class_manage_blue, question_manage_blue
from .QuestionBank import questionbank_blue


def create_app(config):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    @app.before_request
    def before_request():
        g.sql_session = SQLSession(db_url=config.DATABASE_URL)

    app.register_blueprint(class_manage_blue, url_prefix='/management')
    app.register_blueprint(question_manage_blue, url_prefix='/management')

    return app

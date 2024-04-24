from flask import Flask
from flask_cors import CORS

from .DB_connect import db_init
from .Management import class_manage_blue, question_manage_blue
from .QuestionBank import questionbank_blue


def create_app(config):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    db_init(config.DATABASE_URL)
    app.register_blueprint(class_manage_blue, url_prefix='/management')
    app.register_blueprint(question_manage_blue, url_prefix='/management')

    return app

from flask import Flask
from flask_cors import CORS
from .DataAnalyse import db_init
from .Management import management_blue
from .QuestionBank import questionbank_blue

def create_app(config):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    db_init(config.DATABASE_URL)
    app.register_blueprint(management_blue, url_prefix='/management')
    app.register_blueprint(questionbank_blue, url_prefix='/questionbank')

    return app




from flask import Flask
from flask_cors import CORS
from .DataAnalyse import db_init
from .PoseDetection import workbench_blue

def create_app(config):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    db_init(config.DATABASE_URL)
    app.register_blueprint(workbench_blue, url_prefix='/workbench')

    return app




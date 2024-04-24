from src.config import config
from src.app.DB_connect import db_init
from src.app.Management import class_manage_blue

from flask import Flask
from flask_cors import CORS

def test_questions(config):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    db_init(config.DATABASE_URL)
    app.register_blueprint(class_manage_blue)

    return app


if __name__ == "__main__":
    app = test_questions(config)
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True)

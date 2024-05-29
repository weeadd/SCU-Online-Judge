from flask import Flask
from flask_cors import CORS

from src.app.Judge.Judge import judge_blue



def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    app.register_blueprint(judge_blue, url_prefix='/')


    return app

if __name__ == "__main__":
    app = create_app()
    print(app.url_map)
    app.run(host="0.0.0.0", port=5000, debug=True)
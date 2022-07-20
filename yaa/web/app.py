# Imports
import secrets
from threading import Thread
from typing import Optional

from flask import Flask, render_template
from flask_login import LoginManager


# Code
def get_app(app_name: str = __name__, secret_key: str = secrets.token_hex(nbytes=64),
            static_folder: str = "./www/static", template_folder: str = "./www/html_templates") -> Flask:
    app = Flask(app_name, static_url_path='', static_folder=static_folder, template_folder=template_folder)
    app.secret_key = secret_key
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    
    # app.config['UPLOAD_FOLDER'] = "./data/uploads/temp"
    # app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MiB
    
    @app.route("/", methods=['GET'])
    def root():
        return render_template("main.html")
    
    return app


def make_app_thread(app: Optional[Flask] = None, host: str = "127.0.0.1", port: int = "8080", debug: bool = False) -> Thread:
    pass

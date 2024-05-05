"""
Librerian

Functions
    create_app
"""

import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from
from librerian.constants import *

db = SQLAlchemy()

def create_app(test_config=None):
    """
    Create Flask app
    """
    app = Flask(__name__, instance_relative_config=True, static_folder="static")
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "development.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    app.config["SWAGGER"] = {
        "title": "Librerian API",
        "openapi": "3.0.3",
        "uiversion": 3,
        "doc_dir": "./doc"
    }
    swagger = Swagger(app, template_file="doc/librerian.yml")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from . import models
    from . import api

    from librerian.utils import UserConverter, LibraryConverter, BookConverter, WorkConverter

    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.generate_db_command)
    app.cli.add_command(models.empty_db_command)

    app.url_map.converters["user"] = UserConverter
    app.url_map.converters["library"] = LibraryConverter
    app.url_map.converters["book"] = BookConverter
    app.url_map.converters["work"] = WorkConverter

    app.register_blueprint(api.api_bp)

    @app.route("/api/")
    def entry_point():
        pass

    @app.route("/profiles/<resource>/")
    def send_profile_html(resource):
        return send_from_directory(app.static_folder, f"{resource}.html")

    return app

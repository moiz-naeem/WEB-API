import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from librerian.constants import

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "development.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    
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
    
    from librerian.utils import UserConverter, LibraryConverter, BookConverter 

    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.generate_db_command)
    app.cli.add_command(models.nuke)
    app.url_map.converters["user"] = UserConverter
    app.url_map.converters["library"] = LibraryConverter
    app.url_map.converters["book"] = BookConverter 

    app.register_blueprint(api.api_bp)

    @app.route("/test/")
    def test():
        return "Test function works aight", 200

    return app

import os

from flask import Flask

def create_app(test_config=None):
    # Create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'moonlite.sqlite')
    )

    if test_config is None:
        # Apply config pyfile if no test config is applied
        app.config.from_pyfile('config.py', silent = True)
    else:
        # Otherwise, apply the test config
        app.config.from_mapping(test_config)
    
    # Ensures that app.instance_path exists for SQLite
    os.makedirs(app.instance_path, exist_ok = True)
    
    #########
    # Pages #
    #########

    @app.route('/')
    def hello():
        return "hi!!!"

    # Database initialization
    from . import db
    db.init_app(app)

    return app

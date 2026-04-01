import os

from flask import (
        Flask,
        render_template
)
from flask_login import (
    LoginManager,
    current_user
)

from .user import User

def create_app(test_config=None):
    # Create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('CLIENT_SECRET', 'dev'),
        DATABASE = os.path.join(app.instance_path, 'moonlite.sqlite')
    )

    if test_config is None:
        # Apply config pyfile if no test config is applied
        app.config.from_pyfile('config.py', silent = True)
    else:
        # Otherwise, apply the test config
        app.config.from_mapping(test_config)

    login_manager = LoginManager()
    login_manager.init_app(app)
    
    # Ensures that app.instance_path exists for SQLite
    os.makedirs(app.instance_path, exist_ok = True)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)
    
    @app.route('/')
    def index():
        return render_template("index.html")

    # Database initialization
    from . import db
    db.init_app(app)

    # Blueprint registration for authorization
    from . import auth
    app.register_blueprint(auth.bp)

    return app

import os, uuid

from flask import (
        Flask,
        render_template,
        send_from_directory
)
from flask_login import (
    LoginManager,
    current_user
)

from .user import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    user = User.get(user_id)
    return user

def create_app(test_config=None):
    # Create and configure app
    app = Flask(__name__, static_folder="dist/assets", template_folder="dist")
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY'),
        DATABASE = os.path.join(app.instance_path, 'moonlite.sqlite'),
        # IMPORTANT: flask_login needs these cookies for proper sign in and sign out
        SESSION_COOKIE_SAMESITE = "Lax",
        SESSION_COOKIE_SECURE = True
    )

    app.config["INSTANCE_ID"] = str(uuid.uuid4())
    print("APP INSTANCE CREATED:", app.config["INSTANCE_ID"])

    if test_config is None:
        # Apply config pyfile if no test config is applied
        app.config.from_pyfile('config.py', silent = True)
    else:
        # Otherwise, apply the test config
        app.config.from_mapping(test_config)

    login_manager.init_app(app)

    # Ensures that app.instance_path exists for SQLite
    os.makedirs(app.instance_path, exist_ok = True)

    
    # Redirect to index.html for Vue frontend
    @app.route('/')
    def serve_frontend():
        return send_from_directory("dist", "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        return send_from_directory("dist", path)

    # Database initialization
    from . import db
    db.init_app(app)

    # Blueprint registrations
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import api
    app.register_blueprint(api.bp)

    return app

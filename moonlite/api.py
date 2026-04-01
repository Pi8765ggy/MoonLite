from flask import Blueprint, g, jsonify, session
from .db import get_db
from flask_login import current_user

bp = Blueprint('api', __name__, url_prefix = '/api')

@bp.route("/moon")
def moon():
    return jsonify({
        "phase": "Full Moon"
    })

@bp.route("/user")
def user():
    print(session)
    if current_user.is_authenticated:
        return jsonify({
            "logged_in": True,
            "username": current_user.name,
            "email": current_user.email,
            "picture": current_user.profile_pic
        })
    else:
        return jsonify({
            "logged_in": False
        })


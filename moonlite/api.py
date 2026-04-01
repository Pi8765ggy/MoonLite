from flask import Blueprint, g, jsonify

bp = Blueprint('api', __name__, url_prefix = '/api')

@bp.route("/moon")
def moon():
    return jsonify({
        "phase": "Full Moon"
    })

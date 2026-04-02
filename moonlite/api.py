from flask import Blueprint, g, jsonify, session
from .db import get_db
from flask_login import current_user
import base64, os, requests

bp = Blueprint('api', __name__, url_prefix = '/api')

@bp.route("/moon")
def moon():
    # Required format by AstronomyAPI. More details on their website.
    appID = os.environ.get("ASTRONOMY_ID")
    appSecret = os.environ.get("ASTRONOMY_SECRET")
    userpass = appID + ':' + appSecret
    authString = base64.b64encode(userpass.encode()).decode()

    url = "https://api.astronomyapi.com/api/v2/bodies"

    headers = {
        "Authorization": "Basic " + authString
    }
    
    response = requests.get(url, headers = headers)

    print(response.status_code)
    print(response.json())

    return jsonify({
        "phase": "Full Moon"
    })
    

@bp.route("/user")
def user():
    print(session)
    if current_user.is_authenticated:
        return jsonify({
            "logged_in": True,
            "name": current_user.name,
            "email": current_user.email,
            "picture": current_user.profile_pic
        })
    else:
        return jsonify({
            "logged_in": False
        })


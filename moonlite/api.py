from flask import Blueprint, g, jsonify, session
from .db import get_db
from flask_login import current_user
import base64, os, requests
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

bp = Blueprint('api', __name__, url_prefix = '/api')

@bp.route("/moon_phase")
def moon_phase():
    # Required format by AstronomyAPI. More details on their website.
    appID = os.environ.get("ASTRONOMY_ID")
    appSecret = os.environ.get("ASTRONOMY_SECRET")
    userpass = appID + ':' + appSecret
    authString = base64.b64encode(userpass.encode()).decode()

    headers = {
        "Authorization": "Basic " + authString
    }

    url = "https://api.astronomyapi.com/api/v2/studio/moon-phase"

    # TODO: implement getting user lat and long
    latitude = os.environ.get("UCD_LAT")
    longitude = os.environ.get("UCD_LONG")

    body = {
    "format": "png",
    "style": {
        "moonStyle": "default",
        "backgroundStyle": "stars",
        "backgroundColor": "red",
        "headingColor": "white",
        "textColor": "red"
    },
    "observer": {
        "latitude": float(latitude),
        "longitude": float(longitude),
        "date": date.today().strftime("%Y-%m-%d")
    },
        "view": {
            "type": "portrait-simple",
        }
    }

    # Reponse is a url to the image with given body params
    response = requests.post(url, headers = headers, json = body)

    print(response.json())

    return jsonify(response.json())
    

@bp.route("/user")
def user():
    print(session)
    print(current_user.is_authenticated)
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


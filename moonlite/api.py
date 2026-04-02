from flask import Blueprint, g, jsonify, session
from .db import get_db
from flask_login import current_user
import base64, os, requests
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

bp = Blueprint('api', __name__, url_prefix = '/api')

@bp.route("/moon_img")
def moon_img():
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

    day = date.today().strftime("%Y-%m-%d")
    
    body = {
    "format": "svg",
    "style": {
        "moonStyle": "default",
        "backgroundStyle": "solid",
        "backgroundColor": "black",
        # Makes the text invisible
        "headingColor": "black",
        "textColor": "black"
    },
    "observer": {
        "latitude": float(latitude),
        "longitude": float(longitude),
        "date": day
    },
        "view": {
            "type": "portrait-simple",
        }
    }

    # Reponse is a url to the image with given body params
    try:
        response = requests.post(url, headers = headers, json = body)
    except:
        return jsonify(None), 404 # - ERROR
    
    # Extract the image url from the response
    url = response.json()["data"]["imageUrl"]

    body = {
        "imageUrl": url,
        "date": day
    }

    return jsonify(body), 201

@bp.route("/moon_data")
def moon_data():

    return jsonify(None), 404;

@bp.route("/user")
def user():
    # print(session)
    # print(current_user.is_authenticated)
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


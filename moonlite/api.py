from flask import Blueprint, g, jsonify, session, request
from .db import get_db
from flask_login import current_user
import base64, os, requests
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# API URL syntax
# 

bp = Blueprint('api', __name__, url_prefix = '/api')

def genAPIAuth():
    # Required form by astronomy API. More details on website.
    appID = os.environ.get("ASTRONOMY_ID")
    appSecret = os.environ.get("ASTRONOMY_SECRET")
    userpass = appID + ':' + appSecret
    authString = base64.b64encode(userpass.encode()).decode()

    return "Basic " + authString


@bp.route("/moon_img")
def moon_img():

    headers = {
        "Authorization": genAPIAuth()
    }

    url = "https://api.astronomyapi.com/api/v2/studio/moon-phase"

    defaultLat = os.environ.get("UCD_LAT")
    defaultLong = os.environ.get("UCD_LONG")
    defaultDay = date.today().strftime("%Y-%m-%d")

    rLat = request.args.get("lat")
    rLong = request.args.get("lon")
    rDatetime = request.args.get("dt")

    if rLat == "null" or rLong == "null" or rDatetime == "null":
        latitude = defaultLat
        longitude = defaultLong
        day = defaultDay
    else:
        latitude = rLat
        longitude = rLong
        dt = datetime.fromisoformat(rDatetime)
        day = dt.strftime("%Y-%m-%d")

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
        # Note: For some strange reason, querying the moon phase endpoint
        # requires the lat and long as floats, but the bodies positions endpoint
        # needs them as strings. perhaps post an issue to AstronomyAPI?
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
    imgurl = response.json()["data"]["imageUrl"]

    body = {
        "imageUrl": imgurl,
    }

    return jsonify(body), 200

@bp.route("/moon_data")
def moon_data():

    defaultLat = os.environ.get("UCD_LAT")
    defaultLong = os.environ.get("UCD_LONG")
    defaultDay = date.today().strftime("%Y-%m-%d")
    defaultTime = datetime.now().strftime("%H:%M:%S")

    rLat = request.args.get("lat")
    rLong = request.args.get("lon")
    rDatetime = request.args.get("dt")

    print(rLat)
    print(rLong)
    print(rDatetime)

    if rLat == "null" or rLong == "null" or rDatetime == "null":
        latitude = defaultLat
        longitude = defaultLong
        day = defaultDay
        time = defaultTime
    else:
        latitude = rLat
        longitude = rLong
        dt = datetime.fromisoformat(rDatetime)
        day = dt.strftime("%Y-%m-%d")
        time = dt.strftime("%H:%M:00")
    
    headers = {
        "Authorization": genAPIAuth()
    }

    url = "https://api.astronomyapi.com/api/v2/bodies/positions/moon"

    # TODO: implement getting user lat and long

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "elevation": "0",
        "from_date": day,
        "to_date": day,
        "time": time
    }

    try:
        response = requests.get(url, params = params, headers = headers)
        response = response.json()
    except:
        return jsonify({"message": "Erorr in querying atronomy API. Check /moon_data endpoint"}), 500 # - ERROR
    
    # Location object has three keys:
    # longitude - Float
    # latitude - Float
    # elevation - Integer
    qlocation = response["data"]["observer"]["location"]

    # AstroAPI returns "rows" of data, where each row is a different celestial body.
    # It also returns an array of "positions", where each element is a different day.
    # We only query one body (the moon) and one day, 
    # so we want the first (and only) element of rows and positions

    qmoon = response["data"]["table"]["rows"][0]["cells"][0]
    isodate = qmoon["date"]
    dt = datetime.fromisoformat(isodate)
    qdate = dt.strftime("%m / %d / %Y")
    qtime = dt.strftime("%H:%M")
    # dist in km is a string, but dont need such precision for display.
    # convert to float, then round, then convert back to string.
    qdistKM = str(round(float(qmoon["distance"]["fromEarth"]["km"])))
    
    tempalt = qmoon["position"]["horizontal"]["altitude"]["string"]
    tempaltfloat = float(qmoon["position"]["horizontal"]["altitude"]["degrees"]) 
    tempaz = qmoon["position"]["horizontal"]["azimuth"]["string"]

    # If altitude is below horizon, (ie, less than zero), return a basic message
    if tempaltfloat <= 0:
        tempalt = "Below Horizon"

    qposition = {
        "altitude": tempalt,
        "azimuth": tempaz
    }

    qphase = qmoon["extraInfo"]["phase"]["string"]

    formatted = {
        "date": qdate,
        "time": qtime,
        "distance": qdistKM,
        "position": qposition,
        "phase": qphase,
        "location": {
            "latitude": latitude,
            "longitude": longitude
        }
    }
    
    print(formatted)
    return jsonify(formatted), 200

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


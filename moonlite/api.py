from flask import Blueprint, jsonify, request
from .db import get_db
from flask_login import current_user
import base64, os, requests
from datetime import datetime, date

bp = Blueprint('api', __name__, url_prefix = '/api')

# Generates API key as specified by AstronomyAPI.
# More details on AstronomyAPI website.
def genAPIAuth():
    appID = os.environ.get("ASTRONOMY_ID", "")
    appSecret = os.environ.get("ASTRONOMY_SECRET", "")
    userpass = appID + ':' + appSecret
    authString = base64.b64encode(userpass.encode()).decode()

    return "Basic " + authString

# Endpoint for generating the moon image.
# Should be fetched with GET by frontend.
# Expects three url params: lat, lon, dt
# lat and lon should be floats, and dt should be datetime in ISO format.
@bp.route("/moon_img")
def moon_img():
    
    # Generate authorization key
    headers = {
        "Authorization": genAPIAuth()
    }
    
    # AstronomyAPI endpoint for moon image
    url = "https://api.astronomyapi.com/api/v2/studio/moon-phase"

    # Default values. Currently set to UC Davis location.
    # Exact values stored in .env
    # Change this variable and the .env file name to set a different default location.
    defaultLat = os.environ.get("UCD_LAT")
    defaultLong = os.environ.get("UCD_LONG")
    # Defualt day is the current day.
    defaultDay = date.today().strftime("%Y-%m-%d")

    # Gets params from url
    rLat = request.args.get("lat")
    rLong = request.args.get("lon")
    rDatetime = request.args.get("dt")

    # Should only ever be null on the first request.
    # Form and frontend theoretically prevent bad values from coming into backend.
    if rLat == "null" or rLong == "null" or rDatetime == "null" or rLat is None or rLong is None or rDatetime is None:
        latitude = defaultLat
        longitude = defaultLong
        day = defaultDay
    else:
        latitude = rLat
        longitude = rLong
        dt = datetime.fromisoformat(rDatetime)
        day = dt.strftime("%Y-%m-%d")

    # Format for inputting data into AstronomyAPI
    # More info found on website
    body = {
    "format": "svg",
    "style": {
        "moonStyle": "default",
        "backgroundStyle": "stars",
        "backgroundColor": "black",
        "headingColor": "black",
        "textColor": "black"
    },
    "observer": {
        # Note: For some strange reason, querying the moon phase endpoint
        # requires the lat and long as floats, but the bodies positions endpoint
        # needs them as strings. perhaps send a letter to AstronomyAPI?
        "latitude": float(latitude),
        "longitude": float(longitude),
        "date": day
    },
            "view": {
            "type": "portrait-simple",
        }
    }

    # Reponse is a url to the image with given body params
    # Strangely, they want a post request, its specified in the documentation.
    try:
        response = requests.post(url, headers = headers, json = body)
    except:
        return jsonify({"message": "Erorr in querying atronomy API. Check /moon_img endpoint"}), 500
    
    # Extract the image url from the response
    imgurl = response.json()["data"]["imageUrl"]

    body = {
        "imageUrl": imgurl,
    }

    # Return the url as an http response.
    return jsonify(body), 200

# Endpoint for querying data about the moon at a given datetime and location.
# Should be fetched with GET by frontend.
# Expects three url params: lat, lon, dt
# lat and lon should be floats, and dt should be datetime in ISO format.
@bp.route("/moon_data")
def moon_data():

    # Default values as specified in .env
    # Can be changed to any valid float.
    defaultLat = os.environ.get("UCD_LAT")
    defaultLong = os.environ.get("UCD_LONG")
    # Default datetime is today and right now
    defaultDay = date.today().strftime("%Y-%m-%d")
    defaultTime = datetime.now().strftime("%H:%M:%S")

    # Get args from url
    rLat = request.args.get("lat")
    rLong = request.args.get("lon")
    rDatetime = request.args.get("dt")

    # Should only be null on first request (load).
    # All other inputs (on submit form) should already be verified by the vue frontend.
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
    
    # Get authorization key
    headers = {
        "Authorization": genAPIAuth()
    }

    # URL for AstronomyAPI moon data
    url = "https://api.astronomyapi.com/api/v2/bodies/positions/moon"
    
    # params to query data
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
    # It also returns an array of "cells", where each element is a different day.
    # We only query one body (the moon) and one day, 
    # so we want the first (and only) element of rows and cells

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

    # formatted data for frontend to recieve.
    # DO NOT change the object format. MUST update how the frontend recieves data to make changes.
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
    
    return jsonify(formatted), 200

# Endpoint for querying user information.
# Checks the current_user provided by flask_login.
@bp.route("/user")
def user():
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


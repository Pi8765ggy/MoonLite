import functools
import json
import os

from flask import (
    Blueprint,
    g, 
    redirect, 
    render_template, 
    request, 
    session, 
    url_for,
    jsonify,
    current_app
)

from flask_login import (
    LoginManager,
    login_required,
    login_user,
    logout_user,
    current_user
)

from oauthlib.oauth2 import WebApplicationClient
import requests

from .user import User

# Config for google login
GOOGLE_CLIENT_ID = os.environ.get("CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)

bp = Blueprint('auth', __name__, url_prefix = '/auth')

# Endpoint to login to google.
# Should be redirected to by the frontend, not just fetched.
@bp.route("/login")
def login():
    # Get Google URL for login
    # If fails for some reason, send user back to home page.
    try:
        google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    except:
        return redirect(url_for('serve_frontend'))
    
    # Google OAuth endpoint to sign in
    auth_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = client.prepare_request_uri(
        auth_endpoint,
        redirect_uri = request.base_url + "/callback",
        scope = ["openid", "email", "profile"],
    )

    return redirect(request_uri)

# Callback endpoint as specified in above endpoint
@bp.route("/login/callback")
def callback():
    code = request.args.get("code")
    
    # Get token endpoint
    google_provider_cfg = requests.get(GOOGLE_DISCOVERY_URL).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    
    # Prepare request for tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    # Response from request
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )
    
    # Parse tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Get user info from google endpoint using tokens.
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    
    # If email is successfully verified, get specific values from json.
    if userinfo_response.json().get("email_verified"):
        uid = userinfo_response.json()["sub"]
        user_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        given_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400
    
    # Create new user object with parameters from Google
    user = User(
        id_ = uid, name = given_name, email = user_email, profile_pic = picture 
    )
    
    # Add to database if not exists already.
    if not User.get(uid):
        User.create(uid, given_name, user_email, picture)

    # Login with login manager and send back to home page.
    login_user(user)
    return redirect(url_for('serve_frontend'))

# Simply logs out using login manager. Do not need to query google.
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return jsonify({
        "message": "logged out"
    })

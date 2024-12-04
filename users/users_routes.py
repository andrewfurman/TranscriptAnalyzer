from functools import wraps
from flask import Blueprint, jsonify, session, redirect, url_for, current_app
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

# Create Blueprint
users_bp = Blueprint('users', __name__)

# Auth0 config
oauth = OAuth(current_app)

auth0 = oauth.register(
    'auth0',
    client_id=env.get('AUTH0_CLIENT_ID'),
    client_secret=env.get('AUTH0_CLIENT_SECRET'),
    api_base_url=f'https://{env.get("AUTH0_DOMAIN")}',
    access_token_url=f'https://{env.get("AUTH0_DOMAIN")}/oauth/token',
    authorize_url=f'https://{env.get("AUTH0_DOMAIN")}/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)

# Login route
@users_bp.route('/login')
def login():
    return auth0.authorize_redirect(
        redirect_uri=url_for('users.callback', _external=True)
    )

# Callback route
@users_bp.route('/callback')
def callback():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session['jwt_payload'] = userinfo
    session['user'] = {
        'user_id': userinfo['sub'],
        'email': userinfo.get('email', ''),
        'name': userinfo.get('name', '')
    }
    return redirect('/analyze')

# Logout route
@users_bp.route('/logout')
def logout():
    session.clear()
    return redirect(
        'https://' + env.get('AUTH0_DOMAIN') + '/v2/logout?' +
        urlencode(
            {
                'returnTo': url_for('index', _external=True),
                'client_id': env.get('AUTH0_CLIENT_ID')
            },
            quote_via=quote_plus
        )
    )

# Require auth decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated
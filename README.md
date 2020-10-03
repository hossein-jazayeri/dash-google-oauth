# Dash Google OAuth

This is a simple library using Google OAuth to authenticate and view a Dash app
written based on [dash-auth](https://github.com/plotly/dash-auth).

### Setup
```
$ pip install dash-google-oauth
```
Define following EVN variables:
```
FLASK_SECRET_KEY

GOOGLE_AUTH_URL
GOOGLE_AUTH_SCOPE
GOOGLE_AUTH_TOKEN_URI
GOOGLE_AUTH_REDIRECT_URI
GOOGLE_AUTH_USER_INFO_URL
GOOGLE_AUTH_CLIENT_ID
GOOGLE_AUTH_CLIENT_SECRET
```
Example envs using [python-dotenv](https://pypi.org/project/python-dotenv/):
```
FLASK_SECRET_KEY="..."

GOOGLE_AUTH_URL=https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent
GOOGLE_AUTH_SCOPE="openid email profile"
GOOGLE_AUTH_TOKEN_URI=https://oauth2.googleapis.com/token
GOOGLE_AUTH_REDIRECT_URI=http://localhost:5000/login/callback
GOOGLE_AUTH_USER_INFO_URL=https://www.googleapis.com/userinfo/v2/me
GOOGLE_AUTH_CLIENT_ID="..."
GOOGLE_AUTH_CLIENT_SECRET="..."
```

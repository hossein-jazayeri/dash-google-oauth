import os

import flask
from authlib.client import OAuth2Session

from .auth import Auth

COOKIE_EXPIRY = 60 * 60 * 24 * 14
COOKIE_AUTH_USER_NAME = 'AUTH-USER'
COOKIE_AUTH_ACCESS_TOKEN = 'AUTH-TOKEN'

AUTH_STATE_KEY = 'auth_state'

CLIENT_ID = os.environ.get('GOOGLE_AUTH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('GOOGLE_AUTH_CLIENT_SECRET')
AUTH_REDIRECT_URI = os.environ.get('GOOGLE_AUTH_REDIRECT_URI')


class GoogleAuth(Auth):
    def __init__(self, app):
        Auth.__init__(self, app)
        app.server.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
        app.server.config['SESSION_TYPE'] = 'filesystem'

        @app.server.route('/login/callback')
        def callback():
            return self.login_callback()

        @app.server.route('/logout')
        def logout():
            return self.logout()

    def is_authorized(self):
        user = flask.request.cookies.get(COOKIE_AUTH_USER_NAME)
        token = flask.request.cookies.get(COOKIE_AUTH_ACCESS_TOKEN)
        if not user or not token:
            return False
        return flask.session.get(user) == token

    def login_request(self):
        session = OAuth2Session(
            CLIENT_ID,
            CLIENT_SECRET,
            scope=os.environ.get('GOOGLE_AUTH_SCOPE'),
            redirect_uri=AUTH_REDIRECT_URI
        )

        uri, state = session.create_authorization_url(os.environ.get('GOOGLE_AUTH_URL'))

        flask.session[AUTH_STATE_KEY] = state
        flask.session.permanent = True

        return flask.redirect(uri, code=302)

    def auth_wrapper(self, f):
        def wrap(*args, **kwargs):
            if not self.is_authorized():
                return flask.Response(status=403)

            response = f(*args, **kwargs)
            return response

        return wrap

    def index_auth_wrapper(self, original_index):
        def wrap(*args, **kwargs):
            if self.is_authorized():
                return original_index(*args, **kwargs)
            else:
                return self.login_request()

        return wrap

    def login_callback(self):
        if 'error' in flask.request.args:
            if flask.request.args.get('error') == 'access_denied':
                return 'You denied access.'
            return 'Error encountered.'

        if 'code' not in flask.request.args and 'state' not in flask.request.args:
            return self.login_request()
        else:
            # user is successfully authenticated
            google = self.__get_google_auth(state=flask.session[AUTH_STATE_KEY])
            try:
                token = google.fetch_token(
                    os.environ.get('GOOGLE_AUTH_TOKEN_URI'),
                    client_secret=CLIENT_SECRET,
                    authorization_response=flask.request.url
                )
            except Exception as e:
                return e.__dict__

            google = self.__get_google_auth(token=token)
            resp = google.get(os.environ.get('GOOGLE_AUTH_USER_INFO_URL'))
            if resp.status_code == 200:
                user_data = resp.json()
                r = flask.redirect('/')
                r.set_cookie(COOKIE_AUTH_USER_NAME, user_data['name'], max_age=COOKIE_EXPIRY)
                r.set_cookie(COOKIE_AUTH_ACCESS_TOKEN, token['access_token'], max_age=COOKIE_EXPIRY)
                flask.session[user_data['name']] = token['access_token']
                return r

            return 'Could not fetch your information.'

    @staticmethod
    def __get_google_auth(state=None, token=None):
        if token:
            return OAuth2Session(CLIENT_ID, token=token)
        if state:
            return OAuth2Session(
                CLIENT_ID,
                state=state,
                redirect_uri=AUTH_REDIRECT_URI
            )
        return OAuth2Session(
            CLIENT_ID,
            redirect_uri=AUTH_REDIRECT_URI,
        )

    @staticmethod
    def logout():
        r = flask.redirect('/')
        r.delete_cookie(COOKIE_AUTH_USER_NAME)
        r.delete_cookie(COOKIE_AUTH_ACCESS_TOKEN)
        return r

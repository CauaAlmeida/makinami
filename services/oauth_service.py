# services/oauth_service.py

from authlib.integrations.flask_client import OAuth
from flask import Flask, redirect, url_for, session
import os

class OAuthService:
    """
    Handles GitHub OAuth authentication.
    """

    def __init__(self, app: Flask):
        self.oauth = OAuth(app)
        self.github = self.oauth.register(
            name='github',
            client_id=os.getenv('GITHUB_CLIENT_ID'),
            client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
            access_token_url='https://github.com/login/oauth/access_token',
            authorize_url='https://github.com/login/oauth/authorize',
            api_base_url='https://api.github.com/',
            client_kwargs={'scope': 'read:user'}
        )

    def login(self):
        """
        Redirects the user to GitHub for authentication.
        """
        redirect_uri = url_for('authorize', _external=True)
        return self.github.authorize_redirect(redirect_uri)

    def authorize(self):
        """
        Handles the callback from GitHub and retrieves user information.
        """
        token = self.github.authorize_access_token()
        user = self.github.get('user').json()
        session['user'] = {
            'username': user['login'],
            'id': user['id']
        }
        return redirect('/')
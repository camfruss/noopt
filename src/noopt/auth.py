from models import *
from my_logger import logger
from parser import *

from base64 import b64encode
from datetime import datetime, timezone
from getpass import getpass
import multiprocessing
from time import time, sleep
import webbrowser

from dotenv import dotenv_values, set_key
import requests


class _AuthManager:

    _base_url = 'https://api.schwabapi.com'
    _oauth_base = f'{_base_url}/v1/oauth'
    _trader_base = f'{_base_url}/trader/v1'
    _marketdata_base = f'{_base_url}/marketdata/v1'

    def __init__(self, env_path='.env', auto_update_token=False):
        _config = dotenv_values(env_path)

        self._env_path = env_path
        self._auth_update_token = auto_update_token

        self._app_key            = _config.get('APP_KEY')
        self._app_secret         = _config.get('APP_SECRET')
        self._redirect_uri       = _config.get('REDIRECT_URI')
        self._access_token       = _config.get('ACCESS_TOKEN')
        self._access_token_time  = _config.get('ACCESS_TOKEN_TIME', 0)
        self._refresh_token      = _config.get('REFRESH_TOKEN')
        self._refresh_token_time = _config.get('REFRESH_TOKEN_TIME', 0)

        self._access_token_timeout  = 30 * 60           # 30 minutes
        self._refresh_token_timeout = 7 * 24 * 60 * 60  # 7 days
        self._request_timeout       = 60                # 60 seconds

        # run background daemon that updates the access token
        self._token_daemon = multiprocessing.Process(target=self._refresh_daemon)
        self._token_daemon.daemon = True
        if (auto_update_token):
            self._token_daemon.start()

    @property 
    def access_token(self):
        return self._access_token

    @property
    def request_timeout(self):
        return self._request_timeout

    def _refresh_daemon(self) -> None:
        """ Refreshes access token every 29 minutes. Intended to run on a background thread. """
        logger.info('Launching access token refresh daemon')
        while True:
            sleep(self._access_token_timeout - 60)
            self.authenticate()

    def _update(self, key_to_set, value_to_set) -> None:
        """ Updates {key_to_set} to {value_to_set} in the environment path """
        logger.info(f'Updating {key_to_set} in {self._env_path}.')
        _ = set_key(self._env_path, key_to_set, value_to_set)

    def _is_access_token_valid(self) -> bool:
        """ True if the access token is 1) provided and 2) valid / not timed-out """
        is_valid = time() - float(self._access_token_time) < self._access_token_timeout - 60  # type: ignore
        is_valid &= self._access_token is not None

        return is_valid

    def _is_refresh_token_valid(self) -> bool:
        """ True if the refresh token is 1) provided and 2) valid / not timed-out """
        is_valid = time() - float(self._refresh_token_time) < self._refresh_token_timeout - 60  # type: ignore
        is_valid &= self._refresh_token is not None

        return is_valid

    def _login_code(self) -> str:
        """ Returns the code provided by the Schwab API during authentication """
        auth_url = f'{self._oauth_base}/authorize?client_id={self._app_key}&redirect_uri={self._redirect_uri}'
        logger.info('Openning webbrowser to Schwab login')
        webbrowser.open(auth_url)

        response_url = getpass(prompt='> Enter response url: ', )

        start_idx, end_idx = response_url.index('code=') + 5, response_url.index('%40')
        response_code = f"{response_url[start_idx:end_idx]}@"

        return response_code

    def _init_access_token(self) -> dict:
        """ Returns the headers needed for initializing the access token """
        data = {
            'grant_type': 'authorization_code',
            'code': self._login_code(),
            'redirect_uri': self._redirect_uri
        }
        return data

    def _refresh_access_token(self):
        """ Returns the headers needed for refreshing the access token """
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token
        }
        return data

    def authenticate(self):
        """ Initializes or refreshes the Schwab API access token """
        if self._is_access_token_valid():
            logger.info('Access token is already valid')
            return

        authorization_code = b64encode(f'{self._app_key}:{self._app_secret}'.encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': f'Basic {authorization_code}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = self._init_access_token() if not self._is_refresh_token_valid() else self._refresh_access_token()

        message = 'updating' if self._is_refresh_token_valid() else 'initializing'
        logger.info(f'POST: {message} access token')

        response: requests.Response = requests.post(
            url=f'{self._oauth_base}/token',
            headers=headers,
            data=data
        )
        logger.info(response.json())

        access_token = response.json().get('access_token')
        refresh_token = response.json().get('refresh_token')

        self._update('ACCESS_TOKEN', access_token)
        self._update('REFRESH_TOKEN', refresh_token)
        self._update('REFRESH_TOKEN_TIME', str(time()))


auth_manager = _AuthManager()
__all__ = ['auth_manager']


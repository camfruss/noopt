from base64 import b64encode
from getpass import getpass
from time import time, sleep
import webbrowser

import requests
from dotenv import dotenv_values, set_key


class Config:

    def __init__(self, env_path='.env', auto_update_token=False):
        _config = dotenv_values(env_path)

        self._env_path = env_path
        self._auth_update_token = auto_update_token

        self._app_key            = _config.get('APP_KEY')
        self._app_secret         = _config.get('APP_SECRET')
        self._redirect_uri       = _config.get('REDIRECT_URI')
        self._access_token       = _config.get('ACCESS_TOKEN')
        self._refresh_token      = _config.get('REFRESH_TOKEN')
        self._refresh_token_time = _config.get('REFRESH_TOKEN_TIME', 0)

        self._access_token_timeout  = 30 * 60           # 30 minutes
        self._refresh_token_timeout = 7 * 24 * 60 * 60  # 7 days

        while (self._auth_update_token):
            sleep(self._access_token_timeout)
            self.authenticate()

    def _update(self, key_to_set, value_to_set):
        """ """
        _ = set_key(self._env_path, key_to_set, value_to_set)

    def _oath_endpoint(self, x: str) -> str:
        """ """
        return f'https://api.schwabapi.com/v1/oauth{x}'

    def _is_token_valid(self):
        """ 
        """
        is_valid = time() - float(self._refresh_token_time) < self._access_token_timeout - 60  # type: ignore
        is_valid &= self._refresh_token is not None

        return is_valid

    def _login_code(self):
        """
        """
        auth_url = self._oath_endpoint(f'/authorize?client_id={self._app_key}&redirect_uri={self._redirect_uri}')
        webbrowser.open(auth_url)

        response_url = getpass(prompt='> Enter response url: ', )

        start_idx, end_idx = response_url.index('code=') + 5, response_url.index('%40')
        response_code = f"{response_url[start_idx:end_idx]}@"

        return response_code

    def _init_access_token(self):
        data = {
            'grant_type': 'authorization_code',
            'code': self._login_code(),
            'redirect_uri': self._redirect_uri
        }
        return data

    def _refresh_access_token(self):
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token
        }
        return data

    def authenticate(self):
        """ Initializes or refreshes the Schwab API access token """
        authorization_code = b64encode(f'{self._app_key}:{self._app_secret}'.encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': f'Basic {authorization_code}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = self._init_access_token() if not self._is_token_valid() else self._refresh_access_token()
        response: requests.Response = requests.post(
            url=self._oath_endpoint('/token'),
            headers=headers,
            data=data
        )

        access_token = response.json().get('access_token')
        refresh_token = response.json().get('refresh_token')

        self._update('ACCESS_TOKEN', access_token)
        self._update('REFRESH_TOKEN', refresh_token)
        self._update('REFRESH_TOKEN_TIME', str(time()))

def main():
    config = Config() 
    config.authenticate()

if __name__ == "__main__":
    main()


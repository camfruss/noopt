from models import *
from my_logger import logger
from parser import *

from base64 import b64encode
from getpass import getpass
import multiprocessing
from time import time, sleep
import webbrowser

import requests
from dotenv import dotenv_values, set_key


class Client:

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

    def _refresh_daemon(self):
        while True:
            sleep(self._access_token_timeout - 60)
            self.authenticate()

    def _update(self, key_to_set, value_to_set):
        """ """
        _ = set_key(self._env_path, key_to_set, value_to_set)
        logger.info(f'Updated {key_to_set} in {self._env_path}.')

    def _is_access_token_valid(self):
        """ 
        """
        is_valid = time() - float(self._access_token_time) < self._access_token_timeout - 60  # type: ignore
        is_valid &= self._access_token is not None

        return is_valid

    def _is_refresh_token_valid(self):
        """ 
        """
        is_valid = time() - float(self._refresh_token_time) < self._refresh_token_timeout - 60  # type: ignore
        is_valid &= self._refresh_token is not None

        return is_valid

    def _login_code(self):
        """
        """
        auth_url = f'{self._oauth_base}/authorize?client_id={self._app_key}&redirect_uri={self._redirect_uri}'
        logger.info('Openning webbrowser to Schwab login')
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
        if self._is_access_token_valid():
            return

        authorization_code = b64encode(f'{self._app_key}:{self._app_secret}'.encode('utf-8')).decode('utf-8')
        headers = {
            'Authorization': f'Basic {authorization_code}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = self._init_access_token() if not self._is_refresh_token_valid() else self._refresh_access_token()
        response: requests.Response = requests.post(
            url=f'{self._oauth_base}/token',
            headers=headers,
            data=data
        )

        access_token = response.json().get('access_token')
        refresh_token = response.json().get('refresh_token')

        self._update('ACCESS_TOKEN', access_token)
        self._update('REFRESH_TOKEN', refresh_token)
        self._update('REFRESH_TOKEN_TIME', str(time()))

    def _market_data_request(self, endpoint: str, params: dict):
        """
        quotes(take in parameters) -> construct get_request -> parse response -> return
        """
        return requests.get(f'{self._marketdata_base}{endpoint}',
                     headers={'Authorization': f'Bearer {self._access_token}'},
                     params=params,
                     timeout=self._request_timeout)

    def quotes(self,
        symbols: str | list[str],
        fields: str | list[str] = 'all',
        indicative: bool = False
    ):
        """
        Keyword Arguments
        symbols -- 
        fields -- { quote, fundamental, extended, reference, regular, all }
        indicative --
        """
        params = {
            'symbols': symbols,
            'fields': fields,
            'indicative': indicative,
        }
        response = self._market_data_request('/quotes', params=params)
        equities = parse_quotes(response.json())
        return equities

    def expiration_chain(self, symbol: str):
        """
        """
        params = { 
            'symbol': symbol 
        }
        response = self._market_data_request('/expirationchain', params=params)
        expiration_chain = parse_expiration_chain(response.json())
        return expiration_chain

    def chains(self, *,
        symbol: str,
        contract_type: str | None,
        strike_count: int | None,
        include_underlying_quote: bool | None,
        strategy: str | None,
        interval: float | None,
        strike: float | None,
        range_: str | None,
        from_date: datetime | None,
        to_date: datetime | None,
        volatility: float | None,
        underlying_price: float | None,
        interest_rate: float | None,
        days_to_expiration: int | None,
        expiration_month: str | None,
        option_type: str | None,
        entitlement: str | None
    ):
        """
        Keyword Arguments
        symbol -- single symbol 
        contract_type -- contract type | values { CALL, PUT, ALL }
        strike_count -- the number of strikes to return above/below ATM price
        include_underlying_quote -- 
        strategy -- values { SINGLE, ANALYTICAL, COVERED, VERTICAL, CALENDAR, STRANGLE, STRADDLE, BUTTERFLY, CONDOR, DIAGONAL, COLLAR, ROLL }
        interval -- strike interval for SPREAD strategies
        strike -- strike price 
        range_ -- ITM, NTM, OTM
        from_date -- yyyy-MM-dd 
        to_date -- yyyy-MM-dd
        volatility -- volatility to use in ANALYTICAL calculations
        underlying_price -- underlying price to use in ANALYTICAL calculations
        interest_rate -- interest rate to use in ANALYTICAL calculations
        days_to_expiration -- days to expiration to use in ANALYTICAL calculations
        expiration_month -- expiration month | values { JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC, ALL }
        option_type -- 
        entitlement -- { PN, NP, PP }
        """
        params = {
            'symbol': symbol,
            'contractType': contract_type,
            'strikeCount': strike_count,
            'includeUnderlyingQuote': include_underlying_quote,
            'strategy': strategy,
            'interval': interval,
            'strike': strike,
            'range': range_,
            'fromDate': from_date,
            'toDate': to_date,
            'volatility': volatility,
            'underlyingPrice': underlying_price,
            'interest_rate': interest_rate,
            'daysToExpiration': days_to_expiration,
            'expMonth': expiration_month,
            'optionType': option_type,
            'entitlement': entitlement
        }
        params = { k:v for k,v in params.items() if v is not None }
        response = self._market_data_request('/chains', params=params)
        chains = parse_chains(response.json())
        return chains

def main():
    client = Client() 
    client.authenticate()
    _ = client.quotes('AAPL')
    _ = client.expiration_chain('')  # TODO: combine strs to comma separated str

if __name__ == "__main__":
    main()


from models import *
from my_logger import logger
from parser import *

from base64 import b64encode
from datetime import datetime, timezone
from getpass import getpass
import multiprocessing
from pprint import pp
from time import time, sleep
import webbrowser

from dotenv import dotenv_values, set_key
import polars as pl
import requests


USE_CACHED = True  # load cached API responses

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

    @staticmethod
    def _str_format(symbols: str | list[str]) -> str:
        return ','.join(symbols) if isinstance(symbols, list) else str  # type: ignore

    def _refresh_daemon(self):
        while True:
            sleep(self._access_token_timeout - 60)
            self.authenticate()

    def _update(self, key_to_set, value_to_set):
        """ 
        """
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
        self._update('REFRESH_TOKEN_TIME', str(time()))  # TODO: does refresh toen update? or just access token? 

    def _market_data_request(self, endpoint: str, params: dict):
        """
        quotes(take in parameters) -> construct get_request -> parse response -> return
        """
        if USE_CACHED:
            with open(f'./data{endpoint}.json', 'r') as f:
                response = json.loads(f.read())
        else:
            response = requests.get(
                f'{self._marketdata_base}{endpoint}',
                headers={'Authorization': f'Bearer {self._access_token}'},
                params=params,
                timeout=self._request_timeout
            )
            response = response.json()

        return response

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
            'symbols': Client._str_format(symbols),
            'fields': fields,
            'indicative': indicative,
        }
        response = self._market_data_request('/quotes', params=params)
        equities = parse_quotes(response)
        return equities

    def expiration_chain(self, symbol: str):
        """
        """
        params = { 
            'symbol': symbol 
        }
        response = self._market_data_request('/expirationchain', params=params)
        expiration_chain = parse_expiration_chain(response)
        return expiration_chain

    def chains(self, symbol: str, **kwargs):
        """
        Keyword Arguments
        symbol -- single symbol 
        **contract_type : str -- contract type | values { CALL, PUT, ALL }
        **strike_count : int -- the number of strikes to return above/below ATM price
        **include_underlying_quote : bool -- 
        **strategy : str -- values { SINGLE, ANALYTICAL, COVERED, VERTICAL, CALENDAR, STRANGLE, STRADDLE, BUTTERFLY, CONDOR, DIAGONAL, COLLAR, ROLL }
        **interval : float -- strike interval for SPREAD strategies
        **strike : float -- strike price 
        **range : str -- ITM, NTM, OTM
        **from_date : datetime -- yyyy-MM-dd 
        **to_date : datetime -- yyyy-MM-dd
        **volatility : float -- volatility to use in ANALYTICAL calculations
        **underlying_price : float -- underlying price to use in ANALYTICAL calculations
        **interest_rate : float -- interest rate to use in ANALYTICAL calculations
        **days_to_expiration : int -- days to expiration to use in ANALYTICAL calculations
        **expiration_month : str -- expiration month | values { JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC, ALL }
        **option_type : str -- 
        **entitlement : str -- { PN, NP, PP }
        """
        params = {
            'symbol': symbol,
            'contractType': kwargs.get('contract_type', 'ALL'),
            'strikeCount': kwargs.get('strike_count', 5),
            'includeUnderlyingQuote': kwargs.get('include_underlying_quote', False),
            'strategy': kwargs.get('strategy'),
            'interval': kwargs.get('interval'),
            'strike': kwargs.get('strike'),
            'range': kwargs.get('range'),
            'fromDate': kwargs.get('from_date'),
            'toDate': kwargs.get('to_date'),
            'volatility': kwargs.get('volatility'),
            'underlyingPrice': kwargs.get('underlying_price'),
            'interest_rate': kwargs.get('interest_rate'),
            'daysToExpiration': kwargs.get('days_to_expiration'),
            'expMonth': kwargs.get('expiration_month'),
            'optionType': kwargs.get('option_type'),
            'entitlement': kwargs.get('entitlement')
        }
        params = { k:v for k,v in params.items() if v is not None }
        response = self._market_data_request('/chains', params=params)
        chains = parse_chains(response)
        return chains

def main():
    client = Client() 
    #client.authenticate()

    #with open('./data/symbols.txt', 'r') as f:
    #    symbols = f.readlines()
    # 
    #equities = client.quotes(symbols)
    #pl.from_dicts([ equity.to_dict() for equity in equities ]).write_csv(f'./data/{datetime.now(timezone.utc).isoformat()}Z.csv')

    chains = client.chains('AAPL')
    _ = chains.to_dictl()
    pl.from_dicts(chains.to_dictl()).write_csv(f'./data/{datetime.now(timezone.utc).isoformat()}Z.csv')

    
    # _ = client.expiration_chain('')  # TODO: combine strs to comma separated str


if __name__ == "__main__":
    main()


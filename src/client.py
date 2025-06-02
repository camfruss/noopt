from models import *

from base64 import b64encode
from getpass import getpass
import json
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
        self._refresh_token      = _config.get('REFRESH_TOKEN')
        self._refresh_token_time = _config.get('REFRESH_TOKEN_TIME', 0)

        self._access_token_timeout  = 30 * 60           # 30 minutes
        self._refresh_token_timeout = 7 * 24 * 60 * 60  # 7 days
        self._request_timeout       = 60                # 60 seconds

    def _update(self, key_to_set, value_to_set):
        """ """
        _ = set_key(self._env_path, key_to_set, value_to_set)

    def _is_token_valid(self):
        """ 
        """
        is_valid = time() - float(self._refresh_token_time) < self._access_token_timeout - 60  # type: ignore
        is_valid &= self._refresh_token is not None

        return is_valid

    def _login_code(self):
        """
        """
        auth_url = f'{self._oauth_base}/authorize?client_id={self._app_key}&redirect_uri={self._redirect_uri}'
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
            url=f'{self._oauth_base}/token',
            headers=headers,
            data=data
        )

        access_token = response.json().get('access_token')
        refresh_token = response.json().get('refresh_token')

        self._update('ACCESS_TOKEN', access_token)
        self._update('REFRESH_TOKEN', refresh_token)
        self._update('REFRESH_TOKEN_TIME', str(time()))

        while (self._auth_update_token):
            sleep(self._access_token_timeout)
            self.authenticate()

    def _market_data_request(self, endpoint: str, params: dict):
        """
        quotes(take in parameters) -> construct get_request -> parse response -> return
        """
        return requests.get(f'{self._marketdata_base}{endpoint}',
                     headers={'Authorization': f'Bearer {self._access_token}'},
                     params=params,
                     timeout=self._request_timeout)

    def _parse_quotes(self) -> list[Equity]:
        """
        endpoint: /quotes
        """
        with open('./data/quotes.json', 'r') as f:
            response = json.loads(f.read())

        equities = []
        for _, value in response.items():
            if value['assetMainType'] != 'EQUITY':
                continue

            equity = Equity(**value)
            equity.reference = Reference(**value.get('reference', {}))
            equity.quote = Quote(**value.get('quote', {}))
            equity.regular = Regular(**value.get('regular', {}))
            equity.fundamental = Fundamental(**value.get('fundamental', {}))
            equities.append(equity)

        return equities

    def quotes(self,
        symbols: str | list[str],
        fields: str | list[str] = 'all',
        indicative: bool = False
    ):
        """
        { quote, fundamental, extended, reference, regular, all }
        """

        params = {
            'symbols': symbols,
            'fields': fields,
            'indicative': indicative,
        }
        _ = self._market_data_request('/quotes', params=params)

    def _parse_expiration_chain(self) -> list[ExpirationDate]:
        """
        endpoint: /expirationchain
        
        Gets series of expiration dates for an optionable symbol
        """
        with open('./data/expirationchain.json', 'r') as f:
            response = json.loads(f.read())['expirationList']

        expiration_dates = []
        for elm in response:
            expiration_dates.append(ExpirationDate(**elm))

        return expiration_dates

    def expiration_chain(self):
        ...

    def _parse_chains(self) -> tuple[dict[datetime, list[Contract]], dict[datetime, list[Contract]]]:
        """
        endpoint: /chains
        
        Gets pair of call and put contracts
        """
        with open('./data/aapl.json', 'r') as f:
            response = json.loads(f.read())
            
        def date_map(key):
            date_format = "%Y-%m-%d"
            
            result = {}
            for expr_date_str, contracts in response[key].items():
                date = datetime.strptime(expr_date_str.partition(':')[0], date_format)
                for _, data in contracts.items():
                    result[date] = Contract(**data[0])
            return result

        calls = date_map('callExpDateMap')
        puts = date_map('putExpDateMap')
        return calls, puts

    def chains(self,
        symbol: str,
        contract_type: str,  # CALL, PUT, ALL
        strike_count: int,
        include_underlying_quote: bool,
        strategy: str,  # SINGLE, ANALYTICAL, COVERED, VERTICAL, CALENDAR, STRANGLE, STRADDLE, BUTTERFLY, CONDOR, DIAGONAL, COLLAR, ROLL
        interval: float,
        strike: float,
        range_: str,  # ITM, NTM, OTM
        from_date: datetime,  # yyyy-MM-dd 
        to_date: datetime,  # yyyy-MM-dd
        volitility: float,
        underlying_price: float,
        interest_rate: float, 
        days_to_expiration: int,  # applies to ANALYTICAL only
        expiration_month: str,  # JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC, ALL
        option_type: str,
        entitlement: str  # PN, NP, PP
    ):
        """
        """
        params = {
            'symbol': symbol,
            'contractType': contract_type.upper(),
            'strikeCount': strike_count
        }
        _ = self._market_data_request('/chains', params=params)
        

def main():
    client = Client() 
    client.authenticate()

if __name__ == "__main__":
    main()


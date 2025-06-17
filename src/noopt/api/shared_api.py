from auth import auth_manager
from config import config

from enum import Enum
import json

import requests


class APICategory(Enum):
    """
    Schwab has 6 API Products
    1. Account & Client Data
    2. Advisor Services
    3. Data Aggregation Services
    4. Tax Data
    5. Trader API - Commerical
    6. Trader API - Individual 

    Only the individual trader API is implemented (as of 2025/06/17), and it's broken into an
    'Accounts and Trading' and 'Market Data' component.
    """
    DATA = 'data'
    TRADER = 'trader'

_base_url = 'https://api.schwabapi.com'
_marketdata_base = f'{_base_url}/marketdata/v1'
_trader_base = f'{_base_url}/'

def str_format(symbols: str | list[str]) -> str:
    """ Formats list of symbols into API-compatible format """
    return ','.join(symbols) if isinstance(symbols, list) else str  # type: ignore

def api_request(api: APICategory, endpoint: str, params: dict = {}):
    match api:
        case APICategory.DATA:
            pass
        case APICategory.TRADER:
            pass

    if config.use_cache:
        with open(f'./data{endpoint}.json', 'r') as f:
            response = json.loads(f.read())
    else:
        response = requests.get(
            f'{_marketdata_base}{endpoint}',
            headers={'Authorization': f'Bearer {auth_manager.access_token}'},
            params=params,
            timeout=auth_manager.request_timeout
        )
        response = response.json()

    return response


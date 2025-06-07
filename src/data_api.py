from auth import auth_manager
from config import config
from parser import *

import json

import requests


_base_url = 'https://api.schwabapi.com'
_marketdata_base = f'{_base_url}/marketdata/v1'

def _str_format(symbols: str | list[str]) -> str:
    """ Formats list of symbols into API-compatible format """
    return ','.join(symbols) if isinstance(symbols, list) else str  # type: ignore

def _market_data_request(endpoint: str, params: dict):
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


def quotes(
    symbols: str | list[str],
    fields: str | list[str] = 'all',
    indicative: bool = False
):
    """
    Arguments
    symbols -- 
    fields -- { quote, fundamental, extended, reference, regular, all }
    indicative --
    """
    params = {
        'symbols': _str_format(symbols),
        'fields': fields,
        'indicative': indicative,
    }
    response = _market_data_request('/quotes', params=params)
    equities = parse_quotes(response)
    return equities

def expiration_chain(symbol: str):
    """
    """
    params = { 'symbol': symbol }
    response = _market_data_request('/expirationchain', params=params)
    expiration_chain = parse_expiration_chain(response)
    return expiration_chain

def chains(symbol: str, **kwargs):
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
    response = _market_data_request('/chains', params=params)
    chains = parse_chains(response)
    return chains


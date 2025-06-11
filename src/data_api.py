from auth import auth_manager
from config import config
from parser import *

import json
from typing import overload

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

@overload
def quotes(
    symbols: list[str],
    fields: str | list[str] = 'all',
    indicative: bool = False
):
    """
    Get quotes by list of symbols

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

@overload
def quotes(symbol: str, fields: str | list[str]):
    """
    Get quote by a single symbol

    symbol -- 
    fields -- 
    """
    ...

def quotes():
    ...

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

def pricehistory(
    symbols: str,
    period_type: str,
    period: int, 
    frequency_type: str,
    frequency: int,
    start_date: datetime,
    end_date: datetime,
    need_extended_hours_data: bool,
    need_previous_close: bool
):
    """
    symbol
    periodType -- { day, month, year, ytd }
    period -- the number of chart period types with default *
        day -- 1, 2, 3, 4, 5, 10*
        month -- 1*, 2, 3, 6
        year -- 1*, 2, 3, 5, 10, 15, 20
        ytd -- 1*
    frequency_type -- { minute, daily, weekly, monthly }
    frequency -- the time frequency duration
    start_date -- defaults to (end_date - period) excluding weekends, holidays  # UNIX Epoch milliseconds
    end_date -- defaults to market close of previous business day
    need_extended_hours_data -- need extended hours data
    need_previous_close -- need previous close price/date
    """
    ...

def movers(
    symbol_id: str,
    sort: str,
    frequency: int
):
    """
    Get a list of top 10 securities movers for a specific index    
    symbol_id -- index symbol
    sort -- { volume, trades, percent_change_[up|down] }
    frequency -- movers with the specified direction sof up/down { 0*, 1, 5, 10, 30, 60 }
    """
    ...

@overload
def markets(markets: list[str], date: datetime):
    """
    List of markets

    markets -- { equity, option, bond, forex, future }
    date -- [curr, curr+1year], defaults to today  # yyyy-MM-dd format
    """
    ...

@overload
def markets(market_id: str, date: datetime):
    """
    Get market hours for date in the future for a single market

    markets -- { equity, option, bond, forex, future }
    date -- [curr, curr+1year], defaults to today  # yyyy-MM-dd format
    """
    ...

def markets(markets, date):
    return

@overload
def instruments(symbol: str, projection: str):
    """
    symbol -- symbol of a security
    projection -- { symbol-search, symbol-regex, desc-search, desc-regex, search, fundamental }
    """
    ...

@overload
def instruments(cusip_id: str):
    """
    Get basic instrument details

    cusip_id -- cusip of a security
    """
    ...

def instruments():
    return

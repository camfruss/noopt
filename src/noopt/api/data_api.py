from parser import *
from shared_api import APICategory, api_request, str_format


def _market_data_request(endpoint: str, params: dict = {}):
    api_request(APICategory.DATA, endpoint, params=params)

# ----- Quotes -----

def quotes(symbols: list[str], **kwargs):
    """
    Get quotes by list of symbols
    endpoint: /quotes

    Arguments:
        symbols -- list of symbols to retrieve quotes for

    Keyword Arguments:
        fields -- { quote, fundamental, extended, reference, regular, *all }
        indicative : bool --
    """
    params = parse_kwargs({
        'symbols': str_format(symbols),
        'fields': kwargs.get('fields'),
        'indicative': kwargs.get('indicative'),
    })
    response = _market_data_request('/quotes', params=params)
    equities = parse_quotes(response)
    return equities

def quote(symbol: str, fields: str | list[str] = ''):
    """
    Get quote by a single symbol
    endpoint: /{symbol_id}/quotes

    Arguments:
        symbol -- symbol of instrument

    Keyword Arguments:
        fields -- request for a subset of data { quote, fundamental, extended, reference, regular, all* }
    """
    params = parse_kwargs({ 'fields': fields })
    _ = _market_data_request(f'/{symbol}/quotes', params=params)

# ----- Option Chains -----

def chains(symbol: str, **kwargs):
    """
    Get option chain for an optional symbol
    endpoint: /chains

    Arguments:
        symbol -- single symbol 

    Keyword Arguments:
        contract_type : str -- contract type | values { CALL, PUT, ALL }
        strike_count : int -- the number of strikes to return above/below ATM price
        include_underlying_quote : bool -- 
        strategy : str -- values { SINGLE, ANALYTICAL, COVERED, VERTICAL, CALENDAR, STRANGLE, STRADDLE, BUTTERFLY, CONDOR, DIAGONAL, COLLAR, ROLL }
        interval : float -- strike interval for SPREAD strategies
        strike : float -- strike price 
        range : str -- ITM, NTM, OTM
        from_date : datetime -- yyyy-MM-dd 
        to_date : datetime -- yyyy-MM-dd
        volatility : float -- volatility to use in ANALYTICAL calculations
        underlying_price : float -- underlying price to use in ANALYTICAL calculations
        interest_rate : float -- interest rate to use in ANALYTICAL calculations
        days_to_expiration : int -- days to expiration to use in ANALYTICAL calculations
        expiration_month : str -- expiration month | values { JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC, ALL }
        option_type : str -- 
        entitlement : str -- { PN, NP, PP }
    """
    params = parse_kwargs({
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
    })
    response = _market_data_request('/chains', params=params)
    chains = parse_chains(response)
    return chains

def expirationchain(symbol: str):
    """
    Get Option Expiration (Series) information for an optional symbol. Does not include individual
    options contracts for the underlying.
    endpoint: /expirationchain

    Arguments:
        symbol 
    """
    params = parse_kwargs({ 'symbol': symbol })
    response = _market_data_request('/expirationchain', params=params)
    expiration_chain = parse_expiration_chain(response)
    return expiration_chain

# ----- Price History -----

def pricehistory(symbol: str, **kwargs):
    """
    Get historical Open, High, Low, Close, Volume for a given frequency (aggregation). Frequency available is
    dependent on period_type. Date format is in EPOCH milliseconds.
    endpoint: /pricehistory

    Arguments:
        symbol

    Keyword Arguments:
        period_type : str -- { day, month, year, ytd }
        period : int -- the number of chart period types with default *
            day -- 1, 2, 3, 4, 5, 10*
            month -- 1*, 2, 3, 6
            year -- 1*, 2, 3, 5, 10, 15, 20
            ytd -- 1*
        frequency_type : str -- { minute, daily, weekly, monthly }
        frequency : int -- the time frequency duration
        start_date : str-- defaults to (end_date - period) excluding weekends, holidays  # UNIX Epoch milliseconds
        end_date : str -- defaults to market close of previous business day
        need_extended_hours_data : bool -- need extended hours data
        need_previous_close : bool -- need previous close price/date
    """
    params = parse_kwargs({
        'symbol': symbol,
        'periodType': kwargs.get('period_type')
    })
    _ = _market_data_request('/pricehistory', params=params)

# ----- Movers -----

def movers(symbol_id: str, **kwargs):
    """
    Get a list of top 10 securities movers for a specific index    
    endpoint: /movers/{symbol_id}

    Arguments:
        symbol_id -- index symbol
                     { $DJI, $COMPX, $SPX, NYSE, NASDAQ, OTCBB, INDEX_ALL, EQUITY_ALL, OPTION_ALL, 
                       OPTION_PUT, OPTION_CALL }

    Keyword Arguments:
        sort : str -- { VOLUME, TRADES, PERCENT_CHANGE_[UP|DOWN] }
        frequency : int -- movers with the specified direction sof up/down { 0*, 1, 5, 10, 30, 60 }
    """
    params = parse_kwargs({
        'sort': kwargs.get('sort'),
        'frequency': kwargs.get('frequency')
    })
    _ = _market_data_request(f'/movers/{symbol_id}', params=params)

# ----- Market Hours -----

def markets(markets: list[str], **kwargs):
    """
    Get market hours in the future for different markets
    endpoint: /markets 

    Arguments:
        markets -- { equity, option, bond, forex, future }

    Keyword Arguments:
        date : str -- [curr, curr+1year], defaults to today  # yyyy-MM-dd format
    """
    params = parse_kwargs({
        'markets': markets,
        'date': kwargs.get('date')
    })
    _ = _market_data_request('/markets', params=params)

def market(market_id: str, **kwargs):
    """
    Get market hours in the future for a single market
    endpoint: /markets/{market_id}

    Arguments:
        market_id -- { equity, option, bond, forex, future }

    Keyword Arguments:
        date : str -- [curr, curr+1year], defaults to today  # yyyy-MM-dd format
    """
    params = parse_kwargs({ 'date': kwargs.get('date') })
    _ = _market_data_request(f'/markets/{market_id}', params=params)

# ----- Instruments -----

def instruments(symbol: str, projection: str):
    """
    Get instruments by symbols and projections
    endpoint: /instruments

    Arguments:
        symbol -- symbol of a security
        projection -- search by: { symbol-search, symbol-regex, desc-search, desc-regex, search, fundamental }
    """
    params = parse_kwargs({
        'symbol': symbol,
        'projection': projection
    })
    _ = _market_data_request('/instruments', params=params)

def instrument(cusip_id: str):
    """
    Get basic instrument by specific cusip
    endpoint: /instruments/{cusip_id}

    Arguments:
        cusip_id -- cusip of a security
    """
    _ = _market_data_request(f'/instruments/{cusip_id}')


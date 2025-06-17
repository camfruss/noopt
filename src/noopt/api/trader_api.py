from shared_api import APICategory, api_request, str_format 
from parser import parse_kwargs


def _trader_request(endpoint: str, request_type: str = 'GET', params: dict = {}):
    api_request(APICategory.TRADER, endpoint, params=params)

# ----- Common Arguments -----

"""
account_number -- encrypted ID of the account
start_date -- excludes transactions before date, iso-8601 format
end_date -- excludes transactions after date, iso-8601 format
            yyyy-MM-dd'T'HH:mm:ss.SSSZ
status -- only orders of this status should be returned 
          valid options are str repr of trader_enums.Status
max_results : int -- max number of ordered to retrieve, default = 3000
"""

# ----- Accounts -----

def account_numbers():
    """
    Get list of account numbers and their encrypted values
    endpoint: /accounts/accountNumbers
    """
    _ = _trader_request('/accounts/accountNumbers')

def accounts(**kwargs):
    """
    Get linked account(s) balances and positions for the logged in user
    endpoint: /accounts
    
    Keyword Arguments
        fields : str -- which fields to return { positions }
    """
    params = parse_kwargs({ 'fields': str_format(kwargs.get('fields', '')) })
    _ = _trader_request('/accounts', params=params)

def account(account_number: str, **kwargs):
    """
    Get a specific account balance and positions for the logged in user
    endpoint: /accounts/{accountNumber}

    Arguments:
        account_number

    Keyword Arguments:
        fields : str -- which fields to return { positions }
    """
    params = parse_kwargs({ 'fields': str_format(kwargs.get('fields', '')) })
    _ = _trader_request(f'/accounts/{account_number}', params=params)

# ----- Orders -----

def get_orders(account_number: str, start_date: str, end_date: str, **kwargs):
    """
    Get all orders for a specific account. Maximum date range is 1 year.
    endpoint: /accounts/{accountNumber}/orders

    Arguments:
        account_number --
        start_date -- 
        end_date -- 

    Keyword Arguments:
        max_results : int -- max number of ordered to retrieve, default = 3000
        status : str --
    """
    params = parse_kwargs({
        'fromEnteredTime': start_date,
        'toEnteredTime': end_date,
        'maxResults': kwargs.get('max_results'),
        'status': kwargs.get('status')
    })
    _ = _trader_request(f'/accounts/{account_number}', params=params)

def post_order(account_number: str, order: Order):
    """
    Place an order for a specific account.
    endpoint: /accounts/{accountNumber}/orders

    Arguments:
        account_number
        order -- Order request body
    """
    _ = _trader_request(f'/accounts/{account_number}/orders')

def get_order(account_number: str, order_id: str):
    """
    Get a specific order by its ID, for a specific account
    endpoint: /accounts/{accountNumber}/orders/{orderID}

    Arguments:
        account_number
        order_id
    """
    _ = _trader_request(f'/accounts/{account_number}/orders/{order_id}')

def cancel_order(account_number: str, order_id: str):
    """
    Cancel a specific order by its ID, for a specific account
    endpoint: /accounts/{accountNumber}/orders/{orderID}

    Arguments:
        account_number
        order_id
    """
    _ = _trader_request(f'/accounts/{account_number}/orders/{order_id}')

def replace_order(account_number: str, order_id: str):
    """
    Replace a specific order by its ID, for a specific account
    endpoint: /accounts/{accountNumber}/orders/{orderID}

    Arguments:
        account_number
        order_id
    """
    _ = _trader_request(f'/accounts/{account_number}/orders/{order_id}')

def all_orders(start_date: str, end_date: str):
    """
    Get all orders for all accounts
    endpoint: orders

    Arguments:
        start_date -- must be within 60 days from today's date
        end_date

    Keyword Arguments:
        max_results
        status

    """
    params = parse_kwargs({
        '': ,
    })
    _ = _trader_request('/accounts', params=params)

def preview_order(account_number: str, order: Order):
    """
    Preview an order for a specific account
    endpoint: /accounts/{accountNumber}/previewOrder

    ** Coming Soon ** on Schwab
    """

# ----- Transactions -----

def transactions():
    """
    Arguments:
        types -- specifies that only transactions of this status should be returned
                 { TRADE, RECEIVE_AND_DELIVER, DIVIDEND_OR_INTEREST, ACH_RECEIPT, ACH_DISBURSEMENT, 
                   CASH_RECEIPT, CASH_DISBURSEMENT, ELECTRONIC_FUND, WIRE_OUT, WIRE_IN, JOURNAL,
                   MEMORANDUM, MARGIN_CALL, MONEY_MARKET, SMA_ADJUSTMENT }
    Keyword Arguments:
        symbol: str -- if there is any special character in the symbol, send the encoded value

    """
    params = parse_kwargs({
        '': ,
    })
    _ = _trader_request('/accounts', params=params)

def transaction(account_number: str, transaction_id: int):
    """
    Get specific transaction information for a sepcific account

    Arguments:
        account_number
        transaction_id: the ID of the transaction being retrieved
    """
    params = parse_kwargs({
        '': ,
    })
    _ = _trader_request('/accounts', params=params)

# ----- UserPreference -----

def user_preference():
    """
    Get user preference information for the logged in user.
    """
    params = parse_kwargs({
        '': ,
    })
    _ = _trader_request('/accounts', params=params)


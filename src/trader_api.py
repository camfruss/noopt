from typing import override


# ----- Accounts -----

# ----- Orders -----

# ----- Transactions -----

@override
def transactions():
    """
    Arguments:
        account_number -- the encrypted ID of the account
        start_date -- excludes transactions before date, iso-8601 format
        end_date -- excludes transactions after date, iso-8601 format
                    yyyy-MM-dd'T'HH:mm:ss.SSSZ
        types -- specifies that only transactions of this status should be returned
                 { TRADE, RECEIVE_AND_DELIVER, DIVIDEND_OR_INTEREST, ACH_RECEIPT, ACH_DISBURSEMENT, 
                   CASH_RECEIPT, CASH_DISBURSEMENT, ELECTRONIC_FUND, WIRE_OUT, WIRE_IN, JOURNAL,
                   MEMORANDUM, MARGIN_CALL, MONEY_MARKET, SMA_ADJUSTMENT }
    Keyword Arguments:
        symbol: str -- if there is any special character in the symbol, send the encoded value

    """
    ...

@override
def transactions(account_number: str, transaction_id: int):
    """
    Get specific transaction information for a sepcific account

    Arguments:
        account_number: the encrypted ID of the account
        transaction_id: the ID of the transaction being retrieved
    """
    ...

def transactions():
    ...

# ----- UserPreference -----

def user_preference():
    """
    Get user preference information for the logged in user.
    """
    ...

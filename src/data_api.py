from models import *

import json


def quotes() -> list[Equity]:
    """
    endpoint: /quotes
    """
    with open('./tests/quotes.json', 'r') as f:
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

def expiration_chain() -> list[ExpirationDate]:
    """
    endpoint: /expirationchain
    
    Gets series of expiration dates for an optionable symbol
    """
    with open('./tests/expirationchain.json', 'r') as f:
        response = json.loads(f.read())['expirationList']

    expiration_dates = []
    for elm in response:
        expiration_dates.append(ExpirationDate(**elm))

    return expiration_dates

def chains() -> tuple[dict[datetime, list[Contract]], dict[datetime, list[Contract]]]:
    """
    endpoint: /chains
    
    Gets pair of call and put contracts
    """
    with open('./tests/aapl.json', 'r') as f:
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

def serialize():
    ...

def deserialize():
    ...

def main():
    quotes()
    expiration_chain()
    chains()

    ...  
    # have an argparser to restrict data that is taken in
    # --load data.pkl ... store data retrieved
    # --equities file.txt
    # --calls-only --puts-only
    # --strike-width 5
    # --expiration-months [1, 12], default 2
    # --verbose 


if __name__ == "__main__":
    main()


from models import *

import json


def parse_quotes(response) -> list[Equity]:
    """
    endpoint: /quotes
    """
    equities = []
    for _, value in response.items():
        if value.get('assetMainType', '') != 'EQUITY':
            continue

        equity = Equity(**value)
        equity.extended = Extended(**value.get('extended', {}))
        equity.fundamental = Fundamental(**value.get('fundamental', {}))
        equity.quote = Quote(**value.get('quote', {}))
        equity.reference = Reference(**value.get('reference', {}))
        equity.regular = Regular(**value.get('regular', {}))
        equities.append(equity)

    return equities

def parse_expiration_chain(response) -> list[ExpirationDate]:
    """
    Gets series of expiration dates for an optionable symbol
    """
    expiration_dates = []
    for elm in response:
        expiration_dates.append(ExpirationDate(**elm))

    return expiration_dates

def parse_chains(response) -> tuple[dict[datetime, list[Contract]], dict[datetime, list[Contract]]]:
    """
    endpoint: /chains
    
    Gets pair of call and put contracts
    """
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


def main():
    with open('./data/quotes.json', 'r') as f:
        response = json.loads(f.read())
    parse_quotes(response)

    with open('./data/aapl.json', 'r') as f:
        response = json.loads(f.read())

    with open('./data/expirationchain.json', 'r') as f:
        response = json.loads(f.read())['expirationList']
    parse_expiration_chain(response)

if __name__ == '__main__':
    main()

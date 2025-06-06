from models import *

from collections import defaultdict
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

def parse_chains(response) -> Options:
    """
    endpoint: /chains
    
    Gets pair of call and put contracts
    """
    def date_map(key):
        date_format = "%Y-%m-%d"
        
        result = defaultdict(list)
        for expr_date_str, contracts in response[key].items():
            date = datetime.strptime(expr_date_str.partition(':')[0], date_format)
            for _, data in contracts.items():
                result[date].append(Contract(**data[0]))
        return result

    calls = date_map('callExpDateMap')
    puts = date_map('putExpDateMap')
    result = Options(calls=calls, puts=puts)

    return result

def main():
    with open('./data/quotes.json', 'r') as f:
        response = json.loads(f.read())
    parse_quotes(response)

    with open('./data/chains.json', 'r') as f:
        response = json.loads(f.read())
    parse_chains(response)

    with open('./data/expirationchain.json', 'r') as f:
        response = json.loads(f.read())['expirationList']
    parse_expiration_chain(response)

if __name__ == '__main__':
    main()

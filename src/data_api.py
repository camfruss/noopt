from models import *

import argparse
import json
import pickle


def serialize(path, obj) -> None:
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

def deserialize(path) -> type:
    with open(path, 'wb') as f:
        return pickle.load(f)

def get_quotes() -> dict:
    return {}

def quotes() -> list[Equity]:
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

def get_expiration_chain() -> dict:
    return {}

def expiration_chain() -> list[ExpirationDate]:
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

def get_chains() -> dict:
    return {}

def chains() -> tuple[dict[datetime, list[Contract]], dict[datetime, list[Contract]]]:
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--equities', default='./data/spy500.text', help='')
    parser.add_argument('--expiration-months', type=int, default=3, help='[1, 12]')
    parser.add_argument('--strike-width', type=int, default=10, help='')
    parser.add_argument('--verbose', action='store_true')

if __name__ == "__main__":
    main()


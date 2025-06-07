from auth import auth_manager
from config import config
import trader_api as tapi


'''
#with open('./data/symbols.txt', 'r') as f:
#    symbols = f.readlines()

#equities = client.quotes(symbols)
#pl.from_dicts([ equity.to_dict() for equity in equities ]).write_csv(f'./data/{datetime.now(timezone.utc).isoformat()}Z.csv')

chains = client.chains('AAPL')
_ = chains.to_dictl()
pl.from_dicts(chains.to_dictl()).write_csv(f'./data/{datetime.now(timezone.utc).isoformat()}Z.csv')


# _ = client.expiration_chain('')  # TODO: combine strs to comma separated str
'''

def main():
    auth_manager.authenticate()
    config.configure(write_on_response=True)

if __name__ == '__main__':
    main()

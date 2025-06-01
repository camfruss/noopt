import polars as pl

'''
add c_ prefix for cash cc calculations
'''

commission = 0.65  # per contract
margin = 0.50      # set by feds
m_interest_rate = 0.10 # used in OaaSI

dividends = 0

df = pl.DataFrame([vars(obj) for obj in []])

breakeven_price                = pl.col('underlying_ask') - dividends
pts_downside_protection        = pl.col('bid') - pl.col('breakeven_price')
downside_protection            = pl.col('pts_downside_protection') / pl.col('underlying_ask')
net_investment                 = (pl.col('underlying_ask') - pl.col('bid')) * pl.col('multiplier') + commission
profit_if_exercised            = (pl.col('strike_price') + dividends) * pl.col('multiplier') - pl.col('net_investment')
return_if_exercised            = pl.col('profit_if_exercised') / pl.col('net_investment')
profit_if_unchanged            = (pl.col('underlying_ask') + dividends) * pl.col('multiplier') - pl.col('net_investment')
return_if_unchanged            = pl.col('profit_if_unchanged') / pl.col('net_investment')
annualized_return_if_unchanged = 365 * pl.col('return_if_unchanged') / pl.col('days_to_expiration')
#probability_profit             = pl.col('')

m_equity_required                = pl.col('underlying_ask') * m_interest_rate
m_net_investment                 = pl.col('m_equity_required') - (pl.col('bid') * pl.col('multiplier')) + commission
m_debit_balance                  = pl.col('underlying_ask') - pl.col('m_equity_required')
m_interest_changes               = pl.col('m_debit_balance') * m_interest_rate * pl.col('days_to_expiration') / 360,
m_profit_if_exercised            = pl.col('profit_if_exercised') - pl.col('m_interest_changes')
m_return_if_exercised            = pl.col('m_profit_if_exercised') / pl.col('m_net_investment')
m_profit_if_unchanged            = pl.col('profit_if_unchanged') - pl.col('m_net_investment')
m_return_if_unchanged            = pl.col('m_profit_if_unchanged') / pl.col('m_net_investment')
m_breakeven_price                = (pl.col('m_net_investment') + pl.col('m_debit_balance') - (dividends * pl.col('multiplier')) + pl.col('m_interest_changes')) / pl.col('multiplier')
m_pts_downside_protection        = pl.col('underlying_ask') - pl.col('m_breakeven_price')
m_downside_protection            = pl.col('m_pts_downside_protection') / pl.col('underlying_ask')
m_annualized_return_if_unchanged = 365 * pl.col('m_return_if_unchanged') / pl.col('days_to_expiration')
#m_probability_profit             = pl.col('')


def plot():
    ...

def add_columns():
    ...
    # pts. downside protection
    # volatitliy skew

def main():
    ...

if __name__ == "__main__":
    pass


import polars as pl

'''
df = pl.DataFrame([vars(obj) for obj in []])

df.with_columns(
    pts_downside_protection=pl.col('bid'),
    breakeven_price=pl.col('underlying_ask') - pl.col('bid'),
    probability_profit=pl.col(''),
    return_if_exercised=pl.col(''),
    return_if_unchanged=pl.col(''),
    annualized_return_if_unchanged=pl.col(''),

    pts_downside_protection_margined=,
    breakeven_price_margined=,
    probability_profit_margined=,
    return_if_exercised_margined=,
    return_if_unchanged_margined=,
    annualized_return_if_unchanged_margined=,
)
'''

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


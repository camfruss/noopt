from config import config
from my_logger import logger
from models import Equity, Options

import polars as pl


def add_columns(
        underlying : Equity | None = None,
        chains : Options | None = None,
        commission : float = 0.65, 
        acct_margin_req : float = 0.50, 
        m_interest_rate : float = 0.10
    ) -> pl.DataFrame:
    dividends = 0

    if config.use_cache: 
        df = pl.read_csv('./data/chains_df.csv')
        underlying_ask = 200.0        
    else:
        if underlying is None:
            logger.debug('Underlying not provided') 
            raise ValueError
        if chains is None:
            logger.debug('Chains not provided')
            raise ValueError

        df = pl.from_dicts(chains.to_dictl())  # type: ignore
        underlying_ask = underlying.quote.ask_price  # type: ignore

    logger.info('Adding columns to options chain')


    df = df.with_columns(
        c_breakeven_price = underlying_ask - pl.col('bid') - dividends,
        c_net_investment = (underlying_ask - pl.col('bid')) * pl.col('multiplier') + commission,
        m_equity_required = underlying_ask * m_interest_rate,
    ).with_columns(
        c_pts_downside_protection = pl.col('bid') - pl.col('c_breakeven_price'),
        c_profit_if_exercised = (pl.col('strike_price') + dividends) * pl.col('multiplier') - pl.col('c_net_investment'),
        c_profit_if_unchanged = (underlying_ask + dividends) * pl.col('multiplier') - pl.col('c_net_investment'),
        m_net_investment = pl.col('m_equity_required') - (pl.col('bid') * pl.col('multiplier')) + commission,
        m_debit_balance = underlying_ask - pl.col('m_equity_required'),
    ).with_columns(
        c_downside_protection = pl.col('c_pts_downside_protection') / underlying_ask,
        c_return_if_exercised = pl.col('c_profit_if_exercised') / pl.col('c_net_investment'),
        c_return_if_unchanged = pl.col('c_profit_if_unchanged') / pl.col('c_net_investment'),
        m_interest_changes = pl.col('m_debit_balance') * m_interest_rate * pl.col('days_to_expiration') / 360,
        m_profit_if_unchanged = pl.col('c_profit_if_unchanged') - pl.col('m_net_investment'),
    ).with_columns(
        c_annualized_return_if_unchanged = 365 * pl.col('c_return_if_unchanged') / pl.col('days_to_expiration'),
        m_profit_if_exercised = pl.col('c_profit_if_exercised') - pl.col('m_interest_changes'),
        m_return_if_unchanged = pl.col('m_profit_if_unchanged') / pl.col('m_net_investment'),
        m_breakeven_price = \
                (pl.col('m_net_investment') + pl.col('m_debit_balance') - (dividends * pl.col('multiplier')) + pl.col('m_interest_changes')) \
                / pl.col('multiplier'),
    ).with_columns(
        m_return_if_exercised = pl.col('m_profit_if_exercised') / pl.col('m_net_investment'),
        m_pts_downside_protection = underlying_ask - pl.col('m_breakeven_price'),
        m_annualized_return_if_unchanged = 365 * pl.col('m_return_if_unchanged') / pl.col('days_to_expiration'),
    ).with_columns(
        m_downside_protection = pl.col('m_pts_downside_protection') / underlying_ask,
    )

    return df

def main():
    df = add_columns()
    print(df)
    df.write_csv('./data/add_columns.csv')

if __name__ == "__main__":
    main()


from __future__ import annotations

from data_enums import *

from dataclasses import dataclass, fields, MISSING
from datetime import datetime
from functools import wraps
import re


def to_snake_case(name: str) -> str:
    """
    Requires: must be camelCase ... if leading w/ digit, first char must be uppercase.

    1. aBCDe01 -> a_BCDe01
    2.         -> a_BCDe_01
    3.         -> a_BC_De_01
    4.         -> a_bc_de_01 
    """
    name = re.sub(r'(?<=[a-z0-9])([A-Z])', r'_\1', name)
    name = re.sub(r'([0-9]+)', r'_\1', name)
    name = re.sub(r'([A-Z]{2,})([A-Z][a-z])', r'\1_\2', name)
    name = name.lower()

    if name and name[0].isdigit():
        name = '_' + name
    
    return name

def _to_dict(obj) -> dict:
    """
    """
    if obj is None:
        return {}

    data = {}
    for fld in fields(obj):
        value = getattr(obj, fld.name, None)
        if value is not None and value is not MISSING:
            data[fld.name] = value
    return data

def base_init(cls):
    """
    decorator that overwrites the class's __init__ to support camel to snake case conversions
    """
    original = getattr(cls, '__init__', None)

    @wraps(original)  # type: ignore
    def init(self, **kwargs):
        for key, value in kwargs.items():
            snake_key = to_snake_case(key)
            try:
                setattr(self, snake_key, value)
            except AttributeError:
                pass
    
    cls.__init__ = init
    return cls

class FundamentalInst:
    symbol: str
    high_52: float
    low_52: float
    dividend_amount: float
    dividend_yield: float
    dividend_date: str
    pe_ratio: float
    peg_ratio: float
    pb_ratio: float
    pr_ratio: float
    pcf_ratio: float
    gross_margin_ttm: float
    gross_margin_mrq: float
    net_profit_margin_ttm: float
    net_profit_margin_mrq: float
    operating_margin_ttm: float
    operating_margin_mrq: float
    return_on_equity: float
    return_on_assets: float
    return_on_investment: float
    quick_ratio: float
    current_ratio: float
    interest_coverage: float
    total_debt_to_capital: float
    lt_debt_to_equity: float
    total_debt_to_equity: float
    eps_ttm: float
    eps_change_percent_ttm: float
    eps_change_year: float
    eps_change: float
    rev_change_year: float
    rev_change_ttm: float
    rev_change_in: float
    shares_outstanding: float
    market_cap_float: float
    market_cap: float
    book_value_per_share: float
    short_int_to_float: float
    short_int_day_to_cover: float
    div_growth_rate3_year: float
    dividend_pay_amount: float
    dividend_pay_date: str
    beta: float
    vol_1_day_avg: float
    vol_10_day_avg: float
    vol_3_month_avg: float
    avg_10_days_volume: int
    avg_1_day_volume: int
    avg_3_month_volume: int
    declaration_date: str
    dividend_freq: int
    eps: float
    corpaction_date: str
    dtn_volume: int
    next_dividend_pay_date: str
    next_dividend_date: str
    fund_leverage_factor: float
    fund_strategy: str

class Instrument:
    cusip: str
    symbol: str
    description: str
    exchange: str
    asset_type: AssetType
    type_: AssetType 
    
class Bond(Instrument):
    bond_factor: str
    bond_multiplier: str
    bond_price: int

class InstrumentResponse(Instrument):
    bond_multiplier: str
    bond_price: int
    fundamental: FundamentalInst
    instrument_info: Instrument
    bond_instrument_info: Bond

class Hours:
    date: str
    market_type: AssetType
    exchange: str
    category: str
    product: str
    product_name: str
    is_open: bool
    session_hours: dict[datetime, Interval]

class Interval:
    start: str
    end: str

class Screener:
    """ Security info of most moved in an index """
    change: float
    description: str
    direction: str  # { up, down }
    last: float
    symbol: str
    total_volume: int

class Candle:
    close: float
    datetime: int
    datetime_iso_8601: str  # yyyy-MM-dd
    high: float
    low: float
    open_: float
    volume: int

class CandleList:
    candles: list[Candle]
    empty: bool
    previous_close: float
    previous_clase_date: int
    previous_clase_date_iso_8601: str  # yyyy-MM-dd
    symbol: str
    type_: AssetType 

class Fundamental:
    """ Fundamentals of a security """
    avg_10_days_volume: float
    avg_1_year_volume: float
    declaration_date: str  # yyyy-MM-ddTHH:mm:ssZ
    div_amount: float
    div_ex_date: str  # yyyy-MM-ddTHH:mm:ssZ
    div_freq: DivFreq
    div_pay_amount: float
    div_yield: float
    epis: float
    fund_leverage_factor: float
    fund_strategy: FundStrategy
    next_div_ex_date: str  # yyyy-MM-ddTHH:mm:ssZ
    next_div_pay_date: str  # yyyy-MM-ddTHH:mm:ssZ
    pe_ratio: float

# ----- Response -----
# Response schemas

class Response:
    asset_main_type: AssetMainType
    ssid: int
    symbol: str
    realtime: bool

class EquityResponse(Response):
    """ Quote info of Equity security """
    asset_sub_type: EquityAssetSubType
    quote_type: QuoteType
    extended: ExtendedMarket
    fundamental: Fundamental
    quote: QuoteEquity
    reference: ReferenceEquity
    regular: RegularMarket

class ForexResponse(Response):
    quote: QuoteForex
    reference: ReferenceForex

class FutureOptionResponse(Response):
    quote: QuoteFutureOption
    reference: ReferenceFutureOption

class FutureResponse(Response):
    quote: QuoteFuture
    reference: ReferenceFuture

class IndexResponse(Response):
    quote: QuoteIndex
    reference: ReferenceIndex

class MutualFundResponse(Response):
    asset_sub_type: MutualFundAssetSubType
    fundamental: Fundamental
    quote: QuoteMutualFund
    reference: ReferenceMutualFund

class OptionResponse(Response):
    quote: QuoteOption
    reference: ReferenceOption

# ----- Quote -----
# Quote schemas

class Quote:
    _52_week_high: float
    _52_week_low: float
    close_price: float
    high_price: float
    last_price: float
    low_price: float
    net_change: float
    open_price: float
    security_status: str
    total_volume: int
    trade_time: int

class AskBid:
    ask_price: float
    ask_size: int
    bid_price: float
    bid_size: int

class ExtendedMarket(AskBid):
    last_price: float
    last_size: int
    mark: float
    quote_time: int
    total_volume: int
    trade_time: int

class QuoteEquity(Quote, AskBid):
    ask_mic_id: str
    ask_time: int
    bid_mic_id: str
    last_mic_id: str
    mark: float
    mark_change: float
    mark_percent_change: float
    net_percent_change: float
    quote_time: int
    volatility: float

class QuoteForex(Quote, AskBid):
    mark: float
    net_percent_change: float
    quote_time: int
    tick: float  # tick price
    tick_amount: float

class QuoteFuture(Quote, AskBid):
    ask_mic_id: str
    ask_time: int
    bid_mic_id: str
    bid_time: int
    future_percent_change: float
    last_mic_id: str
    last_size: int
    mark: float
    open_interest: int
    quote_time: int
    quoted_in_session: bool
    settle_time: int
    tick: float
    tick_amount: float

class QuoteFutureOption(Quote, AskBid):
    ask_mic_id: str
    bid_mic_id: str
    last_mic_id: str
    last_size: int
    mark: float
    mark_change: float
    open_interest: int
    net_percent_change: float
    open_interest: int
    quote_time: int
    settlement_price: float
    tick: float
    tick_amount: float

class QuoteIndex:
    _52_week_high: float
    _52_week_low: float
    close_price: float
    high_price: float
    last_price: float
    low_price: float
    net_change: float
    net_percent_change: float
    open_price: float
    security_status: str
    total_volume: int
    trade_time: int

class QuoteMutualFund:
    _52_week_high: float
    _52_week_low: float
    close_price: float
    n_av: float  # net asset value
    net_change: float
    net_percent_change: float
    security_status: str
    total_volume: int
    trade_time: int

class QuoteOption:
    ...

class QuoteRequest:
    cusips: list[str]
    fields: list[str]
    ssids: list[int]
    symbols: list[str]
    realtime: bool
    indicative: bool

class QuoteError:
    """ Partial or Custom errors per request """
    invalid_cusips: list[str]
    invalid_ssids: list[int]
    invalid_symbols: list[str]

class QuoteResponse:
    data: dict[str, QuoteResponseObject]  # key is symbol

class QuoteResponseObject:
    data: Quote | QuoteError

# ----- Reference -----
# All Reference Schemas

class ReferenceIndex:
    description: str
    exchange: str
    exchange_name: str = ''  # FutureOption is None, ReferenceMutualFund is MUTUAL_FUND

class ReferenceEquity(ReferenceIndex):
    cusip: str
    fsi_desc: str
    htb_quantity: int  # hard to borrow quatity
    htb_rate: float
    is_hard_to_borrow: bool
    is_shortable: bool
    otc_market_tier: str

class ReferenceForex(ReferenceIndex):
    is_tradable: bool
    market_maker: str
    product: str
    trading_hours: str

class ReferenceFuture(ReferenceIndex):
    future_active_symbol: str
    future_expiration_date: int
    future_is_active: bool
    future_multiplier: float
    future_price_format: str
    future_settlement_price: float
    future_trading_hours: str
    product: str

class ReferenceFutureOption(ReferenceIndex):
    contract_type: ContractType
    multiplier: float
    expiration_date: int
    expiration_style: str
    strike_price: float
    underlying: str 

class ReferenceMutualFund(ReferenceIndex):
    cusip: str

class ReferenceOption:
    ...

class RegularMarket:
    regular_market_last_price: float 
    regular_market_last_size: int
    regular_market_net_change: float 
    regular_market_percent_change: float 
    regular_market_trade_time: int 

class ErrorResponse:
    errors: list[Error]

class Error:
    id_: str
    status: HTTPStatus  # 400, 01, 04, 500
    title: str  # short error description
    detail: str  # detailed error description
    source: ErrorSource

class ErrorSource:
    pointer: list[str]  # list of attributes which lead to this error message
    parameter: str  # parameter name which leads to this error message
    header: str  # header name which lead to this error message

class OptionChain:
    ...

class OptionContractMap:
    ...

class Underlying:
    ask: float
    ask_size: int
    bid: float
    bid_size: int
    change: float
    close: float
    delayed: bool
    description: str
    exchange_name: Exchange
    fifty_two_week_high: float
    fifty_two_week_low: float
    high_price: float
    last: float
    low_price: float
    mark: float
    mark_change: float
    mark_percent_change: float
    open_price: float
    percent_change: float
    quote_time: int
    symbol: str
    total_volume: int
    trade_time: int

class OptionDeliverables:
    symbol: str
    asset_type: AssetType
    deliverable_units: str
    currency_type: Currency

class OptionContract:
    put_call: ContractType  
    symbol: str
    description: str
    exchange_name: str
    bid_price: float
    ask_price: float
    last_price: float
    mark_price: float
    bid_size: int
    ask_size: int
    last_size: int
    high_price: float
    low_price: float
    open_price: float
    close_price: float
    total_volume: int
    trade_date: int
    quote_time_in_long: int 
    trade_time_in_long: int
    net_change: float
    volatility: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    time_value: float
    open_interest: float
    is_in_the_money: bool
    theoretical_option_value: float
    theoretical_volatility: float
    is_mini: bool
    is_non_standard: bool
    option_deliberables_list: list[OptionDeliverables]
    strike_price: float
    expiration_date: str
    days_to_expiration: int
    expiration_type: ExpirationType
    last_trading_day: int
    multiplier: float
    settlement_type: SettlementType
    deliverable_note: str
    is_index_option: bool
    percent_change: float
    mark_change: float
    mark_percent_change: float
    is_penny_pilot: bool
    intrinsic_value: float
    option_root: str

class ExpirationChain:
    status: str
    expiration_list: list[Expiration]

class Expiration:
    days_to_expiration: int
    expiration: str
    expiration_type: ExpirationType
    standard: bool
    settlement_type: SettlementType
    option_roots: str

"""
    def to_dictl(self) -> list[dict]:
        result = []
        for d in [self.puts, self.calls]:
            for _, contracts in d.items():
                for contract in contracts:
                    result.append(_to_dict(contract))

        return result

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'asset_main_type': self.asset_main_type,
            'quote_type': self.quote_type,
            'realtime': self.realtime,
            'ssid': self.ssid,
            **{ f'extended_{k}': v    for k, v in _to_dict(self.extended).items() },
            **{ f'fundamental_{k}': v for k, v in _to_dict(self.fundamental).items() },
            **{ f'quote_{k}': v       for k, v in _to_dict(self.quote).items() },
            **{ f'reference_{k}': v   for k, v in _to_dict(self.reference).items() },
            **{ f'{k}': v             for k, v in _to_dict(self.regular).items() }
        }
"""

from __future__ import annotations

from shared_enums import *
from data_enums import *

from functools import wraps
import re

from pydantic import BaseModel


class Candle(BaseModel):
    close: float
    datetime: int
    datetime_iso_8601: str  # yyyy-MM-dd
    high: float
    low: float
    open_: float
    volume: int

class CandleList(BaseModel):
    candles: list[Candle]
    data_type: AssetType 
    empty: bool
    previous_clase_date: int
    previous_clase_date_iso_8601: str  # yyyy-MM-dd
    previous_close: float
    symbol: str

class Hours(BaseModel):
    category: str
    date: str
    exchange: str
    is_open: bool
    market_type: AssetType
    product: str
    product_name: str
    session_hours: dict[datetime, Interval]

class Interval(BaseModel):
    end: str
    start: str

class Screener(BaseModel):
    """ Security info of most moved in an index """
    change: float
    description: str
    direction: str  # { up, down }
    last: float
    symbol: str
    total_volume: int

class Instrument(BaseModel):
    asset_type: AssetType
    cusip: str
    data_type: AssetType 
    description: str
    exchange: str
    symbol: str

class Bond(Instrument, BaseModel):
    bond_factor: str
    bond_multiplier: str
    bond_price: int

class Fundamental(BaseModel):
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

class FundamentalInst(BaseModel):
    avg_10_days_volume: int
    avg_1_day_volume: int
    avg_3_month_volume: int
    beta: float
    book_value_per_share: float
    corpaction_date: str
    current_ratio: float
    declaration_date: str
    div_growth_rate3_year: float
    dividend_amount: float
    dividend_date: str
    dividend_freq: int
    dividend_pay_amount: float
    dividend_pay_date: str
    dividend_yield: float
    dtn_volume: int
    eps: float
    eps_change: float
    eps_change_percent_ttm: float
    eps_change_year: float
    eps_ttm: float
    fund_leverage_factor: float
    fund_strategy: str
    gross_margin_mrq: float
    gross_margin_ttm: float
    high_52: float
    interest_coverage: float
    low_52: float
    lt_debt_to_equity: float
    market_cap: float
    market_cap_float: float
    net_profit_margin_mrq: float
    net_profit_margin_ttm: float
    next_dividend_date: str
    next_dividend_pay_date: str
    operating_margin_mrq: float
    operating_margin_ttm: float
    pb_ratio: float
    pcf_ratio: float
    pe_ratio: float
    peg_ratio: float
    pr_ratio: float
    quick_ratio: float
    return_on_assets: float
    return_on_equity: float
    return_on_investment: float
    rev_change_in: float
    rev_change_ttm: float
    rev_change_year: float
    shares_outstanding: float
    short_int_day_to_cover: float
    short_int_to_float: float
    symbol: str
    total_debt_to_capital: float
    total_debt_to_equity: float
    vol_10_day_avg: float
    vol_1_day_avg: float
    vol_3_month_avg: float

# ----- Response -----
# Response schemas

class Response(BaseModel):
    asset_main_type: AssetMainType
    realtime: bool
    ssid: int
    symbol: str

class EquityResponse(Response, BaseModel):
    """ Quote info of Equity security """
    asset_sub_type: EquityAssetSubType
    extended: ExtendedMarket
    fundamental: Fundamental
    quote: QuoteEquity
    quote_type: QuoteType
    reference: ReferenceEquity
    regular: RegularMarket

class ForexResponse(Response, BaseModel):
    quote: QuoteForex
    reference: ReferenceForex

class FutureOptionResponse(Response, BaseModel):
    quote: QuoteFutureOption
    reference: ReferenceFutureOption

class FutureResponse(Response, BaseModel):
    quote: QuoteFuture
    reference: ReferenceFuture

class InstrumentResponse(Instrument, BaseModel):
    bond_instrument_info: Bond
    bond_multiplier: str
    bond_price: int
    fundamental: FundamentalInst
    instrument_info: Instrument

class IndexResponse(Response, BaseModel):
    quote: QuoteIndex
    reference: ReferenceIndex

class MutualFundResponse(Response, BaseModel):
    asset_sub_type: MutualFundAssetSubType
    fundamental: Fundamental
    quote: QuoteMutualFund
    reference: ReferenceMutualFund

class OptionResponse(Response, BaseModel):
    quote: QuoteOption
    reference: ReferenceOption

# ----- Quote -----
# Quote schemas

class Quote(BaseModel):
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

class AskBid(BaseModel):
    ask_price: float
    ask_size: int
    bid_price: float
    bid_size: int

class ExtendedMarket(AskBid, BaseModel):
    last_price: float
    last_size: int
    mark: float
    quote_time: int
    total_volume: int
    trade_time: int

class QuoteEquity(Quote, AskBid, BaseModel):
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

class QuoteForex(Quote, AskBid, BaseModel):
    mark: float
    net_percent_change: float
    quote_time: int
    tick: float  # tick price
    tick_amount: float

class QuoteFuture(Quote, AskBid, BaseModel):
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

class QuoteFutureOption(Quote, AskBid, BaseModel):
    ask_mic_id: str
    bid_mic_id: str
    last_mic_id: str
    last_size: int
    mark: float
    mark_change: float
    net_percent_change: float
    open_interest: int
    open_interest: int
    quote_time: int
    settlement_price: float
    tick: float
    tick_amount: float

class QuoteIndex(BaseModel):
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

class QuoteMutualFund(BaseModel):
    _52_week_high: float
    _52_week_low: float
    close_price: float
    n_av: float  # net asset value
    net_change: float
    net_percent_change: float
    security_status: str
    total_volume: int
    trade_time: int

class QuoteOption(Quote, BaseModel):
    delta: float
    gamma: float
    implied_yield: float
    ind_ask_price: float
    ind_bid_price: float
    ind_quote_time: int  # datetime
    last_size: int
    mark: float
    mark_change: float
    mark_percent_change: float
    money_intrinsic_value: float
    net_percent_change: float
    open_interest: float
    quote_time: int  # datetime
    rho: float
    theoretical_option_value: float
    theta: float
    time_value: float
    underlying_price: float
    vega: float
    volatility: float

class QuoteRequest(BaseModel):
    cusips: list[str]
    fields: list[str]
    indicative: bool
    realtime: bool
    ssids: list[int]
    symbols: list[str]

class QuoteError(BaseModel):
    """ Partial or Custom errors per request """
    invalid_cusips: list[str]
    invalid_ssids: list[int]
    invalid_symbols: list[str]

class QuoteResponse(BaseModel):
    data: dict[str, QuoteResponseObject]  # key is symbol

class QuoteResponseObject(BaseModel):
    data: Quote | QuoteError

# ----- Reference -----
# All Reference Schemas

class ReferenceIndex(BaseModel):
    description: str
    exchange: str
    exchange_name: str = ''  # FutureOption is None, ReferenceMutualFund is MUTUAL_FUND

class ReferenceEquity(ReferenceIndex, BaseModel):
    cusip: str
    fsi_desc: str
    htb_quantity: int  # hard to borrow quatity
    htb_rate: float
    is_hard_to_borrow: bool
    is_shortable: bool
    otc_market_tier: str

class ReferenceForex(ReferenceIndex, BaseModel):
    is_tradable: bool
    market_maker: str
    product: str
    trading_hours: str

class ReferenceFuture(ReferenceIndex, BaseModel):
    future_active_symbol: str
    future_expiration_date: int
    future_is_active: bool
    future_multiplier: float
    future_price_format: str
    future_settlement_price: float
    future_trading_hours: str
    product: str

class ReferenceFutureOption(ReferenceIndex, BaseModel):
    contract_type: ContractType
    expiration_date: int
    expiration_style: str
    multiplier: float
    strike_price: float
    underlying: str 

class ReferenceMutualFund(ReferenceIndex, BaseModel):
    cusip: str

class ReferenceOption(BaseModel):
    """ Reference data of Option security """
    contract_type: ContractType
    cusip: str
    days_to_expiration: float
    deliverables: str
    description: str
    exchange: str
    exchange_name: str
    exercise_type: ExerciseType
    expiration_day: int  # [1, 31]
    expiration_month: int  # [1, 12]
    expiration_type: ExpirationType
    expiration_year: int
    is_penny_pilot: bool  # Is this contract part of the Penny Pilot program
    last_trading_day: int
    multiplier: float
    settlement_type: SettlementType
    strike_price: float
    underlying: str  # company, index, or fund name

class RegularMarket(BaseModel):
    regular_market_last_price: float 
    regular_market_last_size: int
    regular_market_net_change: float 
    regular_market_percent_change: float 
    regular_market_trade_time: int 

# ----- Error -----

class ErrorResponse(BaseModel):
    errors: list[Error]

class Error(BaseModel):
    detail: str  # detailed error description
    id_: str
    source: ErrorSource
    status: int  # 400, 01, 04, 500
    title: str  # short error description

class ErrorSource(BaseModel):
    header: str  # header name which lead to this error message
    parameter: str  # parameter name which leads to this error message
    pointer: list[str]  # list of attributes which lead to this error message

# ----- Options -----

class OptionChain(BaseModel):
    call_exp_date_map: dict[str, OptionContractMap]
    days_to_expiration: float
    interest_rate: float
    interval: float
    is_delayed: bool
    is_index: bool
    put_exp_date_map: dict[str, OptionContractMap]
    status: str
    strategy: Strategy
    symbol: str
    underlying: Underlying
    underlying_price: float
    volatility: float

class OptionContractMap(BaseModel):
    data: dict[str, OptionContract]

class Underlying(BaseModel):
    ask: float
    ask_size: int
    bid: float
    bid_size: int
    change: float
    close: float
    delayed: bool
    description: str
    exchange_name: Exchanges
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

class OptionDeliverables(BaseModel):
    asset_type: AssetType
    currency_type: str
    deliverable_units: str
    symbol: str

class OptionContract(BaseModel):
    ask_price: float
    ask_size: int
    bid_price: float
    bid_size: int
    close_price: float
    days_to_expiration: int
    deliverable_note: str
    delta: float
    description: str
    exchange_name: str
    expiration_date: str
    expiration_type: ExpirationType
    gamma: float
    high_price: float
    intrinsic_value: float
    is_in_the_money: bool
    is_index_option: bool
    is_mini: bool
    is_non_standard: bool
    is_penny_pilot: bool
    last_price: float
    last_size: int
    last_trading_day: int
    low_price: float
    mark_change: float
    mark_percent_change: float
    mark_price: float
    multiplier: float
    net_change: float
    open_interest: float
    open_price: float
    option_deliberables_list: list[OptionDeliverables]
    option_root: str
    percent_change: float
    put_call: ContractType  
    quote_time_in_long: int 
    rho: float
    settlement_type: SettlementType
    strike_price: float
    symbol: str
    theoretical_option_value: float
    theoretical_volatility: float
    theta: float
    time_value: float
    total_volume: int
    trade_date: int
    trade_time_in_long: int
    vega: float
    volatility: float

class ExpirationChain(BaseModel):
    expiration_list: list[Expiration]
    status: str

class Expiration(BaseModel):
    days_to_expiration: int
    expiration: str
    expiration_type: ExpirationType
    option_roots: str
    settlement_type: SettlementType
    standard: bool

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

def to_snake_case(name: str) -> str:
    """
    Requires: must be camelCase ... if leading w/ digit, first char must be uppercase.

    1. aBCDe01 -> a_BCDe01
    2.         -> a_BCDe_01
    3.         -> a_BC_De_01
    4.         -> a_bc_de_01 
    """
    name = re.sub(r'(?<=[a-z0-9], [A-Z])', r'_\1', name)
    name = re.sub(r'([0-9]+)', r'_\1', name)
    name = re.sub(r'([A-Z]{2,}, [A-Z][a-z])', r'\1_\2', name)
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


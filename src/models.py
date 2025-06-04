from dataclasses import asdict, dataclass, field
from datetime import datetime
from functools import wraps
import re

import numpy as np

"""
ExpirationDate
Equity
    Reference
    Quote
    Regular
    Fundamental
Contract
"""


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

#    def __init__(self, **kwargs):
#        for key, v in kwargs.items():
#            if (k := to_snake_case(key)) in self.__slots__:  # does NOT include inherited slots
#                self.__setattr__(k, v)

@base_init
@dataclass
class ExpirationDate:
    expiration_date: datetime
    days_to_expiration: int
    expiration_type: str  # W
    standard: bool

@base_init
@dataclass
class Extended:
    ask_price: float
    ask_size: int
    bid_price: float
    last_price: float
    last_size: int
    mark: float
    quote_time: int
    total_volume: int
    trade_time: int

@base_init
@dataclass
class Reference:
    cusip: int
    description: str
    exchange: str
    exchange_name: str
    is_hard_to_borrow: bool
    is_shortable: bool
    htb_quantity: int
    htb_rate: float

@base_init
@dataclass()
class Quote:
    _52_week_high: float
    _52_week_low: float
    ask_mic_id: str
    ask_price: float
    ask_size: float
    ask_time: float
    bid_mic_id: str
    bid_price: float
    bid_size: float
    bid_time: float
    close_price: float
    high_price: float
    last_mic_id: str
    last_price: float
    last_size: float
    low_price: float
    mark: float
    mark_change: float
    mark_percent_change: float
    net_change: float
    net_percent_change: float
    open_price: float
    post_market_change: float
    post_market_percent_change: float
    quote_time: float
    security_status: str
    total_volume: float
    trade_time: float
    volatility: float = np.nan

@base_init
@dataclass
class Regular:
    regular_market_last_price: float
    regular_market_last_size: float
    regular_market_net_change: float
    regular_market_percent_change: float
    regular_market_trade_time: float

@base_init
@dataclass
class Fundamental:
    avg_10_days_volume: float
    avg_1_year_volume: float
    declaration_date: datetime
    div_amount: float
    div_ex_date: datetime
    div_freq: float
    div_pay_amount: float
    div_pay_date: datetime
    div_yield: float
    eps: float
    fund_leverage_factor: float
    last_earnings_date: datetime
    next_div_ex_date: datetime
    next_div_pay_date: datetime  # '2025-05-01T00:00:00Z'  all in this format
    pe_ratio: float

@base_init
@dataclass(slots=True)
class Contract:
    put_call: str  # { CALL, PUT }
    symbol: str
    description: str
    exchange_name: str
    bid: float
    ask: float
    last: float
    mark: float
    bid_size: float
    ask_size: float
    bid_ask_size: str  # "intXint"
    last_size: float
    high_price: float
    low_price: float
    open_price: float
    close_price: float
    total_volume: float
    trade_time_in_long: datetime
    quote_time_in_long: datetime
    net_change: float
    volatility: float
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float
    open_interest: float
    time_value: float
    theoretical_option_value: float
    theoretical_volatility: float
    strike_price: float
    expiration_date: datetime
    days_to_expiration: int
    expiration_type: str  # W: weeklies
    last_trading_day: datetime 
    multiplier: int
    settlement_type: str  # P: physical, C: cash
    deliverable_note: str
    percent_change: float
    mark_change: float
    mark_percent_change: float
    intrinsic_value: float
    extrinsic_value: float
    option_root: str
    exercise_type: str
    high_52_week: float
    low_52_week: float
    penny_pilot: bool
    non_standard: bool
    in_the_money: bool
    mini: bool

@base_init
@dataclass
class Options:
    puts: dict[datetime, list[Contract]]
    calls: dict[datetime, list[Contract]]

@base_init
@dataclass
class Equity:
    symbol: str
    asset_main_type: str
    quote_type: str
    realtime: bool
    ssid: int

    extended: Extended
    fundamental: Fundamental
    quote: Quote
    reference: Reference
    regular: Regular

    # options: Options

    def to_dict(self):
        return {
            'symbol': self.symbol,
            'asset_main_type': self.asset_main_type,
            'quote_type': self.quote_type,
            'realtime': self.realtime,
            'ssid': self.ssid,
            **{ f'extended_{k}': v    for k, v in asdict(self.extended).items()    },
            **{ f'fundamental_{k}': v for k, v in asdict(self.fundamental).items() },
            **{ f'quote_{k}': v       for k, v in asdict(self.quote).items()       },
            **{ f'reference_{k}': v   for k, v in asdict(self.reference).items()   },
            **{ f'{k}': v             for k, v in asdict(self.regular).items()     }
        }


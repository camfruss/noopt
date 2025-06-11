from enum import auto, Enum


class AdvancedOrderType(Enum):
    ...

class OrderBalance(Enum):
    ...

class OrderStrategyType(Enum):
    ...

class Session(Enum):
    ...

class APIOrderStatus(Enum):
    ...

class Duration(Enum):
    ...

class SettlementInstruction(Enum):
    ...

class ComplexOrderStrategyType(Enum):
    ...

class AmountIndicator(Enum):
    ...

class OrderLeg(Enum):
    ...

class OrderType(Enum):
    MARKET = auto()
    LIMIT = auto()
    STOP = auto()
    STOP_LIMIT = auto()
    TRAILING_STOP = auto()
    CABINET = auto()
    NON_MARKETABLE = auto()
    MARKET_ON_CLOSE = auto()
    EXERCISE = auto()
    TRAILING_STOP_LIMIT = auto()
    NET_DEBIT = auto()
    NET_CREDIT = auto()
    NET_ZERO = auto()
    LIMIT_ON_CLOSE = auto()
    UNKNOWN = auto()


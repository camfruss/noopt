from enum import auto, Enum


class FeeType(Enum):
    COMMISSION = auto()
    SEC_FEE = auto()
    STR_FEE = auto()
    R_FEE = auto()
    CDSC_FEE = auto()
    OPT_REG_FEE = auto()
    ADDITIONAL_FEE = auto()
    MISCELLANEOUS_FEE = auto()
    FUTURES_EXCHANGE_FEE = auto()
    LOW_PROCEEDS_COMMISSION = auto()
    BASE_CHARGE = auto()
    GENERAL_CHARGE = auto()
    GST_FEE = auto()
    TAF_FEE = auto()
    INDEX_OPTION_FEE = auto()
    UNKNOWN = auto()

class PositionEffect(Enum):
    OPENING = auto()
    CLOSING = auto()
    AUTOMATIC = auto()
    UNKNOWN = auto()

class AdvancedOrderType(Enum):
    ...

class OrderBalance(Enum):
    ...

class OrderStrategyType(Enum):
    ...

class APIOrderStatus(Enum):
    AWAITING_PARENT_ORDER = auto()
    AWAITING_CONDITION = auto()
    AWAITING_STOP_CONDITION = auto()
    AWAITING_MANUAL_REVIEW = auto()
    ACCEPTED = auto()
    AWAITING_UR_OUT = auto()
    PENDING_ACTIVATION = auto()
    QUEUED = auto()
    WORKING = auto()
    REJECTED = auto()
    PENDING_CANCEL = auto()
    CANCELED = auto()
    PENDING_REPLACE = auto()
    REPLACED = auto()
    FILLED = auto()
    EXPIRED = auto()
    NEW = auto()
    AWAITING_RELEASE_TIME = auto()
    PENDING_ACKNOWLEDGEMENT = auto()
    PENDING_RECALL = auto()
    UNKNOWN = auto()
  
class TransactionType(Enum):
    TRADE = auto()
    RECEIVE_AND_DELIVER = auto()
    DIVIDEND_OR_INTEREST = auto()
    ACH_RECEIPT = auto()
    ACH_DISBURSEMENT = auto()
    CASH_RECEIPT = auto()
    CASH_DISBURSEMENT = auto()
    ELECTRONIC_FUND = auto()
    WIRE_OUT = auto()
    WIRE_IN = auto()
    JOURNAL = auto()
    MEMORANDUM = auto()
    MARGIN_CALL = auto()
    MONEY_MARKET = auto()
    SMA_ADJUSTMENT = auto()

class ComplexOrderStrategyType(Enum):
    NONE = auto()
    COVERED = auto()
    VERTICAL = auto()
    BACK_RATIO = auto()
    CALENDAR = auto()
    DIAGONAL = auto()
    STRADDLE = auto()
    STRANGLE = auto()
    COLLAR_SYNTHETIC = auto()
    BUTTERFLY = auto()
    CONDOR = auto()
    IRON_CONDOR = auto()
    VERTICAL_ROLL = auto()
    COLLAR_WITH_STOCK = auto()
    DOUBLE_DIAGONAL = auto()
    UNBALANCED_BUTTERFLY = auto()
    UNBALANCED_CONDOR = auto()
    UNBALANCED_IRON_CONDOR = auto()
    UNBALANCED_VERTICAL_ROLL = auto()
    MUTUAL_FUND_SWAP = auto()
    CUSTOM = auto()

class OrderLeg(Enum):
    ...

class Session(Enum):
    NORMAL = auto()
    AM = auto()
    PM = auto()
    SEAMLESS = auto()

class Duration(Enum):
    DAY = auto()
    GOOD_TILL_CANCEL = auto()
    FILL_OR_KILL = auto()
    IMMEDIATE_OR_CANCEL = auto()
    END_OF_WEEK = auto()
    END_OF_MONTH = auto()
    NEXT_END_OF_MONTH = auto()
    UNKNOWN = auto()

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

class OrderTypeRequest(Enum):
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

class RequestedDestination(Enum):
    INET = auto()
    ECN_ARCA = auto()
    CBOE = auto()
    AMEX = auto()
    PHLX = auto()
    ISE = auto()
    BOX = auto()
    NYSE = auto()
    NASDAQ = auto()
    BATS = auto()
    C2 = auto()
    AUTO = auto()

class StopPriceLinkBasis(Enum):
    MANUAL = auto()
    BASE = auto()
    TRIGGER = auto()
    LAST = auto()
    BID = auto()
    ASK = auto()
    ASK_BID = auto()
    MARK = auto()
    AVERAGE = auto()

class StopPriceLinkType(Enum):
    VALUE = auto()
    PERCENT = auto()
    TICK = auto()

class StopType(Enum):
    STANDARD = auto()
    BID = auto()
    ASK = auto()
    LAST = auto()
    MARK = auto()

class PriceLinkBasis(Enum):
    MANUAL = auto()
    BASE = auto()
    TRIGGER = auto()
    LAST = auto()
    BID = auto()
    ASK = auto()
    ASK_BID = auto()
    MARK = auto()
    AVERAGE = auto()
class PriceLinkType(Enum):
    VALUE = auto()
    PERCENT = auto()
    TICK = auto()

class TaxLotMethod(Enum):
     FIFO = auto()
     LIFO = auto()
     HIGH_COST = auto()
     LOW_COST = auto()
     AVERAGE_COST = auto()
     SPECIFIC_LOT = auto()
     LOSS_HARVESTER = auto()

class SpecialInstruction(Enum):
    ALL_OR_NONE = auto()
    DO_NOT_REDUCE = auto()
    ALL_OR_NONE_DO_NOT_REDUCE = auto()

class OrderStrtategyType(Enum):
    SINGLE = auto()
    CANCEL = auto()
    RECALL = auto()
    PAIR = auto()
    FLATTEN = auto()
    TWO_DAY_SWAP = auto()
    BLAST_ALL = auto()
    OCO = auto()
    TRIGGER = auto()

class Status(Enum):
    AWAITING_PARENT_ORDER = auto()
    AWAITING_CONDITION = auto()
    AWAITING_STOP_CONDITION = auto()
    AWAITING_MANUAL_REVIEW = auto()
    ACCEPTED = auto()
    AWAITING_UR_OUT = auto()
    PENDING_ACTIVATION = auto()
    QUEUED = auto()
    WORKING = auto()
    REJECTED = auto()
    PENDING_CANCEL = auto()
    CANCELED = auto()
    PENDING_REPLACE = auto()
    REPLACED = auto()
    FILLED = auto()
    EXPIRED = auto()
    NEW = auto()
    AWAITING_RELEASE_TIME = auto()
    PENDING_ACKNOWLEDGEMENT = auto()
    PENDING_RECALL = auto()
    UNKNOWN = auto()

class AmountIndicator(Enum):
    DOLLARS = auto()
    SHARES = auto()
    ALL_SHARES = auto()
    PERCENTAGE = auto()
    UNKNOWN = auto()

class SettlementInstruction(Enum):
    REGULAR = auto()
    CASH = auto()
    NEXT_DAY = auto()
    UNKNOWN = auto()


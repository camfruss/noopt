from enum import auto, Enum


class ActivityType(Enum):
    ACTIVITY_CORRECTION = auto()
    EXECUTION = auto()
    ORDER_ACTION = auto()
    TRANSFER = auto()
    UNKNOWN = auto()

class AdvancedOrderType(Enum):
    BLAST_ALL = auto()
    NONE = auto()
    OCO = auto()
    OT2OCO = auto()
    OT3OCO = auto()
    OTA = auto()
    OTO = auto()
    OTOCO = auto()
    PAIR = auto()

class AmountIndicator(Enum):
    ALL_SHARES = auto()
    DOLLARS = auto()
    PERCENTAGE = auto()
    SHARES = auto()
    UNKNOWN = auto()

class APIOrderStatus(Enum):
    ACCEPTED = auto()
    AWAITING_CONDITION = auto()
    AWAITING_MANUAL_REVIEW = auto()
    AWAITING_PARENT_ORDER = auto()
    AWAITING_RELEASE_TIME = auto()
    AWAITING_STOP_CONDITION = auto()
    AWAITING_UR_OUT = auto()
    CANCELED = auto()
    EXPIRED = auto()
    FILLED = auto()
    NEW = auto()
    PENDING_ACKNOWLEDGEMENT = auto()
    PENDING_ACTIVATION = auto()
    PENDING_CANCEL = auto()
    PENDING_RECALL = auto()
    PENDING_REPLACE = auto()
    QUEUED = auto()
    REJECTED = auto()
    REPLACED = auto()
    UNKNOWN = auto()
    WORKING = auto()

class APIRuleAction(Enum):
    ACCEPT = auto()
    ALERT = auto()
    REJECT = auto()
    REVIEW = auto()
    UNKNOWN = auto()

class AssetType(Enum):
    CASH_EQUIVALENT = auto()
    COLLECTIVE_INVESTMENT = auto()
    CURRENCY = auto()
    EQUITY = auto()
    FIXED_INCOME = auto()
    FOREX = auto()
    FUTURE = auto()
    INDEX = auto()
    MUTUAL_FUND = auto()
    OPTION = auto()
    PRODUCT = auto()

class CashType(Enum):
    MONEY_MARKET_FUND = auto()
    SAVINGS = auto()
    SWEEP_VEHICLE = auto()
    UNKNOWN = auto()

class CollectiveType(Enum):
    CLOSED_END_FUND = auto()
    EXCHANGE_TRADED_FUND = auto()
    INDEX = auto()
    UNITS = auto()
    UNIT_INVESTMENT_TRUST = auto()

class ComplexOrderStrategyType(Enum):
    BACK_RATIO = auto()
    BUTTERFLY = auto()
    CALENDAR = auto()
    COLLAR_SYNTHETIC = auto()
    COLLAR_WITH_STOCK = auto()
    CONDOR = auto()
    COVERED = auto()
    CUSTOM = auto()
    DIAGONAL = auto()
    DOUBLE_DIAGONAL = auto()
    IRON_CONDOR = auto()
    MUTUAL_FUND_SWAP = auto()
    NONE = auto()
    STRADDLE = auto()
    STRANGLE = auto()
    UNBALANCED_BUTTERFLY = auto()
    UNBALANCED_CONDOR = auto()
    UNBALANCED_IRON_CONDOR = auto()
    UNBALANCED_VERTICAL_ROLL = auto()
    VERTICAL = auto()
    VERTICAL_ROLL = auto()

class Duration(Enum):
    DAY = auto()
    END_OF_MONTH = auto()
    END_OF_WEEK = auto()
    FILL_OR_KILL = auto()
    GOOD_TILL_CANCEL = auto()
    IMMEDIATE_OR_CANCEL = auto()
    NEXT_END_OF_MONTH = auto()
    UNKNOWN = auto()

class EquityType(Enum):
    COMMON_STOCK = auto()
    COMPONENT_UNIT = auto()
    CONVERTIBLE_PREFERRED_STOCK = auto()
    CONVERTIBLE_STOCK = auto()
    DEPOSITORY_RECEIPT = auto()
    LIMITED_PARTNERSHIP = auto()
    PREFERRED_DEPOSITORY_RECEIPT = auto()
    PREFERRED_STOCK = auto()
    RESTRICTED_STOCK = auto()
    RIGHT = auto()
    UNKNOWN = auto()
    WARRANT = auto()
    WHEN_ISSUED = auto()

class FeeType(Enum):
    ADDITIONAL_FEE = auto()
    BASE_CHARGE = auto()
    CDSC_FEE = auto()
    COMMISSION = auto()
    FUTURES_EXCHANGE_FEE = auto()
    GENERAL_CHARGE = auto()
    GST_FEE = auto()
    INDEX_OPTION_FEE = auto()
    LOW_PROCEEDS_COMMISSION = auto()
    MISCELLANEOUS_FEE = auto()
    OPT_REG_FEE = auto()
    R_FEE = auto()
    SEC_FEE = auto()
    STR_FEE = auto()
    TAF_FEE = auto()
    UNKNOWN = auto()

class FixedIncomeType(Enum):
    AGENCY_BOND = auto()
    ASSET_BACKED_SECURITY = auto()
    BOND_UNIT = auto()
    CERTIFICATE_OF_DEPOSIT = auto()
    COLLATERALIZED_MORTGAGE_OBLIGATION = auto()
    CONVERTIBLE_BOND = auto()
    CORPORATE_BOND = auto()
    GNMA_BONDS = auto()
    GOVERNMENT_MORTGAGE = auto()
    MUNICIPAL_ASSESSMENT_DISTRICT = auto()
    MUNICIPAL_BOND = auto()
    OTHER_GOVERNMENT = auto()
    SHORT_TERM_PAPER = auto()
    UNKNOWN = auto()
    US_TREASURY_BILL = auto()
    US_TREASURY_BOND = auto()
    US_TREASURY_NOTE = auto()
    US_TREASURY_ZERO_COUPON = auto()
    WHEN_AS_AND_IF_ISSUED_BOND = auto()

class ForexType(Enum):
    NBBO = auto()
    STANDARD = auto()
    UNKNOWN = auto()

class FutureType(Enum):
    STANDARD = auto()
    UNKNOWN = auto()

class IndexType(Enum):
    BROAD_BASED = auto()
    NARROW_BASED = auto()
    UNKNOWN = auto()

class Instruction(Enum):
    BUY = auto()
    BUY_TO_CLOSE = auto()
    BUY_TO_COVER = auto()
    BUY_TO_OPEN = auto()
    EXCHANGE = auto()
    SELL = auto()
    SELL_SHORT = auto()
    SELL_SHORT_EXEMPT = auto()
    SELL_TO_CLOSE = auto()
    SELL_TO_OPEN = auto()

class LegType(Enum):
    CASH_EQUIVALENT = auto()
    COLLECTIVE_INVESTMENT = auto()
    CURRENCY = auto()
    EQUITY = auto()
    FIXED_INCOME = auto()
    INDEX = auto()
    MUTUAL_FUND = auto()
    OPTION = auto()

class MutualFundType(Enum):
    NOT_APPLICABLE = auto()
    NO_LOAD_NON_TAXABLE = auto()
    NO_LOAD_TAXABLE = auto()
    OPEN_END_NON_TAXABLE = auto()
    OPEN_END_TAXABLE = auto()
    UNKNOWN = auto()

class OptionType(Enum):
    BARRIER = auto()
    BINARY = auto()
    UNKNOWN = auto()
    VANILLA = auto()

class OrderStrategyType(Enum):
    BLAST_ALL = auto()
    CANCEL = auto()
    FLATTEN = auto()
    OCO = auto()
    PAIR = auto()
    RECALL = auto()
    SINGLE = auto()
    TRIGGER = auto()
    TWO_DAY_SWAP = auto()

class OrderType(Enum):
    CABINET = auto()
    EXERCISE = auto()
    LIMIT = auto()
    LIMIT_ON_CLOSE = auto()
    MARKET = auto()
    MARKET_ON_CLOSE = auto()
    NET_CREDIT = auto()
    NET_DEBIT = auto()
    NET_ZERO = auto()
    NON_MARKETABLE = auto()
    STOP = auto()
    STOP_LIMIT = auto()
    TRAILING_STOP = auto()
    TRAILING_STOP_LIMIT = auto()
    UNKNOWN = auto()

class OrderTypeRequest(Enum):
    CABINET = auto()
    EXERCISE = auto()
    LIMIT = auto()
    LIMIT_ON_CLOSE = auto()
    MARKET = auto()
    MARKET_ON_CLOSE = auto()
    NET_CREDIT = auto()
    NET_DEBIT = auto()
    NET_ZERO = auto()
    NON_MARKETABLE = auto()
    STOP = auto()
    STOP_LIMIT = auto()
    TRAILING_STOP = auto()
    TRAILING_STOP_LIMIT = auto()

class PositionEffect(Enum):
    AUTOMATIC = auto()
    CLOSING = auto()
    OPENING = auto()
    UNKNOWN = auto()

class PriceLinkBasis(Enum):
    ASK = auto()
    ASK_BID = auto()
    AVERAGE = auto()
    BASE = auto()
    BID = auto()
    LAST = auto()
    MANUAL = auto()
    MARK = auto()
    TRIGGER = auto()

class PriceLinkType(Enum):
    PERCENT = auto()
    TICK = auto()
    VALUE = auto()

class ProductType(Enum):
    TBD = auto()
    UNKNOWN = auto()

class RequestedDestination(Enum):
    AMEX = auto()
    AUTO = auto()
    BATS = auto()
    BOX = auto()
    C2 = auto()
    CBOE = auto()
    ECN_ARCA = auto()
    INET = auto()
    ISE = auto()
    NASDAQ = auto()
    NYSE = auto()
    PHLX = auto()

class Session(Enum):
    AM = auto()
    NORMAL = auto()
    PM = auto()
    SEAMLESS = auto()

class SettlementInstruction(Enum):
    CASH = auto()
    NEXT_DAY = auto()
    REGULAR = auto()
    UNKNOWN = auto()

class SpecialInstruction(Enum):
    ALL_OR_NONE = auto()
    ALL_OR_NONE_DO_NOT_REDUCE = auto()
    DO_NOT_REDUCE = auto()

class Status(Enum):
    ACCEPTED = auto()
    AWAITING_CONDITION = auto()
    AWAITING_MANUAL_REVIEW = auto()
    AWAITING_PARENT_ORDER = auto()
    AWAITING_RELEASE_TIME = auto()
    AWAITING_STOP_CONDITION = auto()
    AWAITING_UR_OUT = auto()
    CANCELED = auto()
    EXPIRED = auto()
    FILLED = auto()
    NEW = auto()
    PENDING_ACKNOWLEDGEMENT = auto()
    PENDING_ACTIVATION = auto()
    PENDING_CANCEL = auto()
    PENDING_RECALL = auto()
    PENDING_REPLACE = auto()
    QUEUED = auto()
    REJECTED = auto()
    REPLACED = auto()
    UNKNOWN = auto()
    WORKING = auto()

class StopPriceLinkBasis(Enum):
    ASK = auto()
    ASK_BID = auto()
    AVERAGE = auto()
    BASE = auto()
    BID = auto()
    LAST = auto()
    MANUAL = auto()
    MARK = auto()
    TRIGGER = auto()

class StopPriceLinkType(Enum):
    PERCENT = auto()
    TICK = auto()
    VALUE = auto()

class StopType(Enum):
    ASK = auto()
    BID = auto()
    LAST = auto()
    MARK = auto()
    STANDARD = auto()

class SubAccountType(Enum):
    CASH = auto()
    DIV = auto()
    INCOME = auto()
    MARGIN = auto()
    SHORT = auto()
    UNKNOWN = auto()

class TaxLotMethod(Enum):
    AVERAGE_COST = auto()
    FIFO = auto()
    HIGH_COST = auto()
    LIFO = auto()
    LOSS_HARVESTER = auto()
    LOW_COST = auto()
    SPECIFIC_LOT = auto()

class TransactionType(Enum):
    ACH_DISBURSEMENT = auto()
    ACH_RECEIPT = auto()
    CASH_DISBURSEMENT = auto()
    CASH_RECEIPT = auto()
    DIVIDEND_OR_INTEREST = auto()
    ELECTRONIC_FUND = auto()
    JOURNAL = auto()
    MARGIN_CALL = auto()
    MEMORANDUM = auto()
    MONEY_MARKET = auto()
    RECEIVE_AND_DELIVER = auto()
    SMA_ADJUSTMENT = auto()
    TRADE = auto()
    WIRE_IN = auto()
    WIRE_OUT = auto()

class UserType(Enum):
    ADVISOR_USER = auto()
    BROKER_USER = auto()
    CLIENT_USER = auto()
    SYSTEM_USER = auto()
    UNKNOWN = auto()


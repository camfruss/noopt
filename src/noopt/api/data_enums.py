from enum import auto, Enum


class AssetMainType(Enum):
    BOND = auto()
    EQUITY = auto()
    FOREX = auto()
    FUTURE = auto()
    FUTURE_OPTION = auto()
    INDEX = auto()
    MUTUAL_FUND = auto()
    OPTION = auto()

class AssetType(Enum):
    BOND = auto()
    EQUITY = auto()
    ETF = auto()
    EXTENDED = auto()
    FOREX = auto()
    FUNDAMENTAL = auto()
    FUTURE = auto()
    FUTURE_OPTION = auto()
    INDEX = auto()
    INDICATOR = auto()
    MUTUAL_FUND = auto()
    OPTION = auto()
    UNKNOWN = auto()

class DivFreq(Enum):
    ONE = 1
    TWO = 2 
    THREE = 3
    FOUR = 4
    SIX = 6 
    ELEVEN = 11
    TWELVE = 12
    NONE = 0

class EquityAssetSubType(Enum):
    ADR = auto()
    CEF = auto()
    COE = auto()
    ETF = auto()
    ETN = auto()
    GDR = auto()
    NONE = auto()
    PRF = auto()
    RGT = auto()
    UIT = auto()
    WAR = auto()

class Exchanges(Enum):
    ASE = auto()
    BATS = auto()
    IND = auto()
    NAP = auto()
    NAS = auto()
    NYS = auto()
    OPR = auto()
    PAC = auto()

class ExerciseType(Enum):
    A = auto()  # American
    E  = auto()  # European

class ExpirationType(Enum):
    M = auto()  # End of Month
    Q = auto()  # Quarterly
    S = auto()  # Weekly / Friday Short Term Expirations
    W = auto()  # 3rd Friday of Month / regular options

class FundStrategy(Enum):
    A = auto()  # Active
    L = auto()  # Leveraged
    NONE = auto()
    P = auto()  # Passive
    Q = auto()  # Quantitative
    S = auto()  # Short

class MutualFundAssetSubType(Enum):
    CEF = auto()
    MMF = auto()
    NONE = auto()
    OEF = auto()

class QuoteType(Enum):
    NBBO = auto()  # realtime
    NFL = auto()   # Non-fee liable quote
    NONE = auto()

class SettlementType(Enum):
    A = auto()  # AM
    P = auto()  # PM

class Strategy(Enum):
    ANALYTICAL = auto()
    BUTTERFLY = auto()
    CALENDAR = auto()
    COLLAR = auto()
    CONDOR = auto()
    COVERED = auto()
    DIAGONAL = auto()
    ROLL = auto()
    SINGLE = auto()
    STRADDLE = auto()
    STRANGLE = auto()
    VERTICAL = auto()


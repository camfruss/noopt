from __future__ import annotations

from trader_enums import *


class AccountNumberHash:
    account_number: str
    hash_value: str

class OrderStrategy:
    account_number: str
    advanced_order_type: AdvancedOrderType
    close_time: str  # date-time
    entered_time: str  # date-time
    order_balance: OrderBalance
    order_strategy_type: OrderStrategyType
    order_version: int
    session: Session
    status: APIOrderStatus
    all_or_none: bool
    discretionary: bool
    duration: Duration
    filled_quantity: int
    order_type: OrderType
    order_value: int
    price: int
    quantity: int
    remaining_quantity: int
    sell_non_marginable_first: bool
    settlement_instruction: SettlementInstruction
    strategy: ComplexOrderStrategyType
    amount_indicator: AmountIndicator
    orderLegs: list[OrderLeg]

class OrderLeg:
    ...

class OrderBalance:
    ...

class OrderValidationResult:
    ...

class OrderValidationDetail:
    ...

class APIRuleAction:
    ...

class CommissionAndFee:
    ...

class Commission:
    ...

class CommissionLeg:
    ...

class CommissionValue:
    ...

class Fees:
    ...

class FeeLeg:
    ...

class FeeValue:
    ...

class FeeType:
    ...

class Account:
    ...

class DateParam:
    ...

class Order:
    ...

class OrderRequest:
    ...

class PreviewOrder:
    ...

class OrderActivity:
    ...

class ExecutionLeg:
    ...

class Position:
    ...

class ServiceError:
    ...

class OrderLegCollection:
    ...

class SecuritiesAccount:
    ...

class SecuritiesAccountBase:
    ...

class MarginAccount:
    ...

class MarginInitialBalance:
    ...

class MarginBalance:
    ...

class CashAccount: 
    ...

class CashInitialBalance:
    ...

class CashBalance:
    ...

class TransactionBaseInstrument:
    ...

class AccountsBaseInstrument:
    ...

class AccountsInstrument:
    ...

class TransactionInstrument:
    ...

class TransactionCashEquivalent:
    ...

class CollectiveInvestment:
    ...

class Instruction:
    ...

class AssetType:
    ...

class Currency:
    ...

class TransactionEquity:
    ...

class TransactionFixedIncome:
    ...

class Forex:
    ...

class Future:
    ...

class Index:
    ...

class TransactionMutualFund:
    ...

class TransactionOption:
    ...

class Product:
    ...

class AccountCashEquivalent:
    ...

class AccountEquity:
    ...

class AccountFixedIncome:
    ...

class AccountMutualFund:
    ...

class AccountOption:
    ...

class AccountAPIOptionDeliverable:
    symbol: str
    deliverable_units: float
    api_currency_type: Currency
    asset_type: AssetType

class TransactionAPIOptionDeliverable:
    root_symbol: str
    strike_percent: int
    deliberable_number: int
    deliverable_units: int
    deliverable: TransactionInstrument
    asset_type: AssetType

class Transaction:
    activity_id: int
    time: str  # date-time
    user: UserDetails
    description: str
    account_number: str
    type_: TransactionType
    status: Status
    sub_account: AccountType
    trade_date: str  # date-time
    settlement_date: str  # date-time
    position_id: int
    order_id: int
    net_amount: float
    activity_type: ActivityType
    transfer_items: list[TransferItem]

class UserDetails:
    cd_domain_id: str
    login: str
    type_: UserType
    user_id: int
    system_user_name: str
    first_name: str
    last_name: str
    broker_rep_code: str

class TransferItem:
    instrument: TransactionInstrument
    amount: float
    cost: float
    price: float
    fee_type: FeeType
    position_effect: PositionEffect

class UserPreference:
    accounts: list[UserPreferenceAccount]
    streamer_info: list[StreamerInfo]
    offers: list[Offer]

class UserPreferenceAccount:
    account_number: str
    primary_account: bool  # default: False
    type_: str
    nick_name: str
    account_color: str  # Green, Blue
    display_acct_id: str
    auto_position_effect: bool  # defulat: False

class StreamerInfo:
    streamer_socket_url: str
    schwab_client_customer_id: str
    schwab_client_correl_id: str
    schwab_client_channel: str
    schwab_client_function_id: str

class Offer:
    level_2_permissions: bool   # default False
    mkt_data_permission: str


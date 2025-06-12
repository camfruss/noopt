from __future__ import annotations

from trader_enums import *

from typing import Literal


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
    ask_price: float
    bid_price: float
    last_price: float
    mark_price: float
    projected_commission: float
    quantity: float
    final_symbol: str
    leg_id: int
    asset_type: AssetType
    instruction: Instruction

class OrderBalance:
    order_value: float
    projected_available_fund: float
    projected_buying_power: float
    projected_commission: float

class OrderValidationResult:
    alerts: list[OrderValidationDetail]
    accepts: list[OrderValidationDetail]
    rejects: list[OrderValidationDetail]
    reviews: list[OrderValidationDetail]
    warns: list[OrderValidationDetail]

class OrderValidationDetail:
    validation_rule_name: str
    message: str
    activity_message: str
    original_severity: APIRuleAction
    override_name: str
    override_severity: APIRuleAction

class CommissionAndFee:
    commission: Commission
    fee: Fees
    true_commission: Commission

class Commission:
    commission_legs: list[CommissionLeg]

class CommissionLeg:
    commission_values: list[CommissionValue]

class CommissionValue:
    value: float
    type_: FeeType

class Fees:
    fee_legs: list[FeeLeg]

class FeeLeg:
    fee_values: list[FeeValue]

class FeeValue:
    value: float
    type_: FeeType

class Account:
    securities_account: SecuritiesAccount

class DateParam:
    date: str  # yyyy-MM-dd'T'HH:mm:ss.SSSZ

class BaseOrder:
    session: Session
    duration: Duration
    order_type: OrderType
    cancel_time: str  # datetime
    complex_order_strategy_type: ComplexOrderStrategyType
    quantity: float
    filled_quantity: float
    remaining_quantity: float
    release_time: str  # datetime
    stop_price: float
    stop_price_link_basis: StopPriceLinkBasis
    stop_price_link_type: StopPriceLinkType
    stop_price_offset: float
    stop_type: StopType
    price_link_basis: PriceLinkBasis
    price_link_type: PriceLinkType
    price: float
    tax_lot_method: TaxLotMethod
    order_leg_collection: list[OrderLegCollection]
    activation_price: float
    special_instruction: SpecialInstruction
    order_strategy_type: OrderStrategyType
    order_id: int
    cancelable: bool
    editable: bool
    status: Status
    entered_time: str  # datetime
    close_time: str  # datetime
    account_number: int
    order_activity_collection: list[OrderActivity]
    replacing_order_collection: list  # TODO
    child_order_strategies: list  # TODO
    status_description: str

class Order(BaseOrder):
    requested_destination: RequestedDestination
    tag: str

class OrderRequest(BaseOrder):
    destination_link_name: str    

class PreviewOrder:
    order_id: int
    order_strategy: OrderStrategy
    order_validation_result: OrderValidationResult
    commission_and_fee: CommissionAndFee

class OrderActivity:
    activity_type: ActivityType
    execution_type: ExecutionType
    quantity: float
    order_remaining_quantity: float
    execution_legs: list[ExecutionLeg]

class ExecutionLeg:
    leg_id: int
    price: float
    quantity: float
    mismarked_quantity: float
    instrument_id: int
    time: str  # date-time

class Position:
    ...

class ServiceError:
    message: str
    errors: list[str]

class OrderLegCollection:
    order_leg_type: LegType
    leg_id: int
    instrument: AccountsInstrument
    instruction: Instruction
    position_effect: str
    quantity: float
    quantity_type: QuantityType
    div_cap_gains: DivCapGainsType
    to_symbol: str

class SecuritiesAccount:
    data: MarginAccount | CashAccount

class SecuritiesAccountBase:
    type_: Literal['CASH', 'MARGIN']
    account_number: str
    round_trips: int
    is_day_trader: bool
    is_closing_only_restricted: bool
    pfcb_flag: bool
    positions: list[Position]

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

class BaseAsset:
    asset_type: AssetType
    cusip: str
    symbol: str
    description: str
    instrument_id: int
    net_change: float

class TransactionBaseInstrument(BaseAsset):
    pass

class AccountsBaseInstrument(BaseAsset):
    pass

class AccountsInstrument:
    data: AccountXYZ

class TransactionInstrument:
    data: TransactionCashEquivalent | CollectiveInvestment | Currency | TransactionEquity | \
          TransactionFixedIncome | Forex | Future | Index | TransactionMutualFund | TransactionOption | \
          Product

class TransactionCashEquivalent(BaseAsset):
    type_: CashType

class CollectiveInvestment(BaseAsset):
    type_: CollectiveType

class Currency(BaseAsset):
    pass

class TransactionEquity(BaseAsset):
    type_: EquityType 

class TransactionFixedIncome(BaseAsset):
    type_: FixedIncomeType
    maturitiy_date: str  # date-time
    factor: float
    multiplier: float
    variable_rate: float

class Forex(BaseAsset):
    type_: ForexType
    base_currency: Currency
    counter_currency: Currency

class Future:
    active_contract: bool
    type_: FutureType
    expiration_date: str  # date-time
    last_trading_date: str  # date-time
    first_notice_date: str  # datetime
    multiplier: float
    data: TransactionCashEquivalent | CollectiveInvestment | Currency | TransactionEquity | \
          TransactionFixedIncome | Forex | Index | TransactionMutualFund | TransactionOption | \
          Product

class Index:
    active_contract: bool
    type_: IndexType
    data: TransactionCashEquivalent | CollectiveInvestment | Currency | TransactionEquity | \
          TransactionFixedIncome | Forex | Future | TransactionMutualFund | TransactionOption | \
          Product

class TransactionMutualFund(BaseAsset):
    fund_family_name: str
    fund_family_symbol: str
    fund_group: str
    type_: MutualFundType  # TODO??
    exchange_cutoff_time: str  # datetime
    purchase_cutoff_time: str  # datetime
    redemption_cutoff_time: str  # datetime

class TransactionOption(BaseAsset):
    expiration_date: str  # datetime
    option_deliberables: list[TransactionAPIOptionDeliverable]
    put_call: ContractType
    strike_price: float
    type_: TransactionOptionType
    underlying_symbol: str
    underlying_cusip: str
    deliverable: TransactionInstrument

class Product(BaseAsset):
    type_: ProductType

class AccountCashEquivalent(BaseAsset):
    type_: CashType  # TODO: check

class AccountEquity(BaseAsset):
    pass

class AccountFixedIncome(BaseAsset):
    maturity_date: str   # date-time
    factor: float
    variable_rate: float

class AccountMutualFund(BaseAsset):
    pass

class AccountOption(BaseAsset):
    option_deliverables: list[AccountAPIOptionDeliverable]
    put_call: ContractType
    option_multiplier: int
    type_: TransactionOptionType  # TODO???
    underlying_symbol: str

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


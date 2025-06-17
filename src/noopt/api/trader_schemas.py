from __future__ import annotations

from shared_enums import *
from trader_enums import *

from typing import Literal

from pydantic import BaseModel


class OrderStrategy(BaseModel):
    account_number: str
    advanced_order_type: AdvancedOrderType
    all_or_none: bool
    amount_indicator: AmountIndicator
    close_time: str  # date-time
    discretionary: bool
    duration: Duration
    entered_time: str  # date-time
    filled_quantity: int
    orderLegs: list[OrderLeg]
    order_balance: OrderBalance
    order_strategy_type: OrderStrategyType
    order_type: OrderType
    order_value: int
    order_version: int
    price: int
    quantity: int
    remaining_quantity: int
    sell_non_marginable_first: bool
    session: Session
    settlement_instruction: SettlementInstruction
    status: APIOrderStatus
    strategy: ComplexOrderStrategyType

class OrderLeg(BaseModel):
    ask_price: float
    asset_type: AssetType
    bid_price: float
    final_symbol: str
    instruction: Instruction
    last_price: float
    leg_id: int
    mark_price: float
    projected_commission: float
    quantity: float

class OrderBalance(BaseModel):
    order_value: float
    projected_available_fund: float
    projected_buying_power: float
    projected_commission: float

class OrderValidationResult(BaseModel):
    accepts: list[OrderValidationDetail]
    alerts: list[OrderValidationDetail]
    rejects: list[OrderValidationDetail]
    reviews: list[OrderValidationDetail]
    warns: list[OrderValidationDetail]

class OrderValidationDetail(BaseModel):
    activity_message: str
    message: str
    original_severity: APIRuleAction
    override_name: str
    override_severity: APIRuleAction
    validation_rule_name: str

class BaseOrder(BaseModel):
    account_number: int
    activation_price: float
    cancel_time: str  # datetime
    cancelable: bool
    child_order_strategies: list  # TODO
    close_time: str  # datetime
    complex_order_strategy_type: ComplexOrderStrategyType
    duration: Duration
    editable: bool
    entered_time: str  # datetime
    filled_quantity: float
    order_activity_collection: list[OrderActivity]
    order_id: int
    order_leg_collection: list[OrderLegCollection]
    order_strategy_type: OrderStrategyType
    order_type: OrderType
    price: float
    price_link_basis: PriceLinkBasis
    price_link_type: PriceLinkType
    quantity: float
    release_time: str  # datetime
    remaining_quantity: float
    replacing_order_collection: list  # TODO
    session: Session
    special_instruction: SpecialInstruction
    status: Status
    status_description: str
    stop_price: float
    stop_price_link_basis: StopPriceLinkBasis
    stop_price_link_type: StopPriceLinkType
    stop_price_offset: float
    stop_type: StopType
    tax_lot_method: TaxLotMethod

class Order(BaseOrder, BaseModel):
    requested_destination: RequestedDestination
    tag: str

class OrderLegCollection(BaseModel):
    div_cap_gains: LegType
    instruction: Instruction
    instrument: AccountsInstrument
    leg_id: int
    order_leg_type: LegType
    position_effect: str
    quantity: float
    quantity_type: AmountIndicator
    to_symbol: str

class OrderRequest(BaseOrder, BaseModel):
    destination_link_name: str    

class OrderActivity(BaseModel):
    activity_type: Literal['EXECUTION', 'ORDER_ACTION']
    execution_legs: list[ExecutionLeg]
    execution_type: Literal['FILL']
    order_remaining_quantity: float
    quantity: float

class ExecutionLeg(BaseModel):
    instrument_id: int
    leg_id: int
    mismarked_quantity: float
    price: float
    quantity: float
    time: str  # date-time

class PreviewOrder(BaseModel):
    commission_and_fee: CommissionAndFee
    order_id: int
    order_strategy: OrderStrategy
    order_validation_result: OrderValidationResult

class CommissionAndFee(BaseModel):
    commission: Commission
    fee: Fees
    true_commission: Commission

class Commission(BaseModel):
    commission_legs: list[CommissionLeg]

class CommissionLeg(BaseModel):
    commission_values: list[CommissionValue]

class CommissionValue(BaseModel):
    data_type: FeeType
    value: float

class Fees(BaseModel):
    fee_legs: list[FeeLeg]

class FeeLeg(BaseModel):
    fee_values: list[FeeValue]

class FeeValue(BaseModel):
    data_type: FeeType
    value: float

class Account(BaseModel):
    securities_account: SecuritiesAccount

class AccountNumberHash(BaseModel):
    account_number: str
    hash_value: str

class Position(BaseModel):
    aged_quantity: float
    average_long_price: float
    average_price: float
    average_short_price: float
    current_day_cost: float
    current_day_profit_loss: float
    current_day_profit_loss_percentage: float
    instrument: AccountsInstrument
    long_open_profit_loss: float
    long_quantity: float
    maintencance_requirement: float
    market_value: float
    previous_session_long_quantity: float
    previous_session_long_quantity: float
    settled_long_quantity: float
    settled_short_quantity: float
    short_open_profit_loss: float
    short_quantity: float
    tax_lot_average_long_price: float
    tax_lot_average_short_price: float

class ServiceError(BaseModel):
    errors: list[str]
    message: str

class SecuritiesAccount(BaseModel):
    data: MarginAccount | CashAccount

class SecuritiesAccountBase(BaseModel):
    account_number: str
    data_type: Literal['CASH', 'MARGIN']
    is_closing_only_restricted: bool
    is_day_trader: bool
    pfcb_flag: bool
    positions: list[Position]
    round_trips: int

class InitialBalanceBase(BaseModel):
    account_value: float
    accrued_interest: float
    bond_value: float
    cash_available_for_trading: float
    cash_balance: float
    cash_receipts: float
    is_in_call: float
    liquidation_value: float
    long_option_market_value: float
    long_stock_value: float
    money_market_fund: float
    mutual_fund_value: float
    pending_deposits: float
    short_option_market_value: float
    short_stock_value: float
    unsettled_cash: float

class MarginAccount(SecuritiesAccountBase, BaseModel):
    current_balances: MarginBalance
    initial_balances: MarginInitialBalance
    projected_balances: MarginBalance

class MarginInitialBalance(InitialBalanceBase, BaseModel):
    available_funds_non_marginable_trade: float
    buying_power: float
    day_trading_buying_power: float
    day_trading_buying_power_call: float
    day_trading_equity_call: float
    equity: float
    equity_percentage: float
    long_margin_value: float
    maintenance_call: float
    maintenance_requirement: float
    margin: float
    margin_balance: float
    margin_equity: float
    reg_t_call: float
    short_balance: float
    short_margin_value: float
    total_cash: float

class MarginBalance(BaseModel):
    available_funds: float
    available_funds_non_marginable_trade: float
    buying_power: float
    buying_power_non_marginable_trade: float
    day_trading_buying_power: float
    day_trading_buying_power_call: float
    equity: float
    equity_percentage: float
    is_in_call: float
    long_margin_value: float
    maintenance_call: float
    maintenance_requirement: float
    margin_balance: float
    option_buying_power: float
    reg_t_call: float
    short_balance: float
    short_margin_value: float
    sma: float
    stock_buying_power: float

class CashAccount(SecuritiesAccountBase, BaseModel): 
    current_balances: CashBalance
    initial_balances: CashInitialBalance
    projected_balances: CashBalance

class CashInitialBalance(InitialBalanceBase, BaseModel):
    cash_available_for_withdrawal: float
    cash_debit_call_value: float

class CashBalance(BaseModel):
    cash_available_for_trading: float
    cash_available_for_withdrawal: float
    cash_call: float
    cash_debit_call_value: float
    long_non_marginable_market_value: float
    total_cash: float
    unsettled_cash: float

class BaseAsset(BaseModel):
    asset_type: AssetType
    cusip: str
    description: str
    instrument_id: int
    net_change: float
    symbol: str

class TransactionBaseInstrument(BaseAsset, BaseModel):
    pass

class AccountsBaseInstrument(BaseAsset, BaseModel):
    pass

class AccountsInstrument(BaseModel):
    data: AccountCashEquivalent | AccountEquity | AccountFixedIncome | AccountMutualFund | AccountOption

class TransactionInstrument(BaseModel):
    data: TransactionCashEquivalent | CollectiveInvestment | Currency | TransactionEquity | \
          TransactionFixedIncome | Forex | Future | Index | TransactionMutualFund | TransactionOption | \
          Product

class TransactionCashEquivalent(BaseAsset, BaseModel):
    data_type: CashType

class CollectiveInvestment(BaseAsset, BaseModel):
    data_type: CollectiveType

class Currency(BaseAsset, BaseModel):
    pass

class TransactionEquity(BaseAsset, BaseModel):
    data_type: EquityType 

class TransactionFixedIncome(BaseAsset, BaseModel):
    data_type: FixedIncomeType
    factor: float
    maturitiy_date: str  # date-time
    multiplier: float
    variable_rate: float

class Forex(BaseAsset, BaseModel):
    base_currency: Currency
    counter_currency: Currency
    data_type: ForexType

class Future(BaseModel):
    active_contract: bool
    expiration_date: str  # date-time
    first_notice_date: str  # datetime
    last_trading_date: str  # date-time
    multiplier: float
    data_type: FutureType
    
    data: TransactionCashEquivalent | CollectiveInvestment | Currency | TransactionEquity | \
          TransactionFixedIncome | Forex | Index | TransactionMutualFund | TransactionOption | \
          Product

class Index(BaseModel):
    active_contract: bool
    data_type: IndexType

    data: TransactionCashEquivalent | CollectiveInvestment | Currency | TransactionEquity | \
          TransactionFixedIncome | Forex | Future | TransactionMutualFund | TransactionOption | \
          Product

class TransactionMutualFund(BaseAsset, BaseModel):
    data_type: MutualFundType  # TODO??
    exchange_cutoff_time: str  # datetime
    fund_family_name: str
    fund_family_symbol: str
    fund_group: str
    purchase_cutoff_time: str  # datetime
    redemption_cutoff_time: str  # datetime

class TransactionOption(BaseAsset, BaseModel):
    data_type: OptionType
    deliverable: TransactionInstrument
    expiration_date: str  # datetime
    option_deliberables: list[TransactionAPIOptionDeliverable]
    put_call: ContractType
    strike_price: float
    underlying_cusip: str
    underlying_symbol: str

class Product(BaseAsset, BaseModel):
    data_type: ProductType

class AccountCashEquivalent(BaseAsset, BaseModel):
    data_type: CashType  # TODO: check

class AccountEquity(BaseAsset, BaseModel):
    pass

class AccountFixedIncome(BaseAsset, BaseModel):
    factor: float
    maturity_date: str   # date-time
    variable_rate: float

class AccountMutualFund(BaseAsset, BaseModel):
    pass

class AccountOption(BaseAsset, BaseModel):
    data_type: OptionType  # TODO???
    option_deliverables: list[AccountAPIOptionDeliverable]
    option_multiplier: int
    put_call: ContractType
    underlying_symbol: str

class AccountAPIOptionDeliverable(BaseModel):
    api_currency_type: Currency
    asset_type: AssetType
    deliverable_units: float
    symbol: str

class TransactionAPIOptionDeliverable(BaseModel):
    asset_type: AssetType
    deliberable_number: int
    deliverable: TransactionInstrument
    deliverable_units: int
    root_symbol: str
    strike_percent: int

class Transaction(BaseModel):
    account_number: str
    activity_id: int
    activity_type: ActivityType
    data_type: TransactionType
    description: str
    net_amount: float
    order_id: int
    position_id: int
    settlement_date: str  # date-time
    status: Status
    sub_account: SubAccountType
    time: str  # date-time
    trade_date: str  # date-time
    transfer_items: list[TransferItem]
    user: UserDetails

class UserDetails(BaseModel):
    broker_rep_code: str
    cd_domain_id: str
    data_type: UserType
    first_name: str
    last_name: str
    login: str
    system_user_name: str
    user_id: int

class TransferItem(BaseModel):
    amount: float
    cost: float
    fee_type: FeeType
    instrument: TransactionInstrument
    position_effect: PositionEffect
    price: float

class UserPreference(BaseModel):
    accounts: list[UserPreferenceAccount]
    offers: list[Offer]
    streamer_info: list[StreamerInfo]

class UserPreferenceAccount(BaseModel):
    account_color: str  # Green, Blue
    account_number: str
    auto_position_effect: bool  # defulat: False
    data_type: str
    display_acct_id: str
    nick_name: str
    primary_account: bool  # default: False

class StreamerInfo(BaseModel):
    schwab_client_channel: str
    schwab_client_correl_id: str
    schwab_client_customer_id: str
    schwab_client_function_id: str
    streamer_socket_url: str

class Offer(BaseModel):
    level_2_permissions: bool   # default False
    mkt_data_permission: str

class DateParam(BaseModel):
    date: str  # yyyy-MM-dd'T'HH:mm:ss.SSSZ


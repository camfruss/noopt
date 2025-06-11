from trader_enums import *

from datetime import datetime


class AccountNumberHash:
    account_number: str
    hash_value: str

class OrderStrategy:
    account_number: str
    advanced_order_type: AdvancedOrderType
    close_time: datetime
    entered_time: datetime
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

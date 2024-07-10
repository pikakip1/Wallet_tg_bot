from aiogram.fsm.state import State, StatesGroup


class WalletCreate(StatesGroup):
    create_wallet = State()


class TransactionRecord(StatesGroup):
    transaction_type = State()
    transaction_category = State()
    transaction_amount = State()
    transaction_comment = State()


class StatisticWallet(StatesGroup):
    menu_statistic = State()
    type_statistic = State()


class AddAccount(StatesGroup):
    set_account = State()

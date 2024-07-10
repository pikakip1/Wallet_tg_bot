from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from database import async_db_manager
from filters.chat_type import IsAllowedUserId
from keyboards.transaction_record import get_menu_statistic_inline_keyboard
from services.wallet_service import WalletService
from states.transaction_record import StatisticWallet

allowed_user_ids = [353032411, 1288729238]

statistic = Router()


@statistic.message(F.text.startswith("Баланс"), IsAllowedUserId(allowed_user_ids))
async def get_balance(message: Message):
    wallet_balance = await WalletService(message.from_user.id).get_wallet_balance("Основной")
    await message.answer(text=str(wallet_balance))


@statistic.message(F.text.startswith("Статистика"), IsAllowedUserId(allowed_user_ids))
@statistic.message(Command(commands=["statistic"]), IsAllowedUserId(allowed_user_ids))
async def get_menu_statistic(message: Message, state: FSMContext):
    await message.answer(text="Статистика", reply_markup=get_menu_statistic_inline_keyboard())
    await state.set_state(StatisticWallet.menu_statistic)


@statistic.callback_query(
    F.data.endswith("записи"),
    IsAllowedUserId(allowed_user_ids),
    StatisticWallet.menu_statistic,
)
async def get_last_transaction(callback: CallbackQuery, state: FSMContext):
    async with async_db_manager.async_session_factory() as session:
        async with session.begin():
            wallet_service = WalletService(callback.from_user.id)
            wallet_statistic = await wallet_service.get_last_records(session=session, wallet_name="Основной")
            stats_text = "\n".join(wallet_statistic)

            await callback.message.answer(text=stats_text, reply_markup=get_menu_statistic_inline_keyboard())


@statistic.callback_query(
    F.data.endswith("категориям"),
    IsAllowedUserId(allowed_user_ids),
    StatisticWallet.menu_statistic,
)
async def get_statistic_categories(callback: CallbackQuery, state: FSMContext):
    async with async_db_manager.async_session_factory() as session:
        async with session.begin():

            categories_statistics = await WalletService(callback.from_user.id).get_statistic_categories(
                session=session,
                wallet_name="Основной",
            )
            await callback.message.answer(
                text=categories_statistics,
                reply_markup=get_menu_statistic_inline_keyboard(),
            )

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from filters.chat_type import IsAllowedUserId
from keyboards.transaction_record import get_category_inline_keyboard, make_menu_keyboard, make_start_button, \
    make_cancel_btn, get_menu_statistic_inline_keyboard
from services.statistic import WalletQueries
from services.wallet_management import Transactions
from states.transaction_record import TransactionRecord, StatisticWallet

menu = Router()

allowed_user_ids = [353032411, 1288729238]


@menu.message(Command(commands=['menu']), IsAllowedUserId(allowed_user_ids),  StateFilter(None))
async def start_menu(message: Message, state: FSMContext):
    chose_menu = ['Доход', 'Расход', 'Баланс']

    await message.answer(
        text='Выбери действие',
        reply_markup=make_menu_keyboard(chose_menu)
    )

    await state.set_state(TransactionRecord.transaction_type)


@menu.message(F.text.in_(['Доход', 'Расход']), IsAllowedUserId(allowed_user_ids),  TransactionRecord.transaction_type)
async def get_type_record(message: Message, state: FSMContext):
    await message.answer(
        reply_markup=make_cancel_btn(),
        text='Для отмены нажми Отмена',
    )
    categories = ['Одежда', 'Еда', 'Аренда']
    await state.update_data(transaction_type=message.text.lower())
    await message.answer(
        text='Выбери тип',
        reply_markup=get_category_inline_keyboard(categories),
    )

    await state.set_state(TransactionRecord.transaction_category)


@menu.message(IsAllowedUserId(allowed_user_ids),  TransactionRecord.transaction_type)
async def get_type_record_incorrect(message: Message, state: FSMContext):
    chose_menu = ['Доход', 'Расход', 'Баланс']
    await message.answer(
        text='Не нужно ничего вводить, выбери тип на кнопках',
        reply_markup=make_menu_keyboard(chose_menu)
    )


@menu.callback_query(
    F.data.startswith('category_'),
    IsAllowedUserId(allowed_user_ids),
    TransactionRecord.transaction_category,
)
async def get_categories(callback: CallbackQuery, state: FSMContext):
    user_category = callback.data.split("_")[-1]
    await state.update_data(transaction_category=user_category)
    user_date = await state.get_data()
    await callback.message.answer(
        text=f'Записываю в {user_date["transaction_type"]} категорию {user_category}\nВведите сумму'
    )
    await state.set_state(TransactionRecord.transaction_amount)


@menu.message(IsAllowedUserId(allowed_user_ids),  TransactionRecord.transaction_category)
async def get_categories_incorrect(message: Message, state: FSMContext):
    categories = ['Одежда', 'Еда', 'Аренда']
    await message.answer(
        text='Не нужно ничего вводить, выбери нужную кнопку',
        reply_markup=get_category_inline_keyboard(categories)
    )


@menu.message(IsAllowedUserId(allowed_user_ids),  TransactionRecord.transaction_amount)
async def get_amount(message: Message, state: FSMContext):
    if message.text.isdigit():
        amount = int(message.text)
        await state.update_data(transaction_amount=amount)
        await message.answer(text=f'Добавьте комментарий или введите "-"')
        await state.set_state(TransactionRecord.transaction_comment)
    else:
        await message.answer(text=f'Пожалуйста, введите корректное число.')


@menu.message(IsAllowedUserId(allowed_user_ids),  TransactionRecord.transaction_comment)
async def get_comment(message: Message, state: FSMContext):
    await state.update_data(transaction_comment=message.text)
    user_date = await state.get_data()
    transaction = Transactions(message.from_user.id)

    await transaction.add_transaction(
        amount=user_date["transaction_amount"],
        category=user_date["transaction_category"],
        type_transaction='income' if user_date["transaction_type"] == 'доход' else 'expense',
        comment=user_date['transaction_comment'],
        wallet_name='Основной'
    )

    await message.answer(
        text=f'Добавлена запись:\n'
             f'- Тип: {user_date["transaction_type"]}\n'
             f'- Категория: {user_date["transaction_category"]}\n'
             f'- Сумма: {user_date["transaction_amount"]}\n'
             f'- Комментарий: {user_date["transaction_comment"]}',
        reply_markup=make_start_button()
    )
    await state.clear()


@menu.message(Command(commands=['statistic']), IsAllowedUserId(allowed_user_ids))
async def get_menu_statistic(message: Message, state: FSMContext):
    await message.answer(
        text='Выбери статистику',
        reply_markup=get_menu_statistic_inline_keyboard()
    )
    await state.set_state(StatisticWallet.menu_statistic)


@menu.message(Command(commands=['statistic']), IsAllowedUserId(allowed_user_ids), StatisticWallet.menu_statistic)
async def get_menu_statistic(message: Message, state: FSMContext):
    wallet = WalletQueries(message.from_user.id)
    wallet_statistics = wallet.get_last_records()
    await message.answer(
        text='Выбери статистику',
        reply_markup=get_menu_statistic_inline_keyboard()
    )
    await state.set_state(StatisticWallet.type_statistic)
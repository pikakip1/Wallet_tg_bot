from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from filters.chat_type import IsAllowedUserId
from services.registration import add_wallet
from states.transaction_record import WalletCreate

common_router = Router()

allowed_user_ids = [353032411, 1288729238]


@common_router.message(F.text.lower() == 'отмена', IsAllowedUserId(allowed_user_ids))
async def btn_cancel(message: Message, state: FSMContext):
    await cmd_cancel(message, state)


@common_router.message(Command(commands=['start']), IsAllowedUserId(allowed_user_ids))
async def start_menu(message: Message, state: FSMContext):
    await message.answer(
        text='Бот для ведения денежных передвижений',
    )


@common_router.message(Command(commands=['Add_wallet']), IsAllowedUserId(allowed_user_ids))
async def start_menu(message: Message, state: FSMContext):
    print(message.text)
    await message.answer(
        text=f'Для добавления кошелька введите:\n'
             'Название кошелька и счет на кошельке'
    )
    await state.set_state(WalletCreate.create_wallet)


@common_router.message(IsAllowedUserId(allowed_user_ids), WalletCreate.create_wallet)
async def start_menu(message: Message, state: FSMContext):
    *wallet_name, amount = message.text.split()
    if wallet_name:
        amount = int(amount) if amount.isdigit() else 0
        await message.answer(text=f'Добавляю кошелек: {" ".join(wallet_name)} с суммой {amount}')
        await state.clear()
        await add_wallet(" ".join(wallet_name), amount, message.from_user.id)

    else:
        await message.answer(text=f'Ошибка ввода, введите название кошелька и сумму')


@common_router.message(Command(commands=['cancel']))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )


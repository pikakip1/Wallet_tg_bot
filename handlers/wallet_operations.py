from datetime import datetime

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from filters.chat_type import IsAllowedUserId

allowed_user_ids = [353032411]

wallet_operations_router = Router()
wallet_operations_router.message.filter(IsAllowedUserId(allowed_user_ids))


@wallet_operations_router.message(F.text.split()[0].lower() == 'расход')
async def add_expense(message: Message):
    await message.reply('Добавлен расход')


@wallet_operations_router.message(F.text.split()[0].lower() == 'доход')
async def add_income(message: Message):
    await message.reply('Добавлен доход')


@wallet_operations_router.message(F.text.split()[0].lower() == 'баланс')
async def check_balance(message: Message):
    date_now = datetime.now().strftime('%d/%m/%y %H:%M')
    await message.reply(f'Баланс на {date_now}')


@wallet_operations_router.message(F.text == 'Итог за предыдущий месяц')
async def check_balance(message: Message):
    date_now = datetime.now().month - 1
    await message.reply(f'Баланс за {date_now} месяц')

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from filters.chat_type import IsAllowedUserId
from keyboards.transaction_record import make_menu_keyboard
from services.account_service import AccountService
from services.wallet_service import WalletService
from states.transaction_record import AddAccount, WalletCreate

common_router = Router()

allowed_user_ids = [353032411, 1288729238]


@common_router.message(F.text.lower() == "отмена", IsAllowedUserId(allowed_user_ids))
@common_router.message(Command(commands=["cancel"]))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Действие отменено", reply_markup=make_menu_keyboard())


@common_router.message(Command(commands=["start"]), IsAllowedUserId(allowed_user_ids))
async def start_bot(message: Message, state: FSMContext):
    await message.answer(
        text="Бот для ведения денежных передвижений\n" "Введи свое имя",
    )

    await state.set_state(AddAccount.set_account)


@common_router.message(F.text.lower() == "добавить аккаунт", IsAllowedUserId(allowed_user_ids))
async def add_account(message: Message, state: FSMContext):
    await message.answer(
        text="Бот для ведения денежных передвижений\n" "Введи имя аккаунта",
    )

    await state.set_state(AddAccount.set_account)


@common_router.message(IsAllowedUserId(allowed_user_ids), AddAccount.set_account)
async def set_account(message: Message, state: FSMContext):
    await AccountService().add_account(telegram_id=message.from_user.id, name=message.text)
    await state.clear()
    await message.answer(text=f"Добавлен пользователь {message.text}")


@common_router.message(F.text.lower() == "добавить кошелек", IsAllowedUserId(allowed_user_ids))
@common_router.message(Command(commands=["Add_wallet"]), IsAllowedUserId(allowed_user_ids))
async def add_wallet(message: Message, state: FSMContext):
    await message.answer(text="Для добавления кошелька введите:\n" "Название кошелька и счет на кошельке")
    await state.set_state(WalletCreate.create_wallet)


@common_router.message(IsAllowedUserId(allowed_user_ids), WalletCreate.create_wallet)
async def set_wallet(message: Message, state: FSMContext):
    *wallet_name, amount = message.text.split()
    if wallet_name:
        amount = int(amount) if amount.isdigit() else 0
        await message.answer(text=f'Добавляю кошелек: {" ".join(wallet_name)} с суммой {amount}')
        await state.clear()
        await WalletService(message.from_user.id).add_wallet(name_wallet=" ".join(wallet_name), amount=amount)

    else:
        await message.answer(text="Ошибка ввода, введите название кошелька и сумму")

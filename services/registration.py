import asyncio
from uuid import UUID

from sqlalchemy import text

from database import async_db_manager


async def add_accounts(telegram_id: int, name: str):
    async with async_db_manager.async_session_factory() as session:
        async with session.begin():
            await session.execute(text(
                "INSERT INTO accounts (id, name) "
                "VALUES (:id, :name)"
            ), {'id': telegram_id, 'name': name})


async def add_wallet(name_wallet: str, amount: int | float, account_id: int):
    async for session in async_db_manager.get_session():
        async with session.begin():
            await session.execute(
                text("INSERT INTO wallets (name_wallet, amount, account_id) VALUES (:name_wallet, :amount, :account_id)"),
                {"name_wallet": name_wallet, "amount": amount, "account_id": account_id}
            )


async def check_account(telegram_id: int):
    async with async_db_manager.async_session_factory() as session:
        async with session.begin():
            res = await session.execute(text(
                "SELECT name FROM accounts WHERE id = :telegram_id"
            ), {'telegram_id': telegram_id})
            if res.scalar_one_or_none():
                return True
            return False



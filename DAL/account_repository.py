from db.models import Account
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class AccountRepository:
    async def add_account(self, session: AsyncSession, telegram_id: int, name: str):

        new_account = Account(id=telegram_id, name=name)
        session.add(new_account)

    async def check_account(self, session: AsyncSession, telegram_id: int) -> bool:
        res = await session.execute(
            text("SELECT name FROM account WHERE id = :telegram_id"),
            {"telegram_id": telegram_id},
        )
        return res.scalar_one_or_none() is not None

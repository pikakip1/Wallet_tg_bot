from DAL.account_repository import AccountRepository
from database import async_db_manager


class AccountService:
    def __init__(self):
        self.account_repository = AccountRepository()

    async def add_account(self, telegram_id: int, name: str):
        async with async_db_manager.async_session_factory() as session:
            async with session.begin():
                await self.account_repository.add_account(session, telegram_id, name)

    async def check_account(self, telegram_id: int) -> bool:
        async with async_db_manager.async_session_factory() as session:
            async with session.begin():
                return await self.account_repository.check_account(session, telegram_id)

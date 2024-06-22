from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_db_manager


class WalletManager:
    def __init__(self, account_id):
        self.account_id = account_id

    async def update_wallet_amount(self, session: AsyncSession, wallet_id: str, amount: float | int):
        await session.execute(
            text("""
                UPDATE wallets
                SET amount = amount + :amount
                WHERE id = :wallet_id
            """), {'amount': amount, 'wallet_id': wallet_id}
        )

    async def get_wallet_id(self, session: AsyncSession, wallet_name: str) -> str:
        wallet_result = await session.execute(
            text('SELECT id FROM wallets WHERE name_wallet = :wallet_name AND account_id = :account_id'),
            {'wallet_name': wallet_name, 'account_id': self.account_id})
        wallet_id = wallet_result.scalar()

        if not wallet_id:
            raise ValueError(f'Wallet with name "{wallet_name}" not found for account_id {self.account_id}')
        return wallet_id


class CategoryManager:
    async def get_category_id(self, session: AsyncSession, category_name: str) -> str:
        category_result = await session.execute(
            text('SELECT id FROM categories WHERE category_name = :category_name'),
            {'category_name': category_name})
        category_id = category_result.scalar()

        if not category_id:
            raise ValueError(f'Category with name "{category_name}" not found')
        return category_id


class Transactions:
    def __init__(self, account_id):
        self.account_id = account_id
        self.wallet_manager = WalletManager(account_id)
        self.category_manager = CategoryManager()

    async def add_transaction(
            self,
            amount: int | float,
            category: str,
            type_transaction: str,
            comment: str,
            wallet_name: str = 'Основной'
    ):
        async with async_db_manager.async_session_factory() as session:
            async with session.begin():
                wallet_id = await self.wallet_manager.get_wallet_id(session, wallet_name)
                category_id = await self.category_manager.get_category_id(session, category)

                if type_transaction == 'income':
                    await self.wallet_manager.update_wallet_amount(session, wallet_id, amount)
                else:
                    await self.wallet_manager.update_wallet_amount(session, wallet_id, -amount)

                params = {
                    'amount': amount,
                    'comment': comment,
                    'wallet_id': wallet_id,
                    'category_id': category_id,
                    'type_transaction': type_transaction
                }

                await session.execute(text(
                    "INSERT INTO transactions (amount, comment, wallet_id, category_id, type_transaction)"
                    "VALUES (:amount, :comment, :wallet_id, :category_id, :type_transaction)"
                    ), params
                )

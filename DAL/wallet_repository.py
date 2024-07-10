import uuid

from db.models import Wallet
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession


class WalletRepository:
    def __init__(self, account_id: int):
        self.account_id = account_id

    async def update_wallet(self, session: AsyncSession, wallet_name: str, sum_update: int | float):
        statement = await session.execute(
            select(Wallet).filter(Wallet.account_id == self.account_id, Wallet.name_wallet == wallet_name)
        )
        wallet = statement.scalar()
        wallet.amount += sum_update

    async def get_wallet_id(self, session: AsyncSession, wallet_name: str) -> uuid.UUID:
        statement = select(Wallet).filter(Wallet.name_wallet == wallet_name, Wallet.account_id == self.account_id)
        result = await session.execute(statement)
        wallet_id = result.scalar_one().id
        return wallet_id

    async def add_wallet(self, session: AsyncSession, name_wallet: str, amount: int | float):
        new_wallet = Wallet(name_wallet=name_wallet, amount=amount, account_id=self.account_id)
        session.add(new_wallet)
        await session.commit()

    async def get_category_statistics(self, session: AsyncSession, wallet_name: str):
        query = """
            SELECT transaction.amount, transaction.type_transaction, category.category_name
            FROM transaction
            JOIN wallet ON transaction.wallet_id = wallet.id
            JOIN category ON transaction.category_id = category.id
            WHERE wallet.name_wallet = :wallet_name
            AND wallet.account_id = :account_id
            AND transaction.date_transaction >= DATE_TRUNC('month', NOW())
            ORDER BY transaction.date_transaction DESC
        """
        result = await session.execute(
            text(query),
            {
                "wallet_name": wallet_name,
                "account_id": self.account_id,
            },
        )
        return result.fetchall()

    async def get_last_records(self, session: AsyncSession, wallet_name: str, count_records: int = 10):
        last_records_result = await session.execute(
            text(
                "SELECT transaction.amount, date(date_transaction), comment, category.category_name "
                "FROM transaction "
                "JOIN category ON transaction.category_id = category.id "
                "JOIN wallet ON transaction.wallet_id = wallet.id "
                "WHERE wallet.name_wallet = :wallet_name AND wallet.account_id = :account_id "
                "ORDER BY date_transaction DESC "
                "LIMIT :count_records "
            ),
            {
                "wallet_name": wallet_name,
                "count_records": count_records,
                "account_id": self.account_id,
            },
        )
        return last_records_result.fetchall()

    async def get_wallet_amount(self, session: AsyncSession, wallet_name: str):
        query = """
            SELECT amount FROM wallet
            WHERE name_wallet = :wallet_name AND account_id = :account_id
        """
        result = await session.execute(
            text(query),
            {
                "wallet_name": wallet_name,
                "account_id": self.account_id,
            },
        )
        return result.scalar()

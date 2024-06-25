from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class WalletRepository:
    def __init__(self, account_id: int):
        self.account_id = account_id

    async def get_category_statistics(self, session: AsyncSession, wallet_name: str):
        query = """
            SELECT transactions.amount, transactions.type_transaction, categories.category_name
            FROM transactions
            JOIN wallets ON transactions.wallet_id = wallets.id
            JOIN categories ON transactions.category_id = categories.id
            WHERE wallets.name_wallet = :wallet_name
            AND wallets.account_id = :account_id
            AND transactions.date_transaction >= DATE_TRUNC('month', NOW())
            ORDER BY transactions.date_transaction DESC
        """
        result = await session.execute(
            text(query),
            {
                'wallet_name': wallet_name,
                'account_id': self.account_id,
            }
        )
        return result.fetchall()

    async def get_last_records(self, session: AsyncSession, wallet_name: str, count_records: int = 10):
        last_records_result = await session.execute(
            text(
                'SELECT transactions.amount, date(date_transaction), comment, categories.category_name '
                'FROM transactions '
                'JOIN categories ON transactions.category_id = categories.id '
                'JOIN wallets ON transactions.wallet_id = wallets.id '
                'WHERE wallets.name_wallet = :wallet_name AND wallets.account_id = :account_id '
                'ORDER BY date_transaction DESC '
                'LIMIT :count_records '
            ), {'wallet_name': wallet_name, 'count_records': count_records, 'account_id': self.account_id}
        )
        return last_records_result.fetchall()

    async def get_wallet_amount(self, session: AsyncSession, wallet_name: str):
        query = """
            SELECT amount FROM wallets
            WHERE name_wallet = :wallet_name AND account_id = :account_id
        """
        result = await session.execute(
            text(query),
            {
                'wallet_name': wallet_name,
                'account_id': self.account_id,
            }
        )
        return result.scalar()

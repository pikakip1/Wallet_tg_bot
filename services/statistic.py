from datetime import date

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_db_manager


class WalletQueries:
    def __init__(self, account_id: int):
        self.account_id = account_id

    async def get_statistic_category(
            self,
            session: AsyncSession,
            wallet_name: str,
            category_name: str,
            month: int,
            year: int
    ):

        if month + 1 > 12:
            year_end = year + 1
            month_end = 1
        else:
            year_end = year
            month_end = month + 1

        date_start = date(year=year, month=month, day=1)
        date_end = date(year=year_end, month=month_end, day=1)

        statistic_category_result = await session.execute(
            text(
                'SELECT amount, date_transaction, comment '
                'FROM transactions '
                'JOIN categories ON transactions.category_id = categories.id '
                'JOIN wallets ON transactions.wallet_id = wallets.id '
                'WHERE wallet_name = :wallet_name AND wallets.account_id = :account_id '
                'AND category_name = :category_name '
                'AND date_transaction >= :date_start '
                'AND date_transaction < :date_end '
                'ORDER BY date_transaction DESC'
            ), {
                'wallet_name': wallet_name,
                'category_name': category_name,
                'date_start': date_start,
                'date_end': date_end,
                'account_id': self.account_id,
            }
        )
        return statistic_category_result.fetchall()

    async def get_last_records(self, wallet_name: str, count_records: int = 10):
        async with async_db_manager.async_session_factory() as session:
            async with session.begin():
                last_records = await session.execute(
                    text(
                        'SELECT amount, date_transaction, comment, categories.category_name'
                        'FROM transactions'
                        'JOIN categories ON transactions.category_id = categories.id'
                        'JOIN wallets ON transactions.wallet_id = wallets.id'
                        'WHERE wallets.wallet_name = :wallet_name AND wallets.account_id = :account_id'
                        'LIMIT :count_records'
                        'ORDER BY date_transaction DESC'
                    ), {'wallet_name': wallet_name, 'count_records': count_records, 'account_id': self.account_id}
                )
                return last_records.fetchall()

    async def get_amount(self, session: AsyncSession, name_wallet: str):
        amount_result = await session.execute(
            text(
                'SELECT amount FROM wallets'
                'WHERE name_wallet = :name_wallet and account_id = :account_id'
            ), {'name_wallet': name_wallet, 'account_id': self.account_id}
        )

        return amount_result.scalar()
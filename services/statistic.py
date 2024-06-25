from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from DAL.wallet_repository import WalletRepository
from database import async_db_manager


class WalletService:
    def __init__(self, account_id: int):
        self.account_id = account_id
        self.wallet_repository = WalletRepository(account_id)

    async def get_statistic_categories(
            self,
            session: AsyncSession,
            wallet_name: str,

    ):
        statistic_categories = await self.wallet_repository.get_category_statistics(
            session=session,
            wallet_name=wallet_name
        )

        formatted_records = {}
        for record in statistic_categories:
            amount, type_transaction, category = record
            formatted_records.setdefault(category, 0)

            if type_transaction == 'income':
                formatted_records[category] += amount
            else:
                formatted_records[category] -= amount

        formatted_output = '\n'.join([f'{category}: {amount}' for category, amount in formatted_records.items()])

        return formatted_output

    async def get_last_records(self, session: AsyncSession, wallet_name: str, count_records: int = 10) -> list[str]:
        records = await self.wallet_repository.get_last_records(
            session=session,
            wallet_name=wallet_name,
            count_records=count_records
        )

        formatted_records = []
        for record in records:
            formatted_records.append(f'Дата {record[1]}')
            formatted_records.append(f'Сумма {record[0]}')
            formatted_records.append(f'Категория {record[-1]}')
            formatted_records.append(f'Комментарий {record[2]}')
            formatted_records.append('-----')
        return formatted_records

    async def get_wallet_balance(self, session: AsyncSession, wallet_name: str):
        return await self.wallet_repository.get_wallet_amount(session, wallet_name)

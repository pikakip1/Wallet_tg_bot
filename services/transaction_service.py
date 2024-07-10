from DAL.category_repository import CategoryRepository
from DAL.transaction_repository import TransactionRepository
from DAL.wallet_repository import WalletRepository
from database import async_db_manager


class TransactionService:
    def __init__(self, account_id: int):
        self.account_id = account_id
        self.transaction_repository = TransactionRepository()

    async def add_transaction(
        self,
        amount: float,
        category_name: str,
        type_transaction: str,
        comment: str,
        wallet_name: str,
    ):
        async with async_db_manager.async_session_factory() as session:
            async with session.begin():

                wallet_repository = WalletRepository(self.account_id)
                wallet_id = await wallet_repository.get_wallet_id(session=session, wallet_name=wallet_name)

                category_repository = CategoryRepository()
                category_id = await category_repository.get_category_id(session=session, category_name=category_name)

                sum_update = amount if type_transaction == "income" else -amount

                await WalletRepository(self.account_id).update_wallet(
                    session=session, wallet_name=wallet_name, sum_update=sum_update
                )

                await self.transaction_repository.add_transaction(
                    session=session,
                    amount=amount,
                    category_id=category_id,
                    type_transaction=type_transaction,
                    comment=comment,
                    wallet_id=wallet_id,
                )

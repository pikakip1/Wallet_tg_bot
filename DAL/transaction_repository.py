import uuid

from db.models import Transaction
from sqlalchemy.ext.asyncio import AsyncSession


class TransactionRepository:

    async def add_transaction(
        self,
        session: AsyncSession,
        amount: float,
        category_id: uuid.UUID,
        type_transaction: str,
        comment: str,
        wallet_id: uuid.UUID,
    ):
        new_transaction = Transaction(
            amount=amount,
            comment=comment,
            type_transaction=type_transaction,
            wallet_id=wallet_id,
            category_id=category_id,
        )

        session.add(new_transaction)

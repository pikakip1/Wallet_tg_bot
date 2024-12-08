import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, BigInteger, CheckConstraint, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    wallets: Mapped[list["Wallet"]] = relationship(back_populates="account", cascade="all, delete-orphan")


class Wallet(Base):
    __tablename__ = "wallet"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_wallet: Mapped[str] = mapped_column(String(128), nullable=False)
    amount: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False, default=0.0)

    account_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("account.id", ondelete="CASCADE"))
    account: Mapped["Account"] = relationship(back_populates="wallets")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="wallet", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "category"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="category", cascade="all, delete-orphan")


class Transaction(Base):
    __tablename__ = "transaction"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    amount: Mapped[Numeric] = mapped_column(Numeric(10, 2), nullable=False)
    comment: Mapped[str] = mapped_column(String(512), nullable=True)
    date_transaction: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    type_transaction: Mapped[str] = mapped_column(String(16), nullable=False)

    wallet_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("wallet.id", ondelete="CASCADE"))
    category_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("category.id", ondelete="CASCADE"))

    wallet: Mapped["Wallet"] = relationship(back_populates="transactions")
    category: Mapped["Category"] = relationship(back_populates="transactions")

    __table_args__ = (CheckConstraint("type_transaction IN ('expense', 'income')"),)

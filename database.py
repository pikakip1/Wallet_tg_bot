from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session

from config import config


class AsyncDatabaseManager:
    def __init__(self):
        self.async_engine = create_async_engine(
            url=config.DATABASE_URL_asyncpg,
            echo=True,
        )
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine,
            expire_on_commit=False,
        )
        self.async_scoped_session = async_scoped_session(
            session_factory=self.async_session_factory,
            scopefunc=current_task,
        )

    async def get_session(self):
        async with self.async_scoped_session() as session:
            yield session
            await session.commit()
            await session.close()


async_db_manager = AsyncDatabaseManager()
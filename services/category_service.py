from DAL.category_repository import CategoryRepository
from database import async_db_manager


class CategoryService:
    def __init__(self):
        self.category_repository = CategoryRepository()

    async def get_all_categories(self) -> list[str]:
        async with async_db_manager.async_session_factory() as session:
            async with session.begin():
                categories = await self.category_repository.get_all_categories(session)
                return [category[0] for category in categories]

    async def add_category(self, category_name: str):
        async with async_db_manager.async_session_factory() as session:
            async with session.begin():
                await self.category_repository.add_category(session, category_name)

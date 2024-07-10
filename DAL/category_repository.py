from db.models import Category
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryRepository:

    async def get_category_id(self, session: AsyncSession, category_name: str):
        statement = select(Category).filter(Category.category_name == category_name)
        result = await session.execute(statement)
        category_id = result.scalar().id
        return category_id

    async def get_all_categories(self, session: AsyncSession):
        query = text("SELECT category_name FROM category")
        result = await session.execute(query)
        return result.fetchall()

    async def add_category(self, session: AsyncSession, category_name: str):
        new_category = Category(category_name=category_name)
        session.add(new_category)
        await session.commit()

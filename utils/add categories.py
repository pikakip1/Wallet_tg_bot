import asyncio

from database import async_db_manager
from db.models import Category


async def add_categories():
    async for session in async_db_manager.get_session():
        categories = [
            "Одежда",
            "Еда",
            "Транспорт",
            "Аптека",
            "Подписки",
            "Увлечение",
            "Разное",
            "Дом",
            "ЖКХ",
            "Кредитка",
            "Переводы",
            "Подарки",
            "Аренда",
            "Поесть на работе",
            "Кафешки",
            "ЗП",
        ]
        categories_obj = [Category(category_name=category) for category in categories]
        session.add_all(categories_obj)
        await session.commit()


def main():
    asyncio.run(add_categories())

if __name__ == '__main__':
    main()
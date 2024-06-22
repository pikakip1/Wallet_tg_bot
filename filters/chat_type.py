from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAllowedUserId(BaseFilter):
    def __init__(self, allowed_users_ids:  list):
        self.allowed_users_ids = allowed_users_ids

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.allowed_users_ids

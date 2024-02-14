from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from app.requests.admin_req import AdminRequest

class AdminInline():

    async def users():
        builder = InlineKeyboardBuilder()

        id_users = await AdminRequest.get_users()
        for item in id_users:
            print(item)
            builder.add(InlineKeyboardButton(text=item.username, callback_data=f'user_{item.tg_id}'))
        builder.adjust(1)

        return builder.as_markup()
    
    async def url_user(tg_id, username):
        builder = InlineKeyboardBuilder([
            [
                InlineKeyboardButton(text=username, url=f'tg://user?id={tg_id}'),
                InlineKeyboardButton(text='⬅️ Назад', callback_data='backward')
            ]
        ])
        return builder.adjust(1).as_markup()

class UserInline():

    async def url_user(tg_id, username):
        builder = InlineKeyboardBuilder([
            [
                InlineKeyboardButton(text=username, url=f'tg://user?id={tg_id}'),
            ]
        ])
        return builder.as_markup()
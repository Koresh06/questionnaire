from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardRemove, KeyboardButton


async def cancle():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='❌ Отмена'))

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

async def digit_kb(count):

    builder = ReplyKeyboardBuilder()
    for i in range(1, count + 1):
        builder.add(KeyboardButton(text=str(i)))
    builder.row(KeyboardButton(text='❌ Отмена'))

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

async def phone_user():
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='☎️ Отправить телефон', request_contact=True))

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


class AdminReply:

    async def kb_menu_admin():

        builder = ReplyKeyboardBuilder([
            [
                KeyboardButton(text='😎 Пользователи')
            ]
        ])

        return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
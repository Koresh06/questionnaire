from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from app.middlewares.middleware import Is_Admin
from app.keyboards.reply import AdminReply
from app.keyboards.inline import AdminInline
from app.requests.admin_req import AdminRequest
from app.fsm.fsm import NewLetter


admin = Router()

admin.message.middleware(Is_Admin())

@admin.message(Command('admin'))
async def cmd_admin(message: Message):
    await message.answer('Привет хозяин', reply_markup=await AdminReply.kb_menu_admin())


@admin.message(F.text.endswith('Пользователи'))
async def users(message: Message):
    await message.answer(text='Пользователи', reply_markup=await AdminInline.users())


@admin.callback_query(F.data == 'backward')
async def backward(callback: CallbackQuery):
    await callback.message.edit_text(text='Пользователи', reply_markup=await AdminInline.users())


@admin.callback_query(F.data.startswith('user'))
async def cmd_info_user(callback: CallbackQuery):
    tg_id = int(callback.data.split("_")[-1])
    info = await AdminRequest.info_user(tg_id)
    responses = info.data
    await callback.message.edit_text(text=f'🏙️ Город - {responses["town"]}\n😎 Имя - {responses["name"]}\n\nАвто - {responses["quest_one"]}\nРабота - {responses["quest_two"]}\nНавыки - {responses["quest_three"]}\nИнструмент - {responses["quest_four"]}\nМягкие окна - {responses["quest_five"]}\nЧерчение - {responses["quest_six"]}\n\n☎️ Телефон: <tg-spoiler>{responses["phone"]}</tg-spoiler>', reply_markup=await AdminInline.url_user(tg_id, info.username))


# @admin.message(Command(commands='cancel'), ~StateFilter(default_state))
# async def process_cancel_command_state(message: Message, state: FSMContext):
#     await message.answer(text='Отмена рассылки!', reply_markup=await AdminReply.kb_menu_admin())
#     await state.clear()


# @admin.message(F.text.endswith('Сделать рассылку'), StateFilter(default_state))
# async def cmd_distribution(message: Message, state: FSMContext):
#     await state.set_state(NewLetter.text)
#     await message.answer('Отправьте сообщение для рассылки!\n\n❌ Отмена - /cancel')


# @admin.message(NewLetter.text)
# async def cmd_message(message: Message, state: FSMContext):
#     await state.update_data(text=message.text)
#     await message.answer(f'<b><u>Проверьте текст РАССЫЛКИ</u></b>\n\n\n{message.text}\n\n\n❌ Отмена - /cancel', reply_markup=await AdminReply.result_distribution())
#     await state.set_state(NewLetter.result)


# @admin.message(F.text.endswith('Отправить'), NewLetter.result)
# async def cmd_send(message: Message, state: FSMContext):
#     users = await AdminRequest.get_users()
#     data = await state.get_data()
#     for item in users:
#         try:
#             await message.bot.send_message(chat_id=item.tg_id, text=data['text'])
#         except Exception as exxit:
#             print(exxit)
#     await message.answer('🔰 Рассылка завершена', reply_markup=await AdminReply.kb_menu_admin())
#     await state.clear()


# @admin.message(F.text.endswith('Отмена'), NewLetter.result)
# async def cmd_cancle_distribution(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer('Отмена рассылки!', reply_markup=await AdminReply.kb_menu_admin())
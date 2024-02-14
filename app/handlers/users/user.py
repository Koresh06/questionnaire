import config
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

from app.requests.user_req import UserRequests
from app.keyboards.inline import UserInline
from app.fsm.fsm import Question
from app.keyboards.reply import digit_kb, cancle, phone_user
from app.lexicon.lexicon import RESPONSES, TEXT, RESALT


router = Router()

@router.message(F.text.endswith('Отмена'), StateFilter(default_state))
async def process_cancel_command(message: Message, state: FSMContext):
    await message.answer(text='Вы не заполняете форму, поэтому невозможно воспользоваться данной командой!', reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(F.text.endswith('Отмена'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text='Чтобы пройти повторно анкетирование нажмите /start', reply_markup=ReplyKeyboardRemove())
    await state.clear()

@router.message(CommandStart(), StateFilter(default_state))
async def cmd_start(message: Message, state: FSMContext):
    user = await UserRequests.chek_user(message.from_user.id)
    if not user:
        await message.answer(text=TEXT['town'], reply_markup=await cancle())
        await state.set_state(Question.town)
    else:
        await message.answer('Вы уже прошли тестирование!')

@router.message(StateFilter(Question.town))
async def cmd_town(message: Message, state: FSMContext):
    await state.update_data(town=message.text)
    await message.answer(text=TEXT['name'], reply_markup= await cancle())
    await state.set_state(Question.name)

@router.message(StateFilter(Question.name))
async def cmd_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=TEXT[1], reply_markup=await digit_kb(len(RESPONSES['quest_one'])))
    await state.set_state(Question.quest_one)

@router.message(StateFilter(Question.quest_one))
async def cmd_question_one(message: Message, state: FSMContext):
    if int(message.text) == 2:
        await message.answer(text='Извините, наличие автомобиля основное условие. Нам очень жаль  но вы нам не подходите.')
        await state.clear()
    else:
        await state.update_data(quest_one=RESPONSES['quest_one'][int(message.text)])
        await message.answer(text=TEXT[2], reply_markup=await digit_kb(len(RESPONSES['quest_two'])))
        await state.set_state(Question.quest_two)


@router.message(StateFilter(Question.quest_two))
async def cmd_question_two(message: Message, state: FSMContext):
    if int(message.text) == 3:
        await message.answer(text='Мы не сможем обеспечить вас работой на постоянной основе. Мы предлагаем подработку.')
        await state.clear()
    else:
        await state.update_data(quest_two=RESPONSES['quest_two'][int(message.text)])
        await message.answer(text=TEXT[3], reply_markup=await digit_kb(len(RESPONSES['quest_three'])))
        await state.set_state(Question.quest_three)


@router.message(StateFilter(Question.quest_three))
async def cmd_question_three(message: Message, state: FSMContext):
    if int(message.text) == 3:
        await message.answer(text='Нам очень жаль  но вы нам не подходите.')
        await state.clear()
    else:
        await state.update_data(quest_three=RESPONSES['quest_three'][int(message.text)])
        await message.answer(text=TEXT[4], reply_markup=await digit_kb(len(RESPONSES['quest_four'])))
        await state.set_state(Question.quest_four)


@router.message(StateFilter(Question.quest_four))
async def cmd_question_four(message: Message, state: FSMContext):
    if int(message.text) == 3:
        await message.answer(text='Нам очень жаль  но вы нам не подходите.')
        await state.clear()
    else:
        await state.update_data(quest_four=RESPONSES['quest_four'][int(message.text)])
        await message.answer(text=TEXT[5], reply_markup=await digit_kb(len(RESPONSES['quest_five'])))
        await state.set_state(Question.quest_five)


@router.message(StateFilter(Question.quest_five))
async def cmd_question_five(message: Message, state: FSMContext):
    await state.update_data(quest_five=RESPONSES['quest_five'][int(message.text)])
    await message.answer(text=TEXT[6], reply_markup=await digit_kb(len(RESPONSES['quest_six'])))
    await state.set_state(Question.quest_six)


@router.message(StateFilter(Question.quest_six))
async def cmd_question_six(message: Message, state: FSMContext):
    await state.update_data(quest_six=RESPONSES['quest_six'][int(message.text)])
    await message.answer(text='Ваш номер телефона для связи', reply_markup=await phone_user())
    await state.set_state(Question.phone)

@router.message(StateFilter(Question.phone))
async def cmd_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    data = await state.get_data()
    if await UserRequests.save_responces(data, message.from_user.id, message.from_user.first_name):
        await message.answer(text=RESALT['text'], reply_markup=ReplyKeyboardRemove())
        await message.bot.send_message(chat_id=config.ADMIN_ID, text=f'Новый пользователь {message.from_user.first_name}\n\n🏙️ Город - {data["town"]}\n😎 Имя - {data["name"]}\n\nАвто - {data["quest_one"]}\nРабота - {data["quest_two"]}\nНавыки - {data["quest_three"]}\nИнструмент - {data["quest_four"]}\nМягкие окна - {data["quest_five"]}\nЧерчение - {data["quest_six"]}\n\n☎️ Телефон: {data["phone"]}', reply_markup=await UserInline.url_user(message.from_user.id, message.from_user.first_name))
        await state.clear()
    else: 
        await message.answer('Произошла ошибка, обратитесь к алминистратору!')
        await state.clear()
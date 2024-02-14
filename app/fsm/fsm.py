from aiogram.fsm.state import State, StatesGroup


class Question(StatesGroup):

    town = State()
    name = State()
    quest_one = State()
    quest_two = State()
    quest_three = State()
    quest_four = State()
    quest_five = State()
    quest_six = State()
    phone = State()

class NewLetter(StatesGroup):

    text = State()
    result = State()
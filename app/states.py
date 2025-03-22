from aiogram.fsm.state import State, StatesGroup


class Work(StatesGroup):
    text = State()
    photo = State()
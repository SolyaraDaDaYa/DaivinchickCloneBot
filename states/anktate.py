from aiogram.dispatcher.filters.state import StatesGroup, State

class Newanketa(StatesGroup):
    name = State()
    year = State()
    town = State()
    text = State()
    photo = State()
    confirm = State()
    change = State()
    change_text = State()

class Chat(StatesGroup):
    chatfirst = State()
    chat = State()
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Создать анкету"),
        ]
    ],
    resize_keyboard=True
)

menu2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Смотреть анкеты'),KeyboardButton(text='Меня лайкнули')
        ],
        [
            KeyboardButton(text='Моя анкета'),
        ]
    ],
    resize_keyboard=True
)

chatmenu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Прекратить чат'),
        ],
    ],
    resize_keyboard=True
)
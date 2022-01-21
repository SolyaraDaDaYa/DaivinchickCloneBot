from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="Да", callback_data="confirm")],
            [InlineKeyboardButton(text="Ввести описание заново", callback_data="change")],
        ]
    )

changeanketa = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="Изменить анкету", callback_data="anketachange")],
        ]
    )

changeanketa2 = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="Описание", callback_data="opisanie")],
            [InlineKeyboardButton(text="Всю анкету", callback_data="fullank")],
        ]
    )

viewanketa = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="👍🏿", callback_data="likeanketa"),
             InlineKeyboardButton(text="🤢", callback_data="skipanketa")],
        ]
    )

viewlikeanketa = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="Написать", callback_data="sendfirstmsg"),
             InlineKeyboardButton(text="🤢", callback_data="skiplikeanketa")],
        ],
    )

fromidcall = CallbackData('sendmsgto', 'fromuser')

# chatstartanketa = InlineKeyboardMarkup(
#         inline_keyboard=
#         [
#             [InlineKeyboardButton(text="Начать чат", callback_data=fromidcall.new()),
#              InlineKeyboardButton(text="🤢", callback_data="dissend")],
#         ],
#     )
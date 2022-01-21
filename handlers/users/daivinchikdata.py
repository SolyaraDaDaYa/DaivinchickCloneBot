from loader import dp,bot
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import CallbackQuery, Message, ContentType
from utils.db_api.database import DBCommands, Ankets, Users
from data.config import ADMINS
from keyboards.default import keymenu
from keyboards.inline import anketinline
from aiogram.dispatcher import FSMContext
from states.anktate import Newanketa



db = DBCommands()


@dp.message_handler(Command('start'))
async def register_user(message: Message):
    chat_id = message.from_user.id
    user = await db.add_new_user()
    id = user.user_id

    text = f"Приветствую вас!!\nТвой id => {id}"

    if message.from_user.id == ADMINS[0]:
        text += 'Ты админ'
    await bot.send_message(chat_id, text, reply_markup=keymenu.menu)

@dp.message_handler(Command('url'))
async def get_user_url(message: Message):
    url = await db.get_user_url(message.from_user.id)
    await message.answer(f'Твоя ссылка: {url}')

@dp.message_handler(commands=["cancel"], state=Newanketa)
async def cancel(message: Message, state: FSMContext):
    await message.answer("Вы отменили создание анкеты")
    await state.reset_state()


@dp.message_handler(Text('Создать анкету'))
async def create_anketa(message: Message, state: FSMContext):
    anketa = Ankets()
    anketa.anket_id = message.from_user.id
    await Newanketa.name.set()
    await state.update_data(anketa=anketa)
    await message.answer('Введите ваше имя или нажмите /cancel')

@dp.message_handler(state=Newanketa.name)
async def anketa_name(message: Message, state: FSMContext):
    name = message.text
    data = await state.get_data()
    anketa: Ankets = data.get("anketa")
    anketa.anket_name = name
    await Newanketa.year.set()
    await state.update_data(anketa=anketa)
    await message.answer('Введите ваш возраст или нажмите /cancel')

@dp.message_handler(state=Newanketa.year)
async def anketa_year(message: Message, state: FSMContext):
    data = await state.get_data()
    anketa: Ankets = data.get("anketa")

    try:
        year = int(message.text)
    except ValueError:
        await message.answer("Неверное значение, введите число")
        return

    anketa.anket_year = year
    await Newanketa.town.set()
    await state.update_data(anketa=anketa)
    await message.answer('Введите ваш город или нажмите /cancel')

@dp.message_handler(state=Newanketa.town)
async def anketa_town(message: Message, state: FSMContext):
    data = await state.get_data()
    anketa: Ankets = data.get("anketa")

    town = str(message.text).lower()
    anketa.anket_town = town

    await Newanketa.text.set()
    await state.update_data(anketa=anketa)
    await message.answer('Опишите себя или нажмите /cancel')

@dp.message_handler(state=Newanketa.text)
async def anketa_text(message: Message, state: FSMContext):
    data = await state.get_data()
    anketa: Ankets = data.get("anketa")

    text = message.text
    if len(text) <=850:
        anketa.anket_text = text
    else:
        await message.answer('Слишком много текста')
        return

    await Newanketa.photo.set()
    await state.update_data(anketa=anketa)
    await message.answer(f'Скинь фото для анкеты')

@dp.message_handler(state=Newanketa.photo, content_types=ContentType.PHOTO)
async def anketa_photo(message: Message, state: FSMContext):
    data = await state.get_data()
    anketa: Ankets = data.get("anketa")

    photo = message.photo[-1].file_id
    anketa.anket_photo = photo

    await Newanketa.confirm.set()
    await state.update_data(anketa=anketa)
    await message.answer_photo(
        caption=f'Ваша анкета\n\n{anketa.anket_name}, {anketa.anket_town}, {anketa.anket_year} лет\n\n{anketa.anket_text}\n\nПодтверждаете?',
        photo=photo,
        reply_markup=anketinline.markup
    )

@dp.callback_query_handler(text_contains="change", state=Newanketa.confirm)
async def enter_price(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Введите заново свое описание")
    await Newanketa.text.set()

@dp.callback_query_handler(text_contains="confirm", state=Newanketa.confirm)
async def enter_price(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    anketa: Ankets = data.get("anketa")
    await anketa.create()
    await call.message.answer("Анкета создана",reply_markup=keymenu.menu2)
    await state.reset_state()


@dp.message_handler(Text('Моя анкета'))
async def give_anketa(message: Message):
    user_id = message.from_user.id
    anketa = await db.get_anketa(user_id=user_id)
    await message.answer_photo(photo=anketa.anket_photo,
                               caption=f'<b>{anketa.anket_name}, {anketa.anket_town}, {anketa.anket_year} лет</b>\n\n{anketa.anket_text}',
                               reply_markup=anketinline.changeanketa)

@dp.callback_query_handler(text_contains='anketachange')
async def anketa_change(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    user_id = call.from_user.id
    anketa = await db.get_anketa(user_id=user_id)

    await Newanketa.change.set()
    await state.update_data(anketa=anketa)
    await call.message.answer('Что вы хотите изменить?', reply_markup=anketinline.changeanketa2)

@dp.callback_query_handler(text_contains='fullank', state=Newanketa.change)
async def anketa_change_full(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    anketa = data.get("anketa")

    await anketa.delete()
    await Newanketa.name.set()
    await call.message.answer('Введите ваше имя')

@dp.callback_query_handler(text_contains='opisanie', state=Newanketa.change)
async def anketa_change_opisan(call: CallbackQuery):
    await call.message.edit_reply_markup()
    await Newanketa.change_text.set()
    await call.message.answer('Введите описание')

@dp.message_handler(state=Newanketa.change_text)
async def anketa_change_op(message: Message, state: FSMContext):
    data = await state.get_data()
    anketa = data.get("anketa")

    text = message.text
    if len(text) <= 850:
        await anketa.update(anket_text=text).apply()
    else:
        await message.answer('Слишком много текста')
        return

    await anketa.update(anket_text=text).apply()
    await state.reset_state()
    await message.answer('Описание обновлено')



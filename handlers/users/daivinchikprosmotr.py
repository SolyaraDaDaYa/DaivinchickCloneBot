from loader import dp, bot
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message, ContentType
from utils.db_api.database import DBCommands
from keyboards.default import keymenu
from keyboards.inline import anketinline
from aiogram.dispatcher import FSMContext
from states.anktate import Chat
import random
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


db = DBCommands()

@dp.message_handler(Text('Смотреть анкеты'))
async def check_ankets(message: Message, state: FSMContext):
    user_id = message.from_user.id
    anketa = await db.get_anketa(user_id=user_id)

    town = anketa.anket_town

    likes = await db.get_liked(user_id=user_id)

    ankets = await db.get_town_ankets(town=town, user_id=user_id)
    try:
        randanket = random.choice(ankets)
        await message.answer(text='...', reply_markup=keymenu.ReplyKeyboardRemove())
        await message.answer_photo(photo=randanket.anket_photo,
                                   caption=f'<b>{randanket.anket_name}, {randanket.anket_town}, {randanket.anket_year} лет</b>\n\n{randanket.anket_text}',
                                   reply_markup=anketinline.viewanketa)

        await state.update_data(ankets=ankets, randanket=randanket, likes=likes)
    except:
        await message.answer(text='Анкет в твоем городе нету')

@dp.callback_query_handler(text='skipanketa')
async def skip_anketa(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    ankets = data.get("ankets")
    randanket = data.get("randanket")
    try:
        ankets.remove(randanket)
        randanket = random.choice(ankets)
        await call.message.answer_photo(photo=randanket.anket_photo,
                                        caption=f'<b>{randanket.anket_name}, {randanket.anket_town}, {randanket.anket_year} лет</b>\n\n{randanket.anket_text}',
                                        reply_markup=anketinline.viewanketa)

        await state.update_data(ankets=ankets, randanket=randanket)
    except:

        await call.message.answer('Анкеты закончились',reply_markup=keymenu.menu2)

    # if len(ankets) != 0:
    #     randanket = random.choice(ankets)
    #     await call.message.answer_photo(photo=randanket.anket_photo,
    #                                     caption=f'<b>{randanket.anket_name}, {randanket.anket_town}, {randanket.anket_year} лет</b>\n\n{randanket.anket_text}',
    #                                     reply_markup=anketinline.viewanketa)
    #
    #     await state.update_data(ankets=ankets)
    # else:
    #     await call.message.answer('Анкеты закончились',reply_markup=keymenu.menu2)


@dp.callback_query_handler(text='likeanketa')
async def like_anketa(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    ankets = data.get("ankets")
    randanket = data.get("randanket")
    likes = data.get('likes')
    user = call.from_user.id
    if randanket.anket_id not in likes:
        await db.add_like(user_id=user, anket_id=randanket.anket_id)

    try:
        ankets.remove(randanket)
        randanket = random.choice(ankets)
        await call.message.answer_photo(photo=randanket.anket_photo,
                                        caption=f'<b>{randanket.anket_name}, {randanket.anket_town}, {randanket.anket_year} лет</b>\n\n{randanket.anket_text}',
                                        reply_markup=anketinline.viewanketa)

        await state.update_data(ankets=ankets, randanket=randanket)
    except:
        await call.message.answer('Анкеты закончились',reply_markup=keymenu.menu2)


@dp.message_handler(Text('Меня лайкнули'))
async def who_like_ankets(message: Message, state: FSMContext):
    user_id = message.from_user.id
    dellist = []
    try:
        likedid = await db.get_who_liked(user_id=user_id)
        likeankets = await db.get_likeankets(users_id=likedid)
        randanlikeket = random.choice(likeankets)
        await message.answer(text='...', reply_markup=keymenu.ReplyKeyboardRemove())
        await message.answer_photo(photo=randanlikeket.anket_photo,
                                        caption=f'<b>{randanlikeket.anket_name}, {randanlikeket.anket_town}, {randanlikeket.anket_year} лет</b>\n\n{randanlikeket.anket_text}',
                                        reply_markup=anketinline.viewlikeanketa)

        await state.update_data(likeankets=likeankets, randanlikeket=randanlikeket, dellist=dellist)


    except:
        await message.answer('Вас никто не лайкал')



@dp.callback_query_handler(text='skiplikeanketa')
async def skip_like_anketa(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    likeankets = data.get('likeankets')
    randanlikeket = data.get('randanlikeket')
    dellist = data.get('dellist')
    dellist.append(randanlikeket.anket_id)
    try:
        likeankets.remove(randanlikeket)
        randanlikeket = random.choice(likeankets)
        await call.message.answer_photo(photo=randanlikeket.anket_photo,
                                   caption=f'<b>{randanlikeket.anket_name}, {randanlikeket.anket_town}, {randanlikeket.anket_year} лет</b>\n\n{randanlikeket.anket_text}',
                                   reply_markup=anketinline.viewlikeanketa)

        await state.update_data(likeankets=likeankets, randanlikeket=randanlikeket, dellist=dellist)

    except:
        user = call.from_user.id
        for anketa in dellist:
            await db.del_like_ankets(user_id=user,anket_id=anketa)
        await call.message.answer('Это все кто тебя лайкал', reply_markup=keymenu.menu2)
        await state.reset_data()


@dp.callback_query_handler(text='sendfirstmsg')
async def msg_to_anket(call: CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    user = call.from_user.id
    user_ank = await db.get_anketa(user_id=user)
    dellist = data.get('dellist')
    randanlikeket = data.get('randanlikeket')

    if len(dellist) != 0:
        for anketa in dellist:
            await db.del_like_ankets(user_id=user,anket_id=anketa)

    await call.message.answer('Напишите первое сообщение')
    await state.update_data(user_ank=user_ank, randanlikeket=randanlikeket)
    await Chat.chatfirst.set()


fromidcall = CallbackData('sendmsgto', 'fromuserid', 'fromusername', 'touserid', 'tousername')

fromidcalldecl = CallbackData('dissend', 'fromuserid', 'tousername')


@dp.message_handler(state=Chat.chatfirst)
async def send_firstmsg(message: Message, state: FSMContext):
    data = await state.get_data()
    fromuser_ank = data.get('user_ank')
    touser = data.get('randanlikeket')
    try:
        chatstartanketa = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [InlineKeyboardButton(text="Начать чат", callback_data=fromidcall.new(fromuserid=fromuser_ank.anket_id, fromusername=fromuser_ank.anket_name, touserid = touser.anket_id, tousername=touser.anket_name)),
                 InlineKeyboardButton(text="Отклонить", callback_data=fromidcalldecl.new(fromuserid=fromuser_ank.anket_id, tousername=touser.anket_name))],
            ],
        )

        username = fromuser_ank.anket_name
        text = message.text

        await bot.send_message(chat_id=touser.anket_id, text=f'<b>{username}</b>\n\n {text}', reply_markup=chatstartanketa)
        await message.answer('Сообщение отправлено', reply_markup=keymenu.menu2)
        await state.reset_state()
    except:
        print('ошибка в первом сообщении')
        await state.reset_state()
        await state.reset_data()

@dp.callback_query_handler(fromidcalldecl.filter())
async def decline_chat(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    fromuserid = int(callback_data['fromuserid'])
    tousername = callback_data['tousername']
    stat = dp.current_state(chat=fromuserid, user=fromuserid)
    await stat.reset_data()
    await bot.send_message(chat_id=fromuserid, text=f'{tousername} отклонил чат')
    await call.message.answer(f'Вы отклонили чат', reply_markup=keymenu.menu2)
    await state.reset_data()



@dp.callback_query_handler(fromidcall.filter())
async def set_chat(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.edit_reply_markup()
    fromuserid = int(callback_data['fromuserid'])
    fromusername = callback_data['fromusername']
    touserid = int(callback_data['touserid'])
    tousername = callback_data['tousername']


    stat = dp.current_state(chat=fromuserid, user=fromuserid)
    await stat.set_state(Chat.chat)
    await Chat.chat.set()

    await call.message.answer('Чат стартовал', reply_markup=keymenu.chatmenu)
    await bot.send_message(chat_id=fromuserid, text=f'{tousername} стартовал чат',reply_markup=keymenu.chatmenu)
    await state.reset_data()
    await stat.reset_data()
    await state.update_data(fromuserid=fromuserid, fromusername=fromusername, touserid = touserid, tousername=tousername)
    await stat.update_data(fromuserid=fromuserid, fromusername=fromusername, touserid = touserid, tousername=tousername)


@dp.message_handler(state=Chat.chat, text='Прекратить чат')
async def stop_chat(message: Message, state: FSMContext):
    data = await state.get_data()
    fromuserid = data.get('fromuserid')
    touserid = data.get('touserid')
    if message.from_user.id == fromuserid:
        await message.answer('Чат завершен',reply_markup=keymenu.menu2)
        await bot.send_message(chat_id=touserid, reply_markup=keymenu.menu2, text='Чат завершен')
        stat = dp.current_state(chat=touserid, user=touserid)
        await stat.reset_state()
        await stat.reset_data()
    elif message.from_user.id == touserid:
        await message.answer('Чат завершен', reply_markup=keymenu.menu2)
        await bot.send_message(chat_id=fromuserid, reply_markup=keymenu.menu2, text='Чат завершен')
        stat = dp.current_state(chat=fromuserid, user=fromuserid)
        await stat.reset_state()
        await stat.reset_data()


    await state.reset_state()
    await state.reset_data()


@dp.message_handler(state=Chat.chat)
async def do_chat(message: Message, state: FSMContext):
    text = message.text
    data = await state.get_data()
    fromuserid = data.get('fromuserid')
    fromusername = data.get('fromusername')
    touserid = data.get('touserid')
    tousername = data.get('tousername')


    if message.from_user.id == fromuserid:
        await bot.send_message(chat_id=touserid, text=f'<b>{fromusername}</b>\n\n {text}')
    elif message.from_user.id == touserid:
        await bot.send_message(chat_id=fromuserid, text=f'<b>{tousername}</b>\n\n {text}')


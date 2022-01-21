import asyncio, aiohttp
import time
from bs4 import BeautifulSoup
from loader import dp, bot
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
from utils.db_api.database import db, Item

async def add_item(**kwargs):
    await Item(**kwargs).create()

async def get_data(card):

    article = int(card.get('data-popup-nm-id'))
    brand = card.find(class_='brand-name').text.replace(' / ','').strip()
    try:
        price = int(card.find('span',class_='price-commission__current-price').text.replace(' ₽','').replace(' ','').strip())
    except:
        price = 0
    try:
        countotzivi = int(card.find('span',class_='product-card__count').text.strip())
    except:
        countotzivi = 0

    return article, brand, price, countotzivi

async def get_page_data(url,session):
    async with session.get(url=url) as resp:
        soup = BeautifulSoup(await resp.text(), 'lxml')
        cards = soup.find('div',class_='product-card-list').find_all('div',class_='product-card j-card-item')
        for card in cards:
            article,brand,price,countotzivi = await get_data(card)
            try:
                await add_item(article=article,brand=brand,price=price,countotzivi=countotzivi)
            except:
                pass

@dp.message_handler(Command('parse'))
async def mainrun(message: Message):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0',
        'Accept':'*/*'
    }
    starttime = time.time()
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        pag = 1
        for i in range(1,11):
            pages = i * 100
            await message.answer(f'Сделано {i*9}%')
            for page in range(pag,pages+1):
                url = f'https://www.wildberries.ru/catalog/muzhchinam/odezhda?sort=popular&page={page}'
                task = asyncio.create_task(get_page_data(url,session))
                tasks.append(task)
            await asyncio.gather(*tasks)
            pag = pages
    counts = await db.select([db.func.count()]).where(Item.article == Item.article).gino.scalar()
    await message.answer(f"Получено {counts} товаров\nВремя выполнения {int(time.time() - starttime)} сек.")


@dp.message_handler(Command("count"))
async def get_count(message: Message):
    counts = await db.select([db.func.count()]).where(Item.article == Item.article).gino.scalar()
    await message.answer(f"Всего в бд {counts} товаров")

@dp.message_handler(Command('botlink'))
async def get_bot_link(message: Message):
    bot_username = (await bot.me).username
    bot_link = f"https://t.me/{bot_username}"
    await message.answer(f'Сылка на бота:\n{bot_link}')
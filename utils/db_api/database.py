from gino import Gino
from gino.schema import GinoSchemaVisitor
from data.config import POSTGRES_URI
from aiogram import types
from sqlalchemy import (Column, Integer, String, BigInteger)
from sqlalchemy import sql

db = Gino()

# Создаем класс таблицы товаров
class Item(db.Model):
    __tablename__ = 'items'
    query: sql.Select

    article = Column(Integer, primary_key=True, unique=True)
    brand = Column(String)
    price = Column(Integer)
    countotzivi = Column(Integer)

    def __repr__(self):
        return f"""
        Товар № {self.article} - "{self.brand}"
        Цена: {self.price}"""

class Ankets(db.Model):
    __tablename__ = 'Ankets'
    query: sql.Select

    id = Column(Integer, primary_key=True, unique=True)
    anket_id = Column(BigInteger, unique=True)
    anket_name = Column(String)
    anket_year = Column(Integer)
    anket_town = Column(String)
    anket_text = Column(String(1000))
    anket_photo = Column(String(250))

class Anketslikes(db.Model):
    __tablename__ = 'Anketslikes'
    query: sql.Select

    id = Column(Integer, primary_key=True, unique=True)
    user_anket_id = Column(BigInteger)
    who_like_id = Column(BigInteger)


class Users(db.Model):
    __tablename__ = 'Users'
    query: sql.Select

    id = Column(Integer, primary_key=True, unique=True)
    user_id = Column(BigInteger, unique=True)
    username = Column(String)
    full_name = Column(String)
    user_link = Column(String)

# Документация
# http://gino.fantix.pro/en/latest/tutorials/tutorial.html

async def create_db():
    # Устанавливаем связь с базой данных
    await db.set_bind(POSTGRES_URI)
    db.gino: GinoSchemaVisitor

    # Создаем таблицы
    #await db.gino.drop_all()
    await db.gino.create_all()

class DBCommands:
    db.gino: GinoSchemaVisitor
    async def get_user(self, user_id):
        user = await Users.query.where(Users.user_id == user_id).gino.first()
        return user

    async def add_new_user(self):
        user = types.User.get_current()
        old_user = await self.get_user(user.id)
        if old_user:
            return old_user
        new_user = Users()
        new_user.user_id = user.id
        new_user.username = user.username
        new_user.full_name = user.full_name
        new_user.user_link = user.url

        await new_user.create()
        return new_user

    async def get_user_url(self, anketa_id):
        user = await Users.query.where(Users.user_id == anketa_id).gino.first()
        return user.user_link

    async def get_anketa(self, user_id):
        anketa = await Ankets.query.where(Ankets.anket_id == user_id).gino.first()
        return anketa

    async def get_town_ankets(self, town, user_id):
        ankets = await Ankets.query.where(Ankets.anket_id != user_id).where(Ankets.anket_town == town).gino.all()
        return ankets

    async def add_like(self, user_id, anket_id):
        like = Anketslikes()
        like.user_anket_id = anket_id
        like.who_like_id = user_id
        await like.create()
        return like

    async def get_liked(self, user_id):
        likes = await Anketslikes.query.where(Anketslikes.who_like_id == user_id).gino.all()
        likeslist = [like.user_anket_id for like in likes]
        return likeslist

    async def get_who_liked(self, user_id):
        liked = await Anketslikes.query.where(Anketslikes.user_anket_id == user_id).gino.all()
        likedlist = [like.who_like_id for like in liked]
        return likedlist

    async def get_likeankets(self, users_id):
        liked = [await self.get_anketa(user_id=user_id) for user_id in users_id]
        return liked

    async def del_like_ankets(self, user_id, anket_id):
        delik = await Anketslikes.query.where(Anketslikes.user_anket_id == user_id).where(Anketslikes.who_like_id == anket_id).gino.first()
        await delik.delete()
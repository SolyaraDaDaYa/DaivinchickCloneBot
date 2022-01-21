# from sqlalchemy import (Column, Integer, String)
# from sqlalchemy import sql
# from utils.db_api.database import db
#
#
#
# # Создаем класс таблицы товаров
# class Item(db.Model):
#     __tablename__ = 'items'
#     query: sql.Select
#
#     article = Column(Integer, primary_key=True, unique=True)
#     brand = Column(String)
#     price = Column(Integer)
#     countotzivi = Column(Integer)
#
#     def __repr__(self):
#         return f"""
#         Товар № {self.article} - "{self.brand}"
#         Цена: {self.price}"""
#
# class Ankets(db.Model):
#     __tablename__ = 'Ankets'
#     query: sql.Select
#
#     id = Column(Integer, primary_key=True, unique=True)
#     anket_id = Column(Integer)
#     anket_name = Column(String)
#     anket_year = Column(Integer)
#     anket_town = Column(String)
#     anket_text = Column(String)
#     likes = Column(Integer)
#     like_ids = Column(String)
#
# class Users(db.Model):
#     __tablename__ = 'Users'
#     query: sql.Select
#
#     id = Column(Integer, primary_key=True, unique=True)
#     user_id = Column(Integer)
#     username = Column(String)
#     full_name =  Column(String)

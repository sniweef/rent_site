__author__ = 'hzhigeng'

from mongoengine import *


class User(Document):
    nickname = StringField(required=True, unique=True, max_length=50)
    callname = StringField(required=True, max_length=50)
    phone = LongField()
    email = EmailField()
    wechat = StringField(max_length=50)
    qq = LongField()


class RentShop(Document):
    _id = IntField(required=True, unique=True, primary_key=True)
    title = StringField(max_length=50)
    locale = StringField(max_length=50)
    building = StringField(max_length=40)
    price = IntField()
    pictures = ListField(URLField())
    detail = StringField(max_length=300)
    contacter = ReferenceField(User)


class WantedShop(Document):
    _id = IntField(required=True, unique=True, primary_key=True)
    title = StringField(max_length=50)
    detail = StringField(max_length=300)
    contacter = ReferenceField(User)


if __name__ == '__main__':
    connect('rent_shop', username='hzhigeng', password='afb74lgv76')
    user = User(nickname='acb', callname='Mr. Li', phone='12345678')
    user.save()

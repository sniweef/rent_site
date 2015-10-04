import bson
from mongoengine import *

__author__ = 'hzhigeng'


class User(Document):
    nickname = StringField(required=True, unique=True, max_length=50)
    callname = StringField(max_length=50)
    phone = StringField(max_length=50)
    email = EmailField(max_length=50)
    wechat = StringField(max_length=50)
    qq = LongField()


class CustomToJsonDoc(Document):
    def to_json(self):
        data = self.to_mongo()
        data['_id'] = str(data['_id'])
        data['contacter'] = {
            'callname': self.contacter.callname,
            'phone': self.contacter.phone,
            'email': self.contacter.email,
            'wechat': self.contacter.wechat,
            'qq': self.contacter.qq
        }
        return bson.json_util.dumps(data)


class RentShop(Document):
    title = StringField(max_length=50)
    locale = StringField(max_length=50)
    building = StringField(max_length=50)
    price = IntField()
    pictures = ListField(URLField(max_length=100))
    detail = StringField(max_length=300)
    contacter = ReferenceField(User, reverse_delete_rule=CASCADE)

    def to_json(self):
        data = self.to_mongo()
        data['_id'] = str(data['_id'])
        data['contacter'] = {
            'callname': self.contacter.callname,
            'phone': self.contacter.phone,
            'email': self.contacter.email,
            'wechat': self.contacter.wechat,
            'qq': self.contacter.qq
        }
        return bson.json_util.dumps(data)


class WantedShop(Document):
    title = StringField(max_length=50)
    detail = StringField(max_length=300)
    contacter = ReferenceField(User, reverse_delete_rule=CASCADE)

    def to_json(self):
        data = self.to_mongo()
        data['_id'] = str(data['_id'])
        data['contacter'] = {
            'callname': self.contacter.callname,
            'phone': self.contacter.phone,
            'email': self.contacter.email,
            'wechat': self.contacter.wechat,
            'qq': self.contacter.qq
        }
        return bson.json_util.dumps(data)

if __name__ == '__main__':
    from bson.objectid import ObjectId
    connect('rent_shop')
    user = User(nickname=str(ObjectId()), callname='Mr. Li', phone='12345678')
    user.save()
    rent_shop = RentShop(title='asdf', locale='afsdf', price=123456, contacter=user)
    rent_shop.save()

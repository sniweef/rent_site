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
    status = IntField()


class Shop(EmbeddedDocument):
    shop_number = StringField(max_length=10)
    area = FloatField()
    price = StringField(max_length=10)
    project_condition = StringField(max_length=50)
    others = StringField(max_length=50)  # including potential tenants

    def __str__(self):
        return 'shop_number:%s\narea:%d\nprice:%d\nproject_condition:%s\nothers:%s\n' % (self.shop_number, self.area,
                                                                                         self.price,
                                                                                         self.project_condition,
                                                                                         self.others)


class RentProject(Document):
    # create_time = DateTimeField()
    is_approved = BooleanField()
    is_sell = BooleanField()
    pictures = ListField(URLField(max_length=100))
    brochure = URLField(max_length=100)
    project_name = StringField(required=True, max_length=50)
    project_type = StringField(required=True, max_length=10)
    position = StringField(max_length=50)
    address = StringField(required=True, max_length=50)
    contacter = StringField(max_length=50)
    phone = StringField(max_length=50)
    shops_info = ListField(EmbeddedDocumentField(Shop))
    shops_price = ListField(StringField(max_length=10))
    shops_area = ListField(FloatField())
    shops_investment = ListField(StringField(max_length=50))


class WantedShop(Document):
    # create_time = DateTimeField()
    is_approved = BooleanField()
    is_buy = BooleanField()
    wanter_type = StringField(max_length=10)
    intention_type = StringField(max_length=10)
    business_type = StringField(max_length=10)
    brand_name = StringField(max_length=10)
    area = FloatField()
    intention_price = StringField(max_length=10)
    project_demand = StringField(max_length=50)
    contacter = StringField(min_length=1, max_length=50)
    phone = StringField(min_length=1, max_length=50)
    # title = StringField(max_length=50)
    # detail = StringField(max_length=300)
    # contacter = ReferenceField(User, reverse_delete_rule=CASCADE)


if __name__ == '__main__':
    from bson.objectid import ObjectId
    connect('rent_shop')
    user = User(nickname=str(ObjectId()), callname='Mr. Li', phone='12345678')
    user.save()
    rent_shop = RentProject(title='asdf', locale='afsdf', price=123456, contacter=user)
    rent_shop.save()

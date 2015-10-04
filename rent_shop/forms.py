from wtforms import Form, StringField, IntegerField, FieldList
from wtforms.validators import *

__author__ = 'hzhigeng'


class PublishShopForm(Form):
    title = StringField('title', validators=[Length(min=4, max=50)])
    locale = StringField('locale', validators=[Length(min=2, max=50)])
    building = StringField('building', validators=[Length(max=50)])
    price = IntegerField('price')
    pictures = FieldList(StringField(validators=[URL()]))
    detail = StringField('detail', validators=[Length(min=10, max=300)])
    contacter = StringField('contacter', validators=[Length(min=2, max=50)])
    phone = StringField('phone', validators=[Length(min=5, max=50)])
    email = StringField('email', validators=[Email()])
    wechat = StringField('wechat', validators=[Length(max=50)])
    qq = IntegerField('qq')

    def __str__(self):
        return 'Title: ' + self.title.data + '\nLocale: ' + self.locale.data + '\nPrice: ' + str(self.price.data) + \
               '\nPictures: ' + str(self.pictures.data) + '\nDetail: ' + self.detail.data + '\nContacter: ' + \
               self.contacter.data + '\nPhone: ' + self.phone.data + '\nEmail: ' + self.email.data + '\nWechat: ' + \
               self.wechat.data + '\nQQ: ' + str(self.qq.data)

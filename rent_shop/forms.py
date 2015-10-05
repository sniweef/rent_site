from wtforms import Form, StringField, IntegerField, FieldList
from wtforms.validators import *

__author__ = 'hzhigeng'


class ObjectIdValidator(Regexp):
    """
    Validates a ObjectId.

    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, message=None):
        pattern = r'^[0-9a-fA-F]{24}'
        super(ObjectIdValidator, self).__init__(pattern, message=message)

    def __call__(self, form, field):
        if not field.data:
            return True

        message = self.message
        if message is None:
            message = field.gettext('Invalid ObjectId.')

        super(ObjectIdValidator, self).__call__(form, field, message)


class EmailOrEmpty(Email):
    def __call__(self, form, field):
        if not field.data:
            return True
        return super(EmailOrEmpty, self).__call__(form, field)


class PublishRentForm(Form):
    id = StringField('title', validators=[ObjectIdValidator()])
    title = StringField('title', validators=[Length(min=4, max=50)])
    locale = StringField('locale', validators=[Length(min=2, max=50)])
    building = StringField('building', validators=[Length(max=50)])
    price = IntegerField('price')
    pictures = FieldList(StringField(validators=[URL()]))
    detail = StringField('detail', validators=[Length(min=10, max=300)])
    contacter = StringField('contacter', validators=[Length(min=2, max=50)])
    phone = StringField('phone', validators=[Length(min=5, max=50)])
    email = StringField('email', validators=[EmailOrEmpty()])
    wechat = StringField('wechat', validators=[Length(max=50)])
    qq = IntegerField('qq')

    def __str__(self):
        return 'Title: ' + self.title.data + '\nLocale: ' + self.locale.data + '\nPrice: ' + str(self.price.data) + \
               '\nPictures: ' + str(self.pictures.data) + '\nDetail: ' + self.detail.data + '\nContacter: ' + \
               self.contacter.data + '\nPhone: ' + self.phone.data + '\nEmail: ' + self.email.data + '\nWechat: ' + \
               self.wechat.data + '\nQQ: ' + str(self.qq.data)


class PublishWantedForm(Form):
    id = StringField('title', validators=[ObjectIdValidator()])
    title = StringField('title', validators=[Length(min=4, max=50)])
    detail = StringField('detail', validators=[Length(min=10, max=300)])
    contacter = StringField('contacter', validators=[Length(min=2, max=50)])
    phone = StringField('phone', validators=[Length(min=5, max=50)])
    email = StringField('email', validators=[EmailOrEmpty()])
    wechat = StringField('wechat', validators=[Length(max=50)])
    qq = IntegerField('qq')

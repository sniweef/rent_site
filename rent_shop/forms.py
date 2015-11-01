from wtforms import Form, StringField, IntegerField, FieldList, FormField, BooleanField
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


class URLOrEmpty(URL):
    def __call__(self, form, field):
        if not field.data:
            return True
        return super(URLOrEmpty, self).__call__(form, field)


class ShopForm(Form):
    shop_number = StringField('shop_number', validators=[Length(min=1, max=10)])
    area = IntegerField('area')
    price = IntegerField('price')
    project_condition = StringField('project_condition', validators=[Length(max=100)])
    others = StringField('others', validators=[Length(max=100)])


class PublishRentForm(Form):
    id = StringField('id', validators=[ObjectIdValidator()])
    is_sell = BooleanField('is_sell', validators=[DataRequired()])
    project_name = StringField('project_name', validators=[Length(min=1, max=50)])
    project_type = IntegerField('project_type', validators=[DataRequired()])
    position = StringField('position', validators=[Length(max=50)])
    address = StringField('locale', validators=[Length(min=1, max=50), DataRequired()])
    brochure = StringField('brochure', validators=[URLOrEmpty()])
    pictures = FieldList(StringField(validators=[URL()]), max_entries=3)
    contacter = StringField('contacter', validators=[Length(min=1, max=50), DataRequired()])
    phone = StringField('phone', validators=[Length(min=1, max=50), DataRequired()])
    shops_info = FieldList(FormField(ShopForm), label='shops_info', validators=[DataRequired()])

    def __str__(self):
        return ''
        #return 'Title: ' + self.project_name.data + '\nLocale: ' + self.address.data + \
        #       '\nPictures: ' + str(self.resources.data) + '\nDetail: ' + self.detail.data + '\nContacter: ' + \
        #       self.contacter.data + '\nPhone: ' + self.phone.data + '\nEmail: ' + self.email.data + '\nWechat: ' + \
        #       self.wechat.data + '\nQQ: ' + str(self.qq.data)


class PublishWantedForm(Form):
    id = StringField('id', validators=[ObjectIdValidator()])
    is_buy = BooleanField('is_buy', validators=[DataRequired()])
    wanter_type = StringField('wanter_type', validators=[DataRequired()])
    intention_type = StringField('intention_type', validators=[DataRequired()])
    business_type = StringField('business_type', validators=[DataRequired()])
    brand_name = StringField('brand_name', validators=[Length(max=10)])
    area = IntegerField(validators=[DataRequired()])
    intention_price = IntegerField()
    project_demand = StringField('project_demand', validators=[Length(max=50)])
    contacter = StringField('contacter', validators=[Length(min=1, max=50), DataRequired()])
    phone = StringField('phone', validators=[Length(min=1, max=50), DataRequired()])

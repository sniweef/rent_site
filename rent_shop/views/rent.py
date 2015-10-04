from mongoengine.errors import ValidationError, InvalidQueryError
from flask import request, abort
from flask import Blueprint, render_template
from mongoengine import *
from bson.objectid import ObjectId
from rent_shop.models.models import *
from rent_shop.forms import *

__author__ = 'hzhigeng'


rent = Blueprint('rent', __name__, url_prefix='/rent')


@rent.route('/search')
def search_rent():
    try:
        key = request.args.get('key', '')
        from_idx = int(request.args.get('from', 0))
    except ValueError:
        from_idx = 0

    return key + str(from_idx)


@rent.route('/view/<rent_shop_id>')
def view_rent(rent_shop_id):
    try:
        return RentShop.objects(id=rent_shop_id).first().to_json()
    except (ValidationError, InvalidQueryError):
        return '{}'


def search_user(form):
    user = User.objects(Q(phone=form.phone.data) | Q(email=form.email.data) | Q(wechat=form.wechat.data) |
                        Q(qq=form.qq.data)).first()
    if not user:
        user = User(nickname=str(ObjectId()))
    return user


@rent.route('/publish', methods=['GET', 'POST'])
def publish_rent():
    if request.method == 'GET':
        return render_template('publish_rent.html')

    form = PublishShopForm(request.form)
    print form
    if form.validate():
        user = search_user(form)
        user.callname = form.contacter.data
        user.phone = form.phone.data
        user.email = form.email.data
        user.wechat = form.wechat.data
        user.qq = form.qq.data
        user.save()

        shop = RentShop(title=form.title.data, locale=form.locale.data, price=form.price.data, pictures=form.pictures.data,
                        detail=form.detail.data, contacter=user)
        shop.save()
        return 'OK'

    for name, error in form.errors.iteritems():
        err_msg = "'%s': %s" %(name, str(error[0]))
        break  # we only need first error message

    return err_msg, 400


@rent.route('/delete/<rent_shop_id>')
def delete_rent(rent_shop_id):
    pass


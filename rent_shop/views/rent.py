from mongoengine.errors import ValidationError, InvalidQueryError
from flask import request, abort
from flask import Blueprint
from rent_shop.models.models import *

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


@rent.route('/publish', methods=['POST'])
def publish_rent():
    return 'publish'


@rent.route('/delete/<rent_shop_id>')
def delete_rent(rent_shop_id):
    pass


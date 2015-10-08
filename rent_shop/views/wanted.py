from datetime import datetime
from flask import Blueprint, request, abort
from mongoengine import Q
from mongoengine.errors import ValidationError, InvalidQueryError
from rent_shop.models import WantedShop, User
from rent_shop.forms import PublishWantedForm

__author__ = 'hzhigeng'


wanted = Blueprint('wanted', __name__, url_prefix='/wanted')


@wanted.route('/search')
def search_wanted():
    try:
        key = request.args.get('key', '')
        from_idx = int(request.args.get('from', 0))
    except ValueError:
        from_idx = 0

    key = key.strip()
    keys = key.split(' ')

    q_expr = Q(is_approved=True) & Q(project_demand__icontains=keys[0])
    for i in range(1, len(keys)):
        q_expr = q_expr & Q(project_demand__icontains=keys[i])

    query_result = WantedShop.objects(q_expr).order_by('-create_time').\
        only('id', 'is_buy', 'wanter_type', 'intention_type', 'business_type', 'brand_name', 'area').\
        skip(from_idx).limit(10)

    return query_result.to_json()


@wanted.route('/view/<wanted_shop_id>')
def view_wanted(wanted_shop_id):
    try:
        return WantedShop.objects(id=wanted_shop_id).first().to_json()
    except (ValidationError, AttributeError):
        return '{}'


@wanted.route('/publish', methods=['POST'])
def publish_wanted():
    form = PublishWantedForm(request.form)
    if form.validate():
        if form.id.data:
            shop = WantedShop.objects(id=form.id.data).first()
            if not shop:
                return 'Cannot find the specific shop with id %s' % form.id.data, 404
        else:
            shop = WantedShop()
            shop.create_time = datetime.now()

        shop.is_approved = False
        shop.is_buy = form.is_buy.data
        shop.wanter_type = form.wanter_type.data
        shop.intention_type = form.intention_type.data
        shop.business_type = form.business_type.data
        shop.brand_name = form.brand_name.data
        shop.area = form.area.data
        shop.intention_price = form.intention_price.data
        shop.project_demand = form.project_demand.data
        shop.contacter = form.contacter.data
        shop.phone = form.phone.data

        shop.save()
        return str(shop.id)

    err_msg = ''
    for name, error in form.errors.iteritems():
        err_msg = "'%s': %s" % (name, str(error[0]))
        break  # we only need first error message

    return err_msg, 400


@wanted.route('/delete/<wanted_shop_id>')
def delete_wanted(wanted_shop_id):
    try:
        if WantedShop.objects(id=wanted_shop_id).delete():
            return 'OK'
        else:
            abort(404)
    except (ValidationError, AttributeError):
        abort(404)


@wanted.route('/approve/<wanted_shop_id>')
def approve_wanted(wanted_shop_id):
    try:
        wanted_shop = WantedShop.objects(id=wanted_shop_id).first()
        wanted_shop.is_approved = True
        wanted_shop.save()
        return 'OK'
    except (ValidationError, AttributeError):
        abort(404)

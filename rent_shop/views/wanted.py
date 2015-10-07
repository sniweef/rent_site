from flask import Blueprint, request, abort
from mongoengine import Q
from mongoengine.errors import ValidationError, InvalidQueryError
from rent_shop.models import WantedShop, User
from rent_shop.views.rent import get_or_create_user
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

    q_expr = Q(address__icontains=keys[0])
    for i in range(1, len(keys)):
        q_expr = q_expr & Q(address__icontains=keys[i])

    query_result = WantedShop.objects(q_expr).only('id', 'project_name', 'contacter').skip(from_idx).limit(10)

    return query_result.to_json()


@wanted.route('/view/<wanted_shop_id>')
def view_wanted(wanted_shop_id):
    try:
        return WantedShop.objects(id=wanted_shop_id).first().to_json()
    except (ValidationError, InvalidQueryError):
        return '{}'


@wanted.route('/publish', methods=['POST'])
def publish_wanted():
    form = PublishWantedForm(request.form)
    if form.validate():
        user = get_or_create_user(form)
        user.callname = form.contacter.data
        user.phone = form.phone.data
        # Note: Setting email to empty string will cause ValidationError
        user.email = form.email.data if form.email.data else None
        user.wechat = form.wechat.data
        user.qq = form.qq.data
        user.save()

        if form.id.data:
            shop = WantedShop.objects(id=form.id.data).first()
            if not shop:
                return 'Cannot find the specific shop with id %s' % form.id.data, 404
        else:
            shop = WantedShop()

        shop.address = form.project_name.data
        shop.detail = form.detail.data
        shop.contacter = user

        shop.save()
        return 'OK'

    err_msg = ''
    for name, error in form.errors.iteritems():
        err_msg = "'%s': %s" % (name, str(error[0]))
        break  # we only need first error message

    return err_msg, 400


@wanted.route('/delete/<wanted_shop_id>')
def delete_rent(wanted_shop_id):
    try:
        if WantedShop.objects(id=wanted_shop_id).delete():
            return 'OK'
        else:
            abort(404)
    except (ValidationError, InvalidQueryError):
        abort(404)

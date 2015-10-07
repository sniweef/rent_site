from flask import request, abort
from flask import Blueprint, render_template
from mongoengine import Q
from mongoengine.errors import ValidationError, InvalidQueryError
from bson.objectid import ObjectId
from rent_shop.forms import *
from rent_shop.models import RentProject, Shop

__author__ = 'hzhigeng'

rent = Blueprint('rent', __name__, url_prefix='/rent')


@rent.route('/search')
def search_rent():
    try:
        key = request.args.get('key', '')
        from_idx = int(request.args.get('from', 0))
    except ValueError:
        from_idx = 0

    key = key.strip()
    keys = key.split(' ')
    q_expr = Q(is_approved=True)

    if len(keys) > 1:
        q_expr = q_expr & Q(project_name__icontains=keys[1])
        for i in range(2, len(keys)):
            q_expr = q_expr & Q(project_name__icontains=keys[i])
        query_result = RentProject.objects(Q(address__icontains=keys[0]) & q_expr)
        if not query_result:
            query_result = RentProject.objects(Q(project_name__icontains=keys[0]) & q_expr)
    else:
        query_result = RentProject.objects(q_expr & Q(project_name__icontains=key))
        if not query_result:
            query_result = RentProject.objects(q_expr & Q(address__icontains=key))

    return query_result.only('id', 'project_name', 'address', 'shops_price', 'shops_area', 'shops_others').\
        skip(from_idx).limit(10).to_json()


@rent.route('/view/<rent_project_id>')
def view_rent(rent_project_id):
    try:
        return RentProject.objects(id=rent_project_id).first().to_json()
    except (ValidationError, InvalidQueryError):
        return '{}'


def get_or_create_user(form):
    user = User.objects(Q(phone=form.phone.data)).first()
    if not user:
        user = User(nickname=str(ObjectId()))
    return user


@rent.route('/publish', methods=['GET', 'POST'])
def publish_rent():
    if request.method == 'GET':
        return render_template('publish_rent.html')

    form = PublishRentForm(request.form)
    #print form
    if form.validate():
        # user = get_or_create_user(form)
        # user.callname = form.contacter.data
        # user.phone = form.phone.data
        # Note: Setting email to empty string will cause ValidationError
        # user.email = form.email.data if form.email.data else None
        # user.wechat = form.wechat.data
        # user.qq = form.qq.data
        # user.save()

        if form.id.data:
            rent_project = RentProject.objects(id=form.id.data).first()
            if not rent_project:
                return 'Cannot find the specific rent_project with id %s' % form.id.data, 404
        else:
            rent_project = RentProject()

        rent_project.is_approved = False
        rent_project.is_sold = form.is_sold.data
        rent_project.pictures = form.pictures.data
        # url must be None instead of empty string because empty string will cause ValidationError: Not a valid url
        rent_project.brochure = form.brochure.data if form.brochure.data else None
        rent_project.project_name = form.project_name.data
        rent_project.project_type = form.project_type.data
        rent_project.position = form.position.data
        rent_project.address = form.address.data
        rent_project.contacter = form.contacter.data
        rent_project.phone = form.phone.data

        for shop_info in form.shops_info.data:
            new_shop = Shop(shop_number=shop_info['shop_number'], area=shop_info['area'], price=shop_info['price'],
                            project_condition=shop_info['project_condition'], others=shop_info['others'])
            rent_project.shops_info.append(new_shop)
            rent_project.shops_price.append(new_shop.price)
            rent_project.shops_area.append(new_shop.area)
            rent_project.shops_others.append(new_shop.others)

        rent_project.save()
        return 'OK'

    err_msg = ''
    for name, error in form.errors.iteritems():
        err_msg = "'%s': %s" % (name, str(error[0]))
        break  # we only need first error message

    return err_msg, 400


@rent.route('/delete/<rent_project_id>')
def delete_rent(rent_project_id):
    try:
        if RentProject.objects(id=rent_project_id).delete():
            return 'OK'
        else:
            abort(404)
    except ValidationError, InvalidQueryError:
        abort(404)


@rent.route('/approve/<rent_project_id>')
def approve_rent(rent_project_id):
    try:
        rent_project = RentProject.objects(id=rent_project_id).first()
        rent_project.is_approved = True
        rent_project.save()
        return 'OK'
    except (ValidationError, InvalidQueryError):
        abort(404)

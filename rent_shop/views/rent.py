# -*- coding: utf-8

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
        min_area = int(request.args.get('min_area', 0))
        max_area = int(request.args.get('max_area', 0))
        min_price = int(request.args.get('min_price', 0))
        max_price = int(request.args.get('max_price', 0))
        order_by = int(request.args.get('order_by', 0))  # 0:time, 1:price, 2:area
        incr = int(request.args.get('incr', 0))
        investment = request.args.get('invest', '')
        if investment == '其它':
            investment = ''
    except ValueError:
        abort(400)

    key = key.strip()
    keys = key.split(' ')
    q_expr = Q(is_approved=True)

    if max_area > 0 and max_area > min_area:
        q_expr = q_expr & Q(shops_area__gte=min_area, shops_area__lte=max_area)
    elif max_area == 0 and min_area > 0:
        q_expr = q_expr & Q(shops_area__gte=min_area)

    if max_price > 0 and max_price > min_price:
        print max_price, ':', min_price
        q_expr = q_expr & Q(shops_price__gte=min_price, shops_price__lte=max_price)
    elif max_price == 0 and min_price > 0:
        q_expr = q_expr & Q(shops_price__gte=min_price)

    try:
        order_keyword = ['id', 'shops_price', 'shops_area'][order_by]
    except IndexError:
        abort(400)

    if not incr:
        order_keyword = '-' + order_keyword

    if investment:
        q_expr = q_expr & Q(shops_investment=investment)

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

    return query_result.only('id', 'project_name', 'address', 'shops_price', 'shops_area', 'shops_investment').\
        order_by(order_keyword).skip(from_idx).limit(10).to_json()


@rent.route('/view/<rent_project_id>')
def view_rent(rent_project_id):
    try:
        return RentProject.objects(id=rent_project_id).first().to_json()
    except (ValidationError, AttributeError):
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
        if form.id.data:
            rent_project = RentProject.objects(id=form.id.data).first()
            if not rent_project:
                return 'Cannot find the specific rent_project with id %s' % form.id.data, 404
        else:
            rent_project = RentProject()
            # rent_project.create_time = datetime.now()

        rent_project.is_approved = False
        rent_project.is_sell = form.is_sell.data
        rent_project.pictures = form.pictures.data
        # url must be None instead of empty string because empty string will cause ValidationError: Not a valid url
        rent_project.brochure = form.brochure.data if form.brochure.data else None
        rent_project.project_name = form.project_name.data
        rent_project.project_type = form.project_type.data
        rent_project.position = form.position.data
        rent_project.address = form.address.data
        rent_project.contacter = form.contacter.data
        rent_project.phone = form.phone.data

        new_shop_prices = []
        new_shop_areas = []
        for shop_info in form.shops_info.data:
            new_shop = Shop(shop_number=shop_info['shop_number'], area=shop_info['area'], price=shop_info['price'],
                            project_condition=shop_info['project_condition'], others=shop_info['others'])
            rent_project.shops_info.append(new_shop)
            new_shop_prices.append(new_shop.price)
            new_shop_areas.append(new_shop.area)
            # rent_project.shops_price.append(new_shop.price)
            # rent_project.shops_area.append(new_shop.area)
            rent_project.shops_investment.append(new_shop.others)

        new_shop_prices.sort()
        new_shop_areas.sort()
        for i in new_shop_prices:
            rent_project.shops_price.append(i)
        for i in new_shop_areas:
            rent_project.shops_area.append(i)
        rent_project.save()
        return str(rent_project.id)

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
    except (ValidationError, AttributeError):
        abort(404)


@rent.route('/approve/<rent_project_id>')
def approve_rent(rent_project_id):
    try:
        rent_project = RentProject.objects(id=rent_project_id).first()
        rent_project.is_approved = True
        rent_project.save()
        return 'OK'
    except (ValidationError, AttributeError):
        abort(404)

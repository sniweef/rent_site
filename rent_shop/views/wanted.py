from flask import Blueprint, request, abort, render_template
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
        is_buy = True if int(request.args.get('is_buy', 0)) else False
        min_area = int(request.args.get('min_area', 0))
        max_area = int(request.args.get('max_area', 0))
        wanter = request.args.get('wanter', '')
        intention = request.args.get('intention', '')
        business = request.args.get('business', '')
    except ValueError:
        from_idx = 0

    key = key.strip()
    keys = key.split(' ')

    q_expr = Q(is_approved=True) & Q(is_buy=is_buy) & Q(project_demand__icontains=keys[0])
    for i in range(1, len(keys)):
        q_expr = q_expr & Q(project_demand__icontains=keys[i])

    if max_area > 0 and max_area > min_area:
        q_expr = q_expr & Q(area__gte=min_area, area__lte=max_area)
    elif max_area == 0 and min_area > 0:
        q_expr = q_expr & Q(area__gte=min_area)

    if wanter:
        q_expr = q_expr & Q(wanter_type=wanter)
    if intention:
        q_expr = q_expr & Q(intention_type=intention)
    if business:
        q_expr = q_expr & Q(business_type=business)

    query_result = WantedShop.objects(q_expr).order_by('-id').\
        only('id', 'is_buy', 'wanter_type', 'intention_type', 'business_type', 'brand_name', 'area').\
        skip(from_idx)

    show_html = request.args.get('html', '')
    if show_html:
        return render_template('search_wanted_result.html', shop_list=query_result)

    return query_result.limit(10).to_json()


@wanted.route('/view/<wanted_shop_id>')
def view_wanted(wanted_shop_id):
    as_html = request.args.get('html', '')

    try:
        wanted_obj = WantedShop.objects(id=wanted_shop_id).first()
        if as_html:
            return render_template('publish_wanted.html', wanted_shop=wanted_obj, editable=False)
        return wanted_obj.to_json()
    except (ValidationError, AttributeError):
        return '{}'


@wanted.route('/publish', methods=['GET', 'POST'])
def publish_wanted():
    if request.method == 'GET':
        is_buy = True if int(request.args.get('is_buy', 0)) else False
        return render_template('publish_wanted.html', editable=True, is_buy=is_buy)

    form = PublishWantedForm(request.form)
    if form.validate():
        if form.id.data:
            shop = WantedShop.objects(id=form.id.data).first()
            if not shop:
                return 'Cannot find the specific shop with id %s' % form.id.data, 404
        else:
            shop = WantedShop()
            # shop.create_time = datetime.now()

        shop.is_approved = False
        shop.is_buy = form.is_buy.data
        print shop.is_buy
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
        break  # we only return first error message

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
        print wanted_shop, wanted_shop.id
        wanted_shop.is_approved = True
        wanted_shop.save()
        return 'OK'
    except (ValidationError, AttributeError), e:
        print e
        abort(404)


@wanted.route('/list')
def manage_rent():
    obj_list = []
    for i in WantedShop.objects():
        i.project_name = i.project_demand
        obj_list.append(i)

    if request.method == 'GET':
        return render_template('manage.html', obj_list=obj_list, prefix='wanted')


@wanted.route('/search_controller')
def search_controller():
    if request.method == 'GET':
        is_buy = True if int(request.args.get('is_buy', 0)) else False
        return render_template('wanted_project.html', is_buy=is_buy)

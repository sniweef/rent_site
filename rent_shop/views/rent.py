__author__ = 'hzhigeng'

from flask import request, abort
from flask import Blueprint

rent = Blueprint('rent', __name__, url_prefix='/rent')


@rent.route('/search')
def search_rent():
    try:
        key = request.args.get('key', '')
        from_idx = int(request.args.get('from', 0))
    except ValueError:
        from_idx = 0

    return key + str(from_idx)


@rent.route('/view')
def view_rent():
    return 'view_rent'


@rent.route('/publish')
def publish_rent():
    return 'publish'



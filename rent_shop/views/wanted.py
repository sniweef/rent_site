__author__ = 'hzhigeng'

from flask import Blueprint

wanted = Blueprint('wanted', __name__, url_prefix='/wanted')

@wanted.route('/search')
def search_wanted():
    return 'search'

@wanted.route('/view')
def view_wanted():
    pass
    return 'view_wanted'


@wanted.route('/publish')
def publish_wanted():
    return 'publish_wanted'


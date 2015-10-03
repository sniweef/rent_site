import os
from flask import Blueprint, request, url_for
from bson.objectid import ObjectId
from config import SHOP_PICS_ROOT_DIR

__author__ = 'hzhigeng'

pictures = Blueprint('pictures', __name__, url_prefix='/pictures')


@pictures.route('/', methods=['POST'])
def new_pictures():
    dest_dir_name = str(ObjectId()) + '/'
    pic_dir_path = os.path.join(SHOP_PICS_ROOT_DIR, dest_dir_name)

    try:
        os.makedirs(pic_dir_path)
    except IOError:
        print('mkdir %s failed!' % pic_dir_path)
        abort(400)

    #url_preffix = url_for('new_pictures') + dest_dir_name
    url_preffix = '/pictures/' + dest_dir_name
    pic_urls = []

    for file_prefix, file_obj in request.files.iteritems():
        filename_suffix = os.path.splitext(file_obj.filename)[-1]
        new_filename = str(ObjectId()) + filename_suffix
        new_file_path = os.path.join(pic_dir_path, new_filename)
        file_obj.save(new_file_path)
        pic_urls.append(url_preffix + new_filename)

    return str(pic_urls)

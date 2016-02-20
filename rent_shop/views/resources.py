import os
import json
import datetime
from flask import Blueprint, request, abort, send_file
from bson.objectid import ObjectId
from instance.config import SHOP_PICS_ROOT_DIR, PIC_SERVER_PORT, PIC_SERVER_IP

__author__ = 'hzhigeng'

resources = Blueprint('resources', __name__, url_prefix='/resources')


@resources.route('', methods=['POST'])
def new_resources():
    # dest_dir_name = str(ObjectId()) + '/'
    dest_dir_name = datetime.datetime.now().strftime("%Y%m%d") + '/'
    pic_dir_path = os.path.join(SHOP_PICS_ROOT_DIR, dest_dir_name)

    try:
        if not os.path.exists(pic_dir_path):
            os.makedirs(pic_dir_path)
    except IOError:
        print('mkdir %s failed!' % pic_dir_path)
        abort(500)

    url_preffix = 'http://%s:%d/resources/%s' %(PIC_SERVER_IP, PIC_SERVER_PORT, dest_dir_name)
    pic_urls = []

    for file_prefix, file_obj in request.files.iteritems():
        filename_suffix = os.path.splitext(file_obj.filename)[-1]
        new_filename = str(ObjectId()) + filename_suffix
        new_file_path = os.path.join(pic_dir_path, new_filename)
        print filename_suffix, new_file_path
        file_obj.save(new_file_path)
        pic_urls.append(url_preffix + new_filename)

    return json.dumps(pic_urls)


@resources.route('/<shop_pic_dir>/<shop_pic_name>')
def view_resource(shop_pic_dir, shop_pic_name):
    image_path = os.path.join(SHOP_PICS_ROOT_DIR, shop_pic_dir + '/' + shop_pic_name)
    if os.path.exists(image_path):
        return send_file(image_path)
    else:
        abort(404)


@resources.route('/delete/<shop_pic_dir>')
def delete_resource_dir(shop_pic_dir):
    pass


@resources.route('/delete/<shop_pic_dir>/<shop_pic_name>')
def delete_resource(shop_pic_dir):
    pass

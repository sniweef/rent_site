import os
import json
from flask import Blueprint, request, abort, send_file
from bson.objectid import ObjectId
from config import SHOP_PICS_ROOT_DIR, PIC_SERVER_IP, PIC_SERVER_PORT

__author__ = 'hzhigeng'

pictures = Blueprint('pictures', __name__, url_prefix='/pictures')


@pictures.route('', methods=['POST'])
def new_pictures():
    dest_dir_name = str(ObjectId()) + '/'
    pic_dir_path = os.path.join(SHOP_PICS_ROOT_DIR, dest_dir_name)

    try:
        os.makedirs(pic_dir_path)
    except IOError:
        print('mkdir %s failed!' % pic_dir_path)
        abort(400)

    url_preffix = 'http://%s:%d/pictures/%s' %(PIC_SERVER_IP, PIC_SERVER_PORT, dest_dir_name)
    pic_urls = []

    for file_prefix, file_obj in request.files.iteritems():
        filename_suffix = os.path.splitext(file_obj.filename)[-1]
        new_filename = str(ObjectId()) + filename_suffix
        new_file_path = os.path.join(pic_dir_path, new_filename)
        file_obj.save(new_file_path)
        pic_urls.append(url_preffix + new_filename)

    return json.dumps(pic_urls)

@pictures.route('/<shop_pic_dir>/<shop_pic_name>')
def view_picture(shop_pic_dir, shop_pic_name):
    image_path = os.path.join(SHOP_PICS_ROOT_DIR, shop_pic_dir + '/' + shop_pic_name)
    if os.path.exists(image_path):
        return send_file(image_path, mimetype='image/jpg')
    else:
        abort(404)


@pictures.route('/delete/<shop_pic_dir>')
def delete_picture_dir(shop_pic_dir):
    pass


@pictures.route('/delete/<shop_pic_dir>/<shop_pic_name>')
def delete_picture(shop_pic_dir):
    pass

from functools import wraps
from flask.blueprints import Blueprint
from flask import jsonify, request


check_token = Blueprint('check_token', __name__)


def login_required(func):
    # @wraps(func)#修饰内层函数，防止当前装饰器去修改被装饰函数__name__的属性
    def inner():
        token = request.headers.get('access_token')
        if not token:
            return jsonify(msg='User not logged in')
        else:
            return func()
    return inner


@check_token.route('/member/detail', methods=["GET"])
@login_required
def memberDetail():
    return jsonify({"msg": "this is member info"})

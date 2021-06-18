# coding = utf-8
import hashlib
from random import randint

from flask import jsonify, request

from common.db_utils import dbPerform


def randomName():
    u_name = '新用户'
    string_name = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    for i in range(6):
        u_name = u_name + string_name[randint(0, 35)]
    return u_name


def salt():  # 用户盐
    __salt = ''
    int_salt = '1234567890'
    for x in range(6):
        __salt = int_salt[randint(0, 9)] + __salt
    return __salt


def encryption(password, g_salt):  # 密码加密
    # 生成md5对象
    md5 = hashlib.md5(g_salt.encode('utf8'))
    # 对数据加密
    md5.update(password.encode('utf8'))
    # 获取密文
    pwd = md5.hexdigest()
    return pwd


def loginRequired(func):
    def inner():
        token = request.headers.get('access_token')
        if token is None or token == '':
            return jsonify(code=4002, msg='Please login first')
        else:
            func()
            return func()
    return inner
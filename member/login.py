# coding = utf-8
from flask import Blueprint, jsonify, request

from common.utils import dbPerform, encryption

login_Blue = Blueprint('login_Blue', __name__)


@login_Blue.route('/member/login/', methods=['POST'], strict_slashes=False)
def login():  # 登录
    # request.get_data接收raw参数
    # request.form.get接收form_data参数
    email = request.form.get('email')
    password = request.form.get('password')
    if email == '' or password == '' or email is None or password is None:
        return jsonify({'code': 1001, "message": "The email or password cannot be empty"})
    pwd_sql = """ SELECT `password` FROM member WHERE email = '{}' """
    salt_sql = """ SELECT `salt` FROM member WHERE email = '{}' """
    token_sql = """ SELECT `access_token` FROM member_credentials WHERE email = '{}' """
    name_sql = """ SELECT `name` FROM member where `email` = '{}' """
    if len(email) != 0 and len(password) != 0:
        __salt = dbPerform(salt_sql.format(email))
        pwd = dbPerform(pwd_sql.format(email))
        access_token = dbPerform(token_sql.format(email))
        _name = dbPerform(name_sql.format(email))
        __password = encryption(password, __salt)
        if __password == pwd:
            return jsonify({'code': 200, 'message': 'Login successful', "Access_token": access_token, "name": _name})
        else:
            return jsonify({'code': 1002, 'message': 'Please check your email or password'})
    else:
        return jsonify({'code': 1003, 'message': 'An unknown error'})

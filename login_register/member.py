# coding = utf-8
import re

from flask import Blueprint, jsonify, request

from common.connection import sql
from common.member_config import encryption, sendEmail, salt, randomName

loginRegister = Blueprint("loginRegister", __name__)


@loginRegister.route('/login/', methods=['POST'], strict_slashes=False)
def user_login():   # 登录
    # request.get_data接收raw参数
    # request.form.get接收form_data参数
    email = request.form.get('email')
    password = request.form.get('password')

    pwd_sql = "select pwd from member where email = '%s'" % email
    salt_sql = "select salt from member where email = '%s'" % email
    # 判断是否为空或空格
    try:
        if len(email) != 0 and len(password) != 0 :
            __salt = sql(salt_sql)[0][0]
            pwd = sql(pwd_sql)[0][0]
            __password = encryption(password, __salt)
            if __password == pwd:
                return jsonify({'message': 'success', 'code': 200})
            else:
                return jsonify({'message': '请检查您的密码', 'code': 1001})
        else:
            return jsonify({'message': '邮箱或密码不能为空', 'code': 1002})
    except IndexError:
        return jsonify({'message': '请检查您的邮箱格式', 'code': 1003})


@loginRegister.route('/register/', methods=['POST'], strict_slashes=False)
def user_register():    # 注册
    password = request.form.get('password')
    email = request.form.get('email')
    code = request.form.get('code')
    name = randomName()
    """判断是否为空或空格"""
    if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email) is None:
        return jsonify({'message': '请检查您的邮箱格式', 'code': 2001})
    if len(code) == 0 or code.isspace() == True:
        return jsonify({'message': '请输入您的验证码', 'code': 2002})
    if len(password) == 0 or password.isspace() == True:
        return jsonify({'message': '密码不能为空', 'code': 2003})
    else:       # 密码加密
        __salt = salt()
        __password = encryption(password, __salt)
    email_sql = "select email from member"
    code_sql = "select code from email_code where email = '%s' order by id desc limit 1 " % email
    email_result = sql(email_sql)
    email_list = []
    for j in range(len(email_result)):
        email_j = email_result[j][0]
        email_list.append(email_j)
    try:
        if email not in email_list:
            code_result = sql(code_sql)[0][0]
            if code == code_result:
                insert_sql = "insert into member (`name`, `pwd`, `email`, `salt`) values ('%s', '%s', '%s', '%s')" % (name, __password, email, salt)
                sql(insert_sql)
                return jsonify({'message': '注册成功', 'code': 200})
            else :
                return jsonify({'message': '验证码错误', 'code': 2005})
        else:
            return jsonify({'message': '邮箱已存在', 'code': 2004})
    except IndexError:
        return jsonify({'message': '验证码错误', 'code': 2006})


@loginRegister.route('/get_code/', methods=['GET'], strict_slashes=False)
def send_email_():      # 发送验证码
    user_email = request.args.get('email')
    if user_email != '':
        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', user_email):
            sendEmail(user_email)
            return jsonify({'code': 200, 'message': '发送成功'})
        else :
            return jsonify({'message': '请检查您的邮箱格式', 'code': 3001})
    else:
        return jsonify({'message': '请输入邮箱', 'code': 3002})

from Common.member_config import Encryption, Send_email, Salt, Random_name
from Common.connection import Sql
from flask import Blueprint, jsonify, request
import re

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
            salt = Sql(salt_sql)[0][0]
            pwd = Sql(pwd_sql)[0][0]
            __password = Encryption(password, salt)
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
    name = Random_name()
    """判断是否为空或空格"""
    if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email) == None :
        return jsonify({'message': '请检查您的邮箱格式', 'code': 2001})
    if len(code) == 0 or code.isspace() == True:
        return jsonify({'message': '请输入您的验证码', 'code': 2002})
    if len(password) == 0 or password.isspace() == True:
        return jsonify({'message': '密码不能为空', 'code': 2003})
    else:       # 密码加密
        salt = Salt()
        __password = Encryption(password, salt)
    email_sql = "select email from member"
    code_sql = "select code from email_code where email = '%s' order by id desc limit 1 " % email
    email_result = Sql(email_sql)
    email_list = []
    for j in range(len(email_result)):
        email_j = email_result[j][0]
        email_list.append(email_j)
    try:
        if email not in email_list:
            code_result = Sql(code_sql)[0][0]
            if code == code_result:
                insert_sql = "insert into member (`name`, `pwd`, `email`, `salt`) values ('%s', '%s', '%s', '%s')" % (name, __password, email, salt)
                Sql(insert_sql)
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
            Send_email(user_email)
            return jsonify({'code': 200, 'message': '发送成功'})
        else :
            return jsonify({'message': '请检查您的邮箱格式', 'code': 3001})
    else:
        return jsonify({'message': '请输入邮箱', 'code': 3002})

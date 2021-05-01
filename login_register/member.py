# coding = utf-8
import re

from flask import Blueprint, jsonify, request

from common.connection_utils import sql
from common.member_utils import encryption, sendEmail, salt, randomName

loginRegister = Blueprint("loginRegister", __name__)


@loginRegister.route('/login/', methods=['POST'], strict_slashes=False)
def user_login():  # 登录
    # request.get_data接收raw参数
    # request.form.get接收form_data参数
    email = request.form.get('email')
    password = request.form.get('password')
    pwd_sql = """
        SELECT
	        pwd 
        FROM
	        member 
        WHERE
	        email = '{}'
    """
    salt_sql = """
        SELECT
            salt
        FROM
            member
        WHERE
            email = '{}'
    """
    # 判断是否为空或空格
    try:
        if len(email) != 0 and len(password) != 0:
            __salt = sql(salt_sql.format(email))[0][0]
            pwd = sql(pwd_sql.format(email))[0][0]
            __password = encryption(password, __salt)
            if __password == pwd:
                return jsonify({'code': 200, 'message': 'Login successful'})
            else:
                return jsonify({'code': 1001, 'message': 'Please check your password'})
        else:
            return jsonify({'code': 1002, 'message': 'The mailbox or password cannot be empty'})
    except IndexError:
        return jsonify({'code': 1003, 'message': 'Please check your email format'})


@loginRegister.route('/register/', methods=['POST'], strict_slashes=False)
def user_register():  # 注册
    password = request.form.get('password')
    email = request.form.get('email')
    code = request.form.get('code')
    name = randomName()
    email_sql = """
        SELECT
            `email`
        FROM
            member
    """
    code_sql = """
        SELECT
            `code`
        FROM 
            email_code
        WHERE
            email = '{}'
        ORDER BY 
            id DESC
            LIMIT 1     
    """
    insert_sql = """
        INSERT INTO
            member ( `name`, `pwd`, `email`, `salt`)
        VALUES
            ('{}', '{}', '{}', '{}')
    """
    """判断是否为空或空格"""
    if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', email) is None:
        return jsonify({'code': 2001, 'message': 'Please check your email format'})
    if len(code) == 0 or code.isspace() == True:
        return jsonify({'code': 2002, 'message': 'Please enter your verification code'})
    if len(password) == 0 or password.isspace() == True:
        return jsonify({'code': 2003, 'message': 'Password cannot be empty'})
    else:  # 密码加密
        __salt = salt()
        __password = encryption(password, __salt)
    email_result = sql(email_sql)
    email_list = []
    for j in range(len(email_result)):
        email_j = email_result[j][0]
        email_list.append(email_j)
    try:
        if email not in email_list:
            code_result = sql(code_sql.format(email))[0][0]
            if code == code_result:
                sql(insert_sql.format(name, __password, email, __salt))
                return jsonify({'code': 200, 'message': 'Registered successfully'})
            else:
                return jsonify({'code': 2005, 'message': 'Verification code error'})
        else:
            return jsonify({'code': 2004, 'message': 'Email already exists'})
    except IndexError:
        return jsonify({'code': 2006, 'message': 'Verification code error'})


@loginRegister.route('/get_code/', methods=['GET'], strict_slashes=False)
def send_email_():  # 发送验证码
    user_email = request.args.get('email')
    if user_email != '':
        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$', user_email):
            sendEmail(user_email)
            return jsonify({'code': 200, 'message': 'Send a success'})
        else:
            return jsonify({'code': 3001, 'message': 'Please check your email format'})
    else:
        return jsonify({'code': 3002, 'message': 'Please entry your email'})

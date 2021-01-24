from Common.account_number import encryption, send_email, Salt
from Common.connection import Sql
from flask import Blueprint, jsonify, request

loginRegister = Blueprint("loginRegister", __name__)


@loginRegister.route('/login/', methods=['POST'], strict_slashes=False)
def user_login():   # 登录
    """ 
    request.get_data接收raw参数
    request.form.get接收form_data参数
    """
    username = request.form.get('username')  # 备注
    password = request.form.get('password')
    # 密码md5后验证
    salt_sql = "select salt from member where name = '%s'" % username
    salt = Sql(salt_sql)[0][0]
    _password = encryption(password, salt)[0]
    """判断是否为空或空格"""
    if len(username) == 0 or username.isspace() == True:
        return jsonify({'message': '用户名不能为空或空格', 'code': '0'})
    if len(password) == 0 or password.isspace() == True:
        return jsonify({'message': '密码不能为空或空格', 'code': '0'})
    name_sql = "select name from member"
    pwd_sql = "select pwd from member where name = '%s'" % username
    select_username = Sql(name_sql)
    list_name = []
    for i in range(len(select_username)):
        name = select_username[i][0]
        list_name.append(name)
    try:
        pwd = Sql(pwd_sql)[0][0]
    except IndexError:
        return jsonify({'message': '用户名或密码错误', 'code': 0})
    if _password == pwd and username in list_name:
        return jsonify({'message': 'success', 'code': 200})
    elif _password != pwd:
        return jsonify({'message': '密码错误', 'code': 0})
    elif username not in list_name:
        return jsonify({'message': '用户名错误', 'code': 0})


@loginRegister.route('/register/', methods=['POST'], strict_slashes=False)
def user_register():    # 注册
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    code = request.form.get('code')
    # 密码加密
    salt = Salt()
    _password = encryption(password, salt)
    """判断是否为空或空格"""
    if len(username) == 0 or username.isspace() == True:
        return jsonify({'message': '用户名不能为空或空格', 'code': '0'})
    if len(password) == 0 or password.isspace() == True:
        return jsonify({'message': '密码不能为空或空格', 'code': '0'})
    if len(email) == 0 or email.isspace == True:
        return jsonify({'message': '邮箱不能为空或空格', 'code': '0'})
    username_sql = "select name from member"
    email_sql = "select email from member"
    insert_sql = "insert into member (`name`, `pwd`, `email`, `salt`) values ('%s', '%s', '%s' , '%s')" % (username, _password, email, salt)
    code_sql = "select code from email_code where email = '%s' order by id desc limit 1 " % email
    username_result = Sql(username_sql)
    email_result = Sql(email_sql)
    code_result = Sql(code_sql)[0][0]
    username_list = []
    email_list = []
    for i in range(len(username_result)):
        name = username_result[i][0]
        username_list.append(name)

    for j in range(len(email_result)):
        email_j = email_result[j][0]
        email_list.append(email_j)

    if username in username_list:
        return jsonify({'message': '用户名已存在', 'code': 0})
    # elif email in email_list:
    #     return jsonify({'message': '邮箱已存在', 'code': 0})
    elif username not in username_list and code == code_result:
        Sql(insert_sql)
        return jsonify({'message': '注册成功', 'code': 200})


@loginRegister.route('/get_code/', methods=['GET'], strict_slashes=False)
def send_email_():      # 发送验证码
    user_email = request.args.get('email')
    if len(user_email) == 0:
        return jsonify({'message': '请输入验证码'})
    else:
        send_email(user_email)
        return jsonify({'code': 200, 'message': '发送成功'})
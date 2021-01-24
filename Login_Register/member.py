from Common.account_number import encryption, send_email
from Common.connection import select

from flask import Blueprint, jsonify, request

loginRegister = Blueprint("loginRegister", __name__)

"""登录"""


@loginRegister.route('/login/', methods=['POST'], strict_slashes=False)
def user_login():
    """ 
    request.get_data接收raw参数
    request.form.get接收form_data参数
    """

    username = request.form.get('username')  # 备注
    password = request.form.get('password')

    # 密码md5后验证
    _password = encryption(password)
    """判断是否为空或空格"""
    if len(username) == 0 or username.isspace() == True:
        return jsonify({'message': '用户名不能为空或空格', 'code': '0'})
    if len(password) == 0 or password.isspace() == True:
        return jsonify({'message': '密码不能为空或空格', 'code': '0'})

    name_sql = "select name from member"
    pwd_sql = "select pwd from member where name = '%s'" % username
    select_username = select(name_sql)
    list_name = []

    for i in range(len(select_username)):
        name = select_username[i][0]
        list_name.append(name)
    try:
        pwd = select(pwd_sql)[0][0]
    except IndexError:
        return jsonify({'message': '用户名或密码错误', 'code': 0})

    if _password == pwd and username in list_name:
        return jsonify({'message': 'success', 'code': 200})
    elif _password != pwd:
        return jsonify({'message': '密码错误', 'code': 0})
    elif username not in list_name:
        return jsonify({'message': '用户名错误', 'code': 0})


"""注册"""


@loginRegister.route('/register/', methods=['POST'], strict_slashes=False)
def user_register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    code = request.form.get('code')
    # 密码加密
    _password = encryption(password)
    """判断是否为空或空格"""
    if len(username) == 0 or username.isspace() == True:
        return jsonify({'message': '用户名不能为空或空格', 'code': '0'})
    if len(password) == 0 or password.isspace() == True:
        return jsonify({'message': '密码不能为空或空格', 'code': '0'})
    if len(email) == 0 or email.isspace == True:
        return jsonify({'message': '邮箱不能为空或空格', 'code': '0'})

    username_sql = "select name from member"
    email_sql = "select email from member"
    insert_sql = "insert into member (`name`, `pwd`, `email`) values ('%s', '%s', '%s')" % (username, _password, email)
    code_sql = "select code from email_code where email = '%s'" % email
    username_result = select(username_sql)
    email_result = select(email_sql)
    code_result = select(code_sql)[0][0]
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
    elif email in email_list:
        return jsonify({'message': '邮箱已存在', 'code': 0})
    elif username not in username_list and code == code_result:
        select(insert_sql)
        return jsonify({'message': '注册成功', 'code': 200})


@loginRegister.route('/get_code/', methods=['GET'], strict_slashes=False)
def send_email_():
    user_email = request.args.get('email')
    if len(user_email) == 0:
        return jsonify({'message': '请输入验证码'})
    else:
        send_email(user_email)
        return jsonify({'code': 200, 'message': '发送成功'})
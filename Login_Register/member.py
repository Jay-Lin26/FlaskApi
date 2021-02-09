from Common.member_config import encryption, send_email, Salt
from Common.connection import Sql
from flask import Blueprint, jsonify, request

loginRegister = Blueprint("loginRegister", __name__)


@loginRegister.route('/login/', methods=['POST'], strict_slashes=False)
def user_login():   # 登录
    """ 
    request.get_data接收raw参数
    request.form.get接收form_data参数
    """
    email = request.form.get('email')  # 备注
    password = request.form.get('password')
    # 密码md5后验证
    salt_sql = "select salt from member where email = '%s'" % email
    if len(Sql(salt_sql)) == 0:
        return jsonify({'message': '请检查您的邮箱格式', 'code': 1001})
    else:
        salt = Sql(salt_sql)[0][0]
        _password = encryption(password, salt)
    """判断是否为空或空格"""
    if len(email) == 0 or email.isspace() == True:
        return jsonify({'message': '请检查您的邮箱格式', 'code': 1001})
    if len(password) == 0 or password.isspace() == True:
        return jsonify({'message': '密码不能为空或空格', 'code': 1002})
    email_sql = "select email from member"
    pwd_sql = "select pwd from member where email = '%s'" % email
    select_email = Sql(email_sql)
    list_email = []
    for i in range(len(select_email)):
        email = select_email[i][0]
        list_email.append(email)
    try:
        pwd = Sql(pwd_sql)[0][0]
    except IndexError:
        return jsonify({'message': '用户名或密码错误', 'code': 1003})
    if _password == pwd and email in list_email:
        return jsonify({'message': 'success', 'code': 200})
    elif _password != pwd:
        return jsonify({'message': '您输入的密码有误', 'code': 1002})
    elif email not in list_email:
        return jsonify({'message': '邮箱不存在', 'code': 1001})


@loginRegister.route('/register/', methods=['POST'], strict_slashes=False)
def user_register():    # 注册
    password = request.form.get('password')
    email = request.form.get('email')
    code = request.form.get('code')
    name = '新用户4765'
    """判断是否为空或空格"""
    if len(email) == 0 or email.isspace == True:
        return jsonify({'message': '请检查您的邮箱格式', 'code': 2001})
    if len(code) == 0 or code.isspace() == True:
        return jsonify({'message': '请输入您的验证码', 'code': 2002})
    if len(password) == 0 or password.isspace() == True:
        return jsonify({'message': '密码不能为空或空格', 'code': 2003})
    else:       # 密码加密
        salt = Salt()
        _password = encryption(password, salt)
    email_sql = "select email from member"
    code_sql = "select code from email_code where email = '%s' order by id desc limit 1 " % email
    email_result = Sql(email_sql)
    code_result = Sql(code_sql)[0][0]
    email_list = []
    for j in range(len(email_result)):
        email_j = email_result[j][0]
        email_list.append(email_j)
    if email in email_list:
        return jsonify({'message': '邮箱已存在', 'code': 2004})
    elif code != code_result:
        return jsonify({'message': '验证码错误', 'code': 2005})
    elif code == code_result:
        insert_sql = "insert into member (`name`, `pwd`, `email`, `salt`) values ('%s', '%s', '%s', '%s')" % (name, _password, email, salt)
        Sql(insert_sql)
        return jsonify({'message': '注册成功', 'code': 200})


@loginRegister.route('/get_code/', methods=['GET'], strict_slashes=False)
def send_email_():      # 发送验证码
    user_email = request.args.get('email')
    if user_email == '':
        return jsonify({'message': '请输入邮箱'})
    else:
        send_email(user_email)
        return jsonify({'code': 200, 'message': '发送成功'})

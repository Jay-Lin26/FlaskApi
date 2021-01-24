from flask import Flask, make_response, jsonify, request
from userinfo_.account_number import encryption, send_email
from connection import select
from flask_cors import CORS
import pymysql


app = Flask(__name__)
# 解决跨域问题
CORS(app)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)


""" 发送验证码"""


@app.route('/get_code/', methods=['GET'], strict_slashes=False)
def send_email_():
    user_email = request.args.get('email')
    if len(user_email) == 0 :
        return jsonify({'message': '请输入验证码'})
    else:
        send_email(user_email)
        return jsonify({'code': 200, 'message': '发送成功'})


"""获取用户列表"""


@app.route('/userinfo/', methods=['GET'], strict_slashes=False)
def user_info():
    """从params获取参数"""
    username = request.args.get('username')
    """
    从path路径获取参数
    /userinfo/<username>/
    """
    try:
        sql = "select * from member"
        result = select(sql)
        message = []
        for i in range(len(result)):
            uid = result[i][0]
            name = result[i][1]
            pwd = result[i][2]
            email = result[i][3]
            start_message = {
                'id': uid,
                'name': name,
                'pwd': pwd,
                'email': email
            }
            message.append(start_message)
        # _message = json.dumps(message, sort_keys=True, indent=4, separators={',', ':'})
        return jsonify({'code': 200, 'data': message})
    except IndexError:
        return jsonify({'user_info': 'user_info index error', 'code': 200})
    except pymysql.err.ProgrammingError:
        return jsonify({'user_info': 'user_info ProgrammingError', 'code': 200})


"""登录"""


@app.route('/login/', methods=['POST'], strict_slashes=False)
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


@app.route('/register/', methods=['POST'], strict_slashes=False)
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

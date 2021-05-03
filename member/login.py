# coding = utf-8
from flask import Blueprint, jsonify, request

from common.db_utils import dbPerform
from member.utils import encryption

login_Blue = Blueprint('login_Blue', __name__)


@login_Blue.route('/api/v1.0/member/login/', methods=['POST'], strict_slashes=False)
def login():  # 登录
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
    token_sql = """
        SELECT
            `access_token`
        FROM
            access_token
        WHERE
            email = '{}'
    """
    # 判断是否为空或空格
    try:
        if len(email) != 0 and len(password) != 0:
            __salt = dbPerform(salt_sql.format(email))[0][0]
            pwd = dbPerform(pwd_sql.format(email))[0][0]
            access_token = dbPerform(token_sql.format(email))[0][0]
            __password = encryption(password, __salt)
            if __password == pwd:
                return jsonify({'code': 200, 'message': 'Login successful'}), 200, [("Access_token", access_token)]
            else:
                return jsonify({'code': 1001, 'message': 'Please check your password'})
        else:
            return jsonify({'code': 1002, 'message': 'The mailbox or password cannot be empty'})
    except IndexError:
        return jsonify({'code': 1003, 'message': 'Email does not exist'})

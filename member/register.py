# coding = utf-8
import re
import time

from flask import Blueprint, jsonify, request

from flask_api.common.db_utils import dbPerform, dbPerforms
from flask_api.member.utils import encryption, salt, randomName

register_Blue = Blueprint('register_Blue', __name__)


@register_Blue.route('/api/v1.0/member/register/', methods=['POST'], strict_slashes=False)
def register():  # 注册
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
            member ( `name`, `pwd`, `email`, `salt`, `create_time`)
        VALUES
            ('{}', '{}', '{}', '{}', '{}')
    """
    token_sql = """
        INSERT INTO
            access_token (`access_token`, `email`, `create_time`)
        VALUES
            ('{}', '{}', '{}')
    """
    if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com]{1,3}$', email) is None:
        return jsonify({'code': 2001, 'message': 'Please check your email format'})
    if len(code) == 0 or code.isspace() == True:
        return jsonify({'code': 2002, 'message': 'Please enter your verification code'})
    if len(password) == 0 or password.isspace() == True:
        return jsonify({'code': 2003, 'message': 'Password cannot be empty'})
    else:
        __salt = salt()
        __password = encryption(password, __salt)
    email_result = dbPerforms(email_sql)

    if email not in email_result:
        code_result = dbPerform(code_sql.format(email))
        if code == code_result:
            __time = int(time.time())
            dbPerform(insert_sql.format(name, __password, email, __salt, __time))
            __token = encryption(__password, email)
            dbPerform(token_sql.format(__token, email, __time))
            return jsonify({'code': 200, 'message': 'Registered successfully'})
        else:
            return jsonify({'code': 2005, 'message': 'Verification code error'})
    else:
        return jsonify({'code': 2004, 'message': 'Email already exists'})

# coding = utf-8
import re
import time

from flask import Blueprint, jsonify, request

from common.db_utils import dbPerform, dbPerforms
from member.utils import encryption, salt, randomName

register_Blue = Blueprint('register_Blue', __name__)


@register_Blue.route('/api/v1.0/member/register/', methods=['POST'], strict_slashes=False)
def register():  # 注册
    password = request.form.get('password')
    email = request.form.get('email')
    code = request.form.get('code')
    if email == '' or email is None:
        return jsonify({'code': 2001, 'message': 'Email cannot be empty'})
    name = randomName()
    email_sql = """
        SELECT
            `email`
        FROM
            member
    """
    code_sql = """
        SELECT
            `verification_code`
        FROM 
            verification_log
        WHERE
            email = '{}'
        ORDER BY 
            id DESC
            LIMIT 1     
    """
    insert_sql = """
        INSERT INTO
            member ( `name`, `email`, `password`, `salt`, `create_time`)
        VALUES
            ('{}', '{}', '{}', '{}', '{}')
    """
    token_sql = """
        INSERT INTO
            member_credentials (`access_token`, `email`, `update_time`)
        VALUES
            ('{}', '{}', '{}')
    """
    if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com]{1,3}$', email) is None:
        return jsonify({'code': 2001, 'message': 'Please check your email format'})
    if code == '' or code is None:
        return jsonify({'code': 2002, 'message': 'Please enter your verification code'})
    if password == '' or password is None:
        return jsonify({'code': 2003, 'message': 'Password cannot be empty'})
    else:
        __salt = salt()
        __password = encryption(password, __salt)

    email_result = dbPerforms(email_sql)
    print(email_result)

    if email not in email_result:
        code_result = dbPerform(code_sql.format(email))
        if code == code_result:
            __time = int(time.time())
            dbPerform(insert_sql.format(name, email, __password, __salt, __time))
            __token = encryption(__password, email)
            dbPerform(token_sql.format(__token, email, __time))
            return jsonify({'code': 200, 'message': 'Registered successfully'})
        else:
            return jsonify({'code': 2005, 'message': 'Verification code error'})
    else:
        return jsonify({'code': 2004, 'message': 'Email already exists'})

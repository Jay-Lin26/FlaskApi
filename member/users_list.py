# coding = utf-8
from flask import Blueprint, jsonify

from common.db_utils import dbPerform
from member.utils import loginRequired

users_List_Blue = Blueprint('user', __name__)


@users_List_Blue.route('/api/v1.0/member/list', methods=['GET'], strict_slashes=False)
@loginRequired
def usersList():
    try:
        __sql = "select * from member order by uid limit 10"
        result = dbPerform(__sql)
        message = []
        for i in range(len(result)):
            uid = result[i][0]
            name = result[i][1]
            email = result[i][3]
            start_message = {
                'id': uid,
                'name': name,
                'email': email
            }
            message.append(start_message)
        return jsonify({'code': 200, 'data': message})
    except IndexError:
        return jsonify({'code': 200, 'data': []})

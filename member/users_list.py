# coding = utf-8
from flask import Blueprint, jsonify

from common.db_utils import dbPerforms

users_List_Blue = Blueprint('user', __name__)


@users_List_Blue.route('/api/v1.0/member/list', methods=['GET'], strict_slashes=False)
def usersList():
    __sql = "select * from member order by id limit 10"
    result = dbPerforms(__sql)
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

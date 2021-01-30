from flask import Blueprint, jsonify
from Common.connection import Sql
import pymysql

user = Blueprint('user', __name__)


"""获取用户列表"""


@user.route('/user/list', methods=['GET'], strict_slashes=False)
def user_info():
    """从params获取参数"""
    # username = request.args.get('username')
    try:
        sql = "select * from member order by uid limit 10"
        result = Sql(sql)
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
        # _message = json.dumps(message, sort_keys=True, indent=4, separators={',', ':'})
        return jsonify({'code': 200, 'data': message})
    except IndexError:
        return jsonify({'user_info': 'user_info index error', 'code': 200})
    except pymysql.err.ProgrammingError:
        return jsonify({'user_info': 'user_info ProgrammingError', 'code': 200})


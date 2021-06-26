from flask import jsonify, request
from flask.blueprints import Blueprint

from common.utils import dbPerforms

post_Blue = Blueprint("postBlue", __name__)


def resultList(result):
    a_list = []
    for i in range(len(result)):
        tag_id = result[i][2]
        tag_name = result[i][3]
        data = {
            "tag_id": tag_id,
            "tag_name": tag_name
        }
        a_list.append(data)
    return a_list


@post_Blue.route('/api/v1.0/category/tags', methods=['GET'], strict_slashes=False)
def post():
    a_sql = """ SELECT c.id, c.name, t.id, t.name FROM `category` as c inner join tags as t on c.id = t.cid where c.id = 1 """
    b_sql = """ SELECT c.id, c.name, t.id, t.name FROM `category` as c inner join tags as t on c.id = t.cid where c.id = 2 """
    a_result = dbPerforms(a_sql)
    b_result = dbPerforms(b_sql)
    a_id = a_result[0][0]
    a_type = a_result[0][1]
    b_id = b_result[0][0]
    b_type = b_result[0][1]
    a_list, b_list = resultList(a_result), resultList(b_result)
    last_list = [
        {
            "id": a_id,
            "type": a_type,
            "tags": a_list
        },
        {
            "id": b_id,
            "type": b_type,
            "tags": b_list
        }
    ]
    return jsonify({
        "code": 200,
        "message": "success",
        "data": last_list
    })

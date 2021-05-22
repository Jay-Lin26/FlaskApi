from flask.blueprints import Blueprint
from common.db_utils import dbPerforms
from flask import jsonify

article_index_Blue = Blueprint("article_index_Blue", __name__)


@article_index_Blue.route("/api/v1.0/article/index", methods=["get"])
def article_index():
    sql = "select id,title,description,image_url from article where status = '1' limit 8"
    a = dbPerforms(sql)
    info = []
    for i in range(len(a)):
        a_id = a[i][0]
        t = a[i][1]
        d = a[i][2]
        u = a[i][3]
        result = {
            'id': a_id,
            "title": t,
            "desc": d,
            "img_url": u
        }
        info.append(result)
    return jsonify({"code": 200, "data": info})
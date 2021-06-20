from flask.blueprints import Blueprint
from common.utils import dbPerforms, changeTime
from flask import jsonify
import time

articleIndex_Blue = Blueprint("article_index_Blue", __name__)


@articleIndex_Blue.route("/api/v1.0/article/index/", methods=["get"], strict_slashes=False)
def article_index():
    sql = """
SELECT
	a.id,
	a.title,
	a.description,
	a.image_url,
	m.`name`,
	a.views,
	a.release_time 
FROM
	article AS a
	INNER JOIN member AS m ON a.mid = m.id 
WHERE
	`status` = 1 
	LIMIT 8
"""
    a = dbPerforms(sql)
    info = []
    for i in range(len(a)):
        a_id = a[i][0]
        t = a[i][1]
        d = a[i][2]
        u = a[i][3]
        writer = a[i][4]
        view = a[i][5]
        release_time = a[i][6]
        result = {
            'id': a_id,
            "title": t,
            "desc": d,
            "img_url": u,
            "writer": writer,
            "view": view,
            "release_time": changeTime(release_time)
        }
        info.append(result)
    return jsonify({"code": 200, "data": info})

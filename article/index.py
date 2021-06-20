from flask.blueprints import Blueprint
from common.db_utils import dbPerforms
from flask import jsonify
import time

index_Blue = Blueprint("article_index_Blue", __name__)


@index_Blue.route("/api/v1.0/article/index/", methods=["get"], strict_slashes=False)
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
        times = a[i][6]
        time_local = time.localtime(int(times))
        pub_date = time.strftime("%Y-%m-%d", time_local)
        result = {
            'id': a_id,
            "title": t,
            "desc": d,
            "img_url": u,
            "writer": writer,
            "view": view,
            "release_time": pub_date
        }
        info.append(result)
    return jsonify({"code": 200, "data": info})
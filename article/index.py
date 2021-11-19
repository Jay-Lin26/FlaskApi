from flask.blueprints import Blueprint
from common.utils import dbPerforms, changeTime
from flask import jsonify

articleIndex_Blue = Blueprint("article_index_Blue", __name__)


@articleIndex_Blue.route("/article/index/", methods=["get"], strict_slashes=False)
def article_index():
    sql = """
            SELECT
                a.id,
                a.title,
                a.description,
                a.image_url,
                m.`name`,
                a.views,
                a.release_time,
                m.avatar
            FROM
                article AS a
                INNER JOIN member AS m ON a.mid = m.id 
            WHERE
                `status` = 1
                ORDER BY a.id ASC 
                LIMIT 8
        """
    banner_sql = """
            SELECT
                id,
                url 
            FROM
                `images` 
            WHERE
                STATUS = 1
                """
    a = dbPerforms(sql)
    b = dbPerforms(banner_sql)
    info = []
    banner_info = []
    for i in range(len(a)):
        a_id = a[i][0]
        t = a[i][1]
        d = a[i][2]
        u = a[i][3]
        writer = a[i][4]
        view = a[i][5]
        release_time = a[i][6]
        avatar = a[i][7]
        result = {
            'id': a_id,
            "title": t,
            "desc": d,
            "img_url": u,
            "writer": writer,
            "view": view,
            "release_time": changeTime(release_time),
            "avatar": avatar
        }
        info.append(result)
    for j in range(len(b)):
        b_id = b[j][0]
        url = b[j][1]
        b_result = {
            'id': b_id,
            'url': url
        }
        banner_info.append(b_result)
    return jsonify({"code": 200, "message": "success", "banner": banner_info, "data": info})

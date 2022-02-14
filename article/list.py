from flask.blueprints import Blueprint
from common.utils import dbPerforms, changeTime
from flask import jsonify

articleList_Blue = Blueprint("article_list_blue", __name__)


@articleList_Blue.route("/article/list/", methods=["get"], strict_slashes=False)
def article_list():
    article_sql = """ SELECT a.id,a.title,a.description,a.image_url,m.`name`,a.views,a.release_time,m.avatar
                         FROM article AS a
                         INNER JOIN member AS m ON a.mid = m.id 
                         WHERE `status` = 1
                         ORDER BY a.id ASC 
                    """

    article = dbPerforms(article_sql)
    article_dict = []
    for i in range(len(article)):
        a_id = article[i][0]
        t = article[i][1]
        d = article[i][2]
        u = article[i][3]
        writer = article[i][4]
        view = article[i][5]
        release_time = article[i][6]
        avatar = article[i][7]
        article_result = {
            'id': a_id,
            "title": t,
            "desc": d,
            "img_url": u,
            "writer": writer,
            "view": view,
            "release_time": changeTime(release_time),
            "avatar": avatar
        }
        article_dict.append(article_result)

    return jsonify({
        "code": 200,
        "message": "success",
        "article": article_dict,
    })

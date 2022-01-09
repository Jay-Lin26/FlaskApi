from flask.blueprints import Blueprint
from common.utils import dbPerforms, changeTime
from flask import jsonify

articleIndex_Blue = Blueprint("article_index_Blue", __name__)


@articleIndex_Blue.route("/article/index/", methods=["get"], strict_slashes=False)
def article_index():
    article_sql = """ SELECT a.id,a.title,a.description,a.image_url,m.`name`,a.views,a.release_time,m.avatar
                     FROM article AS a
                     INNER JOIN member AS m ON a.mid = m.id 
                     WHERE `status` = 1
                     ORDER BY a.id ASC 
                     LIMIT 8
                """
    banner_sql = """ SELECT id,title,url,track_id
                    FROM `images` 
                    WHERE STATUS = 1
                """
    other_sql = """ SELECT a.id,a.title,a.description,a.image_url,m.`name`,a.views,a.release_time,m.avatar
                   FROM article AS a
                   INNER JOIN member AS m ON a.mid = m.id
                   WHERE a.`tid` = 3 AND `status` = 1
                   ORDER BY a.id ASC
                   limit 8
               """

    article_list = dbPerforms(article_sql)
    banner_list = dbPerforms(banner_sql)
    other_list = dbPerforms(other_sql)

    article_dict = []
    banner_dict = []
    other_dict = []

    for i in range(len(article_list)):
        a_id = article_list[i][0]
        t = article_list[i][1]
        d = article_list[i][2]
        u = article_list[i][3]
        writer = article_list[i][4]
        view = article_list[i][5]
        release_time = article_list[i][6]
        avatar = article_list[i][7]
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

    for j in range(len(banner_list)):
        b_id = banner_list[j][0]
        title = banner_list[j][1]
        url = banner_list[j][2]
        track_id = banner_list[j][3]
        banner_result = {
            'id': b_id,
            'title': title,
            'url': url,
            'track_id': track_id
        }
        banner_dict.append(banner_result)

    for k in range(len(other_list)):
        a_id = other_list[k][0]
        t = other_list[k][1]
        d = other_list[k][2]
        u = other_list[k][3]
        writer = other_list[k][4]
        view = other_list[k][5]
        release_time = other_list[k][6]
        avatar = other_list[k][7]
        other_result = {
            'id': a_id,
            "title": t,
            "desc": d,
            "img_url": u,
            "writer": writer,
            "view": view,
            "release_time": changeTime(release_time),
            "avatar": avatar
        }
        other_dict.append(other_result)

    return jsonify({
        "code": 200,
        "message": "success",
        "banner": banner_dict,
        "article": article_dict,
        "otherArticle": other_dict
    })

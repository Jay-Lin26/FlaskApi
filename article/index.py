from flask.blueprints import Blueprint
from common.utils import dbPerforms, changeTime
from flask import jsonify

articleIndex_Blue = Blueprint("article_index_Blue", __name__)


@articleIndex_Blue.route("/article/index/", methods=["get"], strict_slashes=False)
def article_index():
    articleSql = """ SELECT a.id,a.title,a.description,a.image_url,m.`name`,a.views,a.release_time,m.avatar
                     FROM article AS a
                     INNER JOIN member AS m ON a.mid = m.id 
                     WHERE `status` = 1
                     ORDER BY a.id ASC 
                     LIMIT 8
                """
    bannerSql = """ SELECT id,title,url,track_id
                    FROM `images` 
                    WHERE STATUS = 1
                """
    otherSql = """ SELECT a.id,a.title,a.description,a.image_url,m.`name`,a.views,a.release_time,m.avatar
                   FROM article AS a
                   INNER JOIN member AS m ON a.mid = m.id
                   WHERE a.`tid` = 3 AND `status` = 1
                   ORDER BY a.id ASC
                   limit 8
               """
    articleArr = dbPerforms(articleSql)
    bannerArr = dbPerforms(bannerSql)
    otherArr = dbPerforms(otherSql)
    article_list = []
    banner_list = []
    other_list = []
    for i in range(len(articleArr)):
        a_id = articleArr[i][0]
        t = articleArr[i][1]
        d = articleArr[i][2]
        u = articleArr[i][3]
        writer = articleArr[i][4]
        view = articleArr[i][5]
        release_time = articleArr[i][6]
        avatar = articleArr[i][7]
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
        article_list.append(article_result)
    for j in range(len(bannerArr)):
        b_id = bannerArr[j][0]
        title = bannerArr[j][1]
        url = bannerArr[j][2]
        track_id = bannerArr[j][3]
        banner_result = {
            'id': b_id,
            'title': title,
            'url': url,
            'track_id': track_id
        }
        banner_list.append(banner_result)
    for k in range(len(otherArr)):
        a_id = otherArr[k][0]
        t = otherArr[k][1]
        d = otherArr[k][2]
        u = otherArr[k][3]
        writer = otherArr[k][4]
        view = otherArr[k][5]
        release_time = otherArr[k][6]
        avatar = otherArr[k][7]
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
        other_list.append(other_result)
    return jsonify({"code": 200, "message": "success", "banner": banner_list, "article": article_list, "otherArticle": other_list})

from flask.blueprints import Blueprint
from flask import jsonify, request
from common.utils import dbPerforms, changeTime

tagDetail_Blue = Blueprint("tagDetail", __name__)


@tagDetail_Blue.route("/category/detail", methods=["get"], strict_slashes=False)
def tagDetail():
    tag_id = request.args.get("tag_id")
    if tag_id == '' or tag_id is None:
        return jsonify({"code": 201, "message": "暂无内容", "tag_name": "", "data": ""})
    sql = """ SELECT a.id,a.title,a.description,a.cover_img,a.views,a.release_time,m.`name`,m.avatar,t.`name` 
              FROM article AS a
              INNER JOIN tags AS t ON a.tid = t.id
              INNER JOIN member AS m ON a.mid = m.id 
              WHERE a.tid = '{}'
          """
    try:
        a = dbPerforms(sql.format(int(tag_id)))
        tag_name = a[0][8]
        info = []
        for i in range(len(a)):
            a_id = a[i][0]
            title = a[i][1]
            desc = a[i][2]
            url = a[i][3]
            view = a[i][4]
            release_time = a[i][5]
            writer = a[i][6]
            avatar = a[i][7]
            result = {
                'id': a_id,
                "title": title,
                "desc": desc,
                "img_url": url,
                "view": view,
                "release_time": changeTime(release_time),
                "writer": writer,
                "avatar": avatar
            }
            info.append(result)
        return jsonify({"code": 200, "message": "success", "tag_name": tag_name, "data": info})
    except ValueError:
        return jsonify({"code": 201, "message": "暂无内容", "tag_name": "", "data": ""})
    except IndexError:
        return jsonify({"code": 201, "message": "暂无内容", "tag_name": "", "data": ""})

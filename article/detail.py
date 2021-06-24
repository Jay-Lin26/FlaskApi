from flask import jsonify, request
from flask.blueprints import Blueprint

from common.utils import dbPerforms, dbPerform, changeTime

articleDetail_Blue = Blueprint("blog_detail_Blue", __name__)


@articleDetail_Blue.route('/api/v1.0/article/detail/', methods=['GET'], strict_slashes=False)
def blog_detail():
    article_id = request.args.get('article_id')
    count_sql = """ SELECT count(*) FROM article """
    update_sql = """ update article set views = views + 1 where id = '{}' """
    sql = """SELECT `title`, `content`, `views`, `release_time` FROM article WHERE id = '{}' """
    count_num = dbPerform(count_sql)
    try:
        if int(article_id) > int(count_num) or article_id == ' ' or article_id is None:
            return jsonify({
                'code': 201,
                'message': ' 该文章已被删除或不存在！'
            })
    except ValueError:
        return jsonify({
            'code': 201,
            'message': ' 该文章已被删除或不存在！'
        })
    dbPerform(update_sql.format(article_id))    # 浏览次数加1
    result = dbPerforms(sql.format(article_id))
    title = result[0][0]
    content = result[0][1]
    views = result[0][2]
    release_time = result[0][3]
    return jsonify({
        'code': 200,
        'title': title,
        'content': content,
        'views': views,
        'time': changeTime(release_time)
    })

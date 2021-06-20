import time
from flask import jsonify, request
from flask.blueprints import Blueprint

from common.db_utils import dbPerforms, dbPerform

memberDetail_Blue = Blueprint("blog_detail_Blue", __name__)


@memberDetail_Blue.route('/api/v1.0/article/detail/', methods=['GET'], strict_slashes=False)
def blog_detail():
    article_id = request.args.get('article_id')
    count_sql = """ SELECT count(*) FROM article """
    update_sql = """ update article set views = views + 1 where id = '{}' """
    sql = """SELECT `title`, `content`, `views`, `release_time` FROM article WHERE id = '{}' """
    count_num = dbPerform(count_sql)
    if int(article_id) > int(count_num) or article_id == ' ' or article_id is None:
        return jsonify({'code': 201, 'message': ' 该文章已被删除或不存在！'})
    # 浏览次数加1
    dbPerform(update_sql.format(article_id))
    result = dbPerforms(sql.format(article_id))
    title = result[0][0]
    content = result[0][1]
    views = result[0][2]
    release_time = result[0][3]
    get_time = time.localtime(int(release_time))
    ymd_time = time.strftime("%Y-%m-%d", get_time)
    return jsonify({
        'code': 200,
        'title': title,
        'content': content,
        'views': views,
        'time': ymd_time
    })

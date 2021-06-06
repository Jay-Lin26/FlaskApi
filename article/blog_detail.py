from common.db_utils import dbPerforms, dbPerform
from flask.blueprints import Blueprint
from flask import jsonify, request

blog_detail_Blue = Blueprint("blog_detail_Blue", __name__)


@blog_detail_Blue.route('/api/v1.0/article/detail', methods=['GET'])
def blog_detail():
    article_id = request.args.get('article_id')
    count_sql = """ SELECT count(*) FROM blog_show """
    sql = """SELECT `title`, `content` FROM blog_show WHERE id = '{}' """
    count_num = dbPerform(count_sql)
    if type(article_id) != 'int':
        return jsonify({'code': 201, 'message': ' 该文章已被删除或不存在！ '})
    elif int(article_id) > int(count_num) or article_id == '' or article_id is None:
        return jsonify({'code': 201, 'message': ' 该文章已被删除或不存在！ '})
    result = dbPerforms(sql.format(article_id))
    title = result[0][0]
    content= result[0][1]
    return jsonify({'code': 200, 'title': title, 'content': content})
from common.db_utils import dbPerforms
from flask.blueprints import Blueprint
from flask import jsonify

blog_detail_Blue = Blueprint("blog_detail_Blue", __name__)


@blog_detail_Blue.route('/api/v1.0/article/detail', methods=['GET'])
def blog_detail():
    sql = """SELECT `title`, `content` FROM blog_show WHERE id = '1' """
    result = dbPerforms(sql)
    title = result[0][0]
    content= result[0][1]

    return jsonify({'code': 200, 'title': title, 'content': content})
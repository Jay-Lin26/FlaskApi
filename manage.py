# coding = utf-8
import os
import sys

from flask import Flask
from flask import make_response, jsonify, request
from flask_cors import CORS
from config import *

from member.detail import detail_Blue
from member.login import login_Blue
from member.register import register_Blue
from member.users_list import users_List_Blue
from member.verification import verification_Blue
from article.article_index import article_index_Blue

current = os.getcwd()
sys.path.append(current)

app = Flask(__name__)
# 设置启动配置
app.config.from_pyfile('config.py')
# 解决跨域问题
CORS(app)
# 注册蓝图
app.register_blueprint(login_Blue)  # 登录
app.register_blueprint(register_Blue)
app.register_blueprint(verification_Blue)
app.register_blueprint(detail_Blue)  # 用户信息
app.register_blueprint(users_List_Blue)
app.register_blueprint(article_index_Blue)


@app.errorhandler(404)
def pageNotFound(error):
    return make_response(jsonify({'Error': 'An unknown error'}), 404)


@app.errorhandler(405)
def pageNotFound(error):
    return make_response(jsonify({'Error': 'An unknown error'}), 405)


@app.before_request
def version_check():
    version = request.headers.get('version')
    if version != VERSION:
        return jsonify({'Error': 'An unknown error'})


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)

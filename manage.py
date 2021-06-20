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
from member.list import list_Blue
from member.verification import verification_Blue
from article.index import index_Blue
from article.detail import detail_Blue

current = os.getcwd()
sys.path.append(current)

app = Flask(__name__)
# 设置启动配置
app.config.from_pyfile('config.py')
# 解决跨域问题
CORS(app)
# 注册蓝图 用户
app.register_blueprint(login_Blue)  # 登录
app.register_blueprint(register_Blue)
app.register_blueprint(verification_Blue)
app.register_blueprint(detail_Blue)  # 用户信息
app.register_blueprint(list_Blue)
# 注册蓝图 文章
app.register_blueprint(index_Blue)
app.register_blueprint(detail_Blue)


@app.errorhandler(404)
def pageNotFound(error):
    return make_response(jsonify({'Msg': '未知错误'}), 404)


@app.errorhandler(502)
def pageNotFound(error):
    return make_response(jsonify({'Msg': '服务器遇到了一点问题~~'}), 502)


@app.before_request
def version_check():
    version = request.headers.get('version')
    if version != VERSION:
        return jsonify({'Error': 'An unknown error'})


if __name__ == '__main__':
    app.run()

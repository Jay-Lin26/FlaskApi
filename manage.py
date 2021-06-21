# coding = utf-8
import os
import sys

from flask import Flask
from flask import make_response, jsonify, request
from flask_cors import CORS
from config import *

from member.detail import memberDetail_Blue
from member.login import login_Blue
from member.register import register_Blue
from member.list import memberList_Blue
from member.verification import verification_Blue
from article.index import articleIndex_Blue
from article.detail import articleDetail_Blue

current = os.getcwd()
sys.path.append(current)

app = Flask(__name__)
# 设置启动配置
app.config.from_pyfile('config.py')
# 解决跨域问题
CORS(app, supports_credentials=True)
# 注册蓝图 用户
app.register_blueprint(login_Blue)  # 登录
app.register_blueprint(register_Blue)
app.register_blueprint(verification_Blue)
app.register_blueprint(memberDetail_Blue)  # 用户信息
app.register_blueprint(memberList_Blue)
# 注册蓝图 文章
app.register_blueprint(articleIndex_Blue)
app.register_blueprint(articleDetail_Blue)


@app.errorhandler(404)
def pageNotFound(error):
    return make_response(jsonify({
        'code': 404,
        'Msg': '未知错误'
    }), 404)


@app.errorhandler(502)
def pageNotFound(error):
    return make_response(jsonify({
        'code': 502,
        'Msg': '服务器遇到了一点问题~~'
    }), 502)


@app.before_request
def version_check():
    version = request.headers.get('version')
    if version != VERSION:
        return jsonify({'Msg': '未知错误'})


if __name__ == '__main__':
    app.run()

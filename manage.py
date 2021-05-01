# coding = utf-8
from flask import Flask
from flask import make_response, jsonify, request
from flask_cors import CORS

from login_register.member import loginRegister
from login_register.demo import check_token
from userinfo.user import user

app = Flask(__name__)
# 设置启动配置
app.config["JSON_SORT_KEYS"] = False
# 解决跨域问题
CORS(app)
# 注册蓝图
app.register_blueprint(loginRegister)  # 登录注册/验证码
app.register_blueprint(user)  # 用户信息
app.register_blueprint(check_token)


@app.errorhandler(404)
def pageNotFound(error):
    return make_response(jsonify({'Error': 'Page Not Found'}), 404)


@app.errorhandler(405)
def pageNotFound(error):
    return make_response(jsonify({'Error': 'Page Not Found'}), 405)


@app.before_request
def version_check():
    version = request.headers.get('version')
    if version != '1.0':
        return jsonify({'Error': 'Page Not Found'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

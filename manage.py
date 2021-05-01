# coding = utf-8
from flask import Flask
from flask import make_response, jsonify
from flask_cors import CORS

from login_register.member import loginRegister
from userinfo.user import user

app = Flask(__name__)
# 解决跨域问题
CORS(app)
# 注册蓝图
app.register_blueprint(loginRegister)  # 登录注册/验证码
app.register_blueprint(user)  # 用户信息


@app.errorhandler(404)
def pageNotFound(error):
    return make_response(jsonify({'Error': 'Page Not Found'}), 404)


@app.errorhandler(405)
def pageNotFound(error):
    return make_response(jsonify({'Error': 'Page Not Found'}), 405)


@app.route('/')
def helloWord():
    return 'Welcome My Blog~~~'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

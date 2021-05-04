import re

from flask import Blueprint, jsonify, request

from common.email_utils import sendEmail

verification_Blue = Blueprint('verification', __name__)


@verification_Blue.route('/api/v1.0/member/verification', methods=['GET'], strict_slashes=False)
def sendVerification():
    # 发送验证码
    user_email = request.args.get('email')
    if user_email != '':
        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com]{1,3}$', user_email):
            sendEmail(user_email)
            return jsonify({'code': 200, 'message': 'Send a success'})
        else:
            return jsonify({'code': 3001, 'message': 'Please check your email format'})
    else:
        return jsonify({'code': 3002, 'message': 'Please entry your email'})

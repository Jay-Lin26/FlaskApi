# coding = utf-8
from flask import jsonify
from flask.blueprints import Blueprint

from member.utils import loginRequired

memberDetail_Blue = Blueprint('detail_Blue', __name__)


@memberDetail_Blue.route('/api/v1.0/member/detail/', methods=["GET"], strict_slashes=False)
@loginRequired
def memberDetail():
    return jsonify({"msg": "this is member info"})

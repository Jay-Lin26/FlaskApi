from flask.blueprints import Blueprint
from flask import jsonify

tagDetail_Blue = Blueprint("tagDetail", __name__)


@tagDetail_Blue.route("/api/v1.0/category/detail", methods=["get"], strict_slashes=False)
def tagDetail():
    sql = " "

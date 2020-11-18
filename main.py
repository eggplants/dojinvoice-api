from typing import Any, TypedDict, cast

from flask import Blueprint, Flask, jsonify, request
from werkzeug.datastructures import ImmutableMultiDict

from db import DojinvoiceDB

DB = DojinvoiceDB()
app = Flask(__name__)
v1 = Blueprint("version1", "version1")


class Params(TypedDict):
    offset: int
    random: bool
    page: int
    keyword: str
    category: str
    rate: int
    genre: str
    illustrator: str
    musician: str
    scenario: str
    voice: str
    writer: str


def res_ok(data: Any, status: int) -> Any:
    return jsonify({'data': data}), status


def get_params(args: ImmutableMultiDict[Any, Any]):
    params = cast(Params, {})
    params['offset'] = args.get('offset', default=20, type=int)
    params['random'] = args.get('random', default=True, type=bool)
    params['page'] = args.get('page', default=1, type=int)
    params['keyword'] = args.get('keyword', default='', type=str)
    params['category'] = args.get('category', default='', type=str)
    params['rate'] = args.get('rate', default=1, type=int)
    params['genre'] = args.get('genre', default=1, type=str)
    params['illustrator'] = args.get('illustrator', default=1, type=str)
    params['musician'] = args.get('musician', default=1, type=str)
    params['scenario'] = args.get('scenario', default=1, type=str)
    params['voice'] = args.get('voice', default=1, type=str)
    params['writer'] = args.get('writer', default=1, type=str)
    return params


@v1.route("/search", methods=['GET'])
def index():
    args = request.args
    params = get_params(args)
    return res_ok(DB.search(params), 200)


@v1.route("/category_list")
def category():
    return jsonify({'data': DB.get_category_list()}), 200


@v1.route("/chobit_list")
def chobit():
    return jsonify({'data': DB.get_exist_chobit_list()}), 200


if __name__ == "__main__":
    app.register_blueprint(v1, url_prefix="/v1")
    app.run(host='0.0.0.0', debug=True)

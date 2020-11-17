from typing import Any, Dict, TypedDict, cast

from flask import Blueprint, Flask, jsonify, request

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


def get_params(args):
    params = cast(Params, {})
    params['offset'] = args.get('offset', default=20, type=int)
    params['random'] = args.get('random', default=True, type=bool)
    params['page'] = args.get('page', default=1, type=int)
    params['keyword'] = args.get('keyword', default='', type=str)
    params['category'] = args.get('category', default='', type=str)
    params['rate'] = args.get('rate', default=1, type=int)
    params['genre'] = args.get('rate', default=1, type=int)
    params['illustrator'] = args.get('rate', default=1, type=int)
    params['musician'] = args.get('rate', default=1, type=int)
    params['scenario'] = args.get('rate', default=1, type=int)
    params['voice'] = args.get('rate', default=1, type=int)
    params['writer'] = args.get('rate', default=1, type=int)
    return params


@v1.route("/search", methods=['GET'])
def index():
    args = request.args
    params = get_params(args)
    return res_ok(DB.search(params), 200)


@v1.route("/category_list")
def category():
    return jsonify({'data': DB.get_exist_chobit_list()}), 200


@v1.route("/chobit_list")
def chobit():
    return jsonify({'data': DB.get_exist_chobit_list()}), 200


if __name__ == "__main__":
    app.register_blueprint(v1, url_prefix="/v1")
    app.run(host='0.0.0.0', debug=True)

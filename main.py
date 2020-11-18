#!/usr/bin/env python
from os.path import join
from typing import Any, TypedDict, cast

from flask import Blueprint, Flask, jsonify, send_from_directory

from db import DojinvoiceDB

DB = DojinvoiceDB()
app = Flask(__name__)
v1 = Blueprint('version1', 'version1')


class Params(TypedDict):
    offset: int
    random: bool
    page: int
    keyword: str
    category: str
    max_rate: float
    min_rate: float
    genre: str
    illustrator: str
    musician: str
    scenario: str
    voice: str
    writer: str
    filter_rate: bool


def res_ok(data: Any, status: int) -> Any:
    try:
        data = data
        json = jsonify({'data': data})
        return json, status
    except Exception as e:
        return {'err': e}, 500


def get_params(args) -> Params:
    params = cast(Params, {})
    params['offset'] = args.get('offset', default=20, type=int)
    params['random'] = args.get('random', default=True, type=bool)
    params['page'] = args.get('page', default=1, type=int)
    params['keyword'] = args.get('keyword', default='', type=str)
    params['category'] = args.get('category', default='', type=str)
    params['filter_rate'] = args.get('filter_rate', default=False, type=bool)
    params['max_rate'] = args.get('max_rate', default=5.0, type=float)
    params['min_rate'] = args.get('min_rate', default=0.0, type=float)
    params['genre'] = args.get('genre', default='', type=str)
    params['illustrator'] = args.get('illustrator', default='', type=str)
    params['musician'] = args.get('musician', default='', type=str)
    params['scenario'] = args.get('scenario', default='', type=str)
    params['voice'] = args.get('voice', default='', type=str)
    params['writer'] = args.get('writer', default='', type=str)
    return params


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(join(app.root_path, 'static/img'), 'favicon.ico')


@v1.route('/')
def index():
    return res_ok([str(_) for _ in app.url_map.iter_rules()], 200)


# @v1.route('/search', methods=['GET'])
# def search():
#     args = request.args
#     params = get_params(args)
#     return res_ok(DB.search(params), 200)


@ v1.route('/category')
def category():
    return res_ok(DB.get_category_list(), 200)


@ v1.route('/rate')
def rate():
    return res_ok(DB.get_rate_filtered_list(1.0, 5.0), 200)


@ v1.route('/chobit')
def chobit():
    return res_ok(DB.get_exist_chobit_list(), 200)


@ v1.route('/illustrator')
def illustrator():
    return res_ok(DB.get_illustrator_list(), 200)


@ v1.route('/musician')
def musician():
    return res_ok(DB.get_musician_list(), 200)


@ v1.route('/scenario')
def scenario():
    return res_ok(DB.get_scenario_list(), 200)


@ v1.route('/voice')
def voice():
    return res_ok(DB.get_voice_list(), 200)


@ v1.route('/writer')
def writer():
    return res_ok(DB.get_writer_list(), 200)


@ v1.route('/genre')
def genre():
    return res_ok(DB.get_genre_list(), 200)


def main():
    app.register_blueprint(v1, url_prefix='/v1')
    debug = True
    host = '0.0.0.0'
    app.run(
        # host=host, debug=debug
    )


if __name__ == '__main__':
    main()

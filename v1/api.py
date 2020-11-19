from typing import Any, TypedDict, cast

from db import DojinvoiceDB
from flask import Blueprint, jsonify

# Blueprintのオブジェクトを生成する
app = Blueprint('v1', __name__)
DB = DojinvoiceDB()


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


@app.route('/v1/')
def v1_index():
    return res_ok("there is no content.", 404)


# @app.route('/search', methods=['GET'])
# def search():
#     args = request.args
#     params = get_params(args)
#     return res_ok(DB.search(params), 200)


@app.route('/v1/category')
def category():
    return res_ok(DB.get_category_list(), 200)


@app.route('/v1/rate')
def rate():
    return res_ok(DB.get_rate_filtered_list(1.0, 5.0), 200)


@app.route('/v1/chobit')
def chobit():
    return res_ok(DB.get_exist_chobit_list(), 200)


@app.route('/v1/illustrator')
def illustrator():
    return res_ok(DB.get_illustrator_list(), 200)


@app.route('/v1/musician')
def musician():
    return res_ok(DB.get_musician_list(), 200)


@app.route('/v1/scenario')
def scenario():
    return res_ok(DB.get_scenario_list(), 200)


@app.route('/v1/voice')
def voice():
    return res_ok(DB.get_voice_list(), 200)


@app.route('/v1/writer')
def writer():
    return res_ok(DB.get_writer_list(), 200)


@app.route('/v1/genre')
def genre():
    return res_ok(DB.get_genre_list(), 200)

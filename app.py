#!/usr/bin/env python
from os import environ
from os.path import join
from typing import Any

from flask import Flask, jsonify, send_from_directory

from v1 import api

app = Flask(__name__)
app.register_blueprint(api.app)


def res_ok(data: Any, status: int) -> Any:
    try:
        data = data
        json = jsonify({'data': data})
        return json, status
    except Exception as e:
        return {'err': e}, 500


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(join(app.root_path, 'static/img'),
                               'favicon.ico')


@app.route('/')
def index():
    return res_ok(['v1'], 200)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(environ.get("PORT", 5000)), debug=True)

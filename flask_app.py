from flask import Flask, abort, jsonify
from flask_caching import Cache
from flask_cors import CORS

import main

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/')
@cache.cached(timeout=3600)
def nbis_list_entities():
    return jsonify({'entities': ['restaurant']})


@app.route('/restaurant/')
@cache.cached(timeout=3600)
def nbis_api_list_restaurants():
    return jsonify({'restaurants': main.list_restaurants()})


@app.route('/restaurant/<name>/')
@cache.cached(timeout=3600)
def nbis_api_get_restaurant(name):
    data = main.get_restaurant(name)
    if not data:
        abort(status=404)
    data['menu'] = [{'dish': entry} for entry in data['menu']]
    return jsonify({'restaurant': data})

#!/usr/bin/python
from flask import Flask
from flask import jsonify
from flask import make_response
from flask import request

from send_hub import calculate_routes
from send_hub import backend_resources

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)



@app.route('/')
def index():
    return "sendHub"

@app.route('/relays', methods=['GET'])
def get_relays():
    return jsonify(resources=backend_resources)

@app.route('/relays/routes', methods=['GET'])
def get_relays_routes():
    return jsonify(message="hi")


@app.route('/relays/routes', methods=['POST'])
def post_relays_routes():
    assert "message" in request.json and "recipients" in request.json
    print( request.json )
    return jsonify( calculate_routes("hi",["one","two"],sort_resources=True) )


if __name__ == '__main__':
    app.run(debug=True)

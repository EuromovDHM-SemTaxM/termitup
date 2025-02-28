"""A Python Flask REST API BoilerPlate (CRUD) Style"""
import logging
import sys

from modules_api.configuration import PARAMS
from modules_api.utils.logging import setup_logging

"""prueba"""
import argparse
import os
from flask import Flask, jsonify, make_response, render_template
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
import request_api


APP = Flask(__name__)

setup_logging(console_log_output="stdout", console_log_level="debug", console_log_color=True,
                          logfile_file=PARAMS['logfile_location'], logfile_log_level="warn", logfile_log_color=False,
                          log_line_template="%(color_on)s[%(created)d] [%(threadName)s] [%(levelname)-8s] %(message)s%(color_off)s")

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Termitup"
    }
)
APP.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###


APP.register_blueprint(request_api.get_blueprint())


@APP.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@APP.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@APP.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found - correct /swagger/'}), 404)


@APP.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)


@APP.errorhandler(504)
def handle_504_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Term not found'}), 504)


@APP.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':

    PARSER = argparse.ArgumentParser(
        description="Seans-Python-Flask-REST-Boilerplate")

    PARSER.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    PORT = int(os.environ.get('PORT', 4053))

    if ARGS.debug:
        print("Running in debug mode")
        CORS = CORS(APP)
        APP.run(host='0.0.0.0', port=PORT, debug=True)
    else:
        APP.run(host='0.0.0.0', port=PORT, debug=False)

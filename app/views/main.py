import json

from flask import Blueprint, render_template, jsonify, make_response
from werkzeug.exceptions import abort

bp = Blueprint("bp_main", __name__)


# Here you can read about routing:
# https://flask.palletsprojects.com/en/2.2.x/api/#url-route-registrations
# https://hackersandslackers.com/flask-routes/

@bp.route('/', methods=['GET'])
def main_get():
    return render_template('main.jinja')

a = 0
@bp.route('/check', methods=['GET'])
def test():
    global a
    a += 1
    return {'a': a}
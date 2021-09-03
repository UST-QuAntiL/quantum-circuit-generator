from flask import Blueprint

api = Blueprint('api', __name__)

from . import encoding_controller, error_controller
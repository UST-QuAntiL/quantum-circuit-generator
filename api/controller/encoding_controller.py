from . import api
from ..services import encoding_service
from flask import request


@api.route("/", methods=["GET", "POST"])
def index():
    return "<h1>Quantum Circuit Generator is Running!!!</h1>"


@api.route("/encoding/<name>", methods=["POST"])
def encoding(name):
    if name and request.json:
        return encoding_service.handle_encoding(name, request.json)

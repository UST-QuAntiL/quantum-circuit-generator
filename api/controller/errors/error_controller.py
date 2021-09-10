from flask import request, jsonify
from flask_smorest import Blueprint

blp = Blueprint(
    "errors",
    __name__,
)

# TODO Hide errors as soon as Feature is released - waiting for pull request to be accepated
# https://github.com/marshmallow-code/flask-smorest/pull/277
#  hidden_from_api_spec=True


@blp.app_errorhandler(404)
def page_not_found(e):
    if (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    ):
        response = jsonify({"error" "not found"})
        response.statuscode = 404
        return response
    return "<h1>page not found</h1>", 404


@blp.app_errorhandler(500)
def internal_sever_error(e):
    if (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    ):
        response = jsonify({"error" "internal server error"})
        response.statuscode = 500
        return response
    return "<h1>internal server error</h1>", 500


@blp.route("/", methods=["GET", "POST"])
def index():
    return "<h1>Quantum Circuit Generator is Running!!!</h1>"


def bad_request(message):
    response = jsonify({"error": "bad request", "message": message})
    response.status_code = 400
    return response

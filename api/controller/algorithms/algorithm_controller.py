from flask_smorest import Blueprint
from flask import request
from ...model.circuit_response import CircuitResponseSchema


blp = Blueprint(
    "algorithms",
    __name__,
    url_prefix="/algorithms",
    description="get quantum circuit algorithms",
)

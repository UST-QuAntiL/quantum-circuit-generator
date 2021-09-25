from flask_smorest import Blueprint
from flask import request
from api.services import algorithm_service
from ...model.circuit_response import CircuitResponseSchema
from ...model.algorithm_request import (
        HHLAlgorithmRequestSchema,
        HHLAlgorithmRequest
        )


blp = Blueprint(
    "algorithms",
    __name__,
    url_prefix="/algorithms",
    description="get quantum circuit algorithms",
)


@blp.route("/hhl", methods=["POST"])
@blp.etag
@blp.arguments(
    HHLAlgorithmRequestSchema,
    example=dict(matrix=[[1.5, 0.5], [0.5, 1.5]], vector=[0, 1]),
)
@blp.response(200, CircuitResponseSchema)
def encoding(json: HHLAlgorithmRequest):
    if json:
        return algorithm_service.generate_hhl_algorithm(json)

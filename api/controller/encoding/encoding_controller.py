from flask_smorest import Blueprint
from api.services import encoding_service
from flask import request
from ...model.circuit_response import CircuitResponseSchema
from ...model.encoding_request import (
    BasisEncodingRequestSchema,
    AngleEncodingRequestSchema,
    AmplitudeEncodingRequestSchema,
    SchmidtDecompositionRequestSchema,
)

blp = Blueprint(
    "encodings",
    __name__,
    url_prefix="/encoding",
    description="get quantum circuit encodings",
)


@blp.route("/basis", methods=["POST"])
@blp.etag
@blp.arguments(
    BasisEncodingRequestSchema,
    example=dict(vector=[1.25, 3.14], integral_bits=3, fractional_bits=3),
)
@blp.response(200, CircuitResponseSchema)
def encoding(name):
    if name and request.json:
        return encoding_service.generate_basis_encoding(request.json)


@blp.route("/angle", methods=["POST"])
@blp.etag
@blp.arguments(
    AngleEncodingRequestSchema, example=dict(vector=[1.25, 3.14], rotationaxis="x")
)
@blp.response(200, CircuitResponseSchema)
def encoding(name):
    if name and request.json:
        return encoding_service.generate_angle_encoding(request.json)


@blp.route("/amplitude", methods=["POST"])
@blp.etag
@blp.arguments(AmplitudeEncodingRequestSchema, example=dict(vector=[1.25, 3.14]))
@blp.response(200, CircuitResponseSchema)
def encoding(name):
    if name and request.json:
        return encoding_service.generate_amplitude_encoding(request.json)


@blp.route("/schmidt", methods=["POST"])
@blp.etag
@blp.arguments(
    SchmidtDecompositionRequestSchema, example=dict(vector=[1.25, 3.14, 0, 1])
)
@blp.response(200, CircuitResponseSchema)
def encoding(name):
    if name and request.json:
        return encoding_service.generate_schmidt_decomposition(request.json)


# TODO
# @blp.route("/quam", methods=["POST"])
# @blp.etag
# @blp.arguments(QuamEncodingRequestSchema, example=dict(vector=[1.25, 3.14], n_integral_bits=3, n_fractional_bits=3))
# @blp.response(200,CircuitResponseSchema)
# def encoding(name):
#     if name and request.json:
#         return encoding_service.handle_encoding(name, request.json)

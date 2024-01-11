from flask_smorest import Blueprint
from app.services import encoding_service
from app.model.circuit_response import (
    SchmidtDecompositionResponseSchema,
    AmplitudeEncodingResponseSchema,
    AngleEncodingResponseSchema,
    BasisEncodingResponseSchema,
)
from app.model.encoding_request import (
    BasisEncodingRequestSchema,
    AngleEncodingRequestSchema,
    AmplitudeEncodingRequestSchema,
    SchmidtDecompositionRequestSchema,
    SchmidtDecompositionRequest,
    AmplitudeEncodingRequest,
    AngleEncodingRequest,
    BasisEncodingRequest,
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
    example=dict(
        vector=[1.25, 3.14],
        integral_bits=3,
        fractional_bits=3,
        circuit_format="openqasm2",
    ),
)
@blp.response(200, BasisEncodingResponseSchema)
def encoding(json: BasisEncodingRequest):
    if json:
        return encoding_service.generate_basis_encoding(BasisEncodingRequest(**json))


@blp.route("/angle", methods=["POST"])
@blp.etag
@blp.arguments(
    AngleEncodingRequestSchema,
    example=dict(vector=[1.25, 3.14], rotation_axis="x", circuit_format="openqasm2"),
)
@blp.response(200, AngleEncodingResponseSchema)
def encoding(json: AngleEncodingRequest):
    if json:
        return encoding_service.generate_angle_encoding(AngleEncodingRequest(**json))


@blp.route("/amplitude", methods=["POST"])
@blp.etag
@blp.arguments(
    AmplitudeEncodingRequestSchema,
    example=dict(vector=[1.25, 3.14], circuit_format="openqasm2"),
)
@blp.response(200, AmplitudeEncodingResponseSchema)
def encoding(json: AmplitudeEncodingRequest):
    if json:
        return encoding_service.generate_amplitude_encoding(
            AmplitudeEncodingRequest(**json)
        )


@blp.route("/schmidt", methods=["POST"])
@blp.arguments(
    SchmidtDecompositionRequestSchema,
    example=dict(vector=[1.25, 3.14, 0, 1], circuit_format="openqasm2"),
)
@blp.response(200, SchmidtDecompositionResponseSchema)
def encoding(json: SchmidtDecompositionRequest):
    if json:
        return encoding_service.generate_schmidt_decomposition(
            SchmidtDecompositionRequest(**json)
        )


# TODO
# @blp.route("/quam", methods=["POST"])
# @blp.etag
# @blp.arguments(QuamEncodingRequestSchema, example=dict(vector=[1.25, 3.14], n_integral_bits=3, n_fractional_bits=3), circuit_format="openqasm2")
# @blp.response(200,CircuitResponseSchema)
# def encoding(name):
#     if name and request.json:
#         return encoding_service.handle_encoding(name, request.json)

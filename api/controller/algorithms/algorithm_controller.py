from flask_smorest import Blueprint
from flask import request
from api.services import algorithm_service
from ...model.circuit_response import (
    CircuitResponseSchema,
    HHLResponseSchema,
    QAOAResponseSchema,
    VQLSResponseSchema,
    QFTResponseSchema,
)
from ...model.algorithm_request import (
    HHLAlgorithmRequestSchema,
    HHLAlgorithmRequest,
    QAOAAlgorithmRequestSchema,
    QAOAAlgorithmRequest,
    VQLSAlgorithmRequestSchema,
    VQLSAlgorithmRequest,
    QFTAlgorithmRequestSchema,
    QFTAlgorithmRequest,
)


blp = Blueprint(
    "algorithms",
    __name__,
    url_prefix="/algorithms",
    description="get quantum circuit algorithms",
)


@blp.route("/hhl", methods=["POST"])
@blp.arguments(
    HHLAlgorithmRequestSchema,
    example=dict(matrix=[[1.5, 0.5], [0.5, 1.5]], vector=[0, 1]),
)
@blp.response(200, HHLResponseSchema)
def encoding(json: HHLAlgorithmRequest):
    if json:
        return algorithm_service.generate_hhl_circuit(json)


@blp.route("/qaoa", methods=["POST"])
@blp.arguments(
    QAOAAlgorithmRequestSchema,
    example=dict(
        pauli_op_string="0.5 * ((I^Z^Z) + (Z^I^Z) + (Z^Z^I))",
        reps=2,
        gammas=[1.0, 1.2],
        betas=[0.4, 0.7],
    ),
)
@blp.response(200, QAOAResponseSchema)
def encoding(json: QAOAAlgorithmRequest):
    if json:
        return algorithm_service.generate_qaoa_circuit(json)


@blp.route("/vqls", methods=["POST"])
@blp.arguments(
    VQLSAlgorithmRequestSchema,
    example=dict(
        matrix=[[1.0, 2.0], [2.0, -1.0]],
        vector=[0, 1],
        alphas=[1] * 8,
        l=0,
        lp=0,
        ansatz="EfficientSU2",
    ),
)
@blp.response(200, VQLSResponseSchema)
def encoding(json: VQLSAlgorithmRequest):
    if json:
        return algorithm_service.generate_vqls_circuit(json)


@blp.route("/qft", methods=["POST"])
@blp.arguments(
    QFTAlgorithmRequestSchema,
    example=dict(
        n_qubits=4,
    ),
)
@blp.response(200, QFTResponseSchema)
def encoding(json: QFTAlgorithmRequest):
    if json:
        return algorithm_service.generate_qft_circuit(json)

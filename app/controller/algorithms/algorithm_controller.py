from flask_smorest import Blueprint

from app.services import algorithm_service
from app.model.circuit_response import (
    CircuitResponseSchema,
    HHLResponseSchema,
    QAOAResponseSchema,
    QFTResponseSchema,
    QPEResponseSchema,
    VQEResponseSchema,
    GroverResponseSchema,
)
from app.model.algorithm_request import (
    HHLAlgorithmRequestSchema,
    HHLAlgorithmRequest,
    QAOAAlgorithmRequestSchema,
    QAOAAlgorithmRequest,
    QFTAlgorithmRequestSchema,
    QFTAlgorithmRequest,
    QPEAlgorithmRequestSchema,
    QPEAlgorithmRequest,
    VQEAlgorithmRequestSchema,
    VQEAlgorithmRequest,
    GroverAlgorithmRequestSchema,
    GroverAlgorithmRequest,
    TSPQAOAAlgorithmRequest,
    TSPQAOAAlgorithmRequestSchema,
    MaxCutQAOAAlgorithmRequestSchema,
    MaxCutQAOAAlgorithmRequest,
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


@blp.route("/qft", methods=["POST"])
@blp.arguments(
    QFTAlgorithmRequestSchema,
    example=dict(
        n_qubits=4,
        inverse=False,
        barriers=True,
    ),
)
@blp.response(200, QFTResponseSchema)
def encoding(json: QFTAlgorithmRequest):
    if json:
        return algorithm_service.generate_qft_circuit(json)


@blp.route("/qpe", methods=["POST"])
@blp.arguments(
    QPEAlgorithmRequestSchema,
    example=dict(
        n_eval_qubits=3,
        unitary='OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[1];\np(pi/2) q[0];\n',
    ),
)
@blp.response(200, QPEResponseSchema)
def encoding(json: QPEAlgorithmRequest):
    if json:
        return algorithm_service.generate_qpe_circuit(json)


@blp.route("/vqe", methods=["POST"])
@blp.arguments(
    VQEAlgorithmRequestSchema,
    example=dict(
        parameters=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
        observable="Z^Y",
    ),
)
@blp.response(200, VQEResponseSchema)
def encoding(json: VQEAlgorithmRequest):
    if json:
        return algorithm_service.generate_vqe_circuit(json)


@blp.route("/grover", methods=["POST"])
@blp.arguments(
    GroverAlgorithmRequestSchema,
    example=dict(
        oracle='OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[3];\nccx q[0],q[1],q[2];\n',
        initial_state='OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[3];\nx q[0];\ny q[1];\nz q[2];\n',
        iterations=2,
        reflection_qubits=[0, 1],
        barriers=True,
    ),
)
@blp.response(200, GroverResponseSchema)
def encoding(json: GroverAlgorithmRequest):
    if json:
        return algorithm_service.generate_grover_circuit(json)


@blp.route("/tspqaoa", methods=["POST"])
@blp.etag
@blp.arguments(
    TSPQAOAAlgorithmRequestSchema,
    example=dict(
        adj_matrix=[[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 0]],
        p=2,
        betas=[1.0, 2.0],
        gammas=[1.0, 3.0],
    ),
    description="Currently, only 3x3 and 4x4 matrices supported.",
)
@blp.response(200, CircuitResponseSchema)
def encoding(json: TSPQAOAAlgorithmRequest):
    if json:
        return algorithm_service.generate_tsp_qaoa_circuit(json)


@blp.route("/maxcutqaoa", methods=["POST"])
@blp.etag
@blp.arguments(
    MaxCutQAOAAlgorithmRequestSchema,
    example=dict(
        adj_matrix=[[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 0]],
        beta=1.0,
        gamma=1.0,
    ),
)
@blp.response(200, CircuitResponseSchema)
def encoding(json: MaxCutQAOAAlgorithmRequest):
    if json:
        return algorithm_service.generate_max_cut_qaoa_circuit(json)
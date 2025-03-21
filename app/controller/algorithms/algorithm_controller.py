from flask_smorest import Blueprint
from qiskit import QuantumCircuit

from app.helpermethods import visualizeQasm
from app.services import algorithm_service
from app.model.circuit_response import (
    CircuitResponseSchema,
    HHLResponseSchema,
    QAOAResponseSchema,
    QFTResponseSchema,
    QPEResponseSchema,
    VQEResponseSchema,
    GroverResponseSchema,
    CircuitDrawResponseSchema, CircuitDrawResponse,
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
    KnapsackQAOAAlgorithmRequest,
    KnapsackQAOAAlgorithmRequestSchema,
    CircuitDrawRequestSchema,
    CircuitDrawRequest,
    ShorDiscreteLogAlgorithmRequest,
    ShorDiscreteLogAlgorithmRequestSchema,
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
    example=dict(
        matrix=[[1.5, 0.5], [0.5, 1.5]], vector=[0, 1], circuit_format="openqasm2"
    ),
)
@blp.response(200, HHLResponseSchema)
def encoding(json: HHLAlgorithmRequest):
    if json:
        return algorithm_service.generate_hhl_circuit(HHLAlgorithmRequest(**json))


@blp.route("/qaoa/pauliOperator", methods=["POST"])
@blp.arguments(
    QAOAAlgorithmRequestSchema,
    example=dict(
        pauli_op_string="0.5 * ((I^Z^Z) + (Z^I^Z) + (Z^Z^I))",
        reps=2,
        gammas=[1.0, 1.2],
        betas=[0.4, 0.7],
        circuit_format="openqasm2",
    ),
)
@blp.response(200, QAOAResponseSchema)
def encoding(json: QAOAAlgorithmRequest):
    if json:
        return algorithm_service.generate_qaoa_circuit(QAOAAlgorithmRequest(**json))


@blp.route("/qft", methods=["POST"])
@blp.arguments(
    QFTAlgorithmRequestSchema,
    example=dict(n_qubits=4, inverse=False, barriers=True, circuit_format="openqasm2"),
)
@blp.response(200, QFTResponseSchema)
def encoding(json: QFTAlgorithmRequest):
    if json:
        return algorithm_service.generate_qft_circuit(QFTAlgorithmRequest(**json))


@blp.route("/qpe", methods=["POST"])
@blp.arguments(
    QPEAlgorithmRequestSchema,
    example=dict(
        n_eval_qubits=3,
        unitary='OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[1];\np(pi/2) q[0];\n',
        circuit_format="openqasm2",
    ),
)
@blp.response(200, QPEResponseSchema)
def encoding(json: QPEAlgorithmRequest):
    if json:
        return algorithm_service.generate_qpe_circuit(QPEAlgorithmRequest(**json))


@blp.route("/vqe", methods=["POST"])
@blp.arguments(
    VQEAlgorithmRequestSchema,
    example=dict(
        parameters=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
        observable="Z^Y",
        circuit_format="openqasm2",
    ),
)
@blp.response(200, VQEResponseSchema)
def encoding(json: VQEAlgorithmRequest):
    if json:
        return algorithm_service.generate_vqe_circuit(VQEAlgorithmRequest(**json))


@blp.route("/grover", methods=["POST"])
@blp.arguments(
    GroverAlgorithmRequestSchema,
    example=dict(
        oracle='OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[3];\nccx q[0],q[1],q[2];\n',
        initial_state='OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[3];\nx q[0];\ny q[1];\nz q[2];\n',
        iterations=2,
        reflection_qubits=[0, 1],
        barriers=True,
        circuit_format="openqasm2",
    ),
)
@blp.response(200, GroverResponseSchema)
def encoding(json: GroverAlgorithmRequest):
    if json:
        return algorithm_service.generate_grover_circuit(GroverAlgorithmRequest(**json))


@blp.route("/qaoa/tsp", methods=["POST"])
@blp.arguments(
    TSPQAOAAlgorithmRequestSchema,
    example=dict(
        adj_matrix=[[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 0]],
        p=2,
        betas=[1.0, 2.0],
        gammas=[1.0, 3.0],
        circuit_format="openqasm2",
    ),
    description="Currently, only 3x3 and 4x4 matrices supported.",
)
@blp.response(200, CircuitResponseSchema)
def encoding(json):
    if json:
        return algorithm_service.generate_tsp_qaoa_circuit(
            TSPQAOAAlgorithmRequest(**json)
        )


@blp.route("/qaoa/maxcut", methods=["POST"])
@blp.etag
@blp.arguments(
    MaxCutQAOAAlgorithmRequestSchema,
    example=dict(
        adj_matrix=[[0, 1, 1, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 0]],
        betas=[1.0],
        gammas=[1.0],
        p=1,
        parameterized=False,
        circuit_format="openqasm2",
    ),
)
@blp.response(200, CircuitResponseSchema)
def get_maxcut_circuit(json: dict):
    if json:
        return algorithm_service.generate_max_cut_qaoa_circuit(
            MaxCutQAOAAlgorithmRequest(**json)
        )


@blp.route("/qaoa/knapsack", methods=["POST"])
@blp.etag
@blp.arguments(
    KnapsackQAOAAlgorithmRequestSchema,
    example=dict(
        items=[
            {"value": 5, "weight": 2},
            {"value": 2, "weight": 1},
            {"value": 3, "weight": 2},
        ],
        max_weights=20,
        p=1,
        betas=[1.0],
        gammas=[1.0],
        circuit_format="openqasm2",
    ),
)
@blp.response(200, CircuitResponseSchema)
def get_knapsack_circuit(json: KnapsackQAOAAlgorithmRequest):
    if json:
        return algorithm_service.generate_knapsack_qaoa_circuit(
            KnapsackQAOAAlgorithmRequest(**json)
        )


@blp.route("/shor/discreteLog", methods=["POST"])
@blp.etag
@blp.arguments(
    ShorDiscreteLogAlgorithmRequestSchema,
    example=dict(b=2, g=5, p=7),
    description="""
        b: Finds discrete logarithm of b with respect to generator g and module p
        g: Generator
        p: Prime module
        n: The size of the top register, if not given it will be inferred from the module p""",
)
@blp.response(200, CircuitResponseSchema)
def get_shor_circuit(json: ShorDiscreteLogAlgorithmRequest):
    if json:
        return algorithm_service.generate_shor_discrete_log_circuit(
            ShorDiscreteLogAlgorithmRequest(**json)
        )


@blp.route("/drawCircuit", methods=["POST"])
@blp.arguments(
    CircuitDrawRequestSchema,
    example=dict(circuit="OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[4];\ncreg meas[4];\nh q[0];\nh q[1];\nrzz(1.0) q[0],q[1];\nh q[2];\nrzz(1.0) q[0],q[2];\nrx(2.0) q[0];\nrzz(1.0) q[1],q[2];\nh q[3];\nrzz(1.0) q[1],q[3];\nrx(2.0) q[1];\nrzz(1.0) q[2],q[3];\nrx(2.0) q[2];\nrx(2.0) q[3];\nbarrier q[0],q[1],q[2],q[3];\nmeasure q[0] -> meas[0];\nmeasure q[1] -> meas[1];\nmeasure q[2] -> meas[2];\nmeasure q[3] -> meas[3];\n", circuit_format="openqasm2"),
    description="QASM 2.0 String.",
)
@blp.response(200, CircuitDrawResponseSchema)
def encoding(json):
    if json:
        return CircuitDrawResponse(visualizeQasm(QuantumCircuit.from_qasm_str(CircuitDrawRequest(**json).circuit)))

import codecs
import pickle

import numpy as np

from app.model.algorithm_request import MaxCutQAOAAlgorithmRequest
from app.services.algorithms.knapsack_qaoa_algorithm import KnapsackQAOAAlgorithm
from app.services.algorithms.maxcut_qaoa_algorithm import MaxCutQAOAAlgorithm
from app.services.algorithms.maxcut_qaoa_warm_start_algorithm import (
    MaxCutQAOAWarmStartAlgorithm,
)
from app.services.algorithms.tsp_qaoa_algorithm import TSPQAOAAlgorithm
from qiskit.circuit.quantumcircuit import QuantumCircuit
from app.services.algorithms.hhl_algorithm import HHLAlgorithm
from app.services.algorithms.qaoa_algorithm import QAOAAlgorithm
from app.services.algorithms.qft_algorithm import QFTAlgorithm
from app.services.algorithms.qpe_algorithm import QPEAlgorithm
from app.services.algorithms.vqe_algorithm import VQEAlgorithm
from app.services.algorithms.grover_algorithm import GroverAlgorithm
from app.services.algorithms.pauliParser import PauliParser
from app.services.helper_service import bad_request
from app.model.circuit_response import CircuitResponse


def generate_hhl_circuit(input):
    matrix = input.get("matrix")
    vector = input.get("vector")

    # Check types and dimensions
    matrix_array = np.array(matrix)
    vector_array = np.array(vector)
    if matrix_array.shape[0] != matrix_array.shape[1]:
        return bad_request("Invalid matrix input! Matrix must be square.")
    hermitian = np.allclose(matrix_array, matrix_array.conj().T)
    if not hermitian:
        return bad_request("Invalid matrix input! Matrix must be hermitian.")
    if matrix_array.shape[0] != vector_array.shape[0]:
        return bad_request(
            "Invalid matrix, vector input! Matrix and vector must be of the same dimension."
        )
    if np.log2(matrix_array.shape[0]) % 1 != 0:
        return bad_request("Invalid matrix input! Input matrix dimension must be 2^n.")

    circuit = HHLAlgorithm.create_circuit(matrix, vector)
    return CircuitResponse(
        circuit.qasm(),
        "algorithm/hhl",
        circuit.num_qubits,
        circuit.depth(),
        input,
        circuit_language="openqasm",
    )


def generate_qaoa_circuit(input):
    initial_state = input.get("initial_state")
    pauli_op_string = input.get("pauli_op_string")
    mixer = input.get("mixer")
    reps = input.get("reps")
    gammas = input.get("gammas")
    betas = input.get("betas")

    # check initial state (qasm string)
    try:
        if initial_state is not None:
            initial_state = QuantumCircuit.from_qasm_str(initial_state)
    except Exception as err:
        return bad_request("Invalid initial_state: " + str(err))
    # check Pauli string
    try:
        pauli_op = PauliParser.parse(pauli_op_string)
    except ValueError as err:
        return bad_request("Invalid pauli_op_string: " + str(err))
    # check mixer (qasm string or pauli operator string)
    try:
        if mixer is not None:
            if mixer.startswith("OPENQASM"):
                # OPENQASM String
                mixer = QuantumCircuit.from_qasm_str(mixer)
            else:
                # pauli operator string
                mixer = PauliParser.parse(mixer)
    except Exception as err:
        return bad_request("Invalid mixer: " + str(err))
    # check angle input
    if len(gammas) != reps or (betas is not None and len(betas) != reps):
        return bad_request(
            f"Number of angles and repetitions don't match. You specified {len(gammas)} gamma(s) and {len(betas)} beta(s) for {reps} repetition(s)."
        )

    circuit = QAOAAlgorithm.create_circuit(
        initial_state, pauli_op, mixer, reps, gammas, betas
    )
    return CircuitResponse(
        circuit.qasm(),
        "algorithm/qaoa",
        circuit.num_qubits,
        circuit.depth(),
        input,
        circuit_language="openqasm",
    )


def generate_qft_circuit(input):
    n_qubits = input.get("n_qubits")
    inverse = input.get("inverse")
    barriers = input.get("barriers")

    circuit = QFTAlgorithm.create_circuit(n_qubits, inverse, barriers)
    return CircuitResponse(
        circuit.qasm(),
        "algorithm/qft",
        circuit.num_qubits,
        circuit.depth(),
        input,
        circuit_language="openqasm",
    )


def generate_qpe_circuit(input):
    n_eval_qubits = input.get("n_eval_qubits")
    unitary = input.get("unitary")

    # check Unitary operator (qasm string)
    try:
        if unitary is not None:
            unitary = QuantumCircuit.from_qasm_str(unitary)
    except Exception as err:
        return bad_request("Invalid unitary (qasm string): " + str(err))

    circuit = QPEAlgorithm.create_circuit(n_eval_qubits, unitary)
    return CircuitResponse(
        circuit.qasm(),
        "algorithm/qpe",
        circuit.num_qubits,
        circuit.depth(),
        input,
        circuit_language="openqasm",
    )


def generate_vqe_circuit(input):
    ansatz = input.get("ansatz")
    parameters = input.get("parameters")
    observable = input.get("observable")

    # check Unitary operator (qasm string)
    if ansatz is not None:
        if parameters is not None:
            return bad_request(
                'Custom ansatz and parameters not supported. Remove "parameters" field!'
            )
        try:
            ansatz = QuantumCircuit.from_qasm_str(ansatz)
        except Exception as err:
            return bad_request("Invalid ansatz (qasm string): " + str(err))
    # if custom ansatz is chosen
    if parameters is None:
        parameters = []
    try:
        observable = PauliParser.parse(observable)
    except ValueError as err:
        return bad_request("Invalid observable: " + str(err))

    # check if number of parameters match ansatz
    try:
        circuit = VQEAlgorithm.create_circuit(ansatz, parameters, observable)
    except ValueError as err:
        return bad_request("Verify correctness of parameters: " + str(err))

    return CircuitResponse(
        circuit.qasm(),
        "algorithm/vqe",
        circuit.num_qubits,
        circuit.depth(),
        input,
        circuit_language="openqasm",
    )


def generate_grover_circuit(input):
    oracle = input.get("oracle")
    iterations = input.get("iterations")
    reflection_qubits = input.get("reflection_qubits")
    initial_state = input.get("initial_state")
    barriers = input.get("barriers")

    # check oracle (qasm string)
    try:
        if oracle is not None:
            oracle = QuantumCircuit.from_qasm_str(oracle)
    except Exception as err:
        return bad_request("Invalid oracle (qasm string): " + str(err))
    # check initial_state (qasm string)
    try:
        if initial_state is not None:
            initial_state = QuantumCircuit.from_qasm_str(initial_state)
    except Exception as err:
        return bad_request("Invalid initial_state (qasm string): " + str(err))

    # default number of iterations
    if iterations is None:
        iterations = 1

    circuit = GroverAlgorithm.create_circuit(
        oracle, iterations, reflection_qubits, initial_state, barriers
    )
    return CircuitResponse(
        circuit.qasm(),
        "algorithm/grover",
        circuit.num_qubits,
        circuit.depth(),
        input,
        circuit_language="openqasm",
    )


def generate_max_cut_qaoa_circuit(request: MaxCutQAOAAlgorithmRequest):
    if request.initial_state is not None:
        if request.parameterized:
            circuit = MaxCutQAOAWarmStartAlgorithm.genQaoaMaxcutCircuitTemplate(
                request.adj_matrix, request.initial_state, request.p, request.epsilon
            )
        else:
            import itertools

            params = [
                x
                for x in itertools.chain.from_iterable(
                    itertools.zip_longest(request.gammas, request.betas)
                )
                if x is not None
            ]
            circuit = MaxCutQAOAWarmStartAlgorithm.genQaoaMaxcutCircuit(
                request.adj_matrix,
                params,
                request.initial_state,
                request.p,
                request.epsilon,
            )
    else:
        circuit = MaxCutQAOAAlgorithm.create_circuit(
            request.adj_matrix,
            request.betas,
            request.gammas,
            request.p,
            request.parameterized,
        )

    if not request.parameterized:
        return CircuitResponse(
            circuit.qasm(),
            "algorithm/qaoa",
            circuit.num_qubits,
            circuit.depth(),
            request,
            circuit_language="openqasm",
        )
    else:
        return CircuitResponse(
            codecs.encode(pickle.dumps(circuit), "base64").decode(),
            "algorithm/qaoa",
            circuit.num_qubits,
            circuit.depth(),
            request,
            circuit_language="qiskit",
        )


def generate_tsp_qaoa_circuit(input):
    adj_matrix = input.get("adj_matrix")
    p = input.get("p")
    betas = input.get("betas")
    gammas = input.get("gammas")
    circuit = TSPQAOAAlgorithm.create_circuit(np.array(adj_matrix), p, betas, gammas)
    return CircuitResponse(
        circuit.qasm(),
        "algorithm/tspqaoa",
        circuit.num_qubits,
        circuit.depth(),
        input,
        circuit_language="openqasm",
    )


def generate_knapsack_qaoa_circuit(input):
    items = input.get("items")
    values = [d["value"] for d in items]
    weights = [d["weight"] for d in items]
    max_weights = input.get("max_weights")
    p = input.get("p")
    betas = input.get("betas")
    gammas = input.get("gammas")
    circuit = KnapsackQAOAAlgorithm.create_circuit(
        values, weights, max_weights, p, betas, gammas
    )
    return CircuitResponse(
        circuit.qasm(),
        "algorithm/knapsackqaoa",
        circuit.num_qubits,
        circuit.depth(),
        input,
        circuit_language="openqasm",
    )

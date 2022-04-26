import numpy as np
from flask import jsonify

from qiskit.circuit.quantumcircuit import QuantumCircuit
from api.services.algorithms.hhl_algorithm import HHLAlgorithm
from api.services.algorithms.qaoa_algorithm import QAOAAlgorithm
from api.services.algorithms.vqls_algorithm import VQLSAlgorithm
from api.services.algorithms.qft_algorithm import QFTAlgorithm
from api.services.algorithms.pauliParser import PauliParser
from api.services.helper_service import getCircuitCharacteristics, bad_request
from api.model.circuit_response import CircuitResponse


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
        HHLAlgorithm.qasm_compatible(circuit.qasm()),
        "algorithm/hhl",
        circuit.num_qubits,
        circuit.depth(),
        input,
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
        circuit.qasm(), "algorithm/qaoa", circuit.num_qubits, circuit.depth(), input
    )


def generate_vqls_circuit(input):
    matrix = input.get("matrix")
    vector = input.get("vector")
    alphas = input.get("alphas")
    l = input.get("l")
    lp = input.get("lp")
    ansatz = input.get("ansatz")

    circuit = VQLSAlgorithm.create_circuit(matrix, vector, alphas, l, lp, ansatz)
    return CircuitResponse(
        circuit.qasm(),
        "algorithm/vqls",
        circuit.num_qubits,
        circuit.depth(),
        input,
    )


def generate_qft_circuit(input):
    n_qubits = input.get("n_qubits")

    circuit = QFTAlgorithm.create_circuit(n_qubits)
    return CircuitResponse(
        circuit.qasm(),
        "algorithm/qft",
        circuit.num_qubits,
        circuit.depth(),
        input,
    )

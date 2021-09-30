import numpy as np
from flask import jsonify

from api.services.algorithms.hhl_algorithm import HHLAlgorithm
from api.services.algorithms.qaoa_algorithm import QAOAAlgorithm
from api.services.helper_service import getCircuitCharacteristics, bad_request
from api.model.circuit_response import CircuitResponse

# TODO
def generate_hhl_algorithm(input):
    matrix = input.get("matrix")
    vector = input.get("vector")
    circuit = HHLAlgorithm.create_circuit(matrix, vector)
    # TODO check types and dimensions
    return CircuitResponse(
        circuit.qasm(), "algorithm/hhl", circuit.num_qubits, circuit.depth(), input
    )


# TODO
def generate_qaoa_circuit(input):
    adj_matrix = input.get("adj_matrix")
    beta = input.get("beta")
    gamma = input.get("gamma")
    circuit = QAOAAlgorithm.create_circuit(adj_matrix, beta, gamma)
    return CircuitResponse(
        circuit.qasm(), "algorithm/qaoa", circuit.num_qubits, circuit.depth(), input
    )


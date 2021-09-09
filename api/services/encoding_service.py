import numpy as np
from flask import jsonify

from api.services.Encodings.basis_encoding import BasisEncoding
from api.services.Encodings.angle_encoding import AngleEncoding
from api.services.Encodings.amplitude_encoding import AmplitudeEncoding
from api.services.Encodings.schmidt_decomposition import (
    generate_schmidt_decomposition_from_array,
    Measurement,
)
from api.services.helper_service import getCircuitCharacteristics
from api.model.models import CircuitResponse


def handle_encoding(name, request):
    if name == "basis":
        response = generate_basis_encoding(request)
        return response.to_json()
    elif name == "angle":
        response = generate_angle_encoding(request)
        return response.to_json()
    elif name == "amplitude":
        response = generate_amplitude_encoding(request)
        return response.to_json()
    elif name == "quam":
        response = generate_quam_encoding(request)
        return response.to_json()
    elif name == "schmidt_decomposition":
        response = generate_schmidt_decomposition(request)
        return response.to_json()
    else:
        return "Encoding does not exist"


def generate_basis_encoding(input):
    vector = input.get("vector")
    n_integralbits = input.get("integral_bits")
    n_fractional_part = input.get("fractional_bits")
    if isinstance(vector, list):
        circuit = BasisEncoding.basis_encode_list_subcircuit(
            vector, n_integralbits, n_fractional_part
        )
    else:
        circuit = BasisEncoding.basis_encode_number_subcircuit(
            vector, n_integralbits, n_fractional_part
        )
    return CircuitResponse(
        circuit.qasm(), "encoding/basis", circuit.num_qubits, circuit.depth(), input
    )


def generate_angle_encoding(input):
    vector = input.get("vector")
    rotation_axis = input.get("rotationaxis")
    circuit = AngleEncoding.angle_encode_vector(vector, rotation_axis)

    return CircuitResponse(
        circuit.qasm(), "encoding/angle", circuit.num_qubits, circuit.depth(), input
    )


def generate_amplitude_encoding(input):
    vector = input.get("vector")
    circuit = AmplitudeEncoding.amplitude_encode_vector(vector)
    # width,depth = getCircuitCharacteristics(circuit) TODO dicuss if this makes more sense
    return CircuitResponse(
        circuit.qasm(), "encoding/amplitude", circuit.num_qubits, circuit.depth(), input
    )


def generate_quam_encoding(input):
    return CircuitResponse(None, "encoding/quam", None, None, None)


def generate_schmidt_decomposition(input):
    vector = input.get("vector")
    if np.log2(len(vector)) % 1 != 0:
        response = jsonify(
            {
                "error": "bad request",
                "message": "Invalid vector input! Vector must be of length 2^n",
            }
        )
        response.status_code = 400
        return response
    circuit = generate_schmidt_decomposition_from_array(
        vector, Measurement.noMeasurement
    )
    return CircuitResponse(
        circuit.qasm(), "encoding/schmidt", circuit.num_qubits, circuit.depth(), input
    )

import numpy as np

from app.services.encodings.basis_encoding import BasisEncoding
from app.services.encodings.angle_encoding import AngleEncoding
from app.services.encodings.amplitude_encoding import AmplitudeEncoding
from app.services.encodings.schmidt_decomposition import (
    generate_schmidt_decomposition_from_array,
    Measurement,
)
from app.services.helper_service import bad_request
from app.model.circuit_response import CircuitResponse


def generate_basis_encoding(input):
    vector = input.get("vector")
    n_integral_bits = input.get("integral_bits")
    n_fractional_bits = input.get("fractional_bits")
    vector = vector if isinstance(vector, list) else [vector]
    circuit = BasisEncoding.basis_encode_list_subcircuit(
        vector, n_integral_bits, n_fractional_bits
    )

    return CircuitResponse(
        circuit, "encoding/basis", circuit.num_qubits, circuit.depth(), input
    )


def generate_angle_encoding(input):
    vector = input.get("vector")
    rotation_axis = input.get("rotation_axis")
    circuit = AngleEncoding.angle_encode_vector(vector, rotation_axis)

    return CircuitResponse(
        circuit, "encoding/angle", circuit.num_qubits, circuit.depth(), input
    )


def generate_amplitude_encoding(input):
    vector = input.get("vector")
    circuit = AmplitudeEncoding.amplitude_encode_vector(vector)
    # width,depth = getCircuitCharacteristics(circuit) TODO dicuss if this makes more sense
    return CircuitResponse(
        circuit, "encoding/amplitude", circuit.num_qubits, circuit.depth(), input
    )


def generate_schmidt_decomposition(input):
    vector = input.get("vector")

    if np.log2(len(vector)) % 1 != 0:
        return bad_request("Invalid vector input! Vector must be of length 2^n")

    circuit = generate_schmidt_decomposition_from_array(
        vector, Measurement.noMeasurement
    )
    return CircuitResponse(
        circuit, "encoding/schmidt", circuit.num_qubits, circuit.depth(), input
    )

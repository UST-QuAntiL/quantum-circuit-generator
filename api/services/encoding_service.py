from api.services.Encodings.basis_encoding import BasisEncoding
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
    n_qubits = circuit.num_qubits
    depth = circuit.depth()

    return CircuitResponse(circuit.qasm(), "encoding/basis", n_qubits, depth, input)


def generate_angle_encoding(input):
    return CircuitResponse(None, "encoding/angle", None, None, None)


def generate_amplitude_encoding(input):
    return CircuitResponse(None, "encoding/amplitude", None, None, None)


def generate_quam_encoding(input):
    return CircuitResponse(None, "encoding/quam", None, None, None)


def generate_schmidt_decomposition(input):
    return CircuitResponse(None, "encoding/schmidt", None, None, None)

from api.services.Encodings.basis_encoding import BasisEncoding
from api.model.models import CircuitResponse


def generate_basis_encoding(input):
    vector = input.get('vector')
    n_integralbits = input.get('integral_bits')
    n_fractional_part = input.get('fractional_bits')
    if isinstance(input, list):
        circuit = BasisEncoding.basis_encode_list_subcircuit(vector, n_integralbits, n_fractional_part)
    else:
        circuit = BasisEncoding.basis_encode_number_subcircuit(vector, n_integralbits, n_fractional_part)
    n_qubits = circuit.num_qubits
    depth = circuit.depth()

    return CircuitResponse(circuit.qasm(), "encoding/basis", n_qubits, depth, input)

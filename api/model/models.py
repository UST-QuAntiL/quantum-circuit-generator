from datetime import datetime

class CircuitResponse:
    def __init__(self, circuit, circuit_type, n_qubits, depth, input ):
        self.circuit = circuit
        self.circuit_type = circuit_type
        self.n_qubits = n_qubits
        self.depth = depth
        self.input = input
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def to_json(self):
        json_circuit_response = {
            'circuit': self.circuit,
            'circuit_type': self.circuit_type,
            'n_qubits': self.n_qubits,
            'depth': self.depth,
            'timestamp': self.timestamp,
            'input': self.input
        }
        return json_circuit_response

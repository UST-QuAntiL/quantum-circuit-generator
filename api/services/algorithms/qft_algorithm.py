from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.library import QFT

from api.services.encodings.amplitude_encoding import AmplitudeEncoding


class QFTAlgorithm:
    @classmethod
    def preprocess(cls, vector):
        """Preprocess data
        Check if vector is list
        Prepare amplitude encoding circuit
        If vector is None, a dummy circuit is prepared that is removed later.
        """
        if isinstance(vector, QuantumCircuit):
            vector_circuit = vector
        elif isinstance(vector, list):
            vector_circuit = AmplitudeEncoding.amplitude_encode_vector(vector)
            """q = QuantumRegister(len(vector))
            vector_circuit = QuantumCircuit(q)
            for i, num in enumerate(vector):
                vector_circuit.initialize(num, q[i])"""

        return vector_circuit

    @classmethod
    def create_circuit(cls, num_qubits, approx_degree=0, is_inverse=False):
        """

        :param vector: input vector containing floats
        :param is_inverse: whether to use inverse QFT
        :return: OpenQASM Circuit

        Creates QFT circuit from a vector.
        A preprocession is used for encoding.
        """

        qft_circ = QFT(num_qubits, approximation_degree=approx_degree, inverse=is_inverse, name="qft" if not is_inverse else "iqft")
        return qft_circ

    
if __name__ == '__main__':
    algorithm = QFTAlgorithm()
    circ = algorithm.create_circuit(4,2, True)
    print(circ.qasm())
    print(circ.get_instructions())
    qisk = QuantumCircuit.from_qasm_str(circ.qasm())
    print(qisk)

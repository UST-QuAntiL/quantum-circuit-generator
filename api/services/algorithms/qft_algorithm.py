from qiskit import QuantumRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.library import QFT
import numpy as np

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
    def create_circuit(cls, vector, is_inverse=False):
        """

        :param vector: input vector containing floats
        :param is_inverse: whether to use inverse QFT
        :return: OpenQASM Circuit

        Creates QFT circuit from a vector.
        A preprocession is used for encoding.
        """

        vector_circuit = cls.preprocess(vector)
        qft_circ = QFT(vector_circuit.num_qubits, inverse=is_inverse, name="QFT" if not is_inverse else "IQFT")
        vector_circuit.compose(qft_circ, vector_circuit.qubits, inplace=True)
        print(vector_circuit)
        return vector_circuit

    
if __name__ == '__main__':
    algorithm = QFTAlgorithm()
    algorithm.create_circuit([3, 2, 4, 3, 3, 2, 4, 3], True)

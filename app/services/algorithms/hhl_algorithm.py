from qiskit.circuit.quantumcircuit import QuantumCircuit
# from qiskit.algorithms.linear_solvers.hhl import HHL
import numpy as np

from app.services.encodings.amplitude_encoding import AmplitudeEncoding


class HHLAlgorithm:
    @classmethod
    def preprocess(cls, matrix, vector):
        """Preprocess data
        Matrix to numpy array
        Check if vector is list
        Prepare amplitude encoding circuit
        If vector is None, a dummy circuit is prepared that is removed later.
        """
        # input check
        if isinstance(matrix, list):
            matrix = np.array(matrix)

        if vector is not None:
            if isinstance(vector, QuantumCircuit):
                vector_circuit = vector
            elif isinstance(vector, list):
                vector_circuit = AmplitudeEncoding.amplitude_encode_vector(vector)
                vector_circuit.name = "amplitude_enc"
        else:
            # only HHL and no vector encoding
            # dummy circuit that is poped later
            n_qubits = (
                int(np.log2(matrix.shape[0]))
                if np.log2(matrix.shape[0]) % 1 == 0
                else int(np.log2(matrix.shape[0])) + 1
            )
            vector_circuit = QuantumCircuit(n_qubits)

        return matrix, vector_circuit

    @classmethod
    def create_circuit(cls, matrix, vector=None):
        """
        :param matrix: input matrix to invert containing floats
        :param vector: input vector containing floats
        :return: OpenQASM Circuit

        Creates HHL circuit from np.array(matrix) and vector.
        Custom AmplitudeEncoding is used for vector preparation.
        """
        return "HHL was temporarily deprecated by Qiskit"

        matrix, vector_circuit = cls.preprocess(matrix=matrix, vector=vector)
        hhl = HHL()
        hhl_qc = hhl.construct_circuit(matrix, vector_circuit)

        # remove dummy circuit
        if vector is None:
            hhl_qc.data.pop(0)

        # change gate names
        for element in hhl_qc.data:
            element[0].name = element[0].name.lower()
        hhl_qc.data[2][0].name = "invx"

        # TODO decompose circuit gates
        return hhl_qc

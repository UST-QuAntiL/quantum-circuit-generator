from qiskit import QuantumRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.algorithms.linear_solvers.hhl import HHL
import numpy as np

from api.services.encodings.amplitude_encoding import AmplitudeEncoding


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

        return hhl_qc

    @classmethod
    def qasm_compatible(cls, qasm_str):
        """
        :param qasm_str: qasm string that contains names incompatible with OpenQASM
        :return: compatible string

        This normalization is taylor made and attempts to patch a problem within qiskit.
        The method is therefore not applicable to other circuits.
        """

        qasm = qasm_str
        # get the names of all gates
        qasm_list = qasm.split()
        gate_names = []

        for i in range(len(qasm_list)):
            if qasm_list[i] == "gate":
                gate_names.append(qasm_list[i + 1])

        # remove valid gate names 'amplitude_enc', 'qpe',...
        gate_names = gate_names[:-5]

        # make gate names OPENQASM compatible
        replacements = []
        for gate in gate_names:
            if gate.startswith("ucry"):
                continue
            # replace "+-*/" by "_" and make lowercase
            norm = (
                gate.replace("-", "_")
                .replace("1/", "inv")
                .replace("*", "_")
                .replace("+", "_")
                .lower()
                + "_"
            )
            replacements.append((gate, norm))

        for gate, norm in replacements:
            qasm = qasm.replace(gate, norm)
        qasm = qasm.replace("reset q0;", "")

        return qasm

import numpy as np
from qiskit.circuit.library import PhaseEstimation


class QPEAlgorithm:
    @classmethod
    def create_circuit(cls, n_eval_qubits, unitary):
        """
        :param n_eval_qubits: number of qubits representing the estimated Phase
        :param unitary: QuantumCircuit object (generated from qasm string)
        :return: OpenQASM Circuit

        Creates the circuit of the quantum phase estimation algorithm with
        n_eval_qubits determining how precise the result should be.
        """

        qpe = PhaseEstimation(n_eval_qubits, unitary)
        # decompose to standard gates
        qpe = qpe.decompose()  # split qpe gate
        gate_names = [gate[0].name for gate in qpe.data]
        gate_names = gate_names[n_eval_qubits:]  # ignore Hadamard gates

        qpe = qpe.decompose(gate_names)

        return qpe

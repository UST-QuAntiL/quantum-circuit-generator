import numpy as np

from qiskit import QuantumRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit


class GroverAlgorithm:
    @classmethod
    def create_circuit(cls, n_qubits, inverse, barriers):
        # TODO implementation
        """
        :param n_qubits: number of qubits the QFT should act on
        :param inverse: boolean flag, signaling to return the inverse QFT
        :param barriers: boolean flag, wether or not to insert barriers
        :return: OpenQASM Circuit

        Creates the circuit of the quantum fourier transform with n_qubits.
        Suppose |x> = |x1 x2 ... xn > with x1 being the most significant bit.
        Since in qiskit, the most significant qubit is qn, we have:
        |x1 x2 ... xn > = |qn ... q1 >
        """

        grover = QuantumCircuit(n_qubits)

        return grover

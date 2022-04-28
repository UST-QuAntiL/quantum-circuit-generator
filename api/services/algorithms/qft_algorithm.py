import numpy as np

from qiskit import QuantumRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit


class QFTAlgorithm:
    @classmethod
    def create_circuit(cls, n_qubits, inverse, barriers):
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

        qft = QuantumCircuit(n_qubits)
        for i in reversed(range(n_qubits)):
            if barriers:  # Add barrier if specified
                qft.barrier()
            qft.h(i)
            for j in range(i):
                # control is down 1, 2,...  --> i-(j+1)
                qft.cp(
                    2 * np.pi / 2 ** (j + 2), i - (j + 1), i
                )  # cp(phase, control, target)
        # swaps
        if barriers:
            qft.barrier()
        for i in range(n_qubits // 2):
            qft.swap(i, n_qubits - i - 1)

        if inverse:
            qft = qft.inverse()

        return qft

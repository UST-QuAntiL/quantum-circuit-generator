import numpy as np

from qiskit import QuantumRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.algorithms import VQE


class VQEAlgorithm:
    @classmethod
    def create_circuit(cls, ansatz, parameters, observable):
        """
        :param ansatz: QuantumCircuit (from qasm string) instance describing the ansatz.
                       If None (no ansatz) is given using RealAmplitudes ansatz.
        :param parameters: Parameters for the ansatz circuit
        :param observable: Qubit operator of the Observable given as pauli string
        :return: OpenQASM Circuit of the VQE ansatz

        Description
        """

        vqe = VQE(ansatz=ansatz)
        vqe_qc = vqe.construct_circuit(parameters, observable)[0]

        # decompose default ansatz
        if ansatz is None:
            vqe_qc = vqe_qc.decompose("RealAmplitudes")

        return vqe_qc

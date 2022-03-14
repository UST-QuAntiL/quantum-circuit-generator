import numpy as np

from qiskit import QuantumRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.algorithms.linear_solvers.hhl import HHL

from api.services.encodings.amplitude_encoding import AmplitudeEncoding
from api.services.algorithms.pauliParser import PauliParser

from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA
from qiskit.quantum_info import Pauli
from qiskit.opflow import PauliSumOp


class QAOAAlgorithm:
    @classmethod
    def create_circuit(cls, initial_state, pauli_op, mixer, reps, gammas, betas):
        """
        :param inital_state: quantum circuit used to initialize qaoa, parsed to QuantumCircuit
        :param pauli_op: Pauli operator describing the cost hamiltonian
        :param mixer: Pauli operator describing the mixer or QuantumCircuit instance
        :param reps: number of repetitions, how often each operator is applied, often called parameter p in literature
        :param betas: beta parameters used in qaoa
        :param gammas: gamma parameters used in qaoa
        :return: OpenQASM Circuit

        Creates circuit used in qaoa for MaxCut of undirected graph.
        Custom AmplitudeEncoding is used for vector preparation.
        """

        operator = pauli_op
        optimizer = COBYLA()
        qaoa = QAOA(
            initial_state=initial_state, mixer=mixer, optimizer=optimizer, reps=reps
        )

        if betas is not None:
            # angles in alternating fashion: [gamma1, beta1, gamma2, beta2, ...]
            angles = [
                angle for gamma, beta in zip(gammas, betas) for angle in (gamma, beta)
            ]
        else:
            angles = gammas
        qaoa_qc = qaoa.construct_circuit(angles, operator)[0]

        return qaoa_qc

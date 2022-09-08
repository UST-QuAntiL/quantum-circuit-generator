import numpy as np

from qiskit import QuantumRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.algorithms.linear_solvers.hhl import HHL

from api.services.encodings.amplitude_encoding import AmplitudeEncoding
from api.services.algorithms.pauliParser import PauliParser

from qiskit.algorithms import QAOA
from qiskit.quantum_info import Pauli
from qiskit.opflow import PauliSumOp
from qiskit.compiler import transpile
from qiskit.algorithms.optimizers import COBYLA

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
        qaoa = QAOA(initial_state=initial_state, mixer=mixer, reps=reps)

        if betas is None:  # case for custom mixer
            angles = gammas
        else:
            angles = betas + gammas

        # print(angles)
        qaoa_qc = qaoa.construct_circuit(angles, operator)[0]

        # decompose exp gates
        qaoa_qc = QAOAAlgorithm.decompose_operator_gates(qaoa_qc)

        return qaoa_qc

    @classmethod
    def decompose_operator_gates(cls, qaoa_qc):
        """
        :param qaoa_qc: quantum circuit of the QAOA instance to decompose
        :return: decomposed circuit
        """

        gates = qaoa_qc.data

        for gate in gates:
            if gate[0].name == "PauliEvolution":
                # mark PauliEvolution gates for decomposition
                gate[0].label = "decompose"
        # decompose marked gates
        qaoa_qc = qaoa_qc.decompose("decompose")

        gates = qaoa_qc.data

        for gate in gates:
            if gate[0].name.startswith("exp(it"):
                # mark PauliEvolution gates for decomposition
                gate[0].label = "decompose"
        # decompose marked gates
        qaoa_qc = qaoa_qc.decompose("decompose")

        return qaoa_qc



class MaxCutQAOAAlgorithm:
    @classmethod
    def create_operator(cls, weight_matrix):
        """
        :param matrix: adjacency matrix describing the undirected graph

        Create Hamiltonian operator to be used in QAOA.
        Here we transform an adjacency matrix into an operator to be used in the QAOA circuit.
        """
        weight_matrix = np.array(weight_matrix)
        num_nodes = weight_matrix.shape[0]
        pauli_list = []

        for i in range(num_nodes):
            for j in range(i):
                if weight_matrix[i, j] != 0:
                    x_p = np.zeros(num_nodes, dtype=bool)
                    z_p = np.zeros(num_nodes, dtype=bool)
                    z_p[i] = True
                    z_p[j] = True
                    pauli_list.append([0.5, Pauli((z_p, x_p))])

        pauli_list = [(pauli[1].to_label(), pauli[0]) for pauli in pauli_list]

        return PauliSumOp.from_list(pauli_list)

    @classmethod
    def create_circuit(cls, adj_matrix, beta, gamma):
        """
        :param adj_matrix: adjacency matrix describing the undirected graph
        :param beta: beta parameter used in qaoa
        :param gamma: gamma parameter used in qaoa
        :return: OpenQASM Circuit

        Creates circuit used in qaoa for MaxCut of undirected graph.
        Custom AmplitudeEncoding is used for vector preparation.
        """

        operator = cls.create_operator(adj_matrix)
        optimizer = COBYLA()
        qaoa = QAOA(optimizer)
        qaoa_qc = qaoa.construct_circuit([gamma, beta], operator)[0]

        return qaoa_qc
import numpy as np
from qiskit.algorithms import QAOA
from qiskit.quantum_info import Pauli
from qiskit.opflow import PauliSumOp
from app.services.algorithms.qaoa_algorithm import QAOAAlgorithm


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
        qaoa = QAOA()
        qaoa_qc = qaoa.construct_circuit([beta, gamma], operator)[0]

        # decompose exp gates
        qaoa_qc = QAOAAlgorithm.decompose_operator_gates(qaoa_qc)

        return qaoa_qc

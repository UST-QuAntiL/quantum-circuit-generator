import numpy as np

from qiskit import QuantumRegister
from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.algorithms.linear_solvers.hhl import HHL

from api.services.encodings.amplitude_encoding import AmplitudeEncoding
from api.services.algorithms.pauliParser import PauliParser

from qiskit.algorithms.optimizers import COBYLA
from qiskit.quantum_info import Pauli
from qiskit.opflow import PauliSumOp
from qiskit.circuit.library import EfficientSU2, TwoLocal, NLocal, PauliTwoDesign
import qiskit.circuit.library.n_local as lib_local
from qiskit.opflow import X, Y, Z, I
from qiskit import transpile
import itertools
import functools


class VQLSAlgorithm:
    @classmethod
    def decompose_matrix(cls, A):
        r"""Decomposes a Hermitian matrix A into a linear combination of Pauli operators.

        Args:
            A (array[complex]): a Hermitian matrix of dimension :math:`2^n\times 2^n`
            hide_identity (bool): does not include the :class:`~.Identity` observable within
                the tensor products of the decomposition if ``True``

        Returns:
            tuple[list[float], list[~.Observable]]: a list of coefficients and a list
            of corresponding tensor products of Pauli observables that decompose the Hamiltonian.

        **Example:**

        We can use this function to compute the Pauli operator decomposition of an arbitrary Hermitian
        matrix:

        >>> A = np.array(
        ... [[-2, -2+1j, -2, -2], [-2-1j,  0,  0, -1], [-2,  0, -2, -1], [-2, -1, -1,  0]])
        >>> coeffs, obs_list = decompose_matrix(A)
        >>> coeffs
        [-1.0, -1.5, -0.5, -1.0, -1.5, -1.0, -0.5, 1.0, -0.5, -0.5]
        """
        A = np.array(A)
        n = int(np.log2(len(A)))
        N = 2 ** n

        if A.shape != (N, N):
            raise ValueError(
                "The Hamiltonian should have shape (2**n, 2**n), for any qubit number n>=1"
            )

        if not np.allclose(A, A.conj().T):
            raise ValueError("The Hamiltonian is not Hermitian")

        paulis = [I, X, Y, Z]
        obs = []
        coeffs = []

        for term in itertools.product(paulis, repeat=n):
            matrices = [i.to_matrix() for i in term]
            coeff = np.trace(functools.reduce(np.kron, matrices) @ A) / N
            coeff = np.real_if_close(coeff).item()

            if not np.allclose(coeff, 0):
                coeffs.append(coeff)
                obs.append([t for i, t in enumerate(term)])

        return coeffs, obs

    @classmethod
    def CA(cls, qc, obs_list, idx):
        """Controlled Application"""
        operators = obs_list[idx]

        for j in reversed(range(len(operators))):
            if operators[j] == "I":
                pass
            elif operators[j] == "X":
                qc.cx(ancilla_idx, j)
            elif operators[j] == "Y":
                qc.cy(ancilla_idx, j)
            elif operators[j] == "Z":
                qc.cz(ancilla_idx, j)

    #    @classmethod
    #    def local_hadamard_test(cls, weights, l=None, lp=None, j=None, part=None):
    #
    #        qc = QuantumCircuit(num_qubits+1, 1)
    #
    #        # First Hadamard gate applied to the ancillary qubit.
    #        qc.h(ancilla_idx)
    #
    #        # For estimating the imaginary part of the coefficient "mu", we must add a "-i"
    #        # phase gate.
    #        if part == "Im" or part == "im":
    #            qc.p(-np.pi / 2, ancilla_idx)
    #
    #        qubit_list = range(num_qubits)
    #
    #        # Variational circuit generating a guess for the solution vector |x>
    #        qc.append(ansatz_circuit.bind_parameters(weights), qubit_list)
    #
    #        qc.barrier()
    #        # Controlled application of the unitary component A_l of the problem matrix A.
    #        CA(qc, obs_list, An)
    #
    #        nb = int(np.log2(len(vector)))
    #        vector_circuit = QuantumCircuit(nb)
    #        vector_circuit.isometry(vector / np.linalg.norm(vector), list(range(nb)), None)
    #        vector_circuit = vector_circuit.inverse()
    #
    #        qc.append(vector_circuit, qubit_list)
    #
    #        qc.barrier()
    #
    #        # Controlled Z operator at position j. If j = -1, apply the identity.
    #        if j != -1:
    #            qc.cz(ancilla_idx, j)
    #
    #        qc.barrier()
    #
    #        # Unitary U_b associated to the problem vector |b>.
    #        qc.isometry(vector / np.linalg.norm(vector), list(range(nb)), None)
    #
    #        # Controlled application of Adjoint(A_lp).
    #        #CA_dag(qc, obs_list, lp)
    #        CA(qc, obs_list, Am)
    #
    #        qc.barrier()
    #        # # Second Hadamard gate applied to the ancillary qubit.
    #        qc.h(ancilla_idx)
    #
    #        qc = transpile(qc, basis_gates=['id', 'rz', 'sx', 'x', 'cx'])
    #        qc.barrier()
    #        qc.measure(ancilla_idx, 0)
    #
    #        return qc

    @classmethod
    def create_circuit(cls, matrix, vector, alphas, l, lp, ansatz="EfficientSU2"):
        """
        :param pauli_op_string: Pauli operator string describing the cost hamiltonian
        :param reps: number of repetitions, how often each operator is applied, often called parameter p in literature
        :param betas: beta parameters used in qaoa
        :param gammas: gamma parameters used in qaoa
        :return: OpenQASM Circuit

        Creates circuit used in qaoa for MaxCut of undirected graph.
        Custom AmplitudeEncoding is used for vector preparation.
        """
        # determine number of qubits
        num_qubits = int(np.log2(len(vector)))  # number of system qubits
        ancilla_idx = num_qubits  # Index of the ancillary qubit for the Hadamard test(last position)

        # Convert the matrix to Hamiltonian
        coeffs, obs_list = cls.decompose_matrix(matrix)

        # We grab the requested ansatz circuit class from the Qiskit circuit library
        # n_local module and configure it using the number of qubits
        ansatz_instance = getattr(lib_local, ansatz)
        ansatz_circuit = ansatz_instance(num_qubits)

        # Get the number of parameters in the ansatz circuit.
        num_params = ansatz_circuit.num_parameters

        # circ = ansatz_circuit.bind_parameters(alphas)
        # circ.measure_all()

        # print(circ)

        qc = QuantumCircuit(num_qubits + 1, 1)

        # First Hadamard gate applied to the ancillary qubit.
        qc.h(ancilla_idx)

        # For estimating the imaginary part of the coefficient "mu", we must add a "-i"
        # phase gate.
        # TODO
        part = "Re"
        if part == "Im" or part == "im":
            qc.p(-np.pi / 2, ancilla_idx)

        qubit_list = range(num_qubits)

        # Variational circuit generating a guess for the solution vector |x>
        qc.append(ansatz_circuit.bind_parameters(alphas), qubit_list)

        qc.barrier()
        # Controlled application of the unitary component A_l of the problem matrix A.
        cls.CA(qc, obs_list, l)

        vector_circuit = QuantumCircuit(num_qubits)
        vector_circuit.isometry(
            vector / np.linalg.norm(vector), list(range(num_qubits)), None
        )
        vector_circuit = vector_circuit.inverse()

        qc.append(vector_circuit, qubit_list)

        qc.barrier()

        # Controlled Z operator at position j. If j = -1, apply the identity.
        # TODO
        j = -1
        if j != -1:
            qc.cz(ancilla_idx, j)

        qc.barrier()

        # Unitary U_b associated to the problem vector |b>.
        qc.isometry(vector / np.linalg.norm(vector), list(range(num_qubits)), None)

        # Controlled application of Adjoint(A_lp).
        # CA_dag(qc, obs_list, lp)
        cls.CA(qc, obs_list, lp)

        qc.barrier()
        # # Second Hadamard gate applied to the ancillary qubit.
        qc.h(ancilla_idx)

        print(qc)
        qc = transpile(qc, basis_gates=["id", "rz", "sx", "x", "cx"])
        qc.barrier()
        qc.measure(ancilla_idx, 0)

        print(qc)

        return qc


## The entrypoint for our Runtime Program
# def main(backend, user_messenger,
#         matrix,
#         vector,
#         ansatz='EfficientSU2',
#         ansatz_config={},
#         x0=None,
#         optimizer='SPSA',
#         optimizer_config={'maxiter': 100},
#         shots = 8192,
#         use_measurement_mitigation=False
#        ):
#
#    """
#    The main VQLS program.
#
#    Parameters:
#        backend (ProgramBackend): Qiskit backend instance.
#        user_messenger (UserMessenger): Used to communicate with the
#                                        program user.
#        matrix (numpy array): matrix A.
#        vector (numpy array): vector b, we want to solve Ax = b.
#        ansatz (str): Optional, name of ansatz quantum circuit to use,
#                      default='EfficientSU2'
#        ansatz_config (dict): Optional, configuration parameters for the
#                              ansatz circuit.
#        x0 (array_like): Optional, initial vector of parameters.
#        optimizer (str): Optional, string specifying classical optimizer,
#                         default='SPSA'.
#        optimizer_config (dict): Optional, configuration parameters for the
#                                 optimizer.
#        shots (int): Optional, number of shots to take per circuit.
#        use_measurement_mitigation (bool): Optional, use measurement mitigation,
#                                           default=False.
#
#    Returns:
#        res: The result in SciPy optimization format.
#
#        cost_function: An array with values of cost function for every optimization step
#
#        quantum_solution: solution vector as numpy array
#
#    """
#
#    #determine number of qubits
#    num_qubits = int(np.log2(len(vector))) # number of system qubits
#    tot_qubits = num_qubits + 1  # Addition of an ancillary qubit
#    ancilla_idx = num_qubits  # Index of the ancillary qubit for the Hadamard test(last position)
#
#    #Convert the matrix to Hamiltonian
#    coeffs, obs_list = decompose_matrix(matrix)
#
#    # We grab the requested ansatz circuit class from the Qiskit circuit library
#    # n_local module and configure it using the number of qubits and options
#    # passed in the ansatz_config.
#    ansatz_instance = getattr(lib_local, ansatz)
#    ansatz_circuit = ansatz_instance(num_qubits, **ansatz_config)
#
#    # Get the number of parameters in the ansatz circuit.
#    num_params = ansatz_circuit.num_parameters
#
#    res.x = optimal_params
#
#    circ = ansatz_circuit.bind_parameters(res.x)
#    circ.measure_all()
#
#    print(circ)
#
#    return res, cost_function, quantum_solution

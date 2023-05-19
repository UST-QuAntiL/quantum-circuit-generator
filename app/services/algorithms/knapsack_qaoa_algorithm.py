from qiskit_optimization.applications import Knapsack
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit.algorithms import QAOA


class KnapsackQAOAAlgorithm:
    @classmethod
    def create_circuit(cls, values, weights, max_weights, p, betas, gammas):
        """
        :param values: list of values for the knapsack items which should be maximized
        :param weights: list of weights for the knapsack items
        :param max_weights: maximum weights for all items within the knapsack
        :param p: number of repetitions, how often each operator is applied, often called parameter p in literature
        :param betas: beta parameters used in qaoa
        :param gammas: gamma parameters used in qaoa
        :return: OpenQASM Circuit

        Creates circuit used in QAOA for the knapsack problem
        """

        # generate knapsack problem instance
        problem = Knapsack(values=values, weights=weights, max_weight=max_weights)
        quadratic_program = problem.to_quadratic_program()
        print(quadratic_program.prettyprint())

        # convert to ising model
        converter = QuadraticProgramToQubo()
        operator, offset = converter.convert(quadratic_program).to_ising()
        print('Number of required Qubits:', operator.num_qubits)
        print('Offset:', offset)

        if betas is None:  # case for custom mixer
            angles = gammas
        else:
            angles = betas + gammas
        print('Angles:', angles)

        # generate circuit
        qaoa = QAOA(reps=p)
        qaoa_qc = qaoa.construct_circuit(angles, operator)[0]
        qaoa_qc = qaoa_qc.decompose(reps=100)
        return qaoa_qc

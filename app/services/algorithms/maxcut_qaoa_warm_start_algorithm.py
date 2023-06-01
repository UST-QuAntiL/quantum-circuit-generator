from copy import deepcopy

from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.parameter import Parameter
import numpy as np
from builtins import isinstance


class MaxCutQAOAWarmStartAlgorithm:
    @classmethod
    def genQaoaMaxcutCircuitTemplate(
        cls,
        graph,
        initialString=None,
        p=1,
        measure=True,
        suppressClassicalRegister=False,
        epsilon=0.25,
    ):
        initialIntList = [int(i) for i in initialString]
        initalEpsilonAdjustListed = cls.epsilon_function(
            initialIntList, epsilon=epsilon
        )
        # prepare the quantum and classical resisters
        graph = np.asarray(graph)
        n_vertices = graph.shape[0]
        registers = (
            (n_vertices,) if suppressClassicalRegister else (n_vertices, n_vertices)
        )
        QAOA = QuantumCircuit(*registers)

        # prepare the parameters
        gammas = [Parameter("gamma" + str(i + 1)) for i in range(p)]
        betas = [Parameter("beta" + str(i + 1)) for i in range(p)]

        if initalEpsilonAdjustListed:
            for qubits in range(n_vertices):
                QAOA.ry(
                    2 * np.arcsin(np.sqrt(initalEpsilonAdjustListed[qubits])), qubits
                )
        else:
            # apply the layer of Hadamard gates to all qubits
            QAOA.h(range(n_vertices))

        for iter in range(p):
            QAOA.barrier()
            # apply the Ising type gates with angle gamma along the edges in E
            for i in range(1, n_vertices):
                for j in range(n_vertices - 1):
                    if i > j and graph[i, j] != 0:
                        QAOA.cx(i, j)
                        QAOA.rz(-gammas[iter] * graph[i, j], j)
                        QAOA.cx(i, j)

            # then apply the single qubit X rotations with angle beta to all qubits
            QAOA.barrier()

            if initalEpsilonAdjustListed:
                for qubits in range(n_vertices):
                    # adapted egger et al. WS-Mixer
                    QAOA.ry(
                        2 * np.arcsin(np.sqrt(initalEpsilonAdjustListed[qubits])),
                        qubits,
                    )
                    QAOA.rz(-2 * betas[iter], qubits)
                    QAOA.ry(
                        -2 * np.arcsin(np.sqrt(initalEpsilonAdjustListed[qubits])),
                        qubits,
                    )

                    # default WS-Mixer
                    # QAOA.ry(-2 * np.arcsin(np.sqrt(initalEpsilonAdjustListed[qubits])), qubits)
                    # QAOA.rz(-2 * betas[iter], qubits)
                    # QAOA.ry(2 * np.arcsin(np.sqrt(initalEpsilonAdjustListed[qubits])), qubits)
            else:
                QAOA.rx(2 * betas[iter], range(n_vertices))

        if measure:
            # Finally measure the result in the computational basis
            QAOA.barrier()
            QAOA.measure(range(n_vertices), range(n_vertices)[::-1])

        return QAOA

    @classmethod
    def genQaoaMaxcutCircuit(cls, graph, params, initial=None, p=1, epsilon=0.25):
        template = cls.genQaoaMaxcutCircuitTemplate(
            graph, initial if initial else None, p=p, epsilon=epsilon
        )
        return cls.assignParameters(template, params)

    @classmethod
    def assignParameters(cls, circuit_template, params):
        if not isinstance(params, dict):
            parameter_dict = {}
            parameters = circuit_template.parameters
            for i in range(len(params)):
                if i % 2 == 0:
                    # gamma
                    param_name = "gamma" + str((i // 2) + 1)
                    parameter = ([x for x in parameters if x.name == param_name])[0]
                    parameter_dict[parameter] = params[i]
                else:
                    # beta
                    param_name = "beta" + str((i // 2) + 1)
                    parameter = ([x for x in parameters if x.name == param_name])[0]
                    parameter_dict[parameter] = params[i]
            params = parameter_dict
        return circuit_template.assign_parameters(params)

    @classmethod
    def epsilon_function(cls, initial, epsilon=0.25):
        cut = deepcopy(initial)
        epsilon = 0 if epsilon < 0 else epsilon
        epsilon = 0.5 if epsilon > 0.5 else epsilon
        # increase distance of continuous values from exact 0 and 1
        for i in range(len(cut)):
            if cut[i] > 1 - epsilon:
                cut[i] = 1 - epsilon
            if cut[i] < epsilon:
                cut[i] = epsilon
        return cut

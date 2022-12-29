from qiskit.circuit.quantumcircuit import QuantumCircuit
from qiskit.circuit.parameter import Parameter
import numpy as np
from builtins import isinstance


class MaxCutQAOAWarmStartAlgorithm:
    @classmethod
    def genQaoaMaxcutCircuitTemplate(
        cls, graph, initial=None, p=1, measure=True, suppressClassicalRegister=False
    ):
        # prepare the quantum and classical resisters
        graph = np.asarray(graph)
        n_vertices = graph.shape[0]
        registers = (
            (n_vertices,) if suppressClassicalRegister else (n_vertices, n_vertices)
        )
        QAOA = QuantumCircuit(*registers)

        # prepare the parameters
        gammas = [Parameter("γ" + str(i + 1)) for i in range(p)]
        betas = [Parameter("β" + str(i + 1)) for i in range(p)]

        if initial:
            for qubits in range(n_vertices):
                precomputed_value = int(initial[qubits])
                QAOA.ry(2 * np.arcsin(np.sqrt(precomputed_value)), qubits)
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

            if initial:
                for qubits in range(n_vertices):
                    precomputed_value = int(initial[qubits])
                    # adapted egger et al. WS-Mixer
                    QAOA.ry(2 * np.arcsin(np.sqrt(precomputed_value)), qubits)
                    QAOA.rz(-2 * betas[iter], qubits)
                    QAOA.ry(-2 * np.arcsin(np.sqrt(precomputed_value)), qubits)

                    # default WS-Mixer
                    # QAOA.ry(-2 * np.arcsin(np.sqrt(precomputed_value)), qubits)
                    # QAOA.rz(-2 * betas[iter], qubits)
                    # QAOA.ry(2 * np.arcsin(np.sqrt(precomputed_value)), qubits)
            else:
                QAOA.rx(2 * betas[iter], range(n_vertices))

        if measure:
            # Finally measure the result in the computational basis
            QAOA.barrier()
            QAOA.measure(range(n_vertices), range(n_vertices)[::-1])

        return QAOA

    @classmethod
    def genQaoaMaxcutCircuit(cls, graph, params, initial=None, p=1):
        template = cls.genQaoaMaxcutCircuitTemplate(
            graph, initial if initial else None, p
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
                    param_name = "γ" + str((i // 2) + 1)
                    parameter = ([x for x in parameters if x.name == param_name])[0]
                    parameter_dict[parameter] = params[i]
                else:
                    # beta
                    param_name = "β" + str((i // 2) + 1)
                    parameter = ([x for x in parameters if x.name == param_name])[0]
                    parameter_dict[parameter] = params[i]
            params = parameter_dict
        return circuit_template.assign_parameters(params)

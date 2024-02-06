import marshmallow as ma
from marshmallow import pre_load, ValidationError
import numpy as np


class HHLAlgorithmRequest:
    def __init__(self, matrix, vector, circuit_format="openqasm2"):
        self.matrix = matrix
        self.vector = vector
        self.circuit_format = circuit_format


class HHLAlgorithmRequestSchema(ma.Schema):
    matrix = ma.fields.List(ma.fields.List(ma.fields.Float()))
    vector = ma.fields.List(ma.fields.Float())
    circuit_format = ma.fields.String()


class QAOAAlgorithmRequest:
    def __init__(
        self,
        pauli_op_string,
        gammas=None,
        betas=None,
        initial_state=None,
        mixer=None,
        reps=1,
        circuit_format="openqasm2",
    ):
        if gammas is None:
            gammas = [1] if reps == None else [1] * reps
        self.initial_state = initial_state
        self.pauli_op_string = pauli_op_string
        self.mixer = mixer
        self.reps = reps
        self.gammas = gammas
        self.betas = betas
        self.circuit_format = circuit_format


class QAOAAlgorithmRequestSchema(ma.Schema):
    initial_state = ma.fields.String()
    pauli_op_string = ma.fields.String(required=True)
    mixer = ma.fields.String()
    reps = ma.fields.Int()
    gammas = ma.fields.List(ma.fields.Float(required=True))
    betas = ma.fields.List(ma.fields.Float(required=True))
    circuit_format = ma.fields.String()


class QFTAlgorithmRequest:
    def __init__(self, n_qubits, inverse, barriers, circuit_format="openqasm2"):
        self.n_qubits = n_qubits
        self.inverse = inverse
        self.barriers = barriers
        self.circuit_format = circuit_format


class QFTAlgorithmRequestSchema(ma.Schema):
    n_qubits = ma.fields.Int()
    inverse = ma.fields.Bool()
    barriers = ma.fields.Bool()
    circuit_format = ma.fields.String()


class QPEAlgorithmRequest:
    def __init__(self, n_eval_qubits, unitary, circuit_format="openqasm2"):
        self.n_eval_qubits = n_eval_qubits
        self.unitary = unitary
        self.circuit_format = circuit_format


class QPEAlgorithmRequestSchema(ma.Schema):
    n_eval_qubits = ma.fields.Int()
    unitary = ma.fields.String()
    circuit_format = ma.fields.String()


class VQEAlgorithmRequest:
    def __init__(
        self, observable, ansatz=None, parameters=None, circuit_format="openqasm2"
    ):
        self.ansatz = ansatz
        self.parameters = parameters
        self.observable = observable
        self.circuit_format = circuit_format


class VQEAlgorithmRequestSchema(ma.Schema):
    ansatz = ma.fields.String()
    parameters = ma.fields.List(ma.fields.Float())
    observable = ma.fields.String()
    circuit_format = ma.fields.String()


class GroverAlgorithmRequest:
    def __init__(
        self,
        oracle,
        iterations=None,
        reflection_qubits=None,
        initial_state=None,
        barriers=None,
        circuit_format="openqasm2",
    ):
        self.oracle = oracle
        self.iterations = iterations
        self.reflection_qubits = reflection_qubits
        self.initial_state = initial_state
        self.barriers = barriers
        self.circuit_format = circuit_format


class GroverAlgorithmRequestSchema(ma.Schema):
    oracle = ma.fields.String(required=True)
    iterations = ma.fields.Int()
    reflection_qubits = ma.fields.List(ma.fields.Int())
    initial_state = ma.fields.String()
    barriers = ma.fields.Bool()
    circuit_format = ma.fields.String()


class MaxCutQAOAAlgorithmRequest:
    def __init__(
        self,
        adj_matrix,
        betas=[1],
        gammas=[1],
        p=1,
        parameterized=False,
        initial_state=None,
        epsilon=0.25,
        circuit_format="openqasm2",
    ):
        self.adj_matrix = adj_matrix
        self.betas = betas
        self.gammas = gammas
        self.p = p
        self.parameterized = parameterized
        self.initial_state = initial_state
        self.epsilon = epsilon
        self.circuit_format = circuit_format


class MaxCutQAOAAlgorithmRequestSchema(ma.Schema):
    adj_matrix = ma.fields.List(ma.fields.List(ma.fields.Float()), required=True)
    betas = ma.fields.List(ma.fields.Float(), required=False)
    gammas = ma.fields.List(ma.fields.Float(), required=False)
    p = ma.fields.Integer(required=False)
    parameterized = ma.fields.Boolean(required=False)
    initial_state = ma.fields.String(required=False)
    epsilon = ma.fields.Float(required=False)
    circuit_format = ma.fields.String()


class TSPQAOAAlgorithmRequest:
    def __init__(self, adj_matrix, p, betas, gammas, circuit_format="openqasm2"):
        self.adj_matrix = adj_matrix
        self.p = p
        self.betas = betas
        self.gammas = gammas
        self.circuit_format = circuit_format


class TSPQAOAAlgorithmRequestSchema(ma.Schema):
    adj_matrix = ma.fields.List(ma.fields.List(ma.fields.Float()))
    p = ma.fields.Integer()
    betas = ma.fields.List(ma.fields.Float())
    gammas = ma.fields.List(ma.fields.Float())
    circuit_format = ma.fields.String()


class KnapsackQAOAAlgorithmRequest:
    def __init__(
        self, items, max_weights, p, betas, gammas, circuit_format="openqasm2"
    ):
        self.items = items
        self.max_weights = max_weights
        self.p = p
        self.betas = betas
        self.gammas = gammas
        self.circuit_format = circuit_format


class KnapsackQAOAAlgorithmRequestSchema(ma.Schema):
    items = ma.fields.List(
        ma.fields.Dict(keys=ma.fields.Str(), values=ma.fields.Float())
    )
    max_weights = ma.fields.Integer()
    p = ma.fields.Integer()
    betas = ma.fields.List(ma.fields.Float())
    gammas = ma.fields.List(ma.fields.Float())
    circuit_format = ma.fields.String()


class ShorDiscreteLogAlgorithmRequest:
    def __init__(self, b, g, p, n=-1, circuit_format="openqasm2"):
        self.b = b
        self.g = g
        self.p = p
        self.n = n
        self.circuit_format = circuit_format


class ShorDiscreteLogAlgorithmRequestSchema(ma.Schema):
    max_weights = ma.fields.Integer()
    b = ma.fields.Integer(required=True)
    g = ma.fields.Integer(required=True)
    p = ma.fields.Integer(required=True)
    n = ma.fields.Integer(required=True)

    circuit_format = ma.fields.String()


class CircuitDrawRequest:
    def __init__(self, circuit):
        self.circuit = circuit


class CircuitDrawRequestSchema(ma.Schema):
    circuit = ma.fields.String()

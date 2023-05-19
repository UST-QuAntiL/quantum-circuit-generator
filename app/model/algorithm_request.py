import marshmallow as ma
from marshmallow import pre_load, ValidationError
import numpy as np


class HHLAlgorithmRequest:
    def __init__(self, matrix, vector):
        self.matrix = matrix
        self.vector = vector


class HHLAlgorithmRequestSchema(ma.Schema):
    matrix = ma.fields.List(ma.fields.List(ma.fields.Float()))
    vector = ma.fields.List(ma.fields.Float())


class QAOAAlgorithmRequest:
    def __init__(self, initial_state, pauli_op_string, mixer, reps, gammas, betas):
        self.initial_state = initial_state
        self.pauli_op_string = pauli_op_string
        self.mixer = mixer
        self.reps = reps
        self.gammas = gammas
        self.betas = betas


class QAOAAlgorithmRequestSchema(ma.Schema):
    initial_state = ma.fields.String()
    pauli_op_string = ma.fields.String(required=True)
    mixer = ma.fields.String()
    reps = ma.fields.Int()
    gammas = ma.fields.List(ma.fields.Float(required=True))
    betas = ma.fields.List(ma.fields.Float())


class QFTAlgorithmRequest:
    def __init__(self, n_qubits, inverse, barriers):
        self.n_qubits = n_qubits
        self.inverse = inverse
        self.barriers = barriers


class QFTAlgorithmRequestSchema(ma.Schema):
    n_qubits = ma.fields.Int()
    inverse = ma.fields.Bool()
    barriers = ma.fields.Bool()


class QPEAlgorithmRequest:
    def __init__(self, n_eval_qubits, unitary):
        self.n_eval_qubits = n_eval_qubits
        self.unitary = unitary


class QPEAlgorithmRequestSchema(ma.Schema):
    n_eval_qubits = ma.fields.Int()
    unitary = ma.fields.String()


class VQEAlgorithmRequest:
    def __init__(self, ansatz, parameters, observable):
        self.ansatz = ansatz
        self.parameters = parameters
        self.observable = observable


class VQEAlgorithmRequestSchema(ma.Schema):
    ansatz = ma.fields.String()
    parameters = ma.fields.List(ma.fields.Float())
    observable = ma.fields.String()


class GroverAlgorithmRequest:
    def __init__(self, oracle, iterations, reflection_qubits, initial_state, barriers):
        self.oracle = oracle
        self.iterations = iterations
        self.reflection_qubits = reflection_qubits
        self.initial_state = initial_state
        self.barriers = barriers


class GroverAlgorithmRequestSchema(ma.Schema):
    oracle = ma.fields.String()
    iterations = ma.fields.Int()
    reflection_qubits = ma.fields.List(ma.fields.Int())
    initial_state = ma.fields.String()
    barriers = ma.fields.Bool()


class MaxCutQAOAAlgorithmRequest:
    def __init__(
        self,
        adj_matrix,
        betas=None,
        gammas=None,
        p=1,
        parameterized=False,
        initial_state=None,
        epsilon=0.25,
    ):
        self.adj_matrix = adj_matrix
        self.betas = betas
        self.gammas = gammas
        self.p = p
        self.parameterized = parameterized
        self.initial_state = initial_state
        self.epsilon = epsilon


class MaxCutQAOAAlgorithmRequestSchema(ma.Schema):
    adj_matrix = ma.fields.List(ma.fields.List(ma.fields.Float()), required=True)
    betas = ma.fields.List(ma.fields.Float(), required=False)
    gammas = ma.fields.List(ma.fields.Float(), required=False)
    p = ma.fields.Integer(required=False)
    parameterized = ma.fields.Boolean(required=False)
    initial_state = ma.fields.String(required=False)
    epsilon = ma.fields.Float(required=False)


class TSPQAOAAlgorithmRequest:
    def __init__(self, adj_matrix, p, betas, gammas):
        self.adj_matrix = adj_matrix
        self.p = p
        self.betas = betas
        self.gammas = gammas


class TSPQAOAAlgorithmRequestSchema(ma.Schema):
    adj_matrix = ma.fields.List(ma.fields.List(ma.fields.Float()))
    p = ma.fields.Integer()
    betas = ma.fields.List(ma.fields.Float())
    gammas = ma.fields.List(ma.fields.Float())


class KnapsackQAOAAlgorithmRequest:
    def __init__(self, items, max_weights, p, betas, gammas):
        self.items = items
        self.max_weights = max_weights
        self.p = p
        self.betas = betas
        self.gammas = gammas


class KnapsackQAOAAlgorithmRequestSchema(ma.Schema):
    items = ma.fields.List(
        ma.fields.Dict(keys=ma.fields.Str(), values=ma.fields.Float())
    )
    max_weights = ma.fields.Integer()
    p = ma.fields.Integer()
    betas = ma.fields.List(ma.fields.Float())
    gammas = ma.fields.List(ma.fields.Float())

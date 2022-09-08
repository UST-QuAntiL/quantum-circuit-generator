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


class VQLSAlgorithmRequest:
    def __init__(self, matrix, vector, alphas, l, lp, ansatz):
        self.matrix = matrix
        self.vector = vector
        self.alphas = alphas
        self.l = l
        self.lp = lp
        self.ansatz = ansatz


class VQLSAlgorithmRequestSchema(ma.Schema):
    matrix = ma.fields.List(ma.fields.List(ma.fields.Float()))
    vector = ma.fields.List(ma.fields.Float())
    alphas = ma.fields.List(ma.fields.Float())
    l = ma.fields.Int()
    lp = ma.fields.Int()
    ansatz = ma.fields.String()


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
    def __init__(self, n_qubits, inverse, barriers):
        self.n_qubits = n_qubits


class VQEAlgorithmRequestSchema(ma.Schema):
    n_qubits = ma.fields.Int()


class GroverAlgorithmRequest:
    def __init__(self, n_qubits, inverse, barriers):
        self.n_qubits = n_qubits


class GroverAlgorithmRequestSchema(ma.Schema):
    n_qubits = ma.fields.Int()


class MaxCutQAOAAlgorithmRequest:
    def __init__(self, matrix, beta, gamma):
        self.adj_matrix = matrix
        self.beta = beta
        self.gamma = gamma


class MaxCutQAOAAlgorithmRequestSchema(ma.Schema):
    adj_matrix = ma.fields.List(ma.fields.List(ma.fields.Float()))
    beta = ma.fields.Float()
    gamma = ma.fields.Float()


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
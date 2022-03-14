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
    def __init__(self, initial_state, pauli_op_string, mixer, gammas, betas):
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

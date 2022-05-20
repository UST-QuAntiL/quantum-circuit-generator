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
    def __init__(self, matrix, beta, gamma):
        self.adj_matrix = matrix
        self.beta = beta
        self.gamma = gamma


class QAOAAlgorithmRequestSchema(ma.Schema):
    adj_matrix = ma.fields.List(ma.fields.List(ma.fields.Float()))
    beta = ma.fields.Float()
    gamma = ma.fields.Float()


class QFTAlgorithmRequest:
    def __init__(self, size, approximation_degree, inverse):
        self.size = size
        self.approximation_degree = approximation_degree
        self.inverse = inverse


class QFTAlgorithmRequestSchema(ma.Schema):
    size = ma.fields.Int()
    approximation_degree = ma.fields.Int()
    inverse = ma.fields.Boolean()

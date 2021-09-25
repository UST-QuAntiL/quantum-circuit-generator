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



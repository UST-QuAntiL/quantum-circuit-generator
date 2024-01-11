import marshmallow as ma
from marshmallow import pre_load, ValidationError
import numpy as np


class BasisEncodingRequest:
    def __init__(self, vector, integral_bits, fractional_bits, circuit_format="openqasm2"):
        self.vector = vector
        self.integral_bits = integral_bits
        self.fractional_bits = fractional_bits
        self.circuit_format = circuit_format


class BasisEncodingRequestSchema(ma.Schema):
    vector = ma.fields.List(ma.fields.Float(), required=True)
    integral_bits = ma.fields.Int(required=True)
    fractional_bits = ma.fields.Int(required=True)
    circuit_format = ma.fields.String()


class AngleEncodingRequest:
    def __init__(self, vector, rotation_axis, circuit_format="openqasm2"):
        self.vector = vector
        self.rotation_axis = rotation_axis
        self.circuit_format = circuit_format


class AngleEncodingRequestSchema(ma.Schema):
    vector = ma.fields.List(ma.fields.Float())
    rotation_axis = ma.fields.String()
    circuit_format = ma.fields.String()


class AmplitudeEncodingRequest:
    def __init__(self, vector, circuit_format="openqasm2"):
        self.vector = vector
        self.circuit_format = circuit_format


class AmplitudeEncodingRequestSchema(ma.Schema):
    vector = ma.fields.List(ma.fields.Float())
    circuit_format = ma.fields.String()


class SchmidtDecompositionRequest:
    def __init__(self, vector, circuit_format="openqasm2"):
        self.vector = vector
        self.circuit_format = circuit_format


class SchmidtDecompositionRequestSchema(ma.Schema):
    vector = ma.fields.List(ma.fields.Float())
    circuit_format = ma.fields.String()

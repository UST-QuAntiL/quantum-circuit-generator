from datetime import datetime
import marshmallow as ma
from app.model.encoding_request import (
    BasisEncodingRequestSchema,
    AngleEncodingRequestSchema,
    AmplitudeEncodingRequestSchema,
    SchmidtDecompositionRequestSchema,
)
from app.model.algorithm_request import (
    HHLAlgorithmRequestSchema,
    QAOAAlgorithmRequestSchema,
    QFTAlgorithmRequestSchema,
    QPEAlgorithmRequestSchema,
    VQEAlgorithmRequestSchema,
    GroverAlgorithmRequestSchema,
)
from app.helpermethods import visualizeQasm

class CircuitResponse:
    def __init__(self, circuit, circuit_type, n_qubits, depth, input):
        super().__init__()
        self.circuit = circuit
        self.circuit_type = circuit_type
        self.n_qubits = n_qubits
        self.depth = depth
        self.input = input
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.visualization = visualizeQasm(circuit, input)

    def to_json(self):
        json_circuit_response = {
            "circuit": self.circuit,
            "circuit_type": self.circuit_type,
            "n_qubits": self.n_qubits,
            "depth": self.depth,
            "timestamp": self.timestamp,
            "input": self.input,
            "visualization": self.visualization,
        }
        return json_circuit_response


class CircuitResponseSchema(ma.Schema):
    circuit = ma.fields.String()
    circuit_type = ma.fields.String()
    n_qubits = ma.fields.Int()
    depth = ma.fields.Int()
    timestamp = ma.fields.String()
    visualization = ma.fields.String()

    @property
    def input(self):
        raise NotImplementedError


class BasisEncodingResponseSchema(CircuitResponseSchema):
    input = ma.fields.Nested(BasisEncodingRequestSchema)


class AngleEncodingResponseSchema(CircuitResponseSchema):
    input = ma.fields.Nested(AngleEncodingRequestSchema)


class AmplitudeEncodingResponseSchema(CircuitResponseSchema):
    input = ma.fields.Nested(AmplitudeEncodingRequestSchema)


class SchmidtDecompositionResponseSchema(CircuitResponseSchema):
    input = ma.fields.Nested(SchmidtDecompositionRequestSchema)


class HHLResponseSchema(CircuitResponseSchema):
    input = ma.fields.Nested(HHLAlgorithmRequestSchema)


class QAOAResponseSchema(CircuitResponseSchema):
    input = ma.fields.Nested(QAOAAlgorithmRequestSchema)


class QFTResponseSchema(CircuitResponseSchema):
    input = ma.fields.Nested(QFTAlgorithmRequestSchema)


class QPEResponseSchema(CircuitResponseSchema):
    input = ma.fields.Nested(QPEAlgorithmRequestSchema)


class VQEResponseSchema(CircuitResponseSchema):
    input = ma.fields.Nested(VQEAlgorithmRequestSchema)


class GroverResponseSchema(CircuitResponseSchema):
    input = ma.fields.Nested(GroverAlgorithmRequestSchema)

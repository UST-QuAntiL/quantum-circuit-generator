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

import qiskit.qasm3

def export_circuit(circuit, input):
    if input.parameterized or input.circuit_format == "openqasm3":
        return qiskit.qasm3.dumps(circuit)
    elif input.circuit_format == "openqasm2":
        return circuit.qasm()
    else:
        return 'format unsupported'


class CircuitResponse:
    def __init__(self, circuit, circuit_type, n_qubits, depth, input, circuit_language):
        super().__init__()
        self.circuit = export_circuit(circuit, input)
        self.circuit_type = circuit_type
        self.n_qubits = n_qubits
        self.depth = depth
        self.input = input
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.visualization = visualizeQasm(circuit, input)
        self.circuit_language = circuit_language

    def to_json(self):
        json_circuit_response = {
            "circuit": self.circuit,
            "circuit_type": self.circuit_type,
            "n_qubits": self.n_qubits,
            "depth": self.depth,
            "timestamp": self.timestamp,
            "input": self.input,
            "visualization": self.visualization,
            "circuit_language": self.circuit_language,
        }
        return json_circuit_response


class CircuitResponseSchema(ma.Schema):
    circuit = ma.fields.String()
    circuit_type = ma.fields.String()
    n_qubits = ma.fields.Int()
    depth = ma.fields.Int()
    timestamp = ma.fields.String()
    visualization = ma.fields.String()
    circuit_language = ma.fields.String()

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


class CircuitDrawResponse:
    def __init__(self, visualization):
        super().__init__()
        self.visualization = visualization

    def to_json(self):
        json_circuit_response = {
            "visualization": self.visualization,
        }
        return json_circuit_response


class CircuitDrawResponseSchema(ma.Schema):
    visualization = ma.fields.String()

import codecs
import pickle


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


def export_circuit(circuit, request):
    # THIS OPTION MAY LEAD TO INCOMPATIBLE EXPORT WITH DIFFERENT QISKIT VERSIONS AND IS NOT RECOMMENDED
    if request.circuit_format == "qiskit":
        codecs.encode(pickle.dumps(circuit), "base64").decode(),
    elif (
        hasattr(request, "parameterized") and request.parameterized
    ) or request.circuit_format == "openqasm3":
        circuit_string = qiskit.qasm3.dumps(circuit)
        ### TODO remove once qasm3 import is fixed https://github.com/Qiskit/qiskit-qasm3-import/issues/25 ###
        # remove all prefixes to params
        import re
        patternFind = r"\((\d+\.\d+)\*(.+)\)"
        replacementList = re.findall(patternFind, circuit_string)
        for repl in replacementList:
            patternMatch = r"" + re.escape(repl[0] + "*" + repl[1])
            circuit_string = re.sub(patternMatch, repl[1], circuit_string, 1)
        patternStdGates = r"\"stdgates.inc\""
        circuit_string = re.sub(patternStdGates, "'stdgates.inc'", circuit_string)
        return circuit_string
    elif request.circuit_format == "openqasm2":
        return circuit.qasm()
    else:
        return "format unsupported"


class CircuitResponse:
    def __init__(
        self, circuit, circuit_type, n_qubits, depth, request, circuit_language
    ):
        super().__init__()
        self.circuit = export_circuit(circuit, request)
        self.circuit_type = circuit_type
        self.n_qubits = n_qubits
        self.depth = depth
        self.request = request
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.visualization = visualizeQasm(circuit)
        self.circuit_language = circuit_language

    def to_json(self):
        json_circuit_response = {
            "circuit": self.circuit,
            "circuit_type": self.circuit_type,
            "n_qubits": self.n_qubits,
            "depth": self.depth,
            "timestamp": self.timestamp,
            "request": self.request,
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
    def request(self):
        raise NotImplementedError


class BasisEncodingResponseSchema(CircuitResponseSchema):
    request = ma.fields.Nested(BasisEncodingRequestSchema)


class AngleEncodingResponseSchema(CircuitResponseSchema):
    request = ma.fields.Nested(AngleEncodingRequestSchema)


class AmplitudeEncodingResponseSchema(CircuitResponseSchema):
    request = ma.fields.Nested(AmplitudeEncodingRequestSchema)


class SchmidtDecompositionResponseSchema(CircuitResponseSchema):
    request = ma.fields.Nested(SchmidtDecompositionRequestSchema)


class HHLResponseSchema(CircuitResponseSchema):
    request = ma.fields.Nested(HHLAlgorithmRequestSchema)


class QAOAResponseSchema(CircuitResponseSchema):
    request = ma.fields.Nested(QAOAAlgorithmRequestSchema)


class QFTResponseSchema(CircuitResponseSchema):
    request = ma.fields.Nested(QFTAlgorithmRequestSchema)


class QPEResponseSchema(CircuitResponseSchema):
    request = ma.fields.Nested(QPEAlgorithmRequestSchema)


class VQEResponseSchema(CircuitResponseSchema):
    request = ma.fields.Nested(VQEAlgorithmRequestSchema)


class GroverResponseSchema(CircuitResponseSchema):
    request = ma.fields.Nested(GroverAlgorithmRequestSchema)


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

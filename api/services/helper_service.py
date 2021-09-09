import qiskit
from qiskit.providers.ibmq import IBMQ


def getCircuitCharacteristics(circuit, backend=None):
    if not backend:
        provider = IBMQ.get_provider(hub="ibm-q")
        backend = provider.get_backend("ibmq_qasm_simulator")
        backend = provider.get_backend("ibmq_lima")
    transpiled = qiskit.compiler.transpile(circuit, backend=backend)
    return transpiled.width(), transpiled.depth()

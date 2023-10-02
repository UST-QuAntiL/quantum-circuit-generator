from io import BytesIO
import base64
import codecs
import pickle
from qiskit import QuantumCircuit

def visualizeQasm(circuit, incomingRequest):
    circuit = pickle.loads(codecs.decode(circuit.encode(), "base64")) if hasattr(incomingRequest, "parameterized") and incomingRequest.parameterized else QuantumCircuit.from_qasm_str(circuit)
    if circuit.depth() < 50:
        try:
            return renderLatex(circuit)
        except:
            return renderMatplot(circuit)
    else:
        return "Circuit too large to visualize (maximum depth: 50)"

def renderLatex(circuit):
    latex_circuit = circuit.draw(output='latex')
    buffered = BytesIO()
    latex_circuit.save(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue())
    print(img_str)
    return img_str

def renderMatplot(circuit):
    latex_circuit = circuit.draw(output='mpl')
    buffered = BytesIO()
    latex_circuit.savefig(buffered, format="png")
    img_str = base64.b64encode(buffered.getvalue())
    print(img_str)
    return img_str
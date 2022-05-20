from qiskit.circuit.library import QFT


class QFTAlgorithm:
    @classmethod
    def create_circuit(cls, num_qubits, approx_degree=0, is_inverse=False):
        """

        :param num_qubits: The amount of qubits the QPF works on
        :param approx_degree: The degree to which the circuit will be approximated.
        :param is_inverse: Whether to use inverse QFT
        :return: OpenQASM Circuit

        Creates QFT a QFT circuit using the QFT from Qiskit's library.
        """

        qft_circ = QFT(
            num_qubits,
            approximation_degree=approx_degree,
            inverse=is_inverse,
            name="qft" if not is_inverse else "iqft",
        )
        return qft_circ

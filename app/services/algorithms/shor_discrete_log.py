from typing import Callable

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT

from .shor_arithmetic.brg_mod_exp import mod_exp_brg

import math

from .shor_arithmetic.brg_mod_mult import mult_mod_N_c


class DiscreteLogMoscaEkertSeparateRegister:
    def __init__(
        self,
        b: int,
        g: int,
        p: int,
        n: int = -1,
        mod_exp_constructor: Callable[[int, int, int], QuantumCircuit] = None,
    ) -> None:
        self._b = b
        self._g = g
        self._p = p
        self._n = n

        if mod_exp_constructor is None:
            self._mod_exp_constructor = mod_exp_brg
        else:
            self._mod_exp_constructor = mod_exp_constructor

    def get_circuit(self):
        if self._n == -1:
            n = math.ceil(math.log(self._p, 2))
        else:
            n = self._n
        print("constructing with size n=", n)
        return self._construct_circuit(
            n, self._b, self._g, self._p, self._mod_exp_constructor
        )

    def _construct_circuit(
        self, n: int, b: int, g: int, p: int, mod_exp_constructor
    ) -> QuantumCircuit:
        # infer size of circuit from modular exponentiation circuit
        mod_exp_g = mod_exp_constructor(n, g, p)
        mod_exp_b = mod_exp_constructor(n, b, p)

        iqft = QFT(n).inverse()

        total_circuit_qubits = mod_exp_g.num_qubits
        bottom_register_qubits = total_circuit_qubits - n

        top1reg = QuantumRegister(n, "topstage1")
        top2reg = QuantumRegister(n, "topstage2")
        botreg = QuantumRegister(bottom_register_qubits, "bot")
        meas_stage1 = ClassicalRegister(n, "m1")
        meas_stage2 = ClassicalRegister(n, "m2")

        circuit = QuantumCircuit(top1reg, top2reg, botreg, meas_stage1, meas_stage2)

        # H on top
        circuit.h(top1reg)

        # 1 on bottom
        circuit.x(botreg[0])

        # mod exp g^x mod p
        circuit.append(mod_exp_g, list(top1reg) + list(botreg))

        # iqft top
        circuit.append(iqft, top1reg)

        # h on top2
        circuit.h(top2reg)

        # mod exp b^x' mod p
        circuit.append(mod_exp_b, list(top2reg) + list(botreg))

        # iqft top
        circuit.append(iqft, top2reg)

        # measure top register (stage 1)
        circuit.measure(top1reg, meas_stage1)

        # measurement stage 2
        circuit.measure(top2reg, meas_stage2)

        return circuit


class ShorDiscreteLog:
    """
    b: Finds discrete logarithm of b with respect to generator g and module p.
    g: Generator.
    p: Prime module.
    n: The size of the top register, if not given it will be inferred from the module p.
    """

    @classmethod
    def create_circuit(cls, b, g, p, n):
        shor_discrete_log = DiscreteLogMoscaEkertSeparateRegister(
            b=b, g=g, p=p, n=n
        ).get_circuit()
        return shor_discrete_log

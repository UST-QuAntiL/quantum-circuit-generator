import qiskit
from itertools import product


class ShorDiscreteLog:
    """
    b: Finds discrete logarithm of b with respect to generator g and module p.
    g: Generator.
    p: Prime module.
    r: The order of g if it is known (otherwise it will be calculated)
    n: The size of the top register, if not given it will be inferred from the module p
    """

    @classmethod
    def create_circuit(cls, b, g, p, r, n):
        return None

import ast
from builtins import isinstance
from qiskit.opflow import I, X, Y, Z


class PauliParser:
    @classmethod
    def parse(cls, pauli_string: str):
        tree = ast.parse(pauli_string)
        return cls.instanciate(tree.body[0].value)

    @classmethod
    def instanciate(cls, body):
        if isinstance(body, ast.Num) or isinstance(body, ast.Constant):
            return body.n
        if isinstance(body, ast.UnaryOp):
            if isinstance(body.op, ast.USub):
                return -body.operand.n
        if isinstance(body, ast.Name):
            if body.id == "X":
                return X
            if body.id == "Y":
                return Y
            if body.id == "Z":
                return Z
            if body.id == "I":
                return I
        if isinstance(body, ast.BinOp):
            if isinstance(body.op, ast.Add):
                return cls.instanciate(body.left) + cls.instanciate(body.right)
            if isinstance(body.op, ast.Mult):
                return cls.instanciate(body.left) * cls.instanciate(body.right)
            if isinstance(body.op, ast.Sub):
                return cls.instanciate(body.left) - cls.instanciate(body.right)
            if isinstance(body.op, ast.Div):
                return cls.instanciate(body.left) / cls.instanciate(body.right)
            if isinstance(body.op, ast.BitXor):
                return cls.instanciate(body.left) ^ cls.instanciate(body.right)
        raise Exception("Invalid Pauli string")


# example String
# print(PauliParser.parse('0.5 * ((I^I^Z^Z) + (I^Z^I^Z) + (I^Z^Z^I) + (Z^I^Z^I) + (Z^Z^I^I))'))

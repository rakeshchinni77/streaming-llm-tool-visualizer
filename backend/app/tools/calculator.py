import re
from io import StringIO

from asteval import Interpreter


class CalculatorTool:
    def __init__(self) -> None:
        self._validator = re.compile(r"^[0-9\s\.\+\-\*\/\(\)]+$")

    def calculate(self, expression: str) -> str:
        if not expression or not isinstance(expression, str):
            raise ValueError("Expression must be a non-empty string")

        expression = expression.strip()
        if not expression:
            raise ValueError("Expression must not be empty")

        if not self._validator.match(expression):
            raise ValueError("Invalid calculator expression")

        err_output = StringIO()
        interpreter = Interpreter(usersyms={}, err_writer=err_output)
        result = interpreter(expression)

        if interpreter.error:
            raise ValueError("Invalid calculator expression")

        if isinstance(result, (int, float)):
            return str(result)

        raise ValueError("Calculator expression did not produce a numeric result")

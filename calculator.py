# calculator.py
from math import sqrt, pow, sin, cos, tan, factorial
from utils import CALC_LOG, now_str
import csv

class Calculator:
    """
    Safe-ish evaluator exposing a few math functions.
    Avoids exposing builtins to eval.
    """

    def __init__(self):
        pass

    def _log(self, expr, result):
        try:
            with open(CALC_LOG, "a", newline="", encoding="utf-8") as f:
                w = csv.writer(f)
                w.writerow([now_str(), expr, str(result)])
        except Exception:
            pass

    def evaluate(self, expr: str):
        safe_locals = {
            "sqrt": sqrt,
            "pow": pow,
            "sin": sin,
            "cos": cos,
            "tan": tan,
            "factorial": factorial,
        }
        try:
            result = eval(expr, {"__builtins__": {}}, safe_locals)
            self._log(expr, result)
            return result
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")

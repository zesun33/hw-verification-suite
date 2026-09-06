"""sva.py — Protocol Invariant and Temporal Assertion Verifiers."""

from typing import List, Optional


class TemporalAssertionChecker:
    """Software equivalent of SVA non-overlapping implication (|=>)."""

    def __init__(self, name: str):
        self.name = name
        self.violations = 0
        self.history = []

    def check_implication(self, antecedent_t0: bool, consequent_t1: bool, msg: str = ""):
        """Verifies: antecedent in cycle t implies consequent in cycle t+1."""
        if antecedent_t0 and not consequent_t1:
            self.violations += 1
            error_str = f"SVA VIOLATION [{self.name}]: {msg}"
            self.history.append(error_str)
            return False
        return True

    def assert_zero_violations(self):
        assert self.violations == 0, f"Checker {self.name} accumulated {self.violations} SVA violations:\n" + "\n".join(self.history)

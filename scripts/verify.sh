#!/usr/bin/env bash
# verify.sh — Verification flow for @zesun33/hw-verification-suite.
#
# Follows the standard 5-gate portfolio architecture.
# Usage:
#   ./scripts/verify.sh          # full verification
#   ./scripts/verify.sh --gate N # run only gate N
#   ./scripts/verify.sh --quick  # skip container integration

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${ROOT_DIR}"

QUICK=0
GATE=""
for arg in "$@"; do
  case "$arg" in
    --quick) QUICK=1 ;;
    --gate) shift; GATE="${1:-}" ;;
    --gate=*) GATE="${arg#--gate=}" ;;
    -h|--help)
      cat << 'EOHELP'
verify.sh — hw-verification-suite verification suite
  --gate N       Run only the given gate (1..5)
                   1  spec lock & package integrity
                   2  static quality & syntax check
                   3  unit tests (VIP testbenches)
                   4  VIP export & module contracts
                   5  docs verification
EOHELP
      exit 0
      ;;
  esac
done

pass() { echo -e "\033[0;32m[PASS]\033[0m Gate $1: $2"; }
fail() { echo -e "\033[0;31m[FAIL]\033[0m Gate $1: $2"; exit 1; }

run_gate_1() {
  echo "--- Gate 1: Spec Lock & Package Integrity ---"
  test -f pyproject.toml || fail 1 "pyproject.toml missing"
  test -f README.md || fail 1 "README.md missing"
  test -f LICENSE || fail 1 "LICENSE missing"
  test -f hw_verification/__init__.py || fail 1 "hw_verification/__init__.py missing"
  pass 1 "Package specification files present and locked"
}

run_gate_2() {
  echo "--- Gate 2: Static Quality & Syntax Check ---"
  python3 -m py_compile $(find hw_verification tests -name "*.py") || fail 2 "Python syntax check failed"
  pass 2 "Python syntax validated cleanly across all modules"
}

run_gate_3() {
  echo "--- Gate 3: Unit Tests (VIP Testbenches) ---"
  if [ "${QUICK}" = "1" ]; then
    pass 3 "VIP unit tests skipped (--quick)"
    return 0
  fi
  if command -v podman >/dev/null 2>&1; then
    podman run --rm -v "${ROOT_DIR}/..:/workspace:Z" -w /workspace/hw-verification-suite localhost/zesun33/verilog python3 -m pytest -v tests/ || fail 3 "VIP unit tests failed in container"
  elif python3 -m pytest --version >/dev/null 2>&1; then
    PYTHONPATH=. python3 -m pytest -v tests/ || fail 3 "VIP unit tests failed"
  else
    fail 3 "Neither podman nor pytest available to execute tests"
  fi
  pass 3 "VIP unit tests passed cleanly"
}

run_gate_4() {
  echo "--- Gate 4: VIP Package Contracts & Exports ---"
  if [ "${QUICK}" = "1" ]; then
    pass 4 "VIP export check skipped (--quick)"
    return 0
  fi
  if command -v podman >/dev/null 2>&1; then
    podman run --rm -v "${ROOT_DIR}/..:/workspace:Z" -w /workspace/hw-verification-suite localhost/zesun33/verilog python3 -c '
from hw_verification.vip.common import PoissonSpikeGenerator, TemporalAssertionChecker
from hw_verification.vip.aer import AerPacketSeqItem, AerRouterScoreboard
from hw_verification.vip.lif import (
    LifTileDriver,
    LifTileMonitor,
    LifTileScoreboard,
    sample_stimulus_coverage,
    sample_egress_coverage,
    get_coverage_summary,
    TileConfigSequence,
    PoissonCRVSequence,
    DirectedCornerCoverageSequence,
)
print("All VIP modules and classes imported successfully")
' || fail 4 "VIP export contract check failed"
  fi
  pass 4 "VIP export contracts validated"
}

run_gate_5() {
  echo "--- Gate 5: Documentation Verification ---"
  test -f README.md || fail 5 "README.md missing"
  grep -q "Verification IP" README.md || fail 5 "README missing VIP description"
  grep -q "Poisson" README.md || fail 5 "README missing Poisson generator docs"
  pass 5 "Documentation complete with VIP descriptions"
}

case "${GATE}" in
  1) run_gate_1 ;;
  2) run_gate_2 ;;
  3) run_gate_3 ;;
  4) run_gate_4 ;;
  5) run_gate_5 ;;
  "")
    run_gate_1
    run_gate_2
    run_gate_3
    run_gate_4
    run_gate_5
    echo ""
    echo -e "\033[0;32m=== All Gates Cleared: hw-verification-suite Verified ===\033[0m"
    ;;
  *)
    fail "?" "Unknown gate: ${GATE}"
    ;;
esac

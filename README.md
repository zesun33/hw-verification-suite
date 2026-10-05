# hw-verification-suite

<!-- BEGIN GENERATED PROJECT GUIDE -->

## Purpose and first steps

Reuse Python testbench components for LIF neuron tiles and AER routing.

**Who it is for:** Verification engineers building LIF neuron or AER router testbenches.

**First task:** Inspect the LIF scoreboard and compare its expected membrane state with your design.

**What to expect:** Reusable Python drivers, monitors, scoreboards, and stimulus/coverage utilities.

**Current scope:** Python verification components for specific interfaces. Adapting them to another design requires matching its signals and timing; quick checks skip simulation.

**Start here:** [LIF scoreboard](hw_verification/vip/lif/lif_scoreboard.py).

**Related projects:** [lif-spiking-core](https://github.com/zesun33/lif-spiking-core), [mcp-cocotb](https://github.com/zesun33/mcp-cocotb).

[Choose another project](https://github.com/zesun33/personal-projects/blob/main/GETTING_STARTED.md).
<!-- END GENERATED PROJECT GUIDE -->

> Centralized IEEE 1800.2 PyUVM & Cocotb Verification IP (VIP) Suite for Neuromorphic & Hardware Accelerators.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![Methodology: UVM 1.2](https://img.shields.io/badge/Methodology-IEEE%201800.2%20UVM-purple)](#)

---

## 1. Overview

`hw-verification-suite` is the centralized, reusable Verification IP (VIP) hub providing reusable stimulus, checking, and coverage components for neuromorphic designs:

- **AER 2D Mesh NoC VIP (`hw_verification/vip/aer/`)**: Dimension-Order Routing (DOR) scoreboards, virtual-cut-through protocol checkers, and 2D spatial cross-coverage collectors.
- **LIF Neuromorphic Core VIP (`hw_verification/vip/lif/`)**: Synaptic configuration drivers, membrane potential golden models, SVA temporal refractory assertions, and firing density cross-coverage.
- **Common Behavioral Generators (`hw_verification/vip/common/`)**: Biological Poisson spike generators, temporal implication checkers, and coverage reporting utilities.

---

## 2. Directory Structure

```text
hw-verification-suite/
├── hw_verification/
│   ├── vip/
│   │   ├── aer/            # Address Event Representation VIP
│   │   │   ├── seq_item.py # 16-bit encoded AER spike packets
│   │   │   ├── scoreboard.py # Deadlock-free DOR routing checker
│   │   │   └── coverage.py # 2D mesh spatial distribution bins
│   │   ├── lif/            # Neuromorphic Spiking Core VIP
│   │   │   ├── lif_seq_item.py # Synaptic config & spike vectors
│   │   │   ├── lif_driver.py   # Synchronous BFM
│   │   │   ├── lif_monitor.py  # Passive egress observer
│   │   │   ├── lif_scoreboard.py # Golden model & SVA assertion
│   │   │   └── lif_coverage.py # Firing & refractory cross-coverage
│   │   └── common/
│   │       ├── poisson.py  # Poisson rate distribution generator
│   │       └── sva.py      # Non-overlapping temporal assertion checker
├── tests/
│   └── test_vip_sanity.py  # Unit regression suite
└── pyproject.toml
```

---

## 3. Quick Start

```bash
# Install in editable mode
pip install -e .

# Run test regression
PYTHONPATH=. pytest -v tests/
```

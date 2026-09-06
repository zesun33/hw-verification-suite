# hw-verification-suite

> Centralized IEEE 1800.2 PyUVM & Cocotb Verification IP (VIP) Suite for Neuromorphic & Hardware Accelerators.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](./LICENSE)
[![CI: Passing](https://img.shields.io/badge/CI-Passing-brightgreen)](#)
[![Methodology: UVM 1.2](https://img.shields.io/badge/Methodology-IEEE%201800.2%20UVM-purple)](#)

---

## 1. Overview

`hw-verification-suite` is the centralized, reusable Verification IP (VIP) hub powering industrial-grade pre-silicon sign-off across all neuromorphic computing and hardware accelerator projects in the `zesun33` portfolio:

- **AER 2D Mesh NoC VIP (`vip/aer/`)**: Dimension-Order Routing (DOR) scoreboards, virtual-cut-through protocol checkers, and 2D spatial cross-coverage collectors.
- **LIF Neuromorphic Core VIP (`vip/lif/`)**: Synaptic configuration drivers, membrane potential golden models, SVA temporal refractory assertions, and firing density cross-coverage.
- **Common Behavioral Generators (`vip/common/`)**: Biological Poisson spike generators, temporal implication checkers, and coverage reporting utilities.

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
│   │   │   ├── seq_item.py # Synaptic config & spike vectors
│   │   │   ├── driver.py   # Synchronous BFM
│   │   │   ├── monitor.py  # Passive egress observer
│   │   │   ├── scoreboard.py # Golden model & SVA assertion
│   │   │   └── coverage.py # Firing & refractory cross-coverage
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

# MMALS Geometric Path Memory

**Suggested repository name:** `mmals-geometric-path-memory`

**Short description:** A reproducible engineering study and interactive lab translating Lindblad-Uhlmann open-system geometry into path-sensitive continual learning, domain-shift diagnostics, and evidence-aware AI systems.

## What this repository contains

This repository turns a critical reading of *Open Quantum Dynamics, Coadjoint Orbits, and Uhlmann Holonomy* into a reproducible engineering package. It does **not** claim that the source manuscript's theorems are already publication-ready. Instead, it:

- explains the ideas at three levels: 12-year-old, engineer, and mathematical;
- corrects key geometric oversimplifications involving degeneracy, tangent/normal decomposition, entropy level sets, and path memory;
- derives an engineering abstraction for path-sensitive state evolution;
- applies it to MMALS continual learning, EO/IR domain shift, identity fraud, and evidence-aware test governance;
- provides standalone browser tools and executable notebooks;
- includes tests and CI for reproducibility.

## Quick start

### Read the report

- Compiled PDF: [`docs/Geometric_Path_Memory.pdf`](docs/Geometric_Path_Memory.pdf)
- LaTeX source: [`docs/main.tex`](docs/main.tex)

### Open the interactive tools

No installation is required. Open these files in a modern browser:

- [`tools/open_quantum_order_lab.html`](tools/open_quantum_order_lab.html)
- [`tools/mmals_path_memory_lab.html`](tools/mmals_path_memory_lab.html)

### Run the Python labs

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev,notebooks]"
pytest
jupyter lab
```

### Build the PDF

```bash
make pdf
```

## Repository map

```text
.
├── docs/                  LaTeX report, bibliography, compiled PDF
├── notebooks/             Executable engineering labs
├── tools/                 Standalone interactive HTML tools
├── src/mmals_path_memory/ Reusable geometry and simulation code
├── tests/                 Numerical tests
├── examples/              Minimal runnable examples
├── scripts/               Build and validation scripts
└── .github/workflows/     CI pipeline
```

## Scientific stance

The package separates three layers:

1. **Established background:** density matrices, GKSL/Lindblad dynamics, coadjoint orbits, Uhlmann parallel transport.
2. **Claims in the reviewed manuscript:** geometric obstruction, curvature-dissipation coupling, gauge reduction, and geometric memory interpretation.
3. **Our engineering proposal:** tangent/transverse regime diagnostics, order-sensitive continual-learning metrics, and path-aware evidence models.

The third layer is a research program to validate, not a proved equivalence between quantum physics and machine learning.

## Primary engineering hypothesis

For a density-like state descriptor `rho_t`, decompose local change as

```text
d rho_t = d rho_t_parallel + d rho_t_transverse.
```

- `d rho_t_parallel`: reorientation inside a regime while preserving spectral structure to first order.
- `d rho_t_transverse`: structural change of the spectrum, indicating drift, specialization, forgetting, or regime transition.

Path order is measured with non-commutativity proxies and, where appropriate, discrete Uhlmann transport.

## License

MIT License. See [`LICENSE`](LICENSE).

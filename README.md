# MMALS Geometric Path Memory

<p align="center">
  <a href="https://gharbonnier78.github.io/mmals-geometric-path-memory/report/Geometric_Path_Memory.pdf">
    <img alt="Read the compiled PDF" src="https://img.shields.io/badge/READ_THE_COMPILED_PDF-B30B00?style=for-the-badge&logo=adobeacrobatreader&logoColor=white">
  </a>
  <a href="https://gharbonnier78.github.io/mmals-geometric-path-memory/tools/open_quantum_order_lab.html">
    <img alt="Open Quantum Order Lab" src="https://img.shields.io/badge/OPEN_QUANTUM_ORDER_LAB-4B32C3?style=for-the-badge&logo=atom&logoColor=white">
  </a>
  <a href="https://gharbonnier78.github.io/mmals-geometric-path-memory/tools/mmals_path_memory_lab.html">
    <img alt="Open MMALS Path Memory Lab" src="https://img.shields.io/badge/OPEN_MMALS_PATH_MEMORY_LAB-006B5E?style=for-the-badge&logo=python&logoColor=white">
  </a>
</p>

<p align="center">
  <a href="https://github.com/gharbonnier78/mmals-geometric-path-memory/actions/workflows/ci.yml">
    <img alt="CI" src="https://github.com/gharbonnier78/mmals-geometric-path-memory/actions/workflows/ci.yml/badge.svg">
  </a>
  <a href="https://github.com/gharbonnier78/mmals-geometric-path-memory/actions/workflows/pages.yml">
    <img alt="GitHub Pages" src="https://github.com/gharbonnier78/mmals-geometric-path-memory/actions/workflows/pages.yml/badge.svg">
  </a>
  <a href="LICENSE">
    <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-yellow.svg">
  </a>
</p>

> **Live tools:** the two large buttons above open the deployed browser applications. If GitHub Pages has not completed its first deployment yet, use the source links in [Interactive tools](#interactive-tools) and enable **Settings -> Pages -> Source: GitHub Actions** once.

**Short description:** A reproducible engineering study and interactive lab translating Lindblad-Uhlmann open-system geometry into path-sensitive continual learning, domain-shift diagnostics, and evidence-aware AI systems.

## What this repository contains

This repository turns a critical reading of *Open Quantum Dynamics, Coadjoint Orbits, and Uhlmann Holonomy* into a reproducible engineering package. It does **not** claim that the source manuscript's theorems are already publication-ready. Instead, it:

- explains the ideas at three levels: 12-year-old, engineer, and mathematical;
- corrects key geometric oversimplifications involving degeneracy, tangent/normal decomposition, entropy level sets, and path memory;
- derives an engineering abstraction for path-sensitive state evolution;
- applies it to MMALS continual learning, EO/IR domain shift, identity fraud, and evidence-aware test governance;
- provides standalone browser tools and executable notebooks;
- includes tests and CI for reproducibility.

## Direct access

| Deliverable | Open | Source |
|---|---|---|
| Full compiled report | **[Open PDF](https://gharbonnier78.github.io/mmals-geometric-path-memory/report/Geometric_Path_Memory.pdf)** | [`docs/main.tex`](docs/main.tex) |
| Quantum order lab | **[Launch live tool](https://gharbonnier78.github.io/mmals-geometric-path-memory/tools/open_quantum_order_lab.html)** | [`tools/open_quantum_order_lab.html`](tools/open_quantum_order_lab.html) |
| MMALS path-memory lab | **[Launch live tool](https://gharbonnier78.github.io/mmals-geometric-path-memory/tools/mmals_path_memory_lab.html)** | [`tools/mmals_path_memory_lab.html`](tools/mmals_path_memory_lab.html) |
| Project landing page | **[Open live site](https://gharbonnier78.github.io/mmals-geometric-path-memory/)** | [`site/index.html`](site/index.html) |

## Interactive tools

### Open Quantum Order Lab

Compare **rotation then damping** against **damping then rotation**. The tool visualizes Bloch trajectories and reports trace-distance order gaps, entropy, purity, and exportable JSON results.

[![Launch Open Quantum Order Lab](https://img.shields.io/badge/LAUNCH-OPEN_QUANTUM_ORDER_LAB-4B32C3?style=flat-square&logo=atom&logoColor=white)](https://gharbonnier78.github.io/mmals-geometric-path-memory/tools/open_quantum_order_lab.html)
[![View HTML source](https://img.shields.io/badge/VIEW-HTML_SOURCE-lightgrey?style=flat-square&logo=html5)](tools/open_quantum_order_lab.html)

### MMALS Path Memory Lab

Explore covariance geometry, tangent/transverse change, operation non-commutativity, entropy variation, and host-routing recommendations.

[![Launch MMALS Path Memory Lab](https://img.shields.io/badge/LAUNCH-MMALS_PATH_MEMORY_LAB-006B5E?style=flat-square&logo=python&logoColor=white)](https://gharbonnier78.github.io/mmals-geometric-path-memory/tools/mmals_path_memory_lab.html)
[![View HTML source](https://img.shields.io/badge/VIEW-HTML_SOURCE-lightgrey?style=flat-square&logo=html5)](tools/mmals_path_memory_lab.html)

## Notebooks

| Notebook | Local file | Open in Colab |
|---|---|---|
| Open quantum geometry | [`01_open_quantum_geometry.ipynb`](notebooks/01_open_quantum_geometry.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gharbonnier78/mmals-geometric-path-memory/blob/main/notebooks/01_open_quantum_geometry.ipynb) |
| MMALS path memory | [`02_mmals_path_memory.ipynb`](notebooks/02_mmals_path_memory.ipynb) | [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gharbonnier78/mmals-geometric-path-memory/blob/main/notebooks/02_mmals_path_memory.ipynb) |

The CI workflow executes both notebooks and publishes the verified executed copies as a downloadable workflow artifact.

## Quick start

```bash
git clone https://github.com/gharbonnier78/mmals-geometric-path-memory.git
cd mmals-geometric-path-memory
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
├── site/                  GitHub Pages landing page
├── src/mmals_path_memory/ Reusable geometry and simulation code
├── tests/                 Numerical tests
├── examples/              Minimal runnable examples
├── scripts/               Build and validation scripts
└── .github/workflows/     CI and Pages deployment
```

## Scientific stance

The package separates three layers:

1. **Established background:** density matrices, GKSL/Lindblad dynamics, coadjoint orbits, Uhlmann parallel transport.
2. **Claims in the reviewed manuscript:** geometric obstruction, curvature-dissipation coupling, gauge reduction, and geometric memory interpretation.
3. **Our engineering proposal:** tangent/transverse regime diagnostics, order-sensitive continual-learning metrics, and path-aware evidence models.

The third layer is a research program to validate, not a proved equivalence between quantum physics and machine learning.

## Primary engineering hypothesis

For a density-like state descriptor `rho_t`, decompose local change as:

```text
d rho_t = d rho_t_parallel + d rho_t_transverse
```

- `d rho_t_parallel`: reorientation inside a regime while preserving spectral structure to first order.
- `d rho_t_transverse`: structural change of the spectrum, indicating drift, specialization, forgetting, or regime transition.

Path order is measured with non-commutativity proxies and, where appropriate, discrete Uhlmann transport.

## Citation

Use [`CITATION.cff`](CITATION.cff) or GitHub's **Cite this repository** control.

## License

MIT License. See [`LICENSE`](LICENSE).

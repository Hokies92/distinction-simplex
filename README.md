# Distinction Simplex

Alpha v0.2.0: a reproducible Python toolkit for three-axis barycentric geometry, sensitivity diagnostics, overlays, and transparent validity boundaries.

## Install

```bash
python -m pip install -e '.[dev]'
python -m pytest -q
distinction-simplex examples/nine_thinkers.json --output results --plot
```

The three axes are Abstraction (A), Precision (P), and Projection (R). Normalized scores are plotted in an equilateral simplex. Region labels are conventional, not established empirical categories. Normalization discards absolute magnitude, which is retained separately. Scores in the example are illustrative judgments, not validated measurements.

Outputs include analysis.json, positions.csv, validity_report.md and optional PNG plots. See docs/mathematical_specification.md.

# Texas Environmental Flows — Fish Response & Hydrologic Alteration Metrics

Research-code adaptation of Jay A. Oliver's contributions to environmental-flow research in the McManamay Lab at Baylor University.

## Research context
Associated publication: Lueders, M. B., McManamay, R. A., Oliver, J. A., et al. (2026), *Reconstructing Long-Term Historical Hydrologic Alteration to Support Environmental Flows in Texas*, River Research and Applications. https://doi.org/10.1002/rra.70172

The two source notebooks examine relationships between hydrologic alteration (HIT) metrics and fish-population responses across Texas ecoregions using decision-tree regression. **These are regression analyses, not the separate Random Forest altered-vs-unaltered stream classifier.**

## Contents
- `scripts/metric_depth_sweep.py`: fit multi-output decision-tree regressors separately for each HIT metric, by ecoregion and tree depth; export in-sample R² scores.
- `scripts/analyze_depth_runs.py`: summarize mean R² by depth, inspect discrete curvature/inflection candidates, and plot score curves.
- `requirements.txt`: runtime dependencies.
- `data/README.md`: input-data contract.

## Quick start
```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scripts/metric_depth_sweep.py --input data/pre_tree_rerun.RData --r-object ivern --output-dir outputs --metric-count 130 --max-depth 40
python scripts/analyze_depth_runs.py --input outputs/metric_runs.csv --output-dir outputs/analysis
```

You can also supply `--input data/my_data.csv` or `.xlsx` to the first script. Input must include `region`, the predictor HIT metric columns, and numeric fish response columns. The original notebook assumes the first **130** non-ID columns are HIT metrics and the remainder are fish responses; use `--metric-columns` and `--response-columns` to select named columns explicitly. See `--help` for all arguments.

**Data are not included.** The original `pre_tree_rerun.RData` file is required to reproduce the original analysis. Do not interpret a successful run on another dataset as replication of the paper.

## Methodology and limitations
The original notebook fits `DecisionTreeRegressor` using one HIT metric at a time as X and multiple fish variables as Y. The score is the scikit-learn multi-output **training R²**, not feature importance, out-of-sample predictive skill, or causal impact. Depth-sweep results can overfit as depth increases. This refactor preserves that analytical intent while correcting hard-coded paths, accidental index columns, depth indexing, and ecoregion file-order assumptions. It adds input validation and deterministic outputs.

The second script plots ecoregion-level mean R² by depth and reports **candidate** curvature sign changes. These are exploratory inflection indicators, not formally validated ecological thresholds.

## Authorship and reuse
Original research and methods belong to the publication's author team. This repository documents and refactors the author's research scripts; it does not claim sole authorship of the underlying study. Source notebooks remain in [Portfolio-Code-Examples](https://github.com/jayjayanton/Portfolio-Code-Examples/tree/main/Baylor%20Projects/Machine%20Learning%20Scripts). Verify data-sharing and licensing permissions before redistributing input datasets.

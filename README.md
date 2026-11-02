# Environmental Flows in Texas

This repository brings together scripts I developed while working with the McManamay Lab at Baylor University on environmental flows research in Texas. The work covers three related questions: where a stream's watershed lies, whether a stream resembles a reference or altered condition, and how hydrologic alteration metrics relate to fish populations across Texas ecoregions.

The research contributed to Lueders, M. B., McManamay, R. A., Oliver, J. A., et al. (2026), *Reconstructing Long-Term Historical Hydrologic Alteration to Support Environmental Flows in Texas*, *River Research and Applications*. [Read the paper](https://doi.org/10.1002/rra.70172).

## Watershed delineation

`scripts/watershed_delineation.R` reads stream-gage coordinates from a CSV file and submits each location to the Model My Watershed API. It checks the resulting delineation job and saves the watershed boundary as GeoJSON and GeoPackage files. This provides watershed polygons for mapping and subsequent hydrologic analysis.

The original R code is also retained as `scripts/watershed_delineation_original.R`. The newer script accepts file paths as arguments instead of depending on a particular Windows directory. API availability and authentication requirements may have changed since the original project.

## Identifying altered and reference streams

`scripts/stream_reference_random_forest.py` uses measured stream and watershed characteristics to predict the binary reference/non-reference label. It separates training and testing data, fills missing predictor values using the training set, fits a Random Forest classifier, and writes evaluation metrics and feature rankings. It can also generate predictions for a second dataset.

The original analysis was written in a Jupyter notebook and used a Random Forest regressor with rounded predictions. The current classifier is a revised approach, so its results should not be treated as identical to those of the original notebook.

## Hydrologic alteration metrics and fish populations

`scripts/metric_depth_sweep.py` examines relationships between individual HIT metrics and multiple fish response variables. For each ecoregion, it fits decision-tree regressions across a range of maximum tree depths and records the resulting training R² values.

`scripts/analyze_depth_runs.py` summarizes those results by ecoregion, plots how the average R² changes with tree depth, and identifies candidate changes in the curvature of those trends. These are exploratory comparisons, not validated ecological thresholds or estimates of causal effects.

## Running the analysis

Create a Python environment and install the dependencies:

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

To classify streams:

```bash
python scripts/stream_reference_random_forest.py --train data/Final_dataset_testing_updated_eliminatedgages.csv --predict data/Final_dataset_fitting_updated_eliminatedgages.csv
```

To examine HIT metrics and fish responses:

```bash
python scripts/metric_depth_sweep.py --input data/pre_tree_rerun.RData --r-object ivern --output-dir outputs --metric-count 130 --max-depth 40
python scripts/analyze_depth_runs.py --input outputs/metric_runs.csv --output-dir outputs/analysis
```

To delineate watersheds, install the R packages `httr`, `jsonlite`, and `sf`, then run:

```bash
Rscript scripts/watershed_delineation.R data/gages.csv outputs/watersheds
```

The scripts accept configurable paths. See [workflow notes](docs/workflows.md) for expected columns and additional details.

## Data and interpretation

The original research datasets are not included. Running the scripts requires appropriately structured, authorized input data; reproducing the published results also requires the original datasets and further verification. The R workflow depends on an external API.

The R² values from the decision-tree depth sweep are measured on the training data and should not be interpreted as independent predictive validation. Likewise, the Random Forest classifier is a revised implementation rather than an exact reproduction of the earlier regressor.

This repository documents my coding contributions to a collaborative research project; the publication reflects the work of the full author team.

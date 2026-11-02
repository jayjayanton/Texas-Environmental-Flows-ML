# Baylor environmental flows research workflows

## 1. Watershed extraction
`scripts/watershed_delineation.R` accepts a gage CSV with `POINT_X` (longitude), `POINT_Y` (latitude) and `Gage.Number`. It requests a Model My Watershed delineation, polls the returned job, and exports GeoJSON/GeoPackage. This API is third-party and has not been live-tested here. Authorization can be passed using `MMW_AUTHORIZATION` and `MMW_CSRF_TOKEN` environment variables; never commit credentials.

```bash
Rscript scripts/watershed_delineation.R data/gages.csv outputs/watersheds
```

Install R packages: `install.packages(c("httr","jsonlite","sf"))`.

## 2. Altered versus unaltered stream classification
`notebooks/Random_Forest_Model.ipynb` is the original research notebook. Although it used `RandomForestRegressor` and rounded outputs to binary classes, the target `Ref_Non_Ref_Binary` is a binary label. The refactored `scripts/stream_reference_random_forest.py` uses `RandomForestClassifier`, stratified holdout validation, training-only imputation, and reports classification metrics.

```bash
python scripts/stream_reference_random_forest.py --train data/Final_dataset_testing_updated_eliminatedgages.csv --predict data/Final_dataset_fitting_updated_eliminatedgages.csv
```

This is a **methodological modernization**, not a numerically identical replication of the original regressor. The script deliberately excludes original metadata/label columns and uses numeric predictors. Review leakage risks and label definitions before drawing scientific conclusions.

## 3. Fish response / HIT metric regressions
See the root README for `metric_depth_sweep.py` and `analyze_depth_runs.py`. These are a separate regression analysis from the binary stream-classification workflow.

## Data and limitations
The original datasets are not distributed in this repository. Results cannot be reproduced exactly until authorized input datasets are provided and validated. Avoid uploading sensitive or restricted project data.

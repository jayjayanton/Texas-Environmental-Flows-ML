# How I processed the environmental flows data

## Watershed delineation

I used the Model My Watershed API to delineate watersheds for stream gages. The script reads a CSV containing `Gage.Number`, `POINT_X` (longitude), and `POINT_Y` (latitude), sends the coordinates to the API, checks the returned job, and saves the boundaries as GeoJSON and GeoPackage files.

```bash
Rscript scripts/watershed_delineation.R data/gages.csv outputs/watersheds
```

I use the R packages `httr`, `jsonlite`, and `sf`:

```r
install.packages(c("httr", "jsonlite", "sf"))
```

If authentication is required, I pass it through the `MMW_AUTHORIZATION` and `MMW_CSRF_TOKEN` environment variables instead of storing credentials in the script. I haven't tested the updated workflow against the current live API.

## Stream classification

My original Random Forest notebook used `RandomForestRegressor` to predict a binary reference/non-reference label, then rounded the predictions. I later reorganized that analysis into `scripts/stream_reference_random_forest.py`, using `RandomForestClassifier` because the response is categorical.

```bash
python scripts/stream_reference_random_forest.py --train data/Final_dataset_testing_updated_eliminatedgages.csv --predict data/Final_dataset_fitting_updated_eliminatedgages.csv
```

The newer script uses a stratified training/test split and fills missing values from the training data. It also reports classification metrics and feature importance. I treat it as an updated implementation rather than an exact replication of the original notebook.

## HIT metrics and fish responses

For the HIT metric analysis, I first ran a separate multi-output decision-tree regression for each HIT metric in each ecoregion, predicting multiple fish response variables. I repeated these fits across increasing maximum tree depths and recorded the in-sample R². This gave me a set of model-fit curves for each ecoregion.

I then grouped the results by depth and calculated the mean R² across the metrics with available results at that depth. That was how I reduced many individual curves into one average R²-versus-depth curve per ecoregion. I used numerical second derivatives to flag candidate changes in curvature, plotted each ecoregion's average curve with its inflection candidates, and compared the curves together.

My aim was to understand whether the overall pattern of model fit changed at different depths and how those patterns compared across ecoregions. Because the scores were calculated on training data, and because the contributing metrics could vary by depth, I treated these points as exploratory indicators rather than validated ecological thresholds.

```bash
python scripts/metric_depth_sweep.py --input data/pre_tree_rerun.RData --output-dir outputs
python scripts/analyze_depth_runs.py --input outputs/metric_runs.csv --output-dir outputs/analysis
```

The original plots are in [figures](../figures/), while the saved tabular results are in [tables](../tables/).

## Reproducing the analysis

The original input datasets aren't distributed here. The scripts accept configurable paths, but I would still need the authorized research data to compare a fresh run against the historical results. I also distinguish training R² from independent model validation, and model-curve inflection points from ecological thresholds.

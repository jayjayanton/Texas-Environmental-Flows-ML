# Environmental Flows in Texas

I worked on several parts of an environmental flows research project in the McManamay Lab at Baylor University. My work involved delineating watersheds from stream-gage locations, using Random Forest to distinguish reference and non-reference streams, and exploring how hydrologic alteration (HIT) metrics relate to fish populations across Texas ecoregions.

This work was part of the research published by Lueders, M. B., McManamay, R. A., Oliver, J. A., et al. (2026), *Reconstructing Long-Term Historical Hydrologic Alteration to Support Environmental Flows in Texas*, *River Research and Applications*. [Read the paper](https://doi.org/10.1002/rra.70172).

## Watershed delineation

I used R and the Model My Watershed API to retrieve watershed boundaries for stream gages. The workflow takes a gage's coordinates, submits a delineation request, checks the job result, and saves the watershed geometry for further spatial analysis.

I kept the original code in `scripts/watershed_delineation_original.R`. The version in `scripts/watershed_delineation.R` takes input and output paths as arguments, so it no longer depends on my old Windows directory structure. The external API may require updated authentication or endpoints.

## Reference and non-reference stream classification

I used Random Forest to identify streams classified as reference or non-reference based on stream and watershed characteristics. The original notebook used a Random Forest regressor and rounded its predictions to binary classes.

The current `scripts/stream_reference_random_forest.py` uses a classifier instead. It separates training and test data, handles missing values within the modeling pipeline, evaluates the predictions, and can apply the trained model to another dataset. Since the modeling approach changed, its results won't necessarily match my original notebook.

## HIT metrics and fish responses

I also explored how individual hydrologic alteration metrics relate to fish response variables across Texas ecoregions.

In `scripts/metric_depth_sweep.py`, I fit multi-output decision trees for each metric across a range of tree depths and recorded the training R² scores. I then used `scripts/analyze_depth_runs.py` to compare the mean scores by depth and identify possible inflection points in those curves.

Here, tree depth is the number of successive decision splits a tree is allowed to make from its root to a leaf. As I increased the depth, each tree could fit increasingly detailed patterns in a single HIT metric. I plotted the resulting **training R² against tree depth** for each metric and then averaged those curves by ecoregion. The Ecoregion 4 plot contains multiple overlapping lines because each line corresponds to a different HIT metric; the 4 names the ecoregion, not the number of curves. I used changes in the curvature of the average R²-versus-depth curves to identify exploratory inflection points. These reflect changes in model fit as complexity increases, not necessarily ecological thresholds or validated predictive performance. The [figures README](figures/README.md) explains these plots in more detail.

## Figures and results

I've separated the [figures](figures/) from the [tables](tables/) so the plots can be viewed without mixing them with CSV outputs. The figures include the ten-ecoregion analysis, a combined ecoregion comparison, the Ecoregion 4 HIT metric curves, and the original Random Forest feature-importance plot.

## Running the scripts

Create a Python environment and install the dependencies:

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

For the stream classification:

```bash
python scripts/stream_reference_random_forest.py --train data/Final_dataset_testing_updated_eliminatedgages.csv --predict data/Final_dataset_fitting_updated_eliminatedgages.csv
```

For the HIT metric regressions and tree-depth analysis:

```bash
python scripts/metric_depth_sweep.py --input data/pre_tree_rerun.RData --r-object ivern --output-dir outputs --metric-count 130 --max-depth 40
python scripts/analyze_depth_runs.py --input outputs/metric_runs.csv --output-dir outputs/analysis
```

For watershed delineation, install the R packages `httr`, `jsonlite`, and `sf`, then run:

```bash
Rscript scripts/watershed_delineation.R data/gages.csv outputs/watersheds
```

I explain the expected inputs in [data](data/) and the individual steps in [workflow notes](docs/workflows.md).

## Data and limitations

I haven't included the original research datasets, so reproducing the historical results requires access to those inputs and additional verification. The decision-tree R² values are training scores, not independent test performance, and the updated Random Forest classifier is not an exact reproduction of my original regressor.

This repository documents the programming and analysis I contributed to a collaborative project. The published research reflects the work of the full author team.

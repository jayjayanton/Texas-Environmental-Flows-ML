# Tables and results

I use this folder for the numerical outputs from the environmental flows analyses, separate from the plots in [figures](../figures/).

The [ecoregion inflection-point CSV](ecoregion_inflection_indices.csv) records the candidate indices printed by my original regression-tree notebook for the ten Texas ecoregions. These are positions in the calculated arrays, not confirmed ecological thresholds or flow-metric values.

When I rerun the current scripts, `metric_depth_sweep.py` writes `outputs/metric_runs.csv`. The follow-up `analyze_depth_runs.py` script writes `mean_r2_by_depth.csv` and `candidate_inflections.csv` under `outputs/analysis/`.

I haven't included the full original `Metric_Runs_V2.xlsx` file or the research input datasets here.

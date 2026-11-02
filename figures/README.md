# Figures

I saved these plots from my original environmental flows notebooks to show how I explored stream classification and the relationships between hydrologic alteration (HIT) metrics and fish responses.

## How I got from individual metrics to the inflection-point figures

I started by fitting a multi-output decision-tree regression separately for each HIT metric in each ecoregion. For each metric, I varied the maximum tree depth and recorded the training R². The [Ecoregion 4 plot](ecoregion_4_hit_metric_curves.png) shows those individual metric curves overlaid. I used that plot to inspect how their fit changed as the trees became more complex.

I then grouped the runs by **tree depth** within each ecoregion and calculated the **average R² across the metrics with a recorded score at that depth**. This turned the many individual curves into one representative average R²-versus-depth curve for each ecoregion. I was averaging the model scores, not the fish responses themselves.

Next, I applied numerical derivatives to each average curve. I flagged sign changes in the second derivative as candidate inflection points, which helped me investigate where the curvature of the average model-fit trend changed. Those curves became the [ten-ecoregion panels](ecoregion_inflection_panels.png), and I also plotted the averages together in the [combined ecoregion figure](all_ecoregions_comparison.png).

I used this approach to compare broad model behavior across ecoregions instead of selecting one HIT metric as representative of an entire region. The results remain exploratory: deeper trees can overfit, the number of metrics in each depth-wise average can change as individual trees stop splitting, and curvature changes in training R² are not automatically ecological thresholds.

## HIT metrics, tree depth, and inflection points

For each Texas ecoregion, I ran multi-output decision-tree regressions using individual HIT metrics to predict multiple fish response variables. I tested increasing maximum tree depths and recorded the **in-sample R²** for each run.

**Tree depth** is the maximum number of decision splits along a path from the root of a tree to one of its leaves. At depth 1, the tree makes one split along each path; deeper trees can split the metric into progressively narrower ranges and fit more detailed patterns. Increasing depth gives the model greater flexibility, but can also lead to overfitting.

In these figures, the **horizontal axis is tree depth** and the **vertical axis is training R² (variance explained on the same data used to fit the model)**. Each line in the Ecoregion 4 figure represents a **different HIT metric**, not another tree or another ecoregion. There are many overlapping lines because I evaluated many metrics separately. Their different R² curves show how much of the multivariate fish response variability each individual metric could explain at different depths.

I then averaged the scores across metrics within an ecoregion to compare how explained variance changed as the trees became more complex. I used numerical second derivatives of those average curves to flag possible inflection points. These are changes in the shape of **model performance versus tree depth**, rather than proof of a particular flow threshold or ecological tipping point.

### Original notebook figures

- [Ten ecoregion panels](ecoregion_inflection_panels.png) — I plotted the mean R² versus tree depth separately for each of the ten ecoregions, with candidate changes in curve curvature.
- [Ecoregion 4 HIT metric curves](ecoregion_4_hit_metric_curves.png) — I used Ecoregion 4 as an example to show the individual R²-versus-depth curves before averaging the scores across HIT metrics. This figure contains many overlapping lines, each corresponding to a different HIT metric. I then averaged the available metric scores at each depth to produce one representative curve for the ecoregion. The original notebook describes this section as comparing 171 HIT metrics, while an earlier input-selection step uses 130 predictors; the exact number plotted would need to be confirmed from the original run data.
- [All ecoregions combined](all_ecoregions_comparison.png) — After calculating the mean R² curve separately for each ecoregion, I overlaid all ten curves to compare how model fit changed with tree depth across regions.

## Stream classification

- [Random Forest feature importance](random_forest_feature_importance.png) — I used the original stream classification model to examine which predictors contributed most to its predictions.

These are the original PNGs embedded in my notebooks rather than figures recomputed at a higher DPI. I keep numerical results and CSVs separately in [tables](../tables/).

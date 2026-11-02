# Figures

I saved these plots from my original environmental flows notebooks to show how I explored stream classification and the relationships between hydrologic alteration (HIT) metrics and fish responses.

## HIT metrics, tree depth, and inflection points

For each Texas ecoregion, I ran multi-output decision-tree regressions using individual HIT metrics to predict multiple fish response variables. I tested increasing maximum tree depths and recorded the **in-sample R²** for each run.

**Tree depth** is the maximum number of decision splits along a path from the root of a tree to one of its leaves. At depth 1, the tree makes one split along each path; deeper trees can split the metric into progressively narrower ranges and fit more detailed patterns. Increasing depth gives the model greater flexibility, but can also lead to overfitting.

In these figures, the **horizontal axis is tree depth** and the **vertical axis is training R² (variance explained on the same data used to fit the model)**. Each line in the Ecoregion 4 figure represents a **different HIT metric**, not another tree or another ecoregion. There are many overlapping lines because I evaluated many metrics separately. Their different R² curves show how much of the multivariate fish response variability each individual metric could explain at different depths.

I then averaged the scores across metrics within an ecoregion to compare how explained variance changed as the trees became more complex. I used numerical second derivatives of those average curves to flag possible inflection points. These are changes in the shape of **model performance versus tree depth**, rather than proof of a particular flow threshold or ecological tipping point.

### Original notebook figures

- [Ten ecoregion panels](ecoregion_inflection_panels.png) — I plotted the mean R² versus tree depth separately for each of the ten ecoregions, with candidate changes in curve curvature.
- [All ecoregions combined](all_ecoregions_comparison.png) — I overlaid the mean R² curves to compare how model fit changed with depth across regions.
- [Ecoregion 4 HIT metric curves](ecoregion_4_hit_metric_curves.png) — I overlaid the R²-versus-depth curves for the individual HIT metrics in Ecoregion 4. This includes many more than four curves; the *4* refers to the ecoregion number. The original notebook labels this section as comparing **171 HIT metrics**, while an earlier input-selection step used 130 predictors. The exact count plotted should be verified against the original run data.

## Stream classification

- [Random Forest feature importance](random_forest_feature_importance.png) — I used the original stream classification model to examine which predictors contributed most to its predictions.

These are the original PNGs embedded in my notebooks rather than figures recomputed at a higher DPI. I keep numerical results and CSVs separately in [tables](../tables/).

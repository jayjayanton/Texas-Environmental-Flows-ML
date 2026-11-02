# Model figures

This folder contains visual results from the Baylor environmental flows analysis. Tables and CSV files are maintained separately under [tables/](../tables/).

## Multi-output regression and candidate inflection points

- [Ten ecoregion inflection panels](ecoregion_inflection_panels.svg) — original plot embedded in `Regression_Tree_Runs.ipynb`, cell 6. Shows ecoregion-specific mean R² curves and candidate curvature changes.
- [Combined ecoregion comparison](all_ecoregions_comparison.svg) — original notebook figure from cell 9, displaying the ecoregion curves together.
- [Ecoregion 4 HIT metric curves](ecoregion_4_hit_metric_curves.svg) — original notebook figure from cell 11.

These three figures embed the original notebook PNGs inside SVG containers so they can be stored through the text-file interface. They were not recomputed. The candidate inflection points describe the curvature of the *model score versus tree depth* relationship, not validated ecological thresholds.

## Reference versus non-reference stream classification

- [Random Forest confusion matrix](random_forest_confusion_matrix.svg) — recreated from the original notebook's printed test confusion matrix.
- [Random Forest feature importance](random_forest_feature_importance.svg) — recreated from the original notebook's printed top-ten importance values.

These two figures reflect the historical Random Forest **regressor** and rounded binary predictions, not the newer classifier.

For the original source notebooks, see [Portfolio-Code-Examples](https://github.com/jayjayanton/Portfolio-Code-Examples/tree/main/Baylor%20Projects/Machine%20Learning%20Scripts).

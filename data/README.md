# Input data

I haven't uploaded the original research datasets to this repository. To rerun the HIT metric analysis with authorized data, I place `pre_tree_rerun.RData` in this folder or point the script to its location with `--input`.

The original R object is named `ivern`. My notebook used `region` to identify ecoregions, dropped identifiers such as `COMID` and `year`, and treated the first 130 remaining columns as HIT metrics, with the fish response variables after those columns.

For datasets with a different column order, I use `--metric-columns` and `--response-columns` to select them explicitly.

For the stream classification, the scripts expect a labeled CSV with `Ref_Non_Ref_Binary` and numeric stream or watershed predictors. The watershed delineation script needs `Gage.Number`, `POINT_X`, and `POINT_Y`.

I keep restricted data and API credentials out of the repository.

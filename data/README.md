# Input data

Place the authorized `pre_tree_rerun.RData` file here (or use an absolute path with `--input`). The original R object was named `ivern`.

Required columns: `region` (ecoregion identifier), optional `COMID`, `year`, `huc4`, then HIT predictor columns and numeric fish-response columns. The original notebook selected the first 130 predictor columns after dropping identifiers. Explicitly pass `--metric-columns` and `--response-columns` when the layout differs.

No private or restricted data should be committed.

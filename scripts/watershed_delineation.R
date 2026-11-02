#!/usr/bin/env Rscript
# Reusable Model My Watershed API client; endpoint availability/authentication may change.
suppressPackageStartupMessages({
  library(httr)
  library(jsonlite)
  library(sf)
})
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: Rscript scripts/watershed_delineation.R gages.csv output_dir [base_url]\n",
       "Requires POINT_X, POINT_Y and Gage.Number columns. Configure MMW_AUTHORIZATION / MMW_CSRF_TOKEN as needed.")
}
input <- args[[1]]
out <- args[[2]]
base <- if (length(args) >= 3) args[[3]] else "https://modelmywatershed.org"
dir.create(out, recursive = TRUE, showWarnings = FALSE)
gages <- read.csv(input, check.names = FALSE, stringsAsFactors = FALSE)
needed <- c("POINT_X", "POINT_Y", "Gage.Number")
if (!all(needed %in% names(gages))) stop("Missing columns: ", paste(setdiff(needed, names(gages)), collapse=", "))
auth <- Sys.getenv("MMW_AUTHORIZATION", "")
csrf <- Sys.getenv("MMW_CSRF_TOKEN", "")
headers <- c(Accept="application/json")
if (nzchar(auth)) headers <- c(headers, Authorization=auth)
if (nzchar(csrf)) headers <- c(headers, "X-CSRFToken"=csrf)
get_json <- function(response) {
  stop_for_status(response)
  fromJSON(content(response, as="text", encoding="UTF-8"), simplifyVector=FALSE)
}
for (i in seq_len(nrow(gages))) {
  tryCatch({
    name <- as.character(gages[["Gage.Number"]][i])
    x <- as.numeric(gages[["POINT_X"]][i])
    y <- as.numeric(gages[["POINT_Y"]][i])
    if (!is.finite(x) || !is.finite(y)) stop("Invalid coordinates")
    body <- list(location=list(y, x), snappingOn=TRUE, simplify=0.0001, dataSource="nhd")
    response <- POST(paste0(base, "/api/watershed/"), add_headers(.headers=headers),
                     body=toJSON(body, auto_unbox=TRUE), encode="raw",
                     content_type_json(), timeout(60))
    job <- get_json(response)$job
    if (is.null(job)) stop("No job ID returned")
    result <- NULL
    for (attempt in seq_len(30)) {
      status <- get_json(GET(paste0(base, "/api/jobs/", job, "/"),
                             add_headers(.headers=headers), timeout(60)))
      if (!is.null(status$result$watershed$geometry)) {
        result <- status$result$watershed$geometry
        break
      }
      if (!is.null(status$status) && tolower(status$status) %in% c("failed", "error"))
        stop("API job failed")
      Sys.sleep(2)
    }
    if (is.null(result)) stop("Timed out waiting for watershed geometry")
    feature <- list(type="Feature", properties=list(gage_id=name), geometry=result)
    geojson <- list(type="FeatureCollection", features=list(feature))
    safe <- gsub("[^A-Za-z0-9_-]", "_", name)
    target <- file.path(out, paste0("watershed_", safe, ".geojson"))
    writeLines(toJSON(geojson, auto_unbox=TRUE, digits=12), target)
    # Parse and validate returned GeoJSON via sf; write GeoPackage as a GIS-ready output.
    polygon <- st_read(target, quiet=TRUE)
    if (!all(st_is_valid(polygon))) polygon <- st_make_valid(polygon)
    st_write(polygon, file.path(out, paste0("watershed_", safe, ".gpkg")),
             quiet=TRUE, delete_dsn=TRUE)
    message("Saved ", name)
  }, error=function(e) message("Failed gage row ", i, ": ", conditionMessage(e)))
}

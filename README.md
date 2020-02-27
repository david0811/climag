# Climag

## Agricultural impacts of climate change with a focus on uncertainty quantification

### data
- `ACI_output` contains all output from calculations run on PSU ICDS-ACI HPC cluster.
..* `raw` refers to the unprocessed data: GDD, eGDD, precipitation at the county level as well as yields without the county-fixed effects. ..* `processing` processes the raw output: adds the county-fixed effects to the yields (aligns the means).
- `USDA` contains all code to grab and process historical corn yields from the USDA server.
..* `usda_grab` grabs the historical USDA corn yields as well as harvested areas and processes them to account for county GEOID changes, adds in the “OTHER (COMBINED) COUNTIES” results and saves to CSV file. County FIPS codes were downloaded from the USDA website. ..* `processing_USDA` adds the county or state trends (lowess filter) and calculates the shocks. Note the sum of the county/state production does not equal the state/national production.
- `raster` calculates the growing area for corn in each grid cell (from EarthStat) and saves to geopandas file.
- `response` stores yield response functions, taken from the American Climate Prospectus (Hsiang et. al., Science) but originally Schlenker-Roberts form.
- `grids` combines the nex/gmfd grids with the county shapefiles to produce a finer grid for the yield model, and weights each grid cell within a given county by the corn growing area (the weights sum to 1). It is also run to produce the area-weighted grid for the ag variable calculation.

### analysis
Description of analysis goes here.

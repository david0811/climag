# Climag

## Agricultural impacts of climate change with a focus on uncertainty quantification

### Data
The `data` directory contains all of the 'input' data and its processing, including the yield simulation results that were run on the HPC cluster. All parts of the project outside of the analysis (read plotting) are found here.
- `ACI_output` contains all output from calculations run on PSU ICDS-ACI HPC cluster.
  - `raw` refers to the unprocessed data: GDD, eGDD, precipitation at the county level as well as yields without the county-fixed effects.  
  - `processing` processes the raw output: adds the county-fixed effects to the yields (aligns the means).
- `USDA` contains all code to grab and process historical corn yields from the USDA server.
  - `usda_grab` grabs the historical USDA corn yields as well as harvested areas and processes them to account for county GEOID changes, adds in the “OTHER (COMBINED) COUNTIES” results and saves to CSV file. County FIPS codes were downloaded from the USDA website.
  - `processing_USDA` adds the county or state trends (lowess filter) and calculates the shocks. Note the sum of the county/state production does not equal the state/national production.
- `raster` calculates the growing area for corn in each grid cell (from EarthStat) and saves to geopandas file.
- `response` stores yield response functions, taken from the [Hsiang et. al.](https://science.sciencemag.org/content/356/6345/1362.full?ijkey=x3wZ8kcgtomUM&keytype=ref&siteid=sci) but originally Schlenker-Roberts form.
- `grids` combines the nex/gmfd grids with the county shapefiles to produce a finer grid for the yield model, and weights each grid cell within a given county by the corn growing area (the weights sum to 1). It is also run to produce the area-weighted grid for the agvar calculation.
- `conus_shp` contains all GeoPandas data files and processing necessary for grid calculations and plotting.

### Analysis
The `analysis` directory contains everything required to make the plots, or generally to extract useful insight from this project.
- `weights` contains the county-to-national aggregation weights, taken as the production fraction by each county, each year, from the USDA data.
- `combine` takes all agvar/yield data files and combines them into one datafile.

### Needs checking...
- Do the yields change significantly if calculated without using the EarthStat weights (corn growing area) and instead by a simple area average?
- GMFD yields have only been calculated from 1960 onwards but GMFD data starts in 1954??

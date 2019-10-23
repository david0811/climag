# climag
Agricultural impacts of climate change with a focus on uncertainty quantification

## analysis
`county`
`national` calculates county-to-national weights by production share

## model results
Contains all of the yield hindcasts and projections.
Processing de-trends the county-level yields (via the state trends) and offsets the model results so that the time series mean of each county matches the USDA value

## response
Store yield response functions from the American Climate Prospectus (Hsiang et. al., Science)

## usda yields 
Grabs the historical USDA corn yields as well as harvested areas and processes them to account for county GEOID changes, adds in the “OTHER (COMBINED) COUNTIES” results and saves to CSV file.
The county FIPS codes were downloaded from the USDA website.
Grabs the state yields and calculates a lowess filter to the logarithms (the state data is NOT the sum of the county data)
Grabs the national yield and calculates the logarithms (the state data is NOT the sum of the county or state data)

## raster 
Calculates the growing area for corn in each grid cell (from `raster_data` (EARTH STAT) folder) and saves to geopandas file

## grids
`get_counties` removes all non-conterminous counties.
nex/gmfd combines the nex/gmfd grids with the county shapefiles to produce a fine-tuned grid for the yield model, and weights each grid cell within a given county by the corn growing area (the weights sum to 1)

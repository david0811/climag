# climag
Agricultural impacts of climate change with a focus on uncertainty quantification

response: store yield response functions from the American Climate Prospectus (Hsiang et. al., Science)

usda_yields: grabs the historical USDA corn yields as well as harvested areas, processes to account for county GEOID changes, adds in the “OTHER (COMBINED) COUNTIES” results and saves to CSV file, the county FIPS codes were downloaded from the USDA website; grabs the state yields and calculates a lowess filter to the logarithms (the state data is NOT the sum of the county data); grabs the national yield and calculates the logarithms (the state data is NOT the sum of the county or state data)

raster: calculates the growing area for corn in each grid cell (from raster_data (EARTH STAT) folder) and saves to geopandas file

grids: get_counties removes all non-conterminous counties; nex/gmfd combines the nex/gmfd grids with the county shapefiles to produce a fine-tuned grid for the yield model, and weights each grid cell within a given county by the corn growing area (the weights sum to 1)

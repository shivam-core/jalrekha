# Third-party data and software

Application code: existing MIT licence, copyright Shivam Kore (2026).

## OpenStreetMap
© OpenStreetMap contributors. Geographic database licensed under ODbL 1.0, https://www.openstreetmap.org/copyright and https://opendatacommons.org/licenses/odbl/1-0/ . Prepared road/water database files remain ODbL, not MIT. Public derived database: data/processed/network.json, locations.json, public/data/map.geojson. Retrieval and transformation details are in public/data/manifest.json and scripts/prepare_roads.py. Map data downloaded through https://api.openstreetmap.org/api/0.6/map . No claim of official candidate shelter designation.

## Copernicus DEM
Copernicus DEM GLO-30 provided through the AWS Open Data public bucket. Source: https://registry.opendata.aws/copernicus-dem/ . Copernicus Digital Elevation Model is a Digital Surface Model including buildings and vegetation. Contains modified Copernicus data (2021). Original source attribution: © DLR e.V. 2010–2014 and © Airbus Defence and Space GmbH 2014–2018 provided under COPERNICUS by the European Union and ESA; all rights reserved. Review source free licence at https://spacedata.copernicus.eu/collections/copernicus-digital-elevation-model . Terrain derivatives are not relabelled MIT. No endorsement by source organisations is implied.

## MapLibre GL JS 5.6.1
Vendored JS/CSS in public/vendor. BSD 3-Clause licence reproduced in public/vendor/maplibre-LICENSE.txt. https://github.com/maplibre/maplibre-gl-js . Worker code is embedded by the standard distribution. No remote basemap tile or font dependency is required.

Python package licences remain with their respective authors (FastAPI, Pydantic, NetworkX, Uvicorn, Rasterio, PySheds, NumPy, Shapely, PyProj, Pillow). Preparation packages are excluded from deployment.

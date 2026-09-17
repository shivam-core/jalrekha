"""Windowed public Copernicus GLO-30 crop. Preparation only."""
from pathlib import Path
import json
from datetime import datetime, timezone
import rasterio
from rasterio.windows import from_bounds
ROOT=Path(__file__).resolve().parents[1]
URL='https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N18_00_E073_00_DEM/Copernicus_DSM_COG_10_N18_00_E073_00_DEM.tif'
BOUNDS=(73.815,18.475,73.925,18.580)
def main():
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR', GDAL_HTTP_TIMEOUT='45', GDAL_HTTP_MAX_RETRY='1'):
        with rasterio.open(URL) as src:
            window=from_bounds(*BOUNDS,src.transform).round_offsets().round_lengths()
            a=src.read(1,window=window)
            profile=src.profile.copy(); profile.update(width=a.shape[1],height=a.shape[0],transform=src.window_transform(window),compress='deflate')
            with rasterio.open(ROOT/'data/raw/dem.tif','w',**profile) as out: out.write(a,1)
            info=dict(source=URL,retrieved_at=datetime.now(timezone.utc).isoformat(),bounds=list(rasterio.windows.bounds(window,src.transform)),crs=str(src.crs),shape=list(a.shape),minimum=float(a.min()),maximum=float(a.max()),nodata=src.nodata)
            (ROOT/'data/raw/dem-metadata.json').write_text(json.dumps(info,indent=2)); print(info)
if __name__=='__main__': main()

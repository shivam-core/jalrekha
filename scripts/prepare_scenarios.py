"""Local buffered D8 HAND preparation, projected road sampling, WGS84 overlays."""
from pathlib import Path
import json,hashlib,copy
import numpy as np
import rasterio
from rasterio.warp import calculate_default_transform,reproject,Resampling
from rasterio.features import rasterize
from rasterio.transform import from_bounds,rowcol
from pysheds.grid import Grid
from pysheds.sview import Raster
from shapely.geometry import shape,LineString
from shapely.ops import transform as geom_transform
from pyproj import Transformer
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def read(p):return json.loads((ROOT/p).read_text())
def write(p,o):(ROOT/p).parent.mkdir(parents=True,exist_ok=True);(ROOT/p).write_text(json.dumps(o,separators=(',',':'),allow_nan=False))
def main():
    cfg=read('config/pune.json');crs=cfg['metric_crs'];project=Transformer.from_crs(4326,crs,always_xy=True).transform
    with rasterio.open(ROOT/'data/raw/dem.tif') as src:
        affine,w,h=calculate_default_transform(src.crs,crs,src.width,src.height,*src.bounds,resolution=30)
        dem=np.full((h,w),-9999,dtype='float64')
        reproject(rasterio.band(src,1),dem,src_transform=src.transform,src_crs=src.crs,dst_transform=affine,dst_crs=crs,dst_nodata=-9999,resampling=Resampling.bilinear)
        profile=dict(driver='GTiff',width=w,height=h,count=1,dtype='float64',crs=crs,transform=affine,nodata=-9999)
        with rasterio.open(ROOT/'data/cache/projected.tif','w',**profile) as out:out.write(dem,1)
    grid=Grid.from_raster(str(ROOT/'data/cache/projected.tif'));elevation=grid.read_raster(str(ROOT/'data/cache/projected.tif'))
    print('Conditioning',dem.shape,flush=True)
    filled=grid.fill_depressions(grid.fill_pits(elevation));inflated=grid.resolve_flats(filled)
    fdir=grid.flowdir(inflated);acc=grid.accumulation(fdir)
    water=read('data/raw/water.geojson')['features'];shapes=[geom_transform(project,shape(f['geometry'])).buffer(15) for f in water]
    river=rasterize([(s,1) for s in shapes],out_shape=dem.shape,transform=affine,fill=0).astype(bool)
    mask_view=copy.deepcopy(elevation.viewfinder);mask_view.nodata=False
    drainage=Raster((np.asarray(acc)>cfg['stream_threshold_cells'])|river,viewfinder=mask_view)
    hand=np.asarray(grid.compute_hand(fdir,inflated,drainage));hand[(dem==-9999)|~np.isfinite(hand)]=np.nan
    hand=np.where(np.isfinite(hand),np.maximum(hand,0),np.nan)
    profile.update(nodata=np.nan)
    with rasterio.open(ROOT/'data/cache/hand.tif','w',**profile) as out:out.write(hand,1)
    bounds=cfg['bounds'];dw,dh=360,300;display=np.full((dh,dw),np.nan);display_transform=from_bounds(*bounds,dw,dh)
    reproject(hand,display,src_transform=affine,src_crs=crs,src_nodata=np.nan,dst_transform=display_transform,dst_crs='EPSG:4326',dst_nodata=np.nan,resampling=Resampling.nearest)
    net=read('data/processed/network.json');loc=read('data/processed/locations.json')
    def sample_coords(coords):
        xx,yy=zip(*(project(*c) for c in coords));rr,cc=rowcol(affine,xx,yy);rr=np.asarray(rr);cc=np.asarray(cc);valid=(rr>=0)&(rr<h)&(cc>=0)&(cc<w);vals=np.full(len(rr),np.nan);vals[valid]=hand[rr[valid],cc[valid]];return vals
    samples={}
    for e in net['edges']:
        line=LineString([project(*c) for c in e['geometry']]);ds=np.linspace(0,line.length,max(2,int(np.ceil(line.length/cfg['sample_interval_m']))+1));pts=[line.interpolate(d) for d in ds];rr,cc=rowcol(affine,[p.x for p in pts],[p.y for p in pts]);vals=np.array([hand[r,c] if 0<=r<h and 0<=c<w else np.nan for r,c in zip(rr,cc)]);samples[e['id']]=vals
    def status(vals,level):return 'unknown' if not np.all(np.isfinite(vals)) else 'inundated' if level>0 and np.any(vals<=level) else 'usable'
    levels={};uncertain=[e['id'] for e in net['edges'] if e['bridge'] or e['tunnel']]
    for dm in range(0,81,5):
        level=dm/10;unavailable=[];unknown=[]
        for e in net['edges']:
            vals=samples[e['id']]
            if not np.all(np.isfinite(vals)):unknown.append(e['id'])
            elif not e['bridge'] and not e['tunnel'] and level>0 and np.any(vals<=level):unavailable.append(e['id'])
        rgba=np.zeros((dh,dw,4),dtype=np.uint8);wet=np.isfinite(display)&(display<=level)&(level>0);rgba[wet]=[61,156,232,155]
        # Unknown terrain is an explicit neutral hatch, never classified as dry.
        missing=~np.isfinite(display);yy,xx=np.indices(display.shape);rgba[missing&((xx+yy)%7<2)]=[181,194,202,90]
        path=f'public/data/water/level-{dm:02d}.png';(ROOT/path).parent.mkdir(parents=True,exist_ok=True);Image.fromarray(rgba).save(ROOT/path)
        levels[str(dm)]={'level_m':level,'unavailable_edge_ids':unavailable,'unknown_edge_ids':unknown,'uncertain_edge_ids':uncertain,'origin_status':{o['id']:status(sample_coords([o['coordinates']]),level) for o in loc['origins']},'shelter_status':{s['id']:status(sample_coords([s['coordinates']]),level) for s in loc['shelters']},'overlay_url':'/'+path.removeprefix('public/'),'image_coordinates':[[bounds[0],bounds[3]],[bounds[2],bounds[3]],[bounds[2],bounds[1]],[bounds[0],bounds[1]]],'display_inundated_cells':int(wet.sum())}
    hazards={'mode':'hand','levels':levels};write('data/processed/hazards.json',hazards)
    digest=hashlib.sha256()
    for p in ['data/processed/network.json','data/processed/locations.json','data/processed/hazards.json','config/pune.json']:digest.update((ROOT/p).read_bytes())
    version=digest.hexdigest()[:16]
    manifest={'schema_version':'1','dataset_version':version,'name':cfg['name'],'bounds':bounds,'crs':'EPSG:4326','analysis_crs':crs,'levels':[x/2 for x in range(17)],'sources':[read('data/raw/osm-metadata.json'),read('data/raw/dem-metadata.json')|{'license':'Copernicus DEM free licence; source credits in THIRD_PARTY_NOTICES.md'}],'settings':cfg,'hydrology':{'method':'Pit fill, depression fill, flat resolution, D8 flow, accumulation, HAND to downstream drainage','resolution_m':30,'stream_threshold_cells':500,'river_adjustment':'OSM mapped water geometry buffered by 15 m is added to accumulation drainage; no DEM burning. Hydrology outside the OSM extract uses accumulation alone.','valid_display_fraction':round(float(np.isfinite(display).mean()),4),'display_grid':[dw,dh],'drainage_cells':int(np.asarray(drainage).sum()),'observed_river_cells':int(river.sum())},'assumptions':['Planning simulation, not flood prediction or emergency navigation.','Population is assumed already at each assembly road node; travel from homes is excluded.','Candidate sites and capacities are assumptions, not official shelters.','All vehicle travel uses an assumed 20 km/h, no traffic or vehicle-capacity model.','Allocation may split groups; families are not preserved.','Bridge and tunnel deck heights are unknown; they stay usable unless explicitly closed or terrain coverage is missing.','HAND is a relative terrain scenario, not a gauge reading.','Unknown terrain is excluded conservatively. A small buffered catchment is not the upstream basin.'],'bounds_reason':cfg['bounds_reason']}
    write('data/processed/manifest.json',manifest);write('public/data/manifest.json',manifest)
    print('Dataset',version,'valid fraction',manifest['hydrology']['valid_display_fraction'],flush=True)
    for k in ('0','25','50','80'):print(k,{x:len(levels[k][x]) for x in ('unavailable_edge_ids','unknown_edge_ids')},levels[k]['origin_status'],levels[k]['shelter_status'])
if __name__=='__main__':main()

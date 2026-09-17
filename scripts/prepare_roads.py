"""Prepare directed unsimplified real OSM road links, retaining each way segment."""
import json, math, xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone
import networkx as nx
ROOT=Path(__file__).resolve().parents[1]
def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,separators=(',',':'),ensure_ascii=False))
def main():
    root=ET.parse(ROOT/'data/raw/osm.xml').getroot()
    nodes={n.attrib['id']:[float(n.attrib['lon']),float(n.attrib['lat'])] for n in root.findall('node')}
    allowed={'motorway','motorway_link','trunk','trunk_link','primary','primary_link','secondary','secondary_link','tertiary','tertiary_link','unclassified','residential','living_street','service'}
    edges=[];features=[];water=[]
    def distance(a,b):
        return 6371000*2*math.asin(math.sqrt(math.sin(math.radians(b[1]-a[1])/2)**2+math.cos(math.radians(a[1]))*math.cos(math.radians(b[1]))*math.sin(math.radians(b[0]-a[0])/2)**2))
    for way in root.findall('way'):
        tags={t.attrib['k']:t.attrib['v'] for t in way.findall('tag')};refs=[n.attrib['ref'] for n in way.findall('nd')];refs=[r for r in refs if r in nodes];coords=[nodes[r] for r in refs]
        if len(coords)<2:continue
        wid=way.attrib['id']
        if tags.get('waterway') in ('river','stream','canal') or tags.get('natural')=='water':
            polygon=refs[0]==refs[-1] and len(refs)>=4 and tags.get('natural')=='water'
            f={'type':'Feature','geometry':{'type':'Polygon' if polygon else 'LineString','coordinates':[coords] if polygon else coords},'properties':{'kind':'water','name':tags.get('name','Mula–Mutha waterway'),'osm_id':wid}}
            features.append(f);water.append(f)
        if tags.get('highway') not in allowed or tags.get('area')=='yes' or tags.get('access') in ('private','no') or tags.get('motor_vehicle')=='no' or tags.get('motorcar')=='no':continue
        oneway=tags.get('oneway','yes' if tags.get('junction')=='roundabout' or tags.get('highway')=='motorway' else 'no')
        for i,(u,v) in enumerate(zip(refs,refs[1:])):
            length=distance(nodes[u],nodes[v])
            if length<=0:continue
            pairs=[(u,v,0)] if oneway in ('yes','1','true') else [(v,u,1)] if oneway=='-1' else [(u,v,0),(v,u,1)]
            for a,b,d in pairs:
                eid=f'osm-{wid}-{i}-{d}'
                e={'id':eid,'u':a,'v':b,'key':f'{wid}:{i}:{d}','osm_way':wid,'geometry':[nodes[a],nodes[b]],'length_m':round(length,2),'travel_seconds':max(1,round(length/(20/3.6))),'name':tags.get('name',tags['highway'].replace('_',' ').title()),'highway':tags['highway'],'bridge':tags.get('bridge','no')!='no','tunnel':tags.get('tunnel','no')!='no'}
                edges.append(e)
                features.append({'type':'Feature','geometry':{'type':'LineString','coordinates':e['geometry']},'properties':{k:e[k] for k in ('id','name','bridge','tunnel','u','v')}|{'kind':'road'}})
    used={e[k] for e in edges for k in ('u','v')};graph=nx.DiGraph();graph.add_edges_from((e['u'],e['v']) for e in edges)
    connected=max(nx.strongly_connected_components(graph),key=len)
    def nearest(c):return min(connected,key=lambda n:distance(nodes[n],c))
    origin_specs=[('Sangam west assembly',[73.8565,18.532],240),('Sangam east assembly',[73.868,18.5345],180),('Station north assembly',[73.874,18.532],260),('Mangalwar assembly',[73.863,18.522],200),('Rasta Peth assembly',[73.871,18.518],160),('Somwar assembly',[73.879,18.524],220)]
    shelter_specs=[('Candidate A · western corridor',[73.858,18.525],200,True),('Candidate B · southern corridor',[73.867,18.5165],240,True),('Candidate C · station corridor',[73.88,18.530],180,True),('Candidate D · northern corridor',[73.872,18.538],160,True),('Candidate E · additional site',[73.882,18.521],300,False)]
    def loc(idx,name,c,kind,**kw):
        n=nearest(c)
        return {'id':f'{kind}-{idx+1}','name':name,'node':n,'coordinates':nodes[n],'requested_coordinates':c,'snap_distance_m':round(distance(nodes[n],c),1),'source':f'https://www.openstreetmap.org/node/{n}','assumption':'Manually selected scenario assembly/candidate road access node. No designated shelter or facility suitability verified.',**kw}
    origins=[loc(i,n,c,'origin',assumed_population=p) for i,(n,c,p) in enumerate(origin_specs)]
    shelters=[loc(i,n,c,'shelter',capacity=p,default_open=o) for i,(n,c,p,o) in enumerate(shelter_specs)]
    write(ROOT/'data/processed/network.json',{'nodes':{n:nodes[n] for n in sorted(used)},'edges':edges})
    write(ROOT/'data/processed/locations.json',{'origins':origins,'shelters':shelters})
    write(ROOT/'public/data/map.geojson',{'type':'FeatureCollection','features':features})
    write(ROOT/'data/raw/water.geojson',{'type':'FeatureCollection','features':water})
    write(ROOT/'data/raw/osm-metadata.json',{'source':'https://api.openstreetmap.org/api/0.6/map?bbox=73.855,18.515,73.885,18.54','retrieved_at':datetime.fromtimestamp((ROOT/'data/raw/osm.xml').stat().st_mtime,timezone.utc).isoformat(),'bounds':[73.855,18.515,73.885,18.54],'crs':'EPSG:4326','license':'ODbL 1.0','attribution':'© OpenStreetMap contributors','nodes':len(used),'directed_links':len(edges),'water_features':len(water),'strongly_connected_nodes':len(connected),'speed_assumption_kmh':20,'simplification':'None; every original adjacent OSM node pair retained. Stable way/segment/direction key preserves parallel ways.'})
    print('Prepared',len(used),'nodes,',len(edges),'directed links,',len(water),'water features');print('Snaps:',[(x['name'],x['snap_distance_m']) for x in origins+shelters])
if __name__=='__main__':main()

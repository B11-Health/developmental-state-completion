import hashlib, json, struct, urllib.request, zlib
from pathlib import Path
URL='https://data.celltrackingchallenge.net/training-datasets/Fluo-N3DH-CE.zip'
SIZE=3428322151
OUT=Path(__file__).resolve().parent/'source_data'
OUT.mkdir(exist_ok=True)
headers={'User-Agent':'Mozilla/5.0'}
def get_range(a,b):
    req=urllib.request.Request(URL,headers={**headers,'Range':f'bytes={a}-{b}'})
    return urllib.request.urlopen(req).read()
tail_start=SIZE-262144
tail=get_range(tail_start,SIZE-1)
e=tail.rfind(b'PK\x05\x06')
if e<0: raise RuntimeError('EOCD not found')
_,_,_,_,n,cdsize,cdoff,_=struct.unpack('<4s4H2LH',tail[e:e+22])
p=cdoff-tail_start
targets={}
while p<e and tail[p:p+4]==b'PK\x01\x02':
    h=struct.unpack('<4s6H3L5H2L',tail[p:p+46])
    method,csize,usize=h[4],h[8],h[9]
    fnl,exl,coml,off=h[10],h[11],h[12],h[16]
    name=tail[p+46:p+46+fnl].decode('utf-8','replace')
    if name.endswith('/TRA/man_track.txt'):
        targets[name]=(method,csize,usize,off)
    p += 46+fnl+exl+coml
manifest={'archive_url':URL,'archive_content_length':SIZE,'central_directory_entries':n,'files':[]}
for name,(method,csize,usize,off) in sorted(targets.items()):
    hdr=get_range(off,min(off+4095,SIZE-1))
    lh=struct.unpack('<4s5H3L2H',hdr[:30]); fnl,exl=lh[9],lh[10]
    ds=off+30+fnl+exl
    raw=get_range(ds,ds+csize-1)
    data=zlib.decompress(raw,-15) if method==8 else raw
    if len(data)!=usize: raise RuntimeError((name,len(data),usize))
    seq=name.split('/')[1].split('_')[0]
    dest=OUT/f'{seq}_man_track.txt'
    dest.write_bytes(data)
    manifest['files'].append({'archive_path':name,'local_path':str(dest.relative_to(Path(__file__).resolve().parent)),'compressed_size':csize,'uncompressed_size':usize,'local_header_offset':off,'sha256':hashlib.sha256(data).hexdigest()})
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))

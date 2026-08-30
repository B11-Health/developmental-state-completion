import struct, urllib.request, zlib, binascii, time
from pathlib import Path
UA={"User-Agent":"CodeGym-R5/1.0"}
def head(url):
 r=urllib.request.urlopen(urllib.request.Request(url,method="HEAD",headers=UA),timeout=30); return int(r.headers["Content-Length"])
def get_range(url,start,end):
 last=None
 for attempt in range(4):
  try:
   req=urllib.request.Request(url,headers={**UA,"Range":f"bytes={start}-{end}"})
   with urllib.request.urlopen(req,timeout=120) as r: b=r.read()
   if len(b)!=end-start+1: raise RuntimeError(f"range mismatch {len(b)} != {end-start+1}")
   return b
  except Exception as e:
   last=e; time.sleep(1.5*(attempt+1))
 raise last
def central_directory(url):
 n=head(url); st=max(0,n-262144); tail=get_range(url,st,n-1); i=tail.rfind(b"PK\x05\x06")
 if i<0: raise RuntimeError("EOCD not found")
 _,_,_,_,nt,cs32,co32,_=struct.unpack("<4s4H2LH",tail[i:i+22]); cs,co,total=cs32,co32,nt
 if cs32==0xffffffff or co32==0xffffffff or nt==0xffff:
  li=tail.rfind(b"PK\x06\x07",0,i); _,_,off64,_=struct.unpack("<4sLQL",tail[li:li+20]); z=get_range(url,off64,off64+55); vals=struct.unpack("<4sQ2H2L4Q",z[:56]); total,cs,co=vals[7],vals[8],vals[9]
 return total,get_range(url,co,co+cs-1)
def _z64(extra,nu,nc,no):
 pos=0
 while pos+4<=len(extra):
  tag,size=struct.unpack("<HH",extra[pos:pos+4]); data=extra[pos+4:pos+4+size]; pos+=4+size
  if tag!=1: continue
  k=0; out={}
  if nu: out["u"]=struct.unpack("<Q",data[k:k+8])[0]; k+=8
  if nc: out["c"]=struct.unpack("<Q",data[k:k+8])[0]; k+=8
  if no: out["o"]=struct.unpack("<Q",data[k:k+8])[0]
  return out
 return {}
def entries(url):
 total,cd=central_directory(url); pos=0; out=[]
 while pos+46<=len(cd):
  f=struct.unpack("<4s6H3L5H2L",cd[pos:pos+46]); _,_,_,flag,method,_,_,crc,c32,u32,fnl,xl,cl,ds,ia,ea,o32=f
  fn=cd[pos+46:pos+46+fnl]; extra=cd[pos+46+fnl:pos+46+fnl+xl]; name=fn.decode("utf-8" if flag&0x800 else "cp437",errors="replace"); z=_z64(extra,u32==0xffffffff,c32==0xffffffff,o32==0xffffffff)
  out.append({"name":name,"method":method,"crc":crc,"comp_size":z.get("c",c32),"uncomp_size":z.get("u",u32),"local_offset":z.get("o",o32)})
  pos+=46+fnl+xl+cl
 return out
def extract_bytes(url,e):
 off=e["local_offset"]; h=get_range(url,off,off+29); vals=struct.unpack("<4s5H3L2H",h); fnl,xl=vals[-2],vals[-1]; dataoff=off+30+fnl+xl; data=get_range(url,dataoff,dataoff+e["comp_size"]-1) if e["comp_size"] else b""
 raw=data if e["method"]==0 else zlib.decompress(data,-15) if e["method"]==8 else (_ for _ in ()).throw(RuntimeError("unsupported compression"))
 if len(raw)!=e["uncomp_size"] or (binascii.crc32(raw)&0xffffffff)!=e["crc"]: raise RuntimeError("integrity failure")
 return raw
def extract(url,e,outpath):
 raw=extract_bytes(url,e); outpath=Path(outpath); outpath.parent.mkdir(parents=True,exist_ok=True); outpath.write_bytes(raw); return outpath

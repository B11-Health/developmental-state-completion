const fs=require('fs');
(async()=>{
 const [u,f,totalS,chunkS]=process.argv.slice(2); const total=Number(totalS), chunk=Number(chunkS||8388608);
 fs.mkdirSync(require('path').dirname(f),{recursive:true}); if(!fs.existsSync(f)) fs.writeFileSync(f,'');
 const s=fs.statSync(f).size; if(s>=total){console.log(JSON.stringify({done:true,size:s,total}));return;}
 const e=Math.min(total-1,s+chunk-1); const r=await fetch(u,{headers:{Range:`bytes=${s}-${e}`}});
 if(r.status!==206) throw new Error(`HTTP ${r.status}`); const b=Buffer.from(await r.arrayBuffer()); fs.appendFileSync(f,b);
 const size=fs.statSync(f).size; console.log(JSON.stringify({start:s,end:e,got:b.length,size,total,done:size===total}));
})().catch(e=>{console.error(e);process.exit(1)});

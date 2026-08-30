const fs=require('fs'); const path=require('path');
const base=path.join(__dirname,'raw');
const jobs=[
 ['DS0004',17391047,63858868],['DS0005',17391052,56385544],['DS0007',17391061,64939950],['DS0035',17391295,74069986]
].map(([ds,id,total])=>({ds,total,file:path.join(base,`Strobl2025A-${ds}-Movie-FQ.TIF`),url:`https://zenodo.org/api/records/${id}/files/Strobl2025A-${ds}-Movie-FQ.TIF/content`}));
const chunk=Number(process.argv[2]||4194304);
async function one(j){fs.mkdirSync(path.dirname(j.file),{recursive:true}); if(!fs.existsSync(j.file))fs.writeFileSync(j.file,''); const s=fs.statSync(j.file).size; if(s>=j.total)return {ds:j.ds,size:s,total:j.total,done:true}; const e=Math.min(j.total-1,s+chunk-1); const r=await fetch(j.url,{headers:{Range:`bytes=${s}-${e}`}}); if(r.status!==206)throw new Error(`${j.ds} HTTP ${r.status}`); const b=Buffer.from(await r.arrayBuffer()); fs.appendFileSync(j.file,b); const z=fs.statSync(j.file).size; return {ds:j.ds,start:s,end:e,got:b.length,size:z,total:j.total,done:z===j.total};}
Promise.all(jobs.map(one)).then(x=>console.log(JSON.stringify(x))).catch(e=>{console.error(e);process.exit(1)});

import json, urllib.parse, urllib.request
queries=[
"Computational Mechanics Pattern and Prediction Structure and Simplicity Shalizi Crutchfield",
"Nonlinear controllability and observability Hermann Krener",
"Adaptive Submodularity Theory and Applications in Active Learning and Stochastic Optimization Golovin Krause",
"Towards a Unified Theory of State Abstraction for MDPs Li Walsh Littman",
"The information bottleneck method Tishby Pereira Bialek",
"Sliced inverse regression for dimension reduction Li 1991"
]
out=[]
for q in queries:
 u="https://api.openalex.org/works?"+urllib.parse.urlencode({"search":q,"per-page":5,"sort":"relevance_score:desc"})
 req=urllib.request.Request(u,headers={"User-Agent":"CodeGym-T4/1.0"})
 try:
  d=json.load(urllib.request.urlopen(req,timeout=20))
  rs=[]
  for w in d.get("results",[]):
   rs.append({"title":w.get("title"),"year":w.get("publication_year"),"doi":w.get("doi"),"authors":[a.get("author",{}).get("display_name") for a in w.get("authorships",[])[:6]]})
  out.append({"query":q,"results":rs})
 except Exception as e: out.append({"query":q,"error":repr(e),"results":[]})
open(__file__.replace(".py","_raw.json"),"w",encoding="utf-8").write(json.dumps(out,indent=2))
for x in out:
 print("\n##",x["query"]); [print(r["year"],r["title"],r["doi"],r["authors"]) for r in x["results"][:3]]

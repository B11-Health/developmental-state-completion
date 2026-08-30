import json, urllib.parse, urllib.request, time
from pathlib import Path
queries=[
  "Reeb space connected components fibers quotient map",
  "Reeb graph quotient connected components level sets",
  "monotone light factorization connected fibers continuous map",
  "Stein factorization connected fibers quotient topology",
  "global observability nonlinear systems distinguishability local observability",
  "Hermann Krener nonlinear observability rank condition global observability",
  "hybrid systems mode observability location observability discrete mode",
  "hybrid system detectability discrete mode continuous state observability",
  "covering map inverse branches branch index topology",
  "predictive state representations controlled dynamical systems",
  "input output epsilon transducers computational mechanics",
  "bisimulation quotient continuous systems observations",
  "test cover problem pair separation experiments",
  "active diagnosis hypothesis identification experiment design",
  "minimal sufficient statistic future prediction causal states",
]
out=[]
for q in queries:
    u="https://api.openalex.org/works?"+urllib.parse.urlencode({"search":q,"per-page":8,"sort":"relevance_score:desc"})
    req=urllib.request.Request(u,headers={"User-Agent":"CodeGym-T5/1.0"})
    try:
        with urllib.request.urlopen(req,timeout=30) as r: d=json.load(r)
        rs=[]
        for w in d.get("results",[]):
            rs.append({
                "title":w.get("title"),"year":w.get("publication_year"),"doi":w.get("doi"),
                "type":w.get("type"),"cited_by":w.get("cited_by_count"),
                "authors":[a.get("author",{}).get("display_name") for a in w.get("authorships",[])[:8]],
                "source":(w.get("primary_location") or {}).get("source",{}).get("display_name"),
                "openalex":w.get("id")
            })
        out.append({"query":q,"results":rs})
    except Exception as e:
        out.append({"query":q,"error":repr(e),"results":[]})
    time.sleep(.15)
base=Path(__file__).parent
(base/"literature_search_raw.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
for x in out:
    print("\n##",x["query"])
    for r in x["results"][:5]: print(r["year"],"|",r["title"],"|",r["doi"],"|",r["authors"][:3])

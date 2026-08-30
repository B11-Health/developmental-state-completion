import json, time, urllib.parse, urllib.request
from pathlib import Path
QUERIES = [
    "computational mechanics causal states predictive equivalence",
    "predictive state representations controlled dynamical systems",
    "epsilon transducer input output computational mechanics",
    "nonlinear controllability observability Hermann Krener",
    "structural identifiability nonlinear biological systems observability",
    "bisimulation Markov decision process state abstraction",
    "bisimulation metrics Markov decision process Ferns Panangaden Precup",
    "approximate simulation relations control systems Girard Pappas",
    "sliced inverse regression sufficient dimension reduction",
    "information bottleneck predictive information",
    "state predictive information bottleneck",
    "causal representation learning interventions identifiability",
    "test cover problem approximation algorithms",
    "active diagnosis experiment design hypothesis identification",
    "adaptive submodularity active learning experiment design",
    "nonlinear realization theory input output systems",
]
headers={"User-Agent":"CodeGym-T4-theory-deepening/1.0"}
out=[]
for q in QUERIES:
    url="https://api.openalex.org/works?"+urllib.parse.urlencode({"search":q,"per-page":8,"sort":"relevance_score:desc"})
    req=urllib.request.Request(url,headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data=json.load(r)
        rows=[]
        for w in data.get("results",[]):
            rows.append({
                "id":w.get("id"),
                "title":w.get("title"),
                "year":w.get("publication_year"),
                "doi":w.get("doi"),
                "type":w.get("type"),
                "cited_by_count":w.get("cited_by_count"),
                "venue":((w.get("primary_location") or {}).get("source") or {}).get("display_name"),
                "authors":[a.get("author",{}).get("display_name") for a in w.get("authorships",[])[:8]],
            })
        out.append({"query":q,"results":rows})
    except Exception as e:
        out.append({"query":q,"error":repr(e),"results":[]})
    time.sleep(0.25)
Path(__file__).with_name("literature_search_raw.json").write_text(json.dumps({"source":"OpenAlex API","accessed":"2026-08-30","queries":out},indent=2),encoding="utf-8")
print("queries",len(out),"nonempty",sum(bool(x.get("results")) for x in out))

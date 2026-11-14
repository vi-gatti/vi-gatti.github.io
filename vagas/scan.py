#!/usr/bin/env python3
"""Consulta direta às APIs públicas de ATS (só retornam vagas ABERTAS).
Uso: python3 vagas/scan.py [--probe]  -> imprime Markdown com vagas novas."""
import json, re, subprocess, sys, os, concurrent.futures as cf
HERE = os.path.dirname(os.path.abspath(__file__))
CO = json.load(open(os.path.join(HERE, "empresas.json")))
TITLE = re.compile(r"research|insight|voice of (the )?customer|market intelligence|competitive intelligence|(cx|customer experience) (strateg|analy)", re.I)
EXCL_T = re.compile(r"engineer|scientist|developer|sales|account exec|recruit|intern|phd|security research|ai research|ml research|research engineer|robot|chemist|clinical|lab\b|biolog|physic|hardware", re.I)
LOC_OK = re.compile(r"remote|emea|europe|\beu\b|spain|españa|espana|madrid|valencia|val[eè]ncia|anywhere|worldwide|global|home.?based|distributed", re.I)
LOC_BAD = re.compile(r"\b(us|usa|united states|canada|americas|latam|apac|india|brazil|brasil|m[eé]xico|colombia|argentina|australia|singapore|japan)\b(?!.*(emea|europe|spain))", re.I)

def get(url, data=None):
    cmd = ["curl", "-sSL", "--max-time", "25", "-A", "Mozilla/5.0 job-scan", url]
    if data: cmd += ["-H", "Content-Type: application/json", "-d", json.dumps(data)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    try: return json.loads(r.stdout)
    except Exception: return None

def fetch(ats, slug):
    out = []
    if ats == "greenhouse":
        d = get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs")
        for j in (d or {}).get("jobs", []):
            out.append((j["title"], j.get("location", {}).get("name", ""), j["absolute_url"], j.get("updated_at", "")[:10]))
    elif ats == "greenhouse_eu":
        r = subprocess.run(["curl", "-sSL", "--max-time", "25", "-A", "Mozilla/5.0", f"https://job-boards.eu.greenhouse.io/{slug}"], capture_output=True, text=True).stdout
        m = re.search(r'"jobPosts":\{.*?"data":(\[.*?\])\}', r)
        try: data = json.loads(m.group(1)) if m else []
        except Exception: data = re.findall(r'"title":"([^"]+)".*?"location":"([^"]*)","absolute_url":"([^"]+)","published_at":"([^"]{10})', r); data = [dict(title=a, location=b, absolute_url=c, published_at=d) for a, b, c, d in data]
        for j in data:
            out.append((j["title"], j.get("location", ""), j["absolute_url"], (j.get("published_at") or "")[:10]))
    elif ats == "lever":
        for host in ("api.lever.co", "api.eu.lever.co"):
            d = get(f"https://{host}/v0/postings/{slug}?mode=json")
            if isinstance(d, list) and d:
                for j in d:
                    c = j.get("categories", {})
                    loc = " / ".join(filter(None, [c.get("location", ""), j.get("workplaceType", ""), " ".join(c.get("allLocations", []) or [])]))
                    out.append((j["text"], loc, j["hostedUrl"], ""))
                break
    elif ats == "ashby":
        d = get(f"https://api.ashbyhq.com/posting-api/job-board/{slug}")
        for j in (d or {}).get("jobs", []):
            loc = " / ".join(filter(None, [j.get("location", ""), "Remote" if j.get("isRemote") else "", j.get("workplaceType") or "", " ".join(x.get("location", "") for x in j.get("secondaryLocations", []) or [])]))
            out.append((j["title"], loc, j["jobUrl"], (j.get("publishedAt") or "")[:10]))
    elif ats == "recruitee":
        d = get(f"https://{slug}.recruitee.com/api/offers/")
        for j in (d or {}).get("offers", []):
            loc = " / ".join(filter(None, [j.get("location", ""), "Remote" if j.get("remote") else ""]))
            out.append((j["title"], loc, j["careers_url"], (j.get("published_at") or "")[:10]))
    elif ats == "workable":
        d = get(f"https://apply.workable.com/api/v1/widget/accounts/{slug}")
        for j in (d or {}).get("jobs", []):
            loc = " / ".join(filter(None, [j.get("city", ""), j.get("country", ""), "Remote" if j.get("telecommuting") else ""]))
            out.append((j["title"], loc, j["url"], (j.get("published_on") or "")[:10]))
    elif ats == "smartrecruiters":
        content = []
        for off in range(0, 1000, 100):
            d = get(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings?limit=100&offset={off}") or {}
            content += d.get("content", [])
            if len(d.get("content", [])) < 100: break
        for j in content:
            l = j.get("location", {})
            loc = " / ".join(filter(None, [l.get("city", ""), l.get("country", ""), "Remote" if l.get("remote") else ""]))
            out.append((j["name"], loc, f"https://jobs.smartrecruiters.com/{slug}/{j['id']}", (j.get("releasedDate") or "")[:10]))
    return out

def main():
    probe = "--probe" in sys.argv
    seen_f = os.path.join(HERE, "vistas.txt")
    seen = set(open(seen_f).read().split()) if os.path.exists(seen_f) else set()
    tasks = [(n, a, s) for n, (a, s) in CO.items()]
    hits, dead = [], []
    with cf.ThreadPoolExecutor(16) as ex:
        for (n, a, s), jobs in zip(tasks, ex.map(lambda t: fetch(t[1], t[2]), tasks)):
            if not jobs: dead.append(n); continue
            for t, loc, url, dt in jobs:
                if TITLE.search(t) and not EXCL_T.search(t) and LOC_OK.search(loc) and not (LOC_BAD.search(loc) and not re.search(r"emea|europe|spain|portugal", loc, re.I)):
                    if re.search(r"hybrid|on-?site|onsite", loc, re.I) and not re.search(r"madrid|valencia|spain|españa", loc, re.I): continue
                    hits.append((n, t, loc, url, dt))
    if probe: print("SEM RESPOSTA/0 vagas:", ", ".join(sorted(dead)), file=sys.stderr)
    new = [h for h in hits if h[3] not in seen]
    print(f"Empresas consultadas: {len(tasks)} | vagas de pesquisa abertas c/ local compatível: {len(hits)} | novas: {len(new)}\n")
    print("| Empresa | Vaga | Local | Publicada | Link |\n|---|---|---|---|---|")
    for n, t, loc, url, dt in sorted(new, key=lambda h: h[4], reverse=True):
        print(f"| {n} | {t} | {loc[:60]} | {dt or '-'} | [abrir]({url}) |")
    if "--save" in sys.argv:
        with open(seen_f, "a") as f: f.writelines(h[3] + "\n" for h in new)
main()

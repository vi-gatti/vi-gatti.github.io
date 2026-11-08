"""Case studies: one folder per project, one shared layout.

Each project lives in content/cases/<slug>/:
  case.json   order, published flag and layout options
  en.json     texts in English (es.json and pt.json for the other languages;
              a missing language falls back to English)
  cover.svg   cover illustration (shown on the case page and in project lists)
  figures/    optional redrawn diagrams referenced by the texts
Images for a case go in assets/img/<slug>/.

Folders whose name starts with "_" (such as _template) are never built.
A case with "published": false is left out of the site, the lists and the
navigation, unless the build runs with --drafts.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
CASES = ROOT / "content" / "cases"
UI = json.loads((ROOT / "content" / "ui.json").read_text(encoding="utf-8"))
DOT = '<span class="dot" aria-hidden="true"></span>'
IDS = ["overview", "context", "challenge", "objectives", "approach",
       "findings", "decisions", "outcomes", "contribution"]


# Loading ---------------------------------------------------------------------

def load_cases(drafts=False):
    """Return the cases to build, sorted by their order, numbered from 01."""
    cases = []
    for folder in sorted(CASES.iterdir()):
        if not folder.is_dir() or folder.name.startswith("_"):
            continue
        meta = json.loads((folder / "case.json").read_text(encoding="utf-8"))
        if not meta.get("published", False) and not drafts:
            continue
        texts = {}
        for lang in ("en", "es", "pt"):
            f = folder / f"{lang}.json"
            if f.exists():
                texts[lang] = json.loads(f.read_text(encoding="utf-8"))
        texts.setdefault("es", texts["en"])
        texts.setdefault("pt", texts["en"])
        cases.append({"slug": folder.name, "folder": folder, "meta": meta, "texts": texts})
    cases.sort(key=lambda c: c["meta"].get("order", 999))
    for i, c in enumerate(cases, 1):
        c["num"] = f"{i:02d}"
        c["file"] = f"{c['slug']}.html"
    return cases


def svg(case, name, label, decorative=False):
    path = case["folder"] / name
    if not path.exists():
        return ""
    s = path.read_text(encoding="utf-8").replace("{label}", html.escape(label, quote=True))
    if decorative:
        s = re.sub(r'role="img" aria-label="[^"]*"', 'aria-hidden="true" focusable="false"', s, count=1)
    return s


def plain(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text)).replace("‑", "-")


# Small builders --------------------------------------------------------------

def ps(items, ind=14, cls=None):
    pad = " " * ind
    c = f' class="{cls}"' if cls else ""
    return "\n".join(f"{pad}<p{c}>{x}</p>" for x in items)


def section(i, ui, body):
    sid = IDS[i]
    t = ui["toc"][i]
    return f'''          <section class="case-section" id="{sid}" aria-labelledby="{sid}-title">
            <header>
              <p class="label section-num" aria-hidden="true">{i + 1:02d}</p>
              <h2 id="{sid}-title">{t}</h2>
            </header>
{body}
          </section>'''


def numbered_captions(items):
    return "\n".join(f"                <li><span>{x}</span></li>" for x in items)


# Case page -------------------------------------------------------------------

def render_case(case, lang, cases):
    ui = UI[lang]
    c = case["texts"][lang]
    meta = case["meta"]
    S = []

    # 01 overview
    facts = "\n".join(f"              <div><dt>{k}</dt><dd>{v}</dd></div>"
                      for k, v in zip(ui["facts"], c["facts"]))
    highlight = f'\n            <p class="highlight">{c["overview"][2]}</p>' if len(c["overview"]) > 2 else ""
    S.append(section(0, ui, f'''            <p class="lede">{c["overview"][0]}</p>
            <div class="prose">
{ps(c["overview"][1:2])}
            </div>{highlight}
            <dl class="facts-panel">
{facts}
            </dl>'''))

    # 02 context
    S.append(section(1, ui, f'''            <div class="prose">
{ps(c["context"])}
            </div>'''))

    # 03 challenge: questions first when there are questions, statement first otherwise
    statement = f'''            <div class="statement">
              <p class="statement__text">{c["statement"]}</p>
            </div>'''
    if c.get("questions"):
        qs = "\n".join(f"              <li>{x}</li>" for x in c["questions"])
        body = f'''            <div class="prose">
{ps(c.get("challenge_intro", []))}
              <p class="list-lead">{c["questions_lead"]}</p>
            </div>
            <ol class="panel-list">
{qs}
            </ol>
{statement}'''
    else:
        body = f'''{statement}
            <div class="prose">
{ps(c.get("challenge", []))}
            </div>'''
    S.append(section(2, ui, body))

    # 04 objectives
    objs = "\n".join(f"              <li><p>{x}</p></li>" for x in c["objectives"])
    S.append(section(3, ui, f'''            <p class="list-lead">{c["objectives_lead"]}</p>
            <ol class="numbered">
{objs}
            </ol>'''))

    # 05 approach: stages, then photos and redrawn figures when present
    lis = []
    for k, st in enumerate(c["stages"], 1):
        lis.append(f'''              <li>
                <div class="stages__head">
                  <p class="label">{k:02d}</p>
                  <h3>{st["title"]}</h3>
                </div>
                <div class="stages__body">
{ps(st["paras"], 18)}
                </div>
              </li>''')
    body = f'''            <div class="prose">
              <p>{c["approach_intro"]}</p>
            </div>
            <ol class="stages">
{chr(10).join(lis)}
            </ol>'''
    if c.get("photos"):
        folder = f"{{{{root}}}}assets/img/{case['slug']}"
        imgs = []
        for k, ph in enumerate(c["photos"], 1):
            srcset = ", ".join(f"{folder}/{ph['src']}-{w}.webp {w}w" for w in ph["w"])
            imgs.append(f'''                <div class="photo-grid__item photo-grid__item--{ph["cls"]}">
                  <img src="{folder}/{ph['src']}-{ph['w'][0]}.webp" srcset="{srcset}" sizes="(min-width: 64rem) 34rem, 100vw" width="{ph['size'][0]}" height="{ph['size'][1]}" loading="lazy" decoding="async" alt="{ph['alt']}">
                  <span class="photo-grid__num" aria-hidden="true">{k}</span>
                </div>''')
        body += f'''
            <figure class="photo-grid">
              <p class="label photo-grid__label">{c["photos_label"]}</p>
              <div class="photo-grid__images">
{chr(10).join(imgs)}
              </div>
              <figcaption>
                <ol class="photo-grid__captions">
{numbered_captions([p["caption"] for p in c["photos"]])}
                </ol>
              </figcaption>
            </figure>'''
    if c.get("figures"):
        items = []
        for k, fg in enumerate(c["figures"], 1):
            items.append(f'''                <div class="figure-trio__item">
                  {svg(case, f"figures/{fg['key']}.svg", fg["label"])}
                  <span class="photo-grid__num" aria-hidden="true">{k}</span>
                </div>''')
        note = f'\n                <p class="figure-trio__note">{c["figures_note"]}</p>' if c.get("figures_note") else ""
        body += f'''
            <figure class="figure-trio">
              <p class="label photo-grid__label">{c["figures_label"]}</p>
              <div class="figure-trio__images">
{chr(10).join(items)}
              </div>
              <figcaption>
                <ol class="photo-grid__captions">
{numbered_captions([f["caption"] for f in c["figures"]])}
                </ol>{note}
              </figcaption>
            </figure>'''
    S.append(section(4, ui, body))

    # 06 findings, then customer voices when present
    fl = []
    for h, rest in c["findings"]:
        rp = ("\n" + ps(rest, 18)) if rest else ""
        fl.append(f'''              <li class="finding">
                <div>
                  <h3>{h}</h3>{rp}
                </div>
              </li>''')
    grid = " findings--grid" if meta.get("findings_layout") == "grid" else ""
    body = f'''            <ol class="findings{grid}">
{chr(10).join(fl)}
            </ol>'''
    if c.get("quotes"):
        qv = "\n".join(f"                <li>{q}</li>" for q in c["quotes"])
        body += f'''
            <div class="voices">
              <p class="label">{c["quotes_label"]}</p>
              <ul class="voices__list">
{qv}
              </ul>
            </div>'''
    S.append(section(5, ui, body))

    # 07 decisions
    after = f'\n            <div class="prose">\n              <p>{c["decisions_after"]}</p>\n            </div>' if c.get("decisions_after") else ""
    note = f'\n            <p class="note">{c["decisions_note"]}</p>' if c.get("decisions_note") else ""
    items = "\n".join(f"              <li>{x}</li>" for x in c["decisions_items"])
    S.append(section(6, ui, f'''            <div class="prose">
{ps(c["decisions"])}
              <p class="list-lead">{c["decisions_lead"]}</p>
            </div>
            <ol class="panel-list">
{items}
            </ol>{after}{note}'''))

    # 08 outcomes
    stats = ""
    if c.get("stats"):
        rows = "\n".join(f'                <div><dt class="stat-strip__value">{v}</dt><dd>{t}</dd></div>' for v, t in c["stats"])
        stats = f'''
            <div class="stat-strip">
              <p class="label">{c["stats_label"]}</p>
              <dl>
{rows}
              </dl>
            </div>'''
    onote = f'''
            <aside class="note">
              <p class="label">{ui["note"]}</p>
              <p>{c["outcomes_note"]}</p>
            </aside>''' if c.get("outcomes_note") else ""
    S.append(section(7, ui, f'''            <div class="prose">
{ps(c["outcomes"])}
            </div>{stats}{onote}'''))

    # 09 contribution
    S.append(section(8, ui, f'''            <p class="lede">{c["contribution"][0]}</p>
            <div class="prose">
{ps(c["contribution"][1:])}
            </div>'''))

    # Next case: the following published case, wrapping round to the first
    nxt = ""
    if len(cases) > 1:
        i = next(k for k, x in enumerate(cases) if x["slug"] == case["slug"])
        other = cases[(i + 1) % len(cases)]
        nxt = f'''
      <nav class="case-next band" aria-label="{ui["next"]}">
        <div class="wrap">
          <a href="{other["file"]}">
            <span class="label">{ui["next"]} {DOT} {ui["case"]} {other["num"]}</span>
            <span class="case-next__title">{other["texts"][lang]["title"]}</span>
          </a>
        </div>
      </nav>
'''

    toc = "\n".join(f'            <li><a href="#{i}">{t}</a></li>' for i, t in zip(IDS, ui["toc"]))
    tags = "\n".join(f"          <li>{t}</li>" for t in c["tags"])
    page_meta = {
        "title": f"{ui['case']} {case['num']} · {plain(c['title'])} · Virginia Candido Gatti",
        "description": c["meta_desc"], "section": "work", "script": True,
    }
    return f'''<!--meta {json.dumps(page_meta, ensure_ascii=False)} -->
  <main id="main">
    <article>

      <header class="case-hero wrap">
        <p class="label"><a href="work.html">{ui["work"]}</a> <span aria-hidden="true">/</span> {ui["case"]} {case["num"]}</p>
        <h1 class="case-title">{c["title"]}</h1>
        <p class="case-org">{c["sub"]}</p>
        <ul class="tags" aria-label="{ui["scope"]}">
{tags}
        </ul>
      </header>

      <div class="wrap">
        <figure class="cover">
          {svg(case, "cover.svg", c["cover_label"])}
        </figure>
      </div>

      <div class="wrap grid case-layout">
        <nav class="toc" aria-label="{ui["sections_label"]}">
          <p class="label">{ui["on_page"]}</p>
          <ol>
{toc}
          </ol>
        </nav>

        <div class="case-body">

{chr(10).join(S)}

        </div>
      </div>
{nxt}
    </article>
  </main>
'''


# Project lists ---------------------------------------------------------------

def teaser(case, lang, detailed=False):
    ui = UI[lang]
    c = case["texts"][lang]
    heading = "h2" if detailed else "h3"
    head_cls = ' class="teaser__title"' if detailed else ""
    tags = "\n".join(f"              <li>{t}</li>" for t in c["tags"][:3])
    extra = ""
    if detailed:
        keys = [ui["facts"][0], ui["facts"][2], ui["facts"][3], ui["scope"]]
        vals = [c["facts"][0], c["facts"][2], c["facts"][3], ", ".join(c["tags"])]
        rows = "\n".join(f"              <div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in zip(keys, vals))
        extra = f'''
            <dl class="facts">
{rows}
            </dl>'''
    else:
        extra = f'''
            <ul class="tags" aria-label="{ui["scope"]}">
{tags}
            </ul>'''
    return f'''        <article class="grid teaser">
          <a class="teaser__media teaser__cover" href="{case["file"]}" tabindex="-1" aria-hidden="true">
            {svg(case, "cover.svg", "", decorative=True)}
          </a>
          <div class="teaser__body">
            <p class="label"><span class="num">{ui["teaser_case"]} {case["num"]}</span>{c["sector"]} {DOT} {ui["country"]}</p>
            <{heading}{head_cls}><a href="{case["file"]}">{c["title"]}</a></{heading}>
            <p>{c["sub"]}</p>{extra}
            <a class="link-arrow" href="{case["file"]}">{ui["read"]} {case["num"]}</a>
          </div>
        </article>'''


def project_list(cases, lang, detailed=False):
    return "\n\n".join(teaser(c, lang, detailed) for c in cases)

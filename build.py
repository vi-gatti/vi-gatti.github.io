#!/usr/bin/env python3
"""Builds the static site into ./docs (served by GitHub Pages) from ./src and ./assets.

Usage:  python3 build.py            build the published site
        python3 build.py --drafts   also build cases marked "published": false

Case studies are not written as pages: each one lives in content/cases/<slug>/
and is assembled by casekit.py. The project lists on the Home and Work pages
are generated from the published cases (tokens {{selected_work}} and
{{work_list}} in the page sources).

Each page in src/pages/<lang>/ holds only its <main> content, preceded by a
one line meta comment. The shared layout (head, header, language switcher,
footer) lives in src/layout.html. The output in ./site is plain HTML and can
be uploaded to any static host.
"""
import json
import re
import shutil
import sys
from pathlib import Path

import casekit

ROOT = Path(__file__).parent
SRC = ROOT / "src"
OUT = ROOT / "docs"

# Set to the final address (for example "https://example.com/") when the site
# is published, so the language alternates for search engines are generated.
BASE_URL = "https://vi-gatti.github.io/"
YEAR = "2026"

# Contact details, shown in the footer of every page and on the Contact page.
# Phone in international format, digits only after the plus sign.
CONTACT = {
    "phone_display": "+34 603 850 812",
    "phone_e164": "+34603850812",
    "linkedin": "https://www.linkedin.com/in/virginia-gatti",
    "email": "vihhgatti@gmail.com",
}

# English is the default language and lives at the site root.
LANGS = {
    "en": {
        "name": "English", "short": "EN", "dir": "",
        "skip": "Skip to content", "nav_label": "Main", "lang_label": "Language", "theme": "Dark mode", "location": "Valencian Community, Spain",
        "nav": {"about": "About", "work": "Work", "contact": "Contact"},
        "confidential": "Client names and identifying details are withheld for confidentiality.",
    },
    "es": {
        "name": "Español", "short": "ES", "dir": "es/",
        "skip": "Ir al contenido", "nav_label": "Principal", "lang_label": "Idioma", "theme": "Modo oscuro", "location": "Comunidad Valenciana, España",
        "nav": {"about": "Sobre mí", "work": "Proyectos", "contact": "Contacto"},
        "confidential": "Los nombres de clientes y los datos identificables se omiten por confidencialidad.",
    },
    "pt": {
        "name": "Português", "short": "PT", "dir": "pt/",
        "skip": "Ir para o conteúdo", "nav_label": "Principal", "lang_label": "Idioma", "theme": "Modo escuro", "location": "Comunidade Valenciana, Espanha",
        "nav": {"about": "Sobre", "work": "Projetos", "contact": "Contato"},
        "confidential": "Nomes de clientes e informações identificáveis são omitidos por confidencialidade.",
    },
}
NAV_PAGES = {"about": "about.html", "work": "work.html", "contact": "contact.html"}
META_RE = re.compile(r"^<!--meta (\{.*?\}) -->\n", re.S)


def render(lang, filename, text, layout):
    match = META_RE.match(text)
    if not match:
        raise SystemExit(f"Missing meta comment in {lang}/{filename}")
    meta = json.loads(match.group(1))
    main = text[match.end():].rstrip()
    cfg = LANGS[lang]
    root = "../" if cfg["dir"] else ""

    nav = "\n".join(
        f'            <li><a href="{href}"'
        + (' aria-current="page"' if meta.get("section") == key else "")
        + f">{cfg['nav'][key]}</a></li>"
        for key, href in NAV_PAGES.items()
    )
    langs = "\n".join(
        f'            <li><a href="{root}{other["dir"]}{filename}" lang="{code}" hreflang="{code}"'
        + (' aria-current="true"' if code == lang else "")
        + f' title="{other["name"]}"><span aria-hidden="true">{other["short"]}</span>'
        + f'<span class="visually-hidden">{other["name"]}</span></a></li>'
        for code, other in LANGS.items()
    )
    alternates = ""
    if BASE_URL:
        alternates = "".join(
            f'  <link rel="alternate" hreflang="{code}" href="{BASE_URL}{other["dir"]}{filename}">\n'
            for code, other in LANGS.items()
        )
    scripts = (
        f'  <script src="{root}assets/js/case-nav.js" defer></script>\n'
        if meta.get("script") else ""
    )

    values = {
        "lang": lang, "title": meta["title"], "description": meta["description"],
        "alternates": alternates, "scripts": scripts, "skip": cfg["skip"],
        "nav_label": cfg["nav_label"], "lang_label": cfg["lang_label"],
        "nav": nav, "langs": langs, "main": main, "year": YEAR,
        "confidential": cfg["confidential"], "theme": cfg["theme"],
    }
    html = layout
    for key, value in values.items():
        html = html.replace("{{" + key + "}}", value)
    phone = CONTACT["phone_e164"]
    contact = {
        "location": cfg["location"],
        "phone_display": CONTACT["phone_display"] or '<span class="ph">[phone]</span>',
        "phone_href": f"tel:{phone}" if phone else "#",
        "whatsapp_href": f"https://wa.me/{phone.lstrip('+')}" if phone else "#",
        "linkedin_href": CONTACT["linkedin"] or "#",
        "email": CONTACT["email"],
        "email_href": f"mailto:{CONTACT['email']}",
    }
    html = re.sub(r"\{\{svg:([a-z0-9-]+)\|([^}]*)\}\}",
                  lambda m: (SRC.parent / "content" / "illustrations" / f"{m.group(1)}.svg")
                  .read_text(encoding="utf-8").strip().replace("{label}", m.group(2)), html)
    if meta.get("section") == "contact":
        html = re.sub(r'\s*<div class="site-footer__main">.*?</ul>\s*</div>', "", html, count=1, flags=re.S)
    for key, value in contact.items():
        html = html.replace("{{" + key + "}}", value)
    return html.replace("{{root}}", root)


def main():
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(ROOT / "assets", OUT / "assets")
    cases = casekit.load_cases(drafts="--drafts" in sys.argv)
    count = 0
    for lang, cfg in LANGS.items():
        pages = {}
        for page in sorted((SRC / "pages" / lang).glob("*.html")):
            text = page.read_text(encoding="utf-8")
            text = text.replace("{{selected_work}}", casekit.project_list(cases, lang))
            text = text.replace("{{work_list}}", casekit.project_list(cases, lang, detailed=True))
            pages[page.name] = text
        for case in cases:
            pages[case["file"]] = casekit.render_case(case, lang, cases)
        for name, text in pages.items():
            target = OUT / cfg["dir"] / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(render(lang, name, text, layout), encoding="utf-8")
            count += 1
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Built {count} pages into {OUT}")


if __name__ == "__main__":
    main()

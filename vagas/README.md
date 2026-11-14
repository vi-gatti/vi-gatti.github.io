# Levantamento diário de vagas
- `scan.py` consulta direto os sistemas de vagas das empresas em `empresas.json` (só vagas abertas). Rodar: `python3 vagas/scan.py --save`
- Para incluir uma empresa: adicione `"nome": ["ats", "slug"]` em `empresas.json` (ats: greenhouse, greenhouse_eu, lever, ashby, recruitee, workable, smartrecruiters).
- Relatórios diários em `AAAA-MM-DD.md`; `vistas.txt` evita repetir vagas; critérios em `PERFIL.md`.

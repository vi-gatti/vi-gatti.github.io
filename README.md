# Portfolio · Virginia Candido Gatti

Site estático em três idiomas (inglês, espanhol e português). As páginas finais ficam em `docs/` e são HTML puro, prontas para qualquer hospedagem.

## Visualizar

```bash
cd site && python3 -m http.server 8000
```

Acesse http://localhost:8000. Também é possível abrir `docs/index.html` direto no navegador.

## Estrutura

```
src/layout.html          Cabeçalho, seletor de idioma, rodapé (um único arquivo)
src/pages/en/*.html      Conteúdo em inglês (idioma principal, na raiz do site)
src/pages/es/*.html      Conteúdo em espanhol (docs/es/)
src/pages/pt/*.html      Conteúdo em português (docs/pt/)
assets/css/main.css      Tokens, base, layout, componentes
assets/js/case-nav.js    Marca a seção atual no índice dos cases
assets/fonts/            Inter e Ubuntu em WOFF2, hospedadas localmente
assets/img/              Retrato e futuras imagens
build.py                 Gera docs/ a partir de src/ e assets/
docs/                    Resultado gerado. Não editar à mão.
```

## Atualizar conteúdo

1. Edite o arquivo da página em `src/pages/<idioma>/`.
2. Rode `python3 build.py`.

- Cada página começa com uma linha `<!--meta {...} -->` contendo título, descrição e seção ativa no menu.
- Os textos provisórios estão em `<span class="ph">[...]</span>`. Procure por `class="ph"` para ver o que falta.
- Imagens: dentro de `<figure class="slot">`, troque o bloco `slot__frame` por `<img src="{{root}}assets/img/arquivo.webp" alt="...">`. O `{{root}}` acerta o caminho em todos os idiomas.
- Menu, rodapé e nomes dos idiomas ficam em `build.py` (dicionário `LANGS`) e em `src/layout.html`.

## Pequenos ajustes de texto (guia rápido)

1. Abra o arquivo da página em `src/pages/<idioma>/` (por exemplo `src/pages/pt/about.html`; os textos dos cases ficam em `content/cases/<nome>/<idioma>.json`) num editor de texto simples, como VS Code, TextEdit em modo texto ou Bloco de Notas.
2. Procure a frase com Ctrl+F (Cmd+F no Mac).
3. Troque só o texto entre as tags. Exemplo: em `<p>Texto antigo.</p>`, mude apenas `Texto antigo.`.
4. Para destacar um termo, envolva com `<strong>`: `um <strong>termo</strong> importante`.
5. Não apague nem altere `<`, `>`, `class="..."`, `id="..."` ou a primeira linha `<!--meta ... -->` (só o título e a descrição dentro dela podem mudar).
6. Salve. Para ver o resultado, rode `python3 build.py` e abra `docs/index.html`.

Os arquivos em `docs/` são gerados automaticamente: mudanças feitas direto neles se perdem no próximo build.

## Cases (projetos)

Cada case é uma pasta em `content/cases/<nome>/`. O nome da pasta vira o endereço da página (`case-03` → `case-03.html`).

```
content/cases/case-03/
  case.json   ordem, publicado ou não, formato das descobertas ("list" ou "grid")
  en.json     textos em inglês (es.json e pt.json para os outros idiomas;
              se faltar um idioma, a página usa o inglês)
  cover.svg   ilustração de capa (página do case e listas de projetos)
  figures/    diagramas opcionais citados nos textos
```

Fotos de um case ficam em `assets/img/<nome>/`.

**Novo case:** copie `content/cases/_template` para uma pasta nova (por exemplo `case-03`), preencha os textos e a capa, e rode `python3 build.py`.

**Deixar oculto até ficar pronto:** em `case.json`, use `"published": false`. O case não gera página, não aparece na Home nem em Projetos e fica fora do "próximo case". Para revisar rascunhos, rode `python3 build.py --drafts`.

**Ordem:** o campo `order` define a sequência. Os números (Case 01, 02, 03…) e o "próximo case" são calculados automaticamente a partir dos cases publicados.

Blocos opcionais (aparecem só se existirem no texto): `questions`, `photos`, `figures`, `quotes`, `stats`, `decisions_after`, `decisions_note`.

## Tipografia

Fontes sem serifa, hospedadas localmente (subconjunto latino, que cobre português e espanhol). O navegador só baixa os pesos que a página usa.

- Títulos: Ubuntu Regular (400)
- Texto e interface: Inter Regular (400) e Medium (500)
- Bold disponível para uso pontual: Inter 600, Ubuntu 700

Para trocar a combinação, altere `--font-heading`, `--font-body` e `--heading-weight` no início de `assets/css/main.css`.

Licenças: Inter (SIL Open Font License) e Ubuntu (Ubuntu Font Licence), em `assets/fonts/`.

## Temas claro e escuro

As cores ficam em `:root` (claro) e em `html[data-theme="dark"]` (escuro), no início de `main.css`. O botão usa `assets/js/theme.js`.

## Antes de publicar

- Preencher `BASE_URL` em `build.py` para gerar os links `hreflang` entre idiomas.
- Retirar `<meta name="robots" content="noindex">` de `src/layout.html`.
- Contatos (telefone, WhatsApp, e-mail, LinkedIn) ficam em `CONTACT`, no `build.py`.

# Proposta de arquitetura e direção visual

Etapa 1 do portfólio de Virginia Candido Gatti. Os textos do site são provisórios: todo trecho a ser escrito aparece destacado (fundo argila claro, sublinhado tracejado).

## 1. Arquitetura de informação

```
Home ─┬─ About
      ├─ Work ─┬─ Case Study 01 (serviços financeiros)
      │        └─ Case Study 02 (telecomunicações)
      └─ Contact
```

Navegação principal com três itens: About, Work, Contact. O nome leva à Home. Os cases são acessados pela Home e por Work, e cada case termina com um link para o outro.

| Página | Conteúdo |
|---|---|
| Home | Abertura (nome, áreas, apresentação curta, dados de base) · prévia da trajetória em três fases · dois cases · seis áreas de atuação · contato |
| About | Abertura com retrato · trajetória (Formação, Educação pública, Pesquisa aplicada) · continuidade entre experiência anterior e prática atual · métodos, áreas, setores e idiomas · formação acadêmica · CV |
| Work | Introdução · nota de confidencialidade · dois cases com metadados (organização genérica, foco, papel, período) |
| Case 01 e 02 | As nove seções pedidas, com índice lateral fixo no desktop |
| Contact | E-mail, LinkedIn, CV · localização, fuso, idiomas, formato de trabalho |

Idioma principal: inglês britânico, na raiz do site. Versões em espanhol (`/es/`) e português do Brasil (`/pt/`), com seletor EN · ES · PT no cabeçalho, que leva à mesma página no outro idioma. Os nomes das áreas (UX Research, Product Discovery etc.) ficam em inglês nas três versões, por serem termos usados assim no mercado.

## 2. Direção de arte

Referência: publicação editorial independente. Muito espaço em branco, grade de 12 colunas com uma coluna de rótulos à esquerda (número e nome da seção) e o conteúdo à direita, como as margens de uma revista. Divisórias finas no lugar de cartões. Blocos areia aparecem com função definida: contato, pergunta central do case, próximo case e áreas reservadas para imagens.

Não há fundo escuro, gradiente, sombra, animação decorativa nem ícones. O único movimento é a rolagem suave até as seções do case (desativada para quem prefere movimento reduzido).

## 3. Cor

| Token | Valor | Uso |
|---|---|---|
| paper | #F7F5F0 | Fundo predominante |
| sand | #E8DED1 | Blocos secundários, espaços de imagem |
| clay | #C9A98F | Bordas, tags, marcações discretas |
| terracotta | #A96F55 | Pontos da linha do tempo, numerais grandes, setas, item ativo |
| cocoa | #453D35 | Texto principal |
| link | #84513B | Terracota escurecida para links e textos pequenos |
| ink-soft | #6A5F55 | Texto secundário |

Ajuste importante: a terracota original tem contraste de 3,8:1 sobre o off-white, abaixo do mínimo de acessibilidade para texto pequeno (4,5:1). Por isso ela é usada só em elementos grandes ou decorativos, e os links usam uma variação mais escura (6:1 no off-white, 4,9:1 na areia).

### Revisão 3: tons por idioma

O fundo passou a usar o tom do fundo do retrato. Cada idioma usa a mesma paleta, um pouco mais escura a cada versão. Todas as combinações de texto passam no nível AA.

| Token | Inglês | Espanhol | Português |
|---|---|---|---|
| paper (fundo) | #EEE6E0 | #E6DACF | #DCCDC0 |
| sand (blocos) | #E2D4C8 | #D9C8B9 | #CDBAA8 |
| clay (bordas) | #C4A188 | #BC9880 | #B08A72 |
| cocoa (texto) | #453D35 | #3F3730 | #3A322B |
| ink-soft (texto secundário) | #665A50 | #5E5249 | #54493F |
| link | #80503A | #774932 | #6A3F2B |

A terracota (#A96F55) é a mesma nos três. O retrato tem fundo branco e é aplicado com `mix-blend-mode: multiply`, então assume sozinho a cor de fundo de qualquer idioma.

## 4. Tipografia (revisão 2: somente sem serifa)

- **Ubuntu Regular** nos títulos, no nome e nos numerais: dá personalidade sem peso excessivo. Em medium ela ficou pesada nos títulos, por isso o regular.
- **Inter Regular e Medium** no texto, na navegação, nos rótulos e nos dados: é a mais confortável para leitura longa, sobretudo no celular.
- Testadas também: Inter em tudo e Ubuntu em tudo. A troca é feita em três tokens no CSS.
- Sem itálico, sem caixa-alta com espaçamento, sem letras condensadas. A hierarquia vem de tamanho, peso (400/500) e contraste de cor.
- Tamanhos mais contidos: nome até 56 px, títulos de seção até 34 px, texto em 17 px com entrelinha de 1,65 e linha de até 65 caracteres.
- Fontes hospedadas no próprio site em WOFF2, subconjunto latino, sem chamadas ao Google (RGPD/GDPR).

## 5. Componentes reutilizáveis

Todos em `assets/css/main.css`, seção 4.

| Componente | Classe | Onde aparece |
|---|---|---|
| Rótulo de seção | `.label` + `.num` | Todas as seções |
| Lista de dados | `.facts`, `.facts--grid` | Abertura, Overview, Work, Contact |
| Sequência de fases | `.sequence`, `.sequence--4` | Trajetória, etapas de pesquisa |
| Destaque de case | `.teaser` | Home, Work |
| Índice de áreas | `.areas` | Home |
| Links de contato | `.contact-links` | Home, About, Contact |
| Espaço de imagem | `.slot` (`--wide`, `--strip`, `--portrait`) | Cases, Home, About |
| Nota de margem | `.with-note` + `.note` | Context, Overview |
| Bloco de pergunta | `.statement` | The challenge |
| Lista numerada | `.numbered` | Research objectives |
| Tabela | `.data-table` (`--stack`, `--matrix`) | Métodos, formação, matriz de frentes |
| Achados | `.findings`, `.findings--grid` | Key findings |
| Fluxo | `.flow`, `.flow--two` | From research to decisions, About |
| Resultados com status | `.outcomes` | Outcomes |
| Duas colunas | `.columns` + `.list` | My contribution, About |
| Placeholder | `.ph` | Texto provisório |

## 6. Modelo dos cases

| Seção | Forma | Case 01 | Case 02 |
|---|---|---|---|
| 01 Overview | Resumo + dados | Dados em duas colunas abaixo | Resumo ao lado dos dados |
| 02 Context | Texto | Nota de margem (escopo, restrições) | Diagrama do cenário de serviços |
| 03 Challenge | Bloco areia com a pergunta central | Texto de apoio | Duas listas: complexidade e o que estava em jogo |
| 04 Objectives | Lista numerada | Igual | Igual |
| 05 Approach | Etapas de pesquisa | Quatro fases + tabela de métodos | Matriz frentes × fases |
| 06 Findings | Achados numerados com evidência | Lista com citação + diagrama | Grade 2 × 2 + mapa de jornada |
| 07 Decisions | Fluxo achado → implicação → decisão | Igual | Igual |
| 08 Outcomes | Lista com status | Igual | Igual |
| 09 Contribution | Responsabilidades / trabalho em conjunto | Igual | Igual |

Duas escolhas ligadas ao pedido de não exagerar responsabilidades: a seção 07 fala em "decision or discussion informed", e não em decisão tomada pela pesquisa; a seção 09 separa o que foi responsabilidade sua do que foi feito com outras pessoas. Em Outcomes, cada item tem um status (por exemplo: confirmed, informed, in progress) para deixar claro o que está comprovado.

Os espaços de imagem descrevem o tipo de material esperado (mapa do estudo, síntese redesenhada, jornada), sempre anonimizado. Não há imagens, números ou métricas inventados.

## 7. Responsividade

- Abaixo de 48 rem (768 px): uma coluna; a linha do tempo passa a ser vertical; tabelas de métodos empilham cada linha; o fluxo mostra o rótulo de cada etapa; a matriz rola lateralmente dentro do próprio bloco.
- Entre 48 e 64 rem: grade de 12 colunas; o índice do case fica no topo, em duas colunas.
- Acima de 64 rem: índice lateral fixo, com a seção atual marcada durante a leitura.
- Navegação sempre visível, sem menu escondido: com três itens não é necessário.
- Testado em 375, 900 e 1440 px sem rolagem horizontal.

## 8. Acessibilidade e desempenho

Link para pular ao conteúdo, item ativo da navegação marcado (`aria-current`), foco visível, hierarquia de títulos coerente, contraste AA, estrutura semântica (`dl`, `ol`, `table`, `figure`). Sem framework e sem etapa de build: um CSS (~20 KB) e um script de 1 KB apenas nos cases. O site funciona sem JavaScript.

## 9. Decisões tomadas

- Títulos dos cases: Product Discovery and Go-to-Market Assessment; Strategic UX Research for Digital Transformation.
- Seções da Home: My background, Selected work, Areas of practice.
- Retrato: versão pequena da foto em moldura oval, na abertura da About.
- Idiomas: inglês, espanhol e português.
- Fontes hospedadas localmente.

## 10. Revisão 4

- **Cor única:** o tom antes usado no português (#DCCDC0) passou a valer para os três idiomas.
- **Tema escuro:** botão no cabeçalho (uma bolinha meio preenchida). O claro é o padrão; a escolha fica salva no navegador. Paleta escura: fundo #161412, blocos #24201C, texto #EEE6E0, secundário #B3A69A, links #D9A285, terracota #C98B6E. Tudo passa no nível AA.
- **Abertura da About:** retrato pequeno à esquerda, rótulo, título e texto à direita. O contorno oval agora é desenhado pelo site, completo e na cor do tema. No escuro, a foto fica num camafeu claro.
- **Bolinhas:** assinatura (bolinha terracota antes do nome), separadores do menu e do seletor de idioma, rótulos numerados (01 • About) e separadores de texto (Financial services • Brazil). Elas repetem os pontos da linha do tempo.

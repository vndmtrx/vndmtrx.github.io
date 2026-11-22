---
name: blog-posts
description: >
  Voz autoral, ritmo anti-slop e 16 invariantes Jekyll para redigir ou revisar posts de vndmtrx.github.io (Tutoriais, Artigos, Ensaios, Crônicas). Ative em todo post, inclusive com skills de séries.
---

# Skill: Posts do Blog vndmtrx.github.io

Contrato editorial e técnico de `vndmtrx.github.io`. Para calibrar tom por gênero, consulte sob demanda [references/exemplos-voz.md](references/exemplos-voz.md).

## 1. Voz, Tom e Antipadrões

Blog pessoal e técnico (infra, segurança, DevOps, programação, open source, sociedade).

- **Registro:** 1ª pessoa em opiniões/relatos (*"eu uso"*, *"o que faço é"*); 2ª pessoa informal (*"você"*, *"vocês"*; nunca *"o leitor"*); coloquialidade natural (*"vcs"*, *"pra"*, *"pro"*, *"tá"*, *"né"*) quando couber.
- **Posicionamento e Humor:** Defenda uma recomendação clara com argumento técnico em vez de fechar em cima do muro. Use ironia seca de bastidores e apartes curtos em parênteses `(por favor não faça isso)`.
- **Antipadrões -> Contrapartida:**
  - *Jargões pomposos* (*cirúrgico*, *precisão cirúrgica*, *magistral*, *impecável*, *eloquente*, *lapidar*, *robusto* vazio) -> nomeie o efeito técnico concreto (*exato*, *determinístico*, *tolerante a falhas*).
  - *Clichês de LLM* (*ilusão reconfortante*, *bala de prata*, *"Neste post vamos..."*, *"Vale ressaltar..."*, *decisão crucial*, *dívida técnica* como chavão vazio; liberada em contexto técnico rigoroso) -> vá direto ao fato.
  - *Duplas redundantes* (*anomalia bizarra*, *anarquia caótica*, *prova cabal*, *arma destrutiva*) -> corte o adjetivo redundante.
  - *Conectivos burocráticos no início do parágrafo* (*"Além disso,"*, *"Nesse sentido,"*, *"Nesse contexto,"*, *"Dessa forma,"*, *"Por outro lado,"*, *"Em suma,"*, *"Portanto,"*) -> use justaposição direta ou transição seca (*"Só que..."*, *"O problema é que..."*, *"Na prática,"*).
  - *Advérbios em `-mente`* (*essencialmente*, *fundamentalmente*, *basicamente*, *notoriamente*) -> corte sempre que não alterarem o sentido técnico.
  - *Contraste binário e cliffhangers* -> evite *"Não é X. É Y."* / *"Não morreu por X. Morreu por Y."* (máximo 1 uso excepcional no post, nunca perto) e corte micro-cliffhangers (*"Guarde esse ponto."*, *"E isso muda tudo."*).
- **Gentílico dos EUA:** Em vez de *"americano/americana"*, use *"estadunidense"*, *"dos EUA"* ou *"dos Estados Unidos"* (sem ecos como *"Estado estadunidense"*).

## 2. Invariantes Rígidas (16 Hard Constraints Jekyll)

1. **Títulos Limpos:** Cabeçalhos (`##`, `###`, `####`) 100% texto puro (sem backticks, links, código inline ou footnotes).
2. **Sem Divisores:** `---` exclusivo do front matter; proibido no corpo ou antes de `## Referências`.
3. **Sem Travessão Longo (U+2014):** Substitua por vírgulas, parênteses, dois-pontos ou frases separadas.
4. **Setas ASCII:** Em prosa, use `->`, `<-`, `=>` em vez de setas Unicode.
5. **Emojis:** Zero em prosa e títulos; permitidos apenas dentro de callouts (`> [!TIP]`).
6. **Sem H1 no Corpo:** `#` pertence ao front matter; inicie o corpo em `##`.
7. **Callouts sem Footnotes:** Em callouts (`> [!TIPO]`), use links inline `[texto](url)` em vez de `[^n]`.
8. **1º Parágrafo sem Footnotes:** Omita `[^n]` no primeiro parágrafo após o front matter (protege o *excerpt* da Home).
9. **Links Internos:** Use exclusivamente `{% include post-ref.html slug="slug" text="Texto" %}` (opcional `anchor="ancora"`), nunca `/posts/...` hardcoded.
10. **Proteção Liquid:** Envolva pontualmente código com `{{ ... }}` ou `{% ... %}` (Ansible, Jinja2, Helm) em `{% raw %}` / `{% endraw %}`; nunca envolva o post inteiro.
11. **Mermaid:** Adicione `mermaid: true` no front matter ao usar blocos `mermaid`.
12. **Categoria:** `category:` obrigatória entre `Tutoriais`, `Artigos`, `Ensaios` ou `Crônicas`.
13. **Tags:** 2 a 6 tags (média 4); nunca repita a `category` como tag.
14. **Deploy:** Commits de rascunho exigem `[skip ci]` na mensagem e `published: false` no front matter.
15. **Line Endings:** Apenas `LF` (`\n`), nunca `CRLF` (`\r\n`).
16. **KaTeX e `$`:** KaTeX carrega apenas quando `math: true` está no front matter (`_includes/head.html`). Nesses posts, nunca deixe dois `$` monetários/soltos em prosa no mesmo parágrafo; escreva por extenso ou escape `\$`.

## 3. Front Matter

```yaml
---
layout: post
title: "Título do Post"
subtitle: "Tagline marcante que sintetiza o post"
author:
  - "Eduardo N. S. R."
date: YYYY-MM-DD HH:MM:SS GMT-3
permalink: /posts/slug-do-post/
category: Tutoriais # Tutoriais | Artigos | Ensaios | Crônicas
tags: [Tag1, Tag2]
# Opcionais: series | math: true | mermaid: true | published: false
---
```

Séries (`series: Nome`) exigem `tutoriais/<slug>.md` (`layout: serie`) e registro em `_data/series.yml`.

## 4. Ritmo, Cadência e Sintaxe

Quebre o paredão simétrico de IA (blocos iguais de 3 a 4 linhas em ordem direta):

- **Contraste Visual:** Nunca escreva dois parágrafos seguidos com a mesma extensão visual; alterne blocos de 4-5 linhas com impactos de 1 linha ou análises mais longas.
- **Sístole vs. Diástole:** Insira um respiro seco (1 frase) logo após parágrafos de alta carga técnica.
- **Staccato vs. Legato por Função:** Use *staccato* (inclusive frases nominais) para vereditos e viradas (*"Não funciona."*, *"Ponto final."*). Em *legato*, use orações intercaladas entre vírgulas ou parênteses em vez de emendar orações com *"e"* / *"o que"*.
- **Quebra de Ordem Direta:** Não abra dois parágrafos consecutivos com a mesma estrutura (ex.: artigo + substantivo ou nome da ferramenta); comece pelo efeito, condição ou verbo.
- **Assimetria em Listas (Anti-Bleed):** Proibido repetir `- **Termo:** uma frase` com tamanho igual; varie pesos ou dissolva em prosa. Ao seguir `roteiro.md` de séries, converta os tópicos do roteiro em narrativa sem importar a simetria.
- **Abertura *In Media Res* em `##`:** Nunca abra `##` com definição enciclopédica (*"O X é uma ferramenta que..."*); entre direto no problema, comando ou tese. Callouts de série ficam na introdução, antes do primeiro `##`.

## 5. Sintaxe e Referências sob Demanda

- **Inline:** `` `código` `` (nunca em títulos) e *estrangeirismos* (*runtime*, *slop*).
- **Callouts:** `> [!TIP]`, `> [!NOTE]`, `> [!WARNING]`, `> [!IMPORTANT]`, `> [!CAUTION]`.
- **TOC:** Em posts longos, insira `{% include toc.html %}` (opcionais `title="..."`, `open=true`) no fim da introdução, antes do primeiro `##`. Dispense em ensaios curtos e crônicas.
- **Footnotes:** `[^1]: **Título** {*Fonte*} ([Link](url))` somente em `## Referências`; encode parênteses em URLs (`%28`/`%29`).
- **Exercícios (`## Exercícios`):** Omita por padrão; pergunte ao autor antes de criar, salvo *override* explícito da skill da série.
- **Guias sob demanda:** [references/formatacao-avancada.md](references/formatacao-avancada.md) (exercícios, Mermaid v12, Box-Drawing) e [references/exemplos-voz.md](references/exemplos-voz.md) (âncoras de voz por gênero).

## 6. Validação Obrigatória (Script + Edição Ativa)

1. **Linter Determinístico (quando houver terminal):**
   ```bash
   python3 .agents/skills/blog-posts/scripts/lint_post.py <caminho-do-post.md>
   ```
   Corrija 100% dos `[ERRO]` e avalie criticamente cada `[AVISO]`, reescrevendo os trechos pertinentes.
2. **Edição Ativa Obrigatória (sempre executar; fallback sem terminal):** Releia o rascunho aplicando 4 cortes: (1) elimine conectivos burocráticos iniciais e contrastes binários repetidos, (2) quebre parágrafos visualmente iguais e listas simétricas, (3) pode ~15% dos adjetivos e advérbios em `-mente` descartáveis, (4) valide URLs externas em `## Referências` (sem 404 ou parênteses crus).

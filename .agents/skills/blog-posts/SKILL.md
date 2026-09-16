---
name: blog-posts
description: >
  Diretrizes editoriais, tom de voz e regras de formatação para escrever, rascunhar ou revisar posts do blog pessoal de Eduardo (vndmtrx.github.io). Use esta skill estritamente ao redigir, estruturar ou revisar artigos, tutoriais, ensaios ou crônicas para o blog.
---

# Skill: Posts do Blog vndmtrx.github.io

Diretrizes centrais para escrita, tom de voz e formatação estrita dos posts do blog `vndmtrx.github.io`.

---

## 1. Voz, Tom e Identidade

O blog é pessoal e técnico (infraestrutura, segurança, DevOps, programação, open source e sociedade).

- **Pessoa e Registro:** 1ª pessoa para experiências/opiniões ("eu uso", "o que eu faço é"); 2ª pessoa informal para o público ("você", "vocês" — nunca "o leitor"); informalidade natural ("vcs", "pra", "pro", "tá", "né") quando o momento pede.
- **Posicionamento Firme:** Defenda posições com argumentos técnicos claros. Não apresente opções neutras sem emitir opinião ou apontar a recomendação ideal.
- **Humor e Honestidade:** Humor situacional e autêntico de bastidores de infra/DevOps. Apartes em parênteses `(por favor não faça isso)`.
- **Antipadrões de IA (Proibido):** Nunca use jargões afetados/pomposos (*"cirúrgico"*, *"magistral"*, *"impecável"*, *"eloquente"*, *"lapidar"*, uso vazio de *"robusto"*). Evite clichês (*"Neste post vamos explorar..."*, *"Vale ressaltar que..."*). Proibido reciclar metáforas ou expressões gêmeas ao longo do texto.

---

## 2. Invariantes Rígidas de Formatação (Hard Constraints)

Estas 15 regras são **absolutas** para manter a compatibilidade com o Jekyll (Minima) e GitHub Pages:

1. **Títulos Limpos:** NUNCA use backticks, links, código inline ou footnotes em cabeçalhos (`##`, `###`, `####`). Texto 100% puro.
2. **Sem Divisores (`---`):** NUNCA insira `---` no corpo do post ou antes de `## Referências`. O `---` é exclusivo do front matter YAML.
3. **Sem Travessão Longo (—):** NUNCA use travessão longo. Use vírgulas, dois-pontos ou quebre em frases menores.
4. **Símbolos e Setas em Prosa:** NUNCA use setas Unicode (`→`, `←`) no texto corrido. Use representações ASCII (`->`, `<-`, `=>`).
5. **Emojis Apenas em Callouts:** NUNCA insira emojis soltos no texto corrido. Permitido apenas dentro de callouts (`> [!TIP]`).
6. **Sem H1 no Corpo:** O `#` é exclusivo do título no front matter. No corpo, comece em `##`.
7. **Callouts sem Footnotes:** NUNCA use notas de rodapé (`[^n]`) ou referências indiretas dentro de callouts (`> [!TIPO]`). Use apenas links diretos inline `[texto](url)`.
8. **Primeiro Parágrafo sem Footnotes:** NUNCA use footnotes `[^n]` no primeiro parágrafo após o front matter (para não poluir o *excerpt* da Home).
9. **Links Internos via `post-ref.html`:** Sempre use `{% include post-ref.html slug="slug-do-post" text="Texto" %}` (ou `anchor="ancora"`). Nunca use links relativos/absolutos hardcoded.
10. **Proteção de Código Conflitante com Liquid:** Trechos com `{{ ... }}` ou `{% ... %}` (Ansible, Jinja2, Helm) devem ser envolvidos pontualmente com `{% raw %}` e `{% endraw %}`. Nunca envolva o post inteiro.
11. **Diagramas Mermaid:** Sempre adicione `mermaid: true` no front matter ao usar blocos Mermaid.
12. **Categoria Obrigatória:** O front matter DEVE conter `category:` com uma das 4 opções: `Tutoriais`, `Artigos`, `Ensaios` ou `Crônicas`.
13. **Tags Calibradas:** Média de 4 tags por post (2 a 6). Nunca crie tag idêntica à categoria.
14. **Controle de Deploy (`[skip ci]`):** Commits de rascunhos e edições intermediárias devem conter `[skip ci]` e `published: false` no front matter.
15. **Quebras de Linha Linux (`LF`):** NUNCA use `CRLF` (`\r\n`). O Jekyll depende de `\n\n` para calcular o `post.excerpt`.

---

## 3. Front Matter e Estrutura

```yaml
---
layout: post
title: "Título do Post"
subtitle: "Frase de efeito ou tagline marcante que sintetiza o post"
author:
  - "Eduardo N. S. R."
date: YYYY-MM-DD HH:MM:SS GMT-3
permalink: /posts/slug-do-post/
category: Tutoriais # Tutoriais | Artigos | Ensaios | Crônicas
tags: [Tag1, Tag2]
# Opcionais:
series: Nome da Série
mermaid: true # Se contiver diagramas mermaid
published: false # Enquanto for rascunho
---
```

### Regra para Séries:
Séries de posts (`series: Nome`) exigem sua página dedicada em `tutoriais/<slug>.md` (`layout: serie`) e registro em `_data/series.yml`.

---

## 4. Ritmo e Cadência Fractal (Anti-Uniformidade)

Evite blocos monótonos de IA (3 a 5 frases):
- **Alternância Fibonacci:** Alterne monoversos de impacto (1 frase), díades de causa/efeito (2 frases), tríades argumentativas (3 frases) e blocos densos de análise (5 frases). Evite 3 parágrafos seguidos com mesmo tamanho.
- **Sístole vs. Diástole:** Insira um respiro leve (1 a 2 frases) após parágrafos densos de alta carga técnica.
- **Burstiness:** Alterne frases curtas (*staccato*, 3-7 palavras) com frases elaboradas (*legato*, 20-35 palavras).

---

## 5. Elementos de Sintaxe e Referências Externas

- **Código Inline:** \`comando\`, \`flag\`, \`arquivo\` (nunca em títulos).
- **Estrangeirismos:** *termo em inglês* (*runtime*, *page cache*, *slop*).
- **Callouts:** `> [!TIP] Dica`, `> [!NOTE] Nota`, `> [!WARNING] Atenção`, `> [!IMPORTANT] Importante`, `> [!CAUTION] Aviso Crítico`.
- **Footnotes:** `[^1]: **Título** {*Fonte*} ([Link](url))` exclusivamente na seção final `## Referências`.
- **Diagramas Mermaid, Box-Drawing e Exercícios:** Consulte o guia detalhado em [formatacao-avancada.md](references/formatacao-avancada.md).

---

## 6. Checklist Rápido de Validação

Antes de entregar o post, confirme:
- [ ] 15 Invariantes respeitadas (sem backtick em títulos, sem `---`, sem travessão `—`, sem setas Unicode, sem emoji solto)?
- [ ] Front matter completo (`subtitle`, `category`, `tags`, `author` em lista)?
- [ ] Links internos usando `{% include post-ref.html slug="..." %}` e Liquid protegido com `{% raw %}`?
- [ ] Ritmo dinâmico (sem cadência monótona de IA, zero jargões como "cirúrgico" ou "robusto" vazio)?
- [ ] Footnotes `[^n]` apenas a partir do 2º parágrafo e listados em `## Referências`?

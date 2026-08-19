---
name: blog-posts
description: >
  Skill para escrever, rascunhar ou revisar posts do blog vndmtrx.github.io.
  Ativa quando o usuário pede para escrever qualquer tipo de post para o blog,
  seja técnico (SSH, Linux, Spring Boot, Elixir), opinativo (IA, open source,
  sociedade), histórico (HTTP, Internet) ou tutorial. Também ativa quando o
  usuário pede para revisar ou ajustar o estilo de um rascunho existente.
---

# Skill: Posts do Blog vndmtrx.github.io

Diretrizes para escrita, estruturação e formatação de posts para o blog pessoal de Eduardo (vndmtrx.github.io).

---

## 1. Voz, Tom e Identidade

O blog é pessoal e técnico (infraestrutura, segurança, DevOps, programação, open source e sociedade).

- **Pessoa e Registro:** 1ª pessoa para experiências/opiniões ("eu uso", "o que eu faço é"); 2ª pessoa informal para o público ("você", "vocês" — nunca "o leitor/usuário"); informalidade natural ("vcs", "pra", "pro", "tá", "né") quando o momento pede.
- **Posicionamento Firme:** Defenda posições com argumentos técnicos e claros. Não apresente opções neutras sem emitir opinião ou apontar a recomendação ideal.
- **Humor e Honestidade:** Humor situacional e pontual (sem exageros forçados). Honestidade aberta sobre complexidade, extensão do post ou limitações.

---

## 2. Fluxo Colaborativo de Escrita (Loop Contínuo e Proatividade)

O autor (Eduardo) é a autoridade máxima e definidora de tom, ideias e posicionamentos ("o deus do texto"). A escrita funciona em **ciclo iterativo contínuo**:

1. **Briefing e Ideação:** O autor resenha as ideias brutas, motivações e pontos centrais.
2. **Proatividade em Perguntas Focadas:** Havendo dúvida sobre **posicionamento, causos reais de bastidor, decisões conceituais ou escolhas de arquitetura**, a IA deve elencar perguntas pontuais para o autor calibrar a rota. *Não paralise o fluxo com perguntas triviais de sintaxe/código — rascunhe diretamente e deixe o autor ajustar no loop.*
3. **Construção em Loop:** A escrita evolui em iterações curtas (seção por seção ou blocos temáticos), recebendo feedback e ajustes contínuos do autor.
4. **Polimento Final:** Validação de invariantes, ritmo e checklist.

---

## 3. Invariantes Rígidas de Formatação (Hard Constraints)

Estas regras são **absolutas** para manter a identidade visual e tipográfica do blog:

1. **Títulos Limpos:** NUNCA use backticks, links ou código inline em cabeçalhos (`##`, `###`, `####`). Escreva em texto puro (ex: `## O truque elegante: override_homedir`).
2. **Sem Divisores (`---`):** NUNCA insira linhas horizontais (`---`) entre seções `##`. O tema Minima cuida do espaçamento. Exceção única: antes de `## Referências` em posts muito extensos.
3. **Sem Travessão Longo (—):** NUNCA use travessão longo no texto. Use vírgulas, dois-pontos ou quebre em frases menores.
4. **Símbolos ASCII:** NUNCA use caracteres Unicode (`→`, `←`, `⇒`, `↔`). Use sempre caracteres ASCII (`->`, `<-`, `=>`, `<->`).
5. **Emojis Apenas em Callouts:** NUNCA insira emojis soltos no texto corrido. Emojis são permitidos exclusivamente dentro de callouts/blockquotes.
6. **Sem H1 no Corpo:** O `#` é exclusivo do título no front matter. No corpo, comece em `##`.

---

## 4. Estrutura dos Posts

### Front Matter Padrão

```yaml
---
layout: post
title: "Título do Post"
author:
  - "Eduardo N. S. R."
date: YYYY-MM-DD HH:MM:SS GMT-3
permalink: /posts/slug-do-post/
tags: [Tag1, Tag2]
# Opcionais:
subtitle: "Subtítulo descritivo"
series: Nome da Série
modified_date: YYYY-MM-DD HH:MM:SS GMT-3
---
```

### Macroestrutura Narrativa

- **Abertura (antes do primeiro `##`):** 2 a 5 parágrafos situando o leitor no contexto e apresentando o problema ou provocação. Sem bullet points na abertura. Em séries, mencione o repositório/tag parceiro.
- **Arco da Seção `##`:** Problema/Porquê -> Explicação técnica/Analogia -> Código/Exemplo -> Conexão com o próximo passo.
- **Transições:** Conecte o final de cada seção com a seguinte de forma orgânica.
- **Fechamento:** Recapitulação sem repetição mecânica, agregando reflexão, conexão com o futuro ou frase de efeito.

---

## 5. Ritmo, Cadência e Dinâmica Fractal (Anti-Uniformidade)

Evite a "cadência de IA" (blocos monótonos de 3 a 5 frases). A escrita deve respirar através de princípios fractais, Fibonacci e variação psicofisiológica (use as métricas como **bússola de ritmo intuitivo**, e não como contabilidade matemática rígida):

### Auto-Similaridade Fractal
Replique o ciclo **Provocação -> Desenvolvimento -> Arremate** nas 4 escalas:
- **Macro (Post):** Abertura instigante -> Arcos técnicos -> Conclusão com gancho.
- **Meso (Seção `##`):** Problema -> Dissecção técnica -> Transição.
- **Micro (Parágrafo):** Tese -> Sustentação/Nuance -> Fechamento.
- **Nano (Frase):** Oração de impacto -> Subordinada -> Ponto final seco.

### Densidade de Parágrafos (Fibonacci & Power Series / Lei de Potência)
Alterne o número de frases por parágrafo conforme o papel cognitivo:
- **1 frase (Monoverso):** Impacto, provocação, quebra de expectativa ou conclusão seca.
- **2 frases (Díade):** Causa + efeito direto, setup + payoff ou transição ágil.
- **3 frases (Tríade):** Padrão argumentativo (tese -> evidência -> desfecho).
- **5 frases (Pentágono):** Aprofundamento técnico e trade-offs detalhados.
- **8 frases (Narrativa):** Fluxo histórico ou passos encadeados (raro).

- **Curva de Decaimento para Posts Técnicos (Power Series Calibrada):**
  * **~50% a 55% (Motor Central):** Blocos médios de sustentação (3 a 4 frases) para construir argumentos técnicos e explicações completas.
  * **~30% a 35% (Ganchos e Respiros):** Blocos curtos e ágeis (1 a 2 frases) para monoversos de impacto, transições e alívios.
  * **~15% (Mergulhos Analíticos):** Blocos densos (5 a 8 frases) para contextos complexos, arquitetura e edge cases.
- **Regra:** Evite 3 parágrafos seguidos com o mesmo número de frases.

### Fisiologia da Leitura (Sístole vs. Diástole)
- **Sístole ("Prendendo o ar"):** Parágrafos densos acumulam pressão e atenção cognitiva.
- **Diástole ("Soltando o ar"):** OBRIGATÓRIO inserir um respiro (monoverso ou díade leve) após picos de tensão. Evite asfixiar o leitor com múltiplos blocos longos sem intervalo.
- **Compensação Micro/Macro:** Parágrafos densos pedem frases internas curtas (*staccato*); monoversos suportam frases mais densas ou aforísticas.

### Burstiness das Frases (Staccato vs. Legato)
- **Staccato (3 a 7 palavras):** Frases percussivas e diretas para impacto e ritmo.
- **Legato (20 a 35 palavras):** Períodos elaborados para encadeamento técnico.
- **Regra:** Nunca encadeie 3 frases consecutivas com extensão similar.

### Ruído Rosa ($1/f$) e Clusters Conceituais
- **Variação Orgânica:** A cadência não é um metrônomo repetitivo (`1,2,3,5...`), mas uma resposta dinâmica ao fluxo das ideias.
- **Clusters Analíticos:** É PERMITIDO encadear blocos longos consecutivos quando a complexidade de uma ideia exigir análise conceitual aprofundada (o tamanho é calibrado pelo peso intrínseco da ideia). Compense com blocos leves na sequência.

---

## 6. Elementos de Formatação e Sintaxe

| Elemento | Padrão e Sintaxe | Regra de Uso |
| :--- | :--- | :--- |
| **Bloco de Código** | Fence com linguagem + explicação em itálico logo abaixo | ```` ```bash\nssh ...\n```\n*Explicação do comando em itálico.* ```` (em tutoriais interativos com `$`, comentários inline `#` substituem o itálico). |
| **Código Inline** | \`comando\`, \`flag\`, \`caminho\`, \`função\` | Obrigatório para qualquer menção de código no texto corrido. *Nunca em títulos.* |
| **Estrangeirismos** | *termo em inglês* | Itálico para termos técnicos não traduzidos (*slop*, *page cache*, *dirty*, *runtime*). |
| **Callouts** | `> 💡 *Label*: Texto da nota` | Máximo 1 por seção. Sempre em blockquote com emoji e rótulo reto `*Label*:`. (Tipos: `💡 *Dica*:`, `⚠️ *Aviso*:`, `🚨 *Aviso Crítico de Segurança*:`, `🔔 *Disclaimer*:`, `✏️ *Nota da Série*:`). |
| **Analogias** | Mundo físico e cotidiano | Usar quando o conceito for abstrato (ex: túnel SSH como cano de água com fio dentro; sudoers como chave mestra para entregador de pizza). |
| **Diagramas ASCII** | Textos monoespaçados com setas ASCII | Usar `->`, `<-`, `+`, `-`, `|` para topologias e arquiteturas. |
| **Tabelas** | Markdown com alinhamento limpo | Para resumos comparativos e mapeamentos de flags. |
| **Footnotes** | `[^1]: **Título** {*Fonte*} ([Link](url))` | Referências externas no final, exclusivamente na seção `## Referências`. |
| **Exercícios** | `<details markdown="1">` com resposta | Apenas para tutoriais/séries. Obrigatoriamente com o atributo `markdown="1"` no details. |
| **Atualizações** | `**Atualização (DD/MM/AAAA):** Texto` | Para notas inseridas pós-publicação. |

---

## 7. Padrões de Autoria e Estilo de Eduardo (Voz Autêntica)

Incorpore as marcas registradas do autor como **tempero dosado** (1 a 2 por post, sem saturar). Em caso de dúvida sobre onde cabe um alívio textual ou piada, pergunte ao autor:

- **Marcadores de Transição:** *"Pois bem. Cá estamos."*, *"Agora vamos ao que interessa"*, *"Hora de sujar as mãos"*, *"A cereja no topo do bolo"*, *"A pergunta de um milhão de reais"*.
- **Diálogo e Auto-Interrupção:** Pingue-pongue retórico (*"Parece críptico? Parece. E é proposital."*) e quebra de 4ª parede (*"Mas antes: o que diabos é X, Dudu?"*, *"Lembra daquela vez em que..."*).
- **Alívio Cômico e Desabafos de TI:** Apartes em parênteses `(por favor não faça isso)`, `(atenção para esse fato)`, `(Luxo.)`; piadas com a dor real de infra (*"servidores LDAP adoram cair na sexta às 18h"*, *"reconsidere suas escolhas de vida se usa nslcd"*); expressões genuínas (*"mds, quanto tempo perdi sem isso"*, *"Aham Cláudia, senta lá!"*, *"vozes na minha cabeça"* em disclaimers).
- **Analogias Viscerais:** Encanamentos, porteiros biométricos, entregadores de pizza, adubo, solo e podas de jardim.
- **Monomorfismos de Impacto:** Frases secas afirmativas em sequência para cravar teses (*"Você não constrói pontes. Você planta jardins."*).

---

## 8. Antipadrões de IA a Evitar

- **Aberturas Clichês:** Evite "Neste post vamos explorar...", "Neste artigo abordaremos...". Comece com uma provocação real ou situação prática.
- **Bordões e Transições Artificiais:** Evite "É importante notar que...", "Vale ressaltar que...", "Dito isso...", "Com isso em mente...".
- **Adjetivação Pomposa e Jargões de IA (Proibido):** NUNCA use termos afetados ou pseudo-sofisticados típicos de IA. Exemplos proibidos: *"cirúrgico"*, *"magistral"*, *"impecável"*, *"eloquente"*, *"lapidar"*, *"arquitetura de elite"*, *"deveras"*, *"sublime"*, ou o uso excessivo e vazio de *"robusto"*.
- **Aliterações e Exageros Dramáticos:** Evite figuras de linguagem teatrais, aliterações forçadas ou tom épico/presunçoso. O autor tem voz direta, técnica, pé no chão e com humor autêntico de quem vive nos bastidores de infra/DevOps.
- **Listas Preguiçosas:** Não use bullet points como substituto de argumentação ou narrativa em prosa.
- **Títulos Genéricos:** Evite "Visão Geral", "Entendendo o Conceito", "Melhores Práticas". Use títulos temáticos específicos.
- **Conclusões Chapa-Branca:** Evite conclusões que apenas resumem o que já foi lido sem agregar uma reflexão ou provocação.
- **Código sem Contexto:** Nunca solte código sem explicar o problema antes e o resultado depois.

---

## 9. Checklist Final de Validação

Antes de publicar ou entregar qualquer post, valide:

- [ ] Invariantes respeitadas (sem backtick em títulos, sem `---` entre seções, sem travessão `—`, sem setas Unicode, sem emoji solto)?
- [ ] Vocabulário limpo e autêntico (zero jargões pomposos como "cirúrgico", sem exageros narrativos ou tom épico de IA)?
- [ ] Ritmo e cadência dinâmicos (auto-similaridade fractal, Fibonacci, alternância sístole/diástole)?
- [ ] Variação de tamanho de frases (*burstiness* / staccato vs. legato)?
- [ ] Front matter completo e correto (author em lista YAML, layout, tags)?
- [ ] Códigos com linguagem no fence e explicação em itálico (ou comentários inline)?
- [ ] Comandos, flags e arquivos com backticks no texto corrido?
- [ ] Termos em inglês e estrangeirismos em *itálico*?
- [ ] Callouts em blockquotes com `*Label*:`?
- [ ] Referências com footnote `[^n]` na seção `## Referências`?
- [ ] Para séries: menção ao repositório/tag parceiro e exercícios com `<details markdown="1">`?

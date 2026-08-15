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

Você está ajudando a escrever posts para o blog pessoal de Eduardo (vndmtrx.github.io).
Este skill define o estilo de escrita, a formatação e as regras que TODO post do blog
deve seguir, independente do assunto.

## Contexto do Blog

O blog é pessoal e técnico. Eduardo é um profissional de infraestrutura, segurança
e DevOps que também programa e escreve sobre tecnologia, open source e sociedade.
Os posts variam entre:

- **Tutoriais técnicos** (séries SSH, Elixir, Spring Boot)
- **Análises técnicas aprofundadas** (Copy Fail, história do HTTP)
- **Posts históricos/narrativos** (história da internet)
- **Posts opinativos** (Linux e LLMs, pinkwashing, jardineiro de software)
- **Posts curtos/receita** (chaves SSH/GPG para GitHub)

O blog usa Jekyll com o tema Minima customizado e está hospedado no GitHub Pages.

## Voz e Tom

O texto deve soar como Eduardo escrevendo. Direto, opinativo, com humor pontual
e honesto sobre complexidade. Não é documentação técnica formal, não é artigo
acadêmico. É um blog pessoal de alguém que sabe do que está falando e não tem
medo de defender posições.

### Pessoa e Registro

- **Primeira pessoa** para experiências e opiniões: "eu uso", "na minha visão",
  "o que eu faço é", "não sei se vocês passam por isso, mas...".
- **Segunda pessoa informal** para o leitor: "você", "vocês". Nunca "o leitor"
  ou "o usuário" quando se refere a quem está lendo o post.
- **Tratamento informal com o público**: "vcs", "pra", "pro", "tá", "né"
  aparecem naturalmente no texto quando o tom pede. Não é necessário ser formal
  o tempo todo.

### Opinião e Posicionamento

- Eduardo **sempre defende posições** com argumentos. Não apresenta opções neutras
  sem se posicionar. Exemplos reais:
  - *"a recomendação padrão ouro hoje em dia, e o que eu pessoalmente uso para
    tudo, é o ED25519"*
  - *"Se você ainda está usando nslcd em 2026, eu respeitosamente sugiro que
    reconsidere suas escolhas de vida"*
  - *"Não é sobre ter o editor mais caro ou a distro perfeita"*

### Humor

- O humor aparece quando o momento pede, nunca forçado. Exemplos reais:
  - *"mds, quanto tempo eu perdi sem isso"*
  - *"por favor não faça isso"* (sobre enfiar cabo elétrico num cano de água)
  - *"dar NOPASSWD: ALL no sudoers é como dar a chave mestra do prédio para o
    entregador de pizza"*
  - *"nível 'me conte absolutamente tudo, incluindo o que você teve no café da manhã'"*
  - *"Aham Cláudia, senta lá!"*
- Sem emoji no texto corrido. Emojis aparecem APENAS dentro de callouts/blockquotes.

### Honestidade

- Eduardo admite quando algo é complexo, longo ou quando ele não sabe:
  - *"Ok, admito que no fim das contas a história não ficou tão breve assim."*
  - *"Não chega a ser complicado, mas ter esses passos resumidos em um só lugar ajuda."*
  - *"Aqui chegamos ao final desse primeiro post, que é curto mas é para falar
    um pouco sobre a criação de ambientes iniciais."*

## Estrutura dos Posts

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
---
```

Campos opcionais usados quando aplicável:

```yaml
subtitle: "Subtítulo descritivo"        # usado em séries (ex: Spring Boot)
modified_date: YYYY-MM-DD HH:MM:SS GMT-3  # quando o post é atualizado
series: Nome da Série                   # agrupa posts em séries no blog
```

### Hierarquia de Títulos

```
## Título de Seção Principal
### Subtítulo
#### Sub-subtítulo (usar com moderação)
##### H5 (quase nunca)
```

O `# H1` é reservado para o título do post (definido no front matter) e NUNCA
deve aparecer no corpo do markdown.

**Regras para títulos**:
- NÃO usar `---` (horizontal rule) entre seções. Nunca. Em nenhum contexto. A
  única exceção aceitável é um `---` solitário antes da seção `## Referências`
  para separá-la visualmente do conteúdo, e APENAS se o post for muito longo.
- NÃO usar backticks (código inline) em títulos (`##`, `###`, etc.), pois isso
  quebra a estética visual da tipografia do blog. Escreva o comando ou termo em
  texto limpo (ex: `## O truque elegante: override_homedir` em vez de usar
  backticks).

### Abertura do Post (antes do primeiro ##)

A abertura é o texto antes da primeira seção `##`. Ela deve:

1. **Situar o leitor no contexto**: o que motivou o post, qual problema ele
   resolve ou qual discussão ele propõe.
2. **Apresentar o problema ou a provocação** sem entregar a solução ainda.
3. **Ter entre 2 e 5 parágrafos**. Sem bullet points na abertura.
4. **Para posts de séries**: mencionar o repositório parceiro e/ou a tag do
   capítulo, e situar no contexto da série.

Referência de abertura bem feita (post de túneis SSH):
> *"SSH é daquelas ferramentas que todo mundo na área de infra tem na ponta da
> língua (...) O problema é que boa parte das pessoas pára exatamente por aí."*

Referência de abertura opinativa (post Linux e LLMs):
> *"A internet está fervendo com mais uma daquelas polêmicas que dividem a
> comunidade de software livre..."*

### Arco Narrativo de Cada Seção

Dentro de cada seção `##`, o fluxo natural de escrita é:

1. **O problema ou pergunta**: o "porquê" antes do "como". Nunca inicia com
   bloco de código sem contexto.
2. **A explicação**: clara, com analogias quando o conceito é abstrato.
3. **O código ou exemplo**: sempre seguido de explicação.
4. **A conexão**: como isso se liga ao que veio antes ou vem depois.

Esse arco é implícito. Não precisa ser rigidamente seguido em toda seção, mas
deve ser o fluxo natural. Seções curtas e diretas (como receitas de comando)
podem ser mais enxutas.

### Transições entre Seções

Cada seção deve concluir e conectar com a próxima de forma natural. Evitar
seções que terminam abruptamente sem contexto do que vem a seguir.

Exemplos reais de transições:
- *"Feito isso, e após a configuração do ambiente base pelo script de
  instalação, estamos prontos para a próxima etapa."*
- *"Agora vamos inverter completamente a lógica."*
- *"Com o projeto estruturado, você pode iniciar um console interativo..."*

### Fechamento do Post

A seção final pode se chamar "Conclusão", "Considerações Finais" ou
"Conclusão: [subtítulo temático]", conforme o que soar melhor para o post.

A conclusão deve:
- Recapitular o que foi construído/discutido sem repetir o post inteiro.
- Conectar com posts futuros quando fizer parte de uma série.
- Ter um tom que feche o assunto de forma satisfatória.
- Pode terminar com uma frase de efeito ou provocação.

Exemplos reais:
- *"É conhecimento de ops que todo mundo deveria ter. E de segurança que todo
  mundo deveria temer quando usado errado."*
- *"Nós não somos engenheiros. Somos jardineiros."*
- *"Até a próxima!"* (comum em posts de séries)

## Formatação

### Blocos de Código

Sempre com linguagem especificada no fence. Sempre seguidos de explicação em
itálico:

```elixir
def criar(titulo) do
  %Todo{id: Ecto.UUID.generate(), titulo: titulo, concluido: false}
end
```

*Aqui, `criar/1` retorna um novo struct `%Todo{}` sem persistir nada ainda.*

A explicação em itálico é obrigatória mesmo para blocos de terminal/bash:

```bash
ssh -L 54322:10.0.254.25:5432 usuario_bastion@ip_publico_bastion
```

*Isso abre a porta 54322 na máquina local, criando um túnel via SSH que passa
pelo bastion e redireciona para a porta 5432 do Postgres interno.*

**Exceções à obrigatoriedade do itálico**:
- Sequências de blocos de código que formam um diálogo contínuo (pergunta/resposta
  de terminal), onde a explicação vem num parágrafo normal entre eles.
- Saídas de terminal onde o resultado é auto-evidente e a explicação seria
  redundante.

### Blocos de Código com Comentários Inline

Em tutoriais, Eduardo usa comentários inline nos blocos bash para explicar cada
comando. Esse estilo substitui a explicação em itálico quando cada linha é
auto-documentada:

```bash
$ curl -s "https://get.sdkman.io" | bash
# Instala o sdkman usando o formato recomendado pelo projeto

$ source "$HOME/.sdkman/bin/sdkman-init.sh"
# Ajusta o ENV para já poder usar o sdkman após a instalação
```

O `$` no início indica que é um comando de terminal interativo. Usar quando
o bloco mostra uma sessão real de terminal.

### Comandos e Código Inline

- **Uso obrigatório de backticks**: Todo comando, flag, caminho de arquivo,
  variável, função, struct, pacote ou trecho de código citado no texto corrido
  DEVE estar envolvido por backticks sem exceção (`ssh`, `-L`, `git commit`,
  `/etc/passwd`, `%Todo{}`, `criar/1`, `mix test`, `ed25519`).
- **Exceção em títulos**: Em títulos e subtítulos (`##`, `###`, etc.), NUNCA
  usar backticks para não quebrar a estética visual dos cabeçalhos.

### Termos em Inglês, Neologismos e Siglas

- Palavras em inglês, estrangeirismos, jargões técnicos não traduzidos,
  neologismos e certas expressões devem ser colocados em *itálico* no texto
  corrido:
  - Exemplos reais dos posts: *page cache*, *dirty*, *writeback*, *scratch space*,
    *in-place*, *effective UID*, *fallback*, *round-trip*, *token*, *parser*,
    *bind*, *handshake*, *slop*, *vibe coding*, *air-gapped*, *toy example*,
    *standalone*.

### Callouts (Avisos, Dicas, Notas)

Sempre em blockquote com emoji e label em *itálico simples* `*Label*:` (isso inverte o itálico nativo do CSS em blockquotes do Jekyll/Chirpy, garantindo que o título da nota fique reto/romano enquanto o texto da nota fica em itálico). Máximo um por seção:

> 💡 *Dica*: Para inspecionar processos ao vivo, use `:observer.start()` no IEx.

> ⚠️ *Aviso*: Nunca exponha `/metrics` sem autenticação em produção.

> 🚨 *Aviso Crítico de Segurança*: Use apenas para alertas de segurança ou perda de dados.

> 💡 *Curiosidade*: O randomart não é só decoração de terminal.

> 💡 *Nota*: A variável `%u` é expandida pelo SSSD para o nome do usuário.

> ⚠️ *Importante*: Essa gerência do ciclo de vida dos usuários é um assunto extenso.

Para disclaimers autorais ou notas de série (texto mais longo, tom pessoal), usar o mesmo formato com emoji e label em itálico simples:

> 🔔 *Disclaimer*: Este post reflete exclusivamente a minha opinião pessoal.

> 🔔 *Nota da Série*: Este post faz parte da série...

> 💡 *Nota*: Este post faz parte de uma versão anterior da série.

### Analogias

Usar quando o conceito é abstrato ou contra-intuitivo. Preferir o mundo físico
e cotidiano. Exemplos reais dos posts:
- Túnel SSH -> cano de água com cabo elétrico dentro.
- Certificado SSH -> "carimbo" de uma autoridade certificadora.
- CA privada vazada -> "joia da coroa" da operação.
- Page cache -> memória compartilhada como sala de estar.
- SSSD -> "porteiro biométrico" / "leão de chácara".
- `sudoers NOPASSWD: ALL` -> chave mestra do prédio para o entregador de pizza.

Não forçar analogia onde o código já é autoexplicativo.

### Diagramas ASCII

Usados para topologias, fluxos de rede e arquitetura. Sempre usar setas e caracteres ASCII (`->`, `<-`, `+`, `-`, `|`):

```
[SEU PC] -> [BASTION: IP Público / IP local: 10.0.254.10]
              +-> [REDE INTERNA: 10.0.254.0/24]
                    +-> POSTGRES: 10.0.254.25 (PostgreSQL :5432)
                    +-> DASHBOARD: 10.0.254.50 (HTTPS :443)
```

### Tabelas

Usadas para resumos comparativos e dados estruturados:

| Flag | Quem escuta? | Quando usar |
|------|-------------|-------------|
| `-L` | Seu PC      | Serviços internos |
| `-R` | Bastion     | Receber conexões |

### Referências e Footnotes

Toda referência externa usa footnote `[^n]` no texto, definida na seção
`## Referências` no final do post.

Formato padrão:

```markdown
[^1]: **Título do recurso** {*Nome da Fonte*} ([Link](url))
```

Exemplos reais:
```markdown
[^1]: **ssh(1): Linux manual page** {*man7.org*} ([Link](https://man7.org/...))
[^2]: **Flask Mega-Tutorial** {*Miguel Grinberg*} ([Link](https://blog.miguelgrinberg.com/...))
[^3]: **Documentação do ASDF** {*ASDF VM*} ([Link](https://asdf-vm.com/))
```

A seção de referências SEMPRE se chama `## Referências`.

### Exercícios (apenas para posts de séries/tutoriais)

No final do post, antes da seção de conclusão, apresentar desafios para o
leitor baseados no que foi aprendido. Os exercícios devem ser breves e diretos,
com as respostas em tags `<details markdown="1">`:

```markdown
**1. Descrição do exercício**

<details markdown="1">
<summary>Ver resposta</summary>

\```elixir
# código da resposta
\```

*Explicação da resposta em itálico logo abaixo do código.*

</details>
```

> ⚠️ **Atenção ao Kramdown**: Em Markdown processado pelo Jekyll (Kramdown), tags HTML em bloco como `<details>` exigem obrigatoriamente o atributo `markdown="1"` para que blocos de código e formatações internas sejam renderizados corretamente.

Nunca inventar exercícios que o leitor não conseguirá fazer com base no que
foi ensinado no post.

### Atualizações de Posts

Quando um post é atualizado com informação nova após a publicação, usar o
formato com negrito e data:

**Atualização (DD/MM/AAAA):** Texto da atualização.

## O que NUNCA fazer

### Proibições Absolutas de Estilo

- **Sem travessões longos** (—) no texto. Eduardo naturalmente não usa e não
  quer que IA use. Substituir por vírgula, ponto, dois-pontos ou reestruturar
  a frase.
- **Sem setas Unicode** (`→`, `←`, `↔`, `⇒`, etc.) no texto corrido, diagramas
  ou exemplos. Use sempre a versão ASCII (`->`, `<-`, `<->`, `=>`), a não ser
  que seja explicitamente solicitado (como em exemplos formais de lógica ou
  matemática).
- **Sem linguagem passiva** onde o ativo é possível.
- **Sem "simplesmente" ou "apenas"** para minimizar complexidade.
- **Sem opinião neutra** onde Eduardo teria posição.
- **Sem emoji no texto corrido**. Emojis só dentro de callouts (blockquotes).
- **Sem `---`** (horizontal rule) entre seções. Nunca.

### Proibições de Estrutura Textual de IA

Estas são estruturas que denunciam que o texto foi gerado por IA. Evitar
rigorosamente:

- **Sem frases genéricas de abertura** tipo "Neste post, vamos explorar...",
  "Neste artigo, vamos abordar...". A abertura deve ser uma narrativa real
  que situa o leitor no problema.
- **Sem parágrafos que começam com "É importante notar que..."**,
  "Vale ressaltar que...", "É fundamental destacar que...".
- **Sem listas de bullet points** onde um parágrafo flui melhor. Eduardo usa
  listas quando são efetivamente itens enumeráveis, não como substituto de
  parágrafo.
- **Sem títulos de seção genéricos** como "Visão Geral", "Entendendo o
  Conceito", "Mergulhando Mais Fundo", "Melhores Práticas". Os títulos devem
  ser específicos ao conteúdo (ex: "O Significado do =: Atribuir e Casar
  ao Mesmo Tempo", "O truque elegante: override_homedir").
- **Sem padrão de "primeiro, segundo, terceiro"** para organizar parágrafos
  a menos que esteja realmente enumerando etapas.
- **Sem vocabulário inflado**: "extremamente", "incrivelmente", "absolutamente"
  em excesso. Eduardo usa essas palavras com moderação e quando realmente
  quer dar ênfase.
- **Sem frases de transição artificiais** tipo "Dito isso, vamos ver...",
  "Com isso em mente...", "Tendo estabelecido isso...". As transições devem
  ser naturais e orgânicas.
- **Sem conclusões que apenas repetem** o que o post disse. A conclusão deve
  agregar algo: uma reflexão, uma provocação, uma conexão com o futuro.
- **Sem código sem contexto**. Sempre explicar o problema antes da solução.
- **Sem seções abruptas**. Cada seção conclui e conecta com a próxima.

### Proibições de Formatação

- **Sem H1** (`#`) no corpo do post. O título vem do front matter.
- **Sem backticks em títulos** (`##`, `###`, `####`). NUNCA usar código inline
  nos cabeçalhos para não poluir a estética visual.
- **Sem comandos ou termos de código soltos sem backticks no texto corrido**.
  Tudo que for comando, flag, caminho de arquivo, função ou código inline deve
  usar backticks sem exceção.
- **Sem blocos de código sem linguagem especificada** no fence.
- **Sem callouts fora de blockquote**. O emoji solto no texto não é mais usado.

## Particularidades por Tipo de Post

### Posts Técnicos / Tutoriais

- O cenário/ambiente de teste deve ser declarado quando relevante (ex: "testado
  no Debian 13 Trixie").
- Comandos de terminal podem usar `$` ou `#` para indicar usuário/root.
- Dissecação de comandos complexos é bem-vinda: "Dissecando essa sopa de
  letrinhas do comando...".
- Alertas de segurança devem usar `🚨 **Aviso Crítico de Segurança**`.
- Posts que fazem parte de uma série devem mencionar a série no front matter
  (`series:`) e conectar com posts anteriores/posteriores na abertura e conclusão.

### Posts Opinativos / Ensaísticos

- O disclaimer pessoal (quando necessário) deve vir logo após a abertura, em
  callout com emoji.
- Eduardo cita fontes e referências mesmo em posts opinativos.
- O tom pode ser mais provocativo, mas sempre fundamentado em argumentos.

### Posts Históricos / Narrativos

- Usar tabelas de navegação para posts muito longos (como feito no post da
  história da internet).
- Notas de "mea culpa" sobre extensão são aceitáveis e bem-vindas.
- Cruzar referências com outros posts do blog quando pertinente.

## Checklist Final

Antes de finalizar qualquer post, verificar:

- [ ] A abertura situa o leitor no contexto sem bullet points?
- [ ] Todos os blocos de código têm linguagem especificada e explicação?
- [ ] Todos os comandos, flags, caminhos e código inline estão com backticks?
- [ ] Títulos e subtítulos estão limpos (sem backticks)?
- [ ] Termos em inglês, neologismos e estrangeirismos estão em *itálico*?
- [ ] Todas as referências externas têm footnote no formato correto?
- [ ] A conclusão agrega algo além de repetir o post?
- [ ] Nenhum travessão longo (—) no texto?
- [ ] Nenhuma seta Unicode (→, ←) no texto ou diagramas (apenas versões ASCII -> ou <-)?
- [ ] Nenhum `---` entre seções?
- [ ] Nenhum emoji no texto corrido (fora de callouts)?
- [ ] Nenhum H1 no corpo do post?
- [ ] O front matter está completo com author em formato de lista YAML?
- [ ] Os títulos de seção são específicos (não genéricos tipo "Visão Geral")?
- [ ] As transições entre seções são naturais?
- [ ] O texto não apresenta padrões textuais óbvios de IA?
- [ ] Para séries: repositório parceiro e tag mencionados?
- [ ] Para séries/tutoriais: exercícios com respostas incluídos?

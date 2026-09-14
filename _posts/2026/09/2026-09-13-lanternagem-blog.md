---
layout: post
title: "A Odisséia da Lanternagem Estética do Blog"
subtitle: "Como joguei fora o tema padrão do GitHub Pages, eliminei CDNs externas e construí uma identidade visual leve, offline-first e com a minha cara"
author:
  - "Eduardo N. S. R."
date: 2026-09-13 20:00:00 GMT-3
permalink: /posts/lanternagem-blog/
tags: [Web, CSS, Jekyll, Minimalismo]
category: Artigos
math: true
mermaid: true
---

Existe uma sensação física de incômodo que todo desenvolvedor com mania de artesão conhece bem: olhar para a própria criação e sentir que ela não tem a sua cara. Durante anos, este blog operou sob a sombra acolhedora e cinzenta do Minima, o tema padrão que o Jekyll entrega quando você cria um repositório no GitHub Pages. Ele funciona. Compila sem chiar. Carrega rápido e não quebra.

Só que a sensação constante era a de morar de aluguel em uma casa mobiliada por outra pessoa. Você não pode pintar uma parede sem o reboco inteiro desabar sobre a sua cabeça.

A gota d'água não foi uma falha técnica repentina. Foi o acúmulo silencioso do tempo.

Conforme o blog foi crescendo, acumulando dezenas de artigos analíticos, tutoriais de infraestrutura, trilhas de Kubernetes e reflexões sobre engenharia, o contraste entre o conteúdo e o continente foi ficando incômodo. Eu passava horas polindo argumentos, formatando blocos de código e desenhando diagramas em ASCII, para no final ver tudo espremido em uma tipografia genérica de sistema, com espaçamentos desajeitados e uma paleta sem vida.

O invólucro não fazia justiça ao que estava dentro.

Tomei coragem, abri o terminal e decretei a reforma geral. Foram dias de faxina pesada: arranquei o tema Minima pela raiz, expurguei camadas acumuladas de CSS utilitário, adotei o Pico CSS v2 como fundação semântica, criei uma paleta própria com modos claro e escuro calibrados, trouxe fontes e scripts para dentro do repositório em modo 100% offline-first e validei cada link com o implacável HTMLProofer.

Se acomode na cadeira e pegue um café. A jornada teve tropeços divertidos, algumas teimosias e muita escovação de bytes.

<details class="toc-box" markdown="1" open>
  <summary><strong>Sumário & Índice de Seções (TOC)</strong></summary>

* TOC
{:toc}

</details>

## O inventário do caos: a herança maldita do Minima e do Open Props

O ponto de partida de qualquer reforma honesta é olhar a bagunça de frente. Sem filtro e sem vergonha.

O ecossistema do Jekyll tem uma comodidade perigosa chamada *theme-gem*. Quando você declara `theme: minima` no seu arquivo `_config.yml`, o Jekyll não coloca nenhum arquivo de estilo dentro da sua pasta de trabalho. Ele busca os templates e os parciais de SCSS compilados dentro da instalação global da gem do Ruby, em um diretório oculto do sistema operacional.

A princípio, isso soa como mágica pura:

```text
meu-blog/
├── _config.yml
├── _posts/
└── index.md
```
*A ilusão da simplicidade: o repositório parece limpo porque toda a complexidade está oculta na gem.*

O problema começa quando você decide customizar qualquer detalhe mínimo da interface.

Quer mudar a largura da coluna principal de leitura? Você precisa criar uma pasta `_sass/`, descobrir qual era o nome exato da variável que o tema original usava e torcer para que o seu arquivo seja importado na ordem correta. Quer alterar o comportamento do cabeçalho da página? Precisa copiar o template `header.html` original da gem para dentro de `_includes/` e começar a fazer alterações cirúrgicas no código alheio.

Em pouco tempo, o repositório vira uma colcha de retalhos de arquivos sobrepostos.

Em uma tentativa anterior de modernizar a aparência do site sem ter o trabalho de reconstruir tudo do zero, cometi o clássico erro de empilhar soluções. Resolvi enxertar o Open Props, uma biblioteca moderna de variáveis CSS e tokens de design.

A intenção era nobre. O resultado prático foi uma guerra civil de especificidade.

No DevTools do navegador, inspecionar um simples título de postagem se transformou em uma sessão de arqueologia digital. Eram três camadas distintas de estilos disputando a prioridade de cada seletor: as regras padrão do Minima brigando com as variáveis do Open Props, que por sua vez eram atropeladas por declarações com `!important` que eu mesmo havia escrito na pressa meses antes para consertar alinhamentos tortos.

```scss
/* O cemitério de especificidade herdada que acumulamos */
.site-header .wrapper .site-title {
  color: var(--gray-9) !important;
  font-family: var(--font-sans);
  letter-spacing: -0.05em;
}
```
*Guerra de especificidade no inspetor: seletores profundos brigando por atenção.*

A manutenção virou um pesadelo constante. Mudar o tamanho de uma fonte no rodapé fazia o cabeçalho quebrar em telas de celular; ajustar a cor de um link na Home estragava o contraste das tags nos artigos.

A casa não era minha. Eu me sentia como um inquilino assustado com medo de ligar o chuveiro e queimar a fiação inteira do prédio.

Chega.

Fui até o `Gemfile` e deletei a linha `gem "minima"`. Em seguida, passei a vassoura na pasta de estilos antigos e limpei os arquivos temporários com `bundle exec jekyll clean`.

Assumi a posse definitiva de cada linha de código que seria servida aos leitores deste blog: zero dependências ocultas e zero mágicas de bastidor.

## A revelação semântica: por que o Pico CSS v2?

Quando você decide jogar fora um tema pronto, a primeira encruzilhada que aparece no caminho é a escolha do novo motor de CSS. Em pleno 2026, as opções disponíveis no mercado parecem caminhar para extremos opostos: de um lado, os gigantes utilitários corporativos liderados pelo Tailwind CSS; do outro, bibliotecas pesadas de componentes como Bootstrap e Bulma, carregando dezenas de estilos que fazem qualquer site parecer um painel administrativo de telecomunicações dos anos 2010.

Considerei o Tailwind por cerca de cinco minutos. Descartei logo em seguida.

Não me entenda mal: o Tailwind é uma ferramenta fantástica para construir aplicações web dinâmicas e reativas com React, Vue ou Svelte. Mas em um blog estático de artigos longos, centrado puramente em texto, a abordagem utilitária é um contra-senso desastroso.

O fluxo de escrita em um blog é abrir o editor de texto, criar um arquivo Markdown e redigir a postagem usando a sintaxe clássica e limpa do formato:

```markdown
## Título da Seção

Este é um parágrafo normal de texto com um [link](https://exemplo.com).

> Uma citação relevante de algum autor histórico.
```

O processador do Jekyll (o Kramdown) converte esse arquivo diretamente para tags HTML5 puras: `<h2>`, `<p>`, `<a>` e `<blockquote>`, sem injetar classes utilitárias no meio do caminho. Para usar Tailwind nesse cenário, você seria obrigado a instalar o plugin `@tailwindcss/typography`, aceitar o conjunto opinativo de classes `.prose`, configurar um pipeline pesado de compilação em Node.js com PostCSS e vigiar constantemente o tamanho da saída gerada.

Eu não queria mais esteiras complexas de frontend para rodar um blog de texto. Eu queria simplicidade objetiva.

Foi nesse momento que o **Pico CSS v2** [^1] entrou em cena como a resposta que eu procurava.

O Pico pertence aos chamados frameworks CSS semânticos (ou *classless*). A proposta central dele é de uma elegância desconcertante: em vez de exigir que você decore centenas de classes utilitárias proprietárias para aplicar no seu HTML, o Pico estiliza diretamente os elementos semânticos nativos do próprio HTML5.

Olhe a comparação estrutural entre os dois paradigmas:

```text
┌─────────────────────────────────────────────────────────────┐
│                    O PARADIGMA UTILITÁRIO                   │
│                                                             │
│   Markdown  ──>  Kramdown  ──>  HTML Cru  ──>  ???          │
│                                                 │           │
│   (Exige plugins, wrappers e injeção de classes utilitárias │
│    como: class="text-xl font-bold mb-4 text-slate-800")     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    O PARADIGMA SEMÂNTICO                    │
│                                                             │
│   Markdown  ──>  Kramdown  ──>  HTML5 Nativo  ──>  Navegador│
│                                       │                     │
│                <article>, <header>, <h2>, <blockquote>      │
│                                       │                     │
│             Pico CSS v2 aplica tipografia, contraste        │
│             e ritmo vertical diretamente nas tags!          │
└─────────────────────────────────────────────────────────────┘
```
*Diferença conceitual: a elegância da renderização semântica direta sem intermediários.*

Se você escreve uma tabela em Markdown, o Kramdown cospe a tag `<table>`, e o Pico CSS intercepta essa tag nativa aplicando instantaneamente bordas sutis, tipografia alinhada, espaçamento interno proporcional e rolagem horizontal em telas estreitas, sem exigir uma única classe auxiliar. A mesma dinâmica acontece com caixas retráteis de `<details>`, formulários, cabeçalhos e citações.

O Markdown continua puro, o HTML gerado permanece limpo e o navegador recebe exatamente o que precisa.

Além disso, a versão 2 do Pico CSS foi reescrita inteiramente em SCSS modular, trazendo duas vantagens fundamentais que selaram a minha decisão: todas as escolhas estéticas são expostas por variáveis nativas de CSS com o prefixo `--pico-*`, e a alternância entre temas claro e escuro é controlada diretamente pelo atributo `data-theme` na tag raiz `<html>`.

O casamento foi perfeito. Conquistamos um design system limpo, responsivo e adaptável, com uma folha de estilos que pesa menos de 15 KB compactada e que respeita rigorosamente a semântica da web.

## A alquimia das cores: construindo a paleta própria (Classic vs Dark)

Com a fundação semântica estabelecida, chegou o momento mais saboroso e arriscado de todo o projeto: escolher as cores do blog. Eu tinha um objetivo muito claro e intransigente em mente: fugir a todo custo dos dois erros capitais que dominam a maioria dos temas modernos na internet.

O primeiro erro é o Dark Mode amador, com fundo preto absoluto (<span class="color-swatch" style="background:#000000;"></span>`#000000`) e tipografia em branco puro (<span class="color-swatch" style="background:#ffffff;"></span>`#ffffff`). Esse contraste artificial extremo de 21:1 agride os olhos do leitor, causa fadiga visual rápida em ambientes escuros e deixa aquele efeito fantasma incômodo de pós-imagem na retina quando você desvia o olhar da tela.

O segundo erro é o Light Mode hospitalar: aquele fundo branco puro reflexivo que transforma a tela de um monitor grande de 27 polegadas em uma lâmpada fluorescente ligada a meio metro do seu rosto. Em ambos os casos, a leitura prolongada se torna um exercício de resistência física.

A inspiração para o visual não veio de nenhum tratado acadêmico de teoria das cores. Veio de um hábito muito simples e antigo meu: eu sempre adorei rabiscar e rascunhar ideias no papel com cores fortes e marcantes, do tipo que você encontra nas dezenas de canetas Stabilo ponta fina que acumulei pela mesa ao longo dos anos. Aquele contraste vivo de tinta pigmentada sobre folha de caderno pautado sempre me deu prazer na hora de pensar.

No mundo digital, as minhas referências de conforto visual sempre foram o Monokai Pro [^2] e o Solarized [^3]. Eu queria trazer essa mesma sensação para o blog: fundos que não agridem a vista, superfícies foscas e acentos de destaque que saltam aos olhos como marca-texto bem passado, sem transformar a página em um carnaval de neon.

Ajustei os valores hexadecimais no arquivo `_sass/base/_variables.scss` buscando equilíbrio prático.

> [!NOTE] Confissão de Bastidor
> Sejamos honestos: o meu nível de apego ao Monokai Pro e ao Solarized Dark é quase vício de fábrica. A linha entre "forte inspiração conceitual" e "kibar a paleta inteira com o conta-gotas aberto" é extremamente tênue. Tive que segurar a mão para não copiar os temas na cara dura, calibrando os contrastes para a leitura do blog, mas se você bater o olho e sentir aquele ar familiar de um terminal bem ajeitado de madrugada, já sabe de onde veio.

Para os destaques primários (links e botões), definimos um ciano fechado (<span class="color-swatch" style="background:#007a8a;"></span>`#007a8a`) no tema claro para dar contraste firme sobre o fundo claro, e um ciano elétrico (<span class="color-swatch" style="background:#78dce8;"></span>`#78dce8`) no tema escuro. O restante dos acentos vibrantes segue a lógica das canetas coloridas: vermelho (<span class="color-swatch" style="background:#d62850;"></span>`#d62850` / <span class="color-swatch" style="background:#ff6188;"></span>`#ff6188`) para callouts de perigo e erros críticos, amarelo (<span class="color-swatch" style="background:#9c6f00;"></span>`#9c6f00` / <span class="color-swatch" style="background:#ffd866;"></span>`#ffd866`) para avisos e pontos de atenção, e verde (<span class="color-swatch" style="background:#46851b;"></span>`#46851b` / <span class="color-swatch" style="background:#a9dc76;"></span>`#a9dc76`) para confirmações e dicas práticas.

A tabela abaixo resume os pilares dessa arquitetura de cores em ambos os modos:

| Papel Semântico | Variável SCSS | Tema Claro (`light`) | Tema Escuro (`dark`) | Finalidade de Uso |
| :--- | :--- | :--- | :--- | :--- |
| **Destaque Primário** | `--pico-primary` | <span class="color-swatch" style="background:#007a8a;"></span>`#007a8a` | <span class="color-swatch" style="background:#78dce8;"></span>`#78dce8` | Links, botões ativos e âncoras |
| **Acento Alerta** | `--accent-red` | <span class="color-swatch" style="background:#d62850;"></span>`#d62850` | <span class="color-swatch" style="background:#ff6188;"></span>`#ff6188` | Callouts de perigo e erros |
| **Acento Destaque** | `--accent-yellow` | <span class="color-swatch" style="background:#9c6f00;"></span>`#9c6f00` | <span class="color-swatch" style="background:#ffd866;"></span>`#ffd866` | Avisos e pontos de atenção |
| **Acento Sucesso** | `--accent-green` | <span class="color-swatch" style="background:#46851b;"></span>`#46851b` | <span class="color-swatch" style="background:#a9dc76;"></span>`#a9dc76` | Confirmações e dicas práticas |
| **Bordas Estruturais** | `$theme-*-border` | <span class="color-swatch" style="background:#dee2e6;"></span>`#dee2e6` | <span class="color-swatch" style="background:#403e41;"></span>`#403e41` | Divisores e contornos de cartões |
| **Texto Atenuado** | `$theme-*-muted` | <span class="color-swatch" style="background:#6c757d;"></span>`#6c757d` | <span class="color-swatch" style="background:#939293;"></span>`#939293` | Metadados, datas e legendas |
| **Tipografia Principal**| `$theme-*-fg` | <span class="color-swatch" style="background:#212529;"></span>`#212529` | <span class="color-swatch" style="background:#fcfcfa;"></span>`#fcfcfa` | Corpo do texto e parágrafos |
| **Blocos de Código** | `$theme-*-code` | <span class="color-swatch" style="background:#f1f3f5;"></span>`#f1f3f5` | <span class="color-swatch" style="background:#221f22;"></span>`#221f22` | Fundo do realce de sintaxe |
| **Painéis / Cards** | `$theme-*-panel` | <span class="color-swatch" style="background:#f8f9fa;"></span>`#f8f9fa` | <span class="color-swatch" style="background:#363337;"></span>`#363337` | Fundo de caixas e resumos |
| **Superfície Base** | `$theme-*-bg` | <span class="color-swatch" style="background:#ffffff;"></span>`#ffffff` | <span class="color-swatch" style="background:#2d2a2e;"></span>`#2d2a2e` | Fundo principal da página |

Para sustentar esses acentos coloridos, a fundação neutra cuida do conforto óptico contínuo durante a leitura longa.

No **Tema Escuro (`dark`)**, a base usa um fundo escuro suave em <span class="color-swatch" style="background:#2d2a2e;"></span>`#2d2a2e` que não tenta fazer uma cirurgia de catarata nos olhos do leitor, com cards e painéis em <span class="color-swatch" style="background:#363337;"></span>`#363337` e blocos de código em <span class="color-swatch" style="background:#221f22;"></span>`#221f22`. O texto principal fica em <span class="color-swatch" style="background:#fcfcfa;"></span>`#fcfcfa`, enquanto bordas e textos secundários usam cinzas neutros para não poluir a leitura.

No **Tema Claro (`light`)**, fomos no clássico limpo: fundo branco <span class="color-swatch" style="background:#ffffff;"></span>`#ffffff`, cartões em <span class="color-swatch" style="background:#f8f9fa;"></span>`#f8f9fa` e código em <span class="color-swatch" style="background:#f1f3f5;"></span>`#f1f3f5`. O texto principal usa o grafite <span class="color-swatch" style="background:#212529;"></span>`#212529`, garantindo leitura nítida e sem reflexos chatos de luz.

> [!TIP] Por que está tudo em inglês nas variáveis?
> Você deve estar se perguntando por que o blog é em português, mas os nomes das variáveis SCSS e tokens estão todos em inglês (`panel`, `code`, `muted`, `border`, `cyan`). A resposta é simples: misturar o inglês nativo do Pico CSS (`--pico-background-color`, `--pico-primary`) com termos soltos em português tipo `$tema-fundo-cartao` ou `$cor-destaque` cria um Franken-código bizarro e doloroso de ler. No código, consistência estética é paz de espírito.

Essas variáveis alimentam os seletores nativos do Pico CSS diretamente no SCSS, unificando links, botões e âncoras sob a mesma identidade.

```scss
/* Mapeamento semântico no _sass/base/_variables.scss */
:root:not([data-theme="dark"]),
[data-theme="light"] {
  color-scheme: light;
  --pico-background-color: #{$theme-light-bg};
  --pico-color: #{$theme-light-fg};
  --pico-card-background-color: #{$theme-light-panel};
  --pico-code-background-color: #{$theme-light-code};
  --pico-primary: #{$theme-light-cyan};
}

[data-theme="dark"] {
  color-scheme: dark;
  --pico-background-color: #{$theme-dark-bg};
  --pico-color: #{$theme-dark-fg};
  --pico-card-background-color: #{$theme-dark-panel};
  --pico-code-background-color: #{$theme-dark-code};
  --pico-primary: #{$theme-cyan};
}
```
*Vinculação elegante: o SCSS alimenta as variáveis CSS nativas que o Pico consome.*

Com a paleta pronta, restava resolver um detalhe técnico clássico: alternar entre os temas sem causar o temido FOUC (*Flash of Unstyled Content*).

Sabe quando você entra em um site à noite com o modo escuro ativado no sistema operacional, mas durante meio segundo a página dá aquele clarão branco cegante antes de carregar o estilo correto? Isso acontece quando o script de chaveamento é posicionado no final do arquivo HTML ou dentro de um evento assíncrono `DOMContentLoaded`.

A nossa solução foi um script síncrono enxuto de vinte linhas, posicionado diretamente dentro da tag `<head>` no template `_includes/head.html`:

```html
<script>
  (function() {
    var stored = localStorage.getItem('theme');
    var theme = stored || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme);
  })();
</script>
```
*Script síncrono anti-clarão: executa antes mesmo do primeiro pixel ser desenhado na tela.*

O navegador interpreta esse bloco antes de começar a desenhar o corpo da página. Se o leitor já escolheu um tema anteriormente clicando no botão do cabeçalho, a preferência gravada no `localStorage` é respeitada de imediato; se for a primeira visita, o script consulta a preferência do sistema via `prefers-color-scheme`.

O resultado é uma transição suave: zero piscadas na tela e zero surpresas desagradáveis no meio da noite.

## A faxina dos ativos: a paranóia saudável do 100% offline-first

Se tem uma coisa que me incomoda profundamente na web contemporânea é a dependência cega de CDNs externas para carregar qualquer elemento básico. Você inspeciona um blog simples e encontra chamadas para servidores do Google Fonts, links para scripts do Cloudflare, folhas de estilo puxadas do unpkg e ícones baixados do jsDelivr.

Parece prático no primeiro dia de desenvolvimento, mas na vida real representa uma dívida técnica e ética pesada.

Existem três razões muito sólidas para você exterminar chamadas externas do seu site: privacidade, resiliência e autonomia. Cada vez que o navegador de um leitor faz uma requisição para carregar uma fonte nos servidores de uma Big Tech, ele envia no pacote o endereço IP, detalhes do dispositivo e a página exata que está sendo lida. Além disso, se a CDN sofrer instabilidade ou bloqueio de rotas, o seu site inteiro congela esperando o timeout da conexão.

Por fim, eu adoro escrever e revisar textos enquanto estou viajando de avião ou em locais remotos. Um blog que depende da internet para carregar o próprio visual localmente é um produto quebrado por concepção.

Comecei a faxina pelas fontes tipográficas, eliminando as chamadas remotas do Google Fonts e baixando diretamente da fundição de código aberto da Adobe as famílias `Source Serif 4` (para o corpo do texto) e `Source Code Pro` (para código e terminais). Ao descompactar os pacotes originais, me deparei com a clássica floresta de formatos legados da web: dezenas de arquivos com extensões `.ttf`, `.otf`, `.eot` e `.woff`.

Perguntei a mim mesmo se precisávamos de todo esse entulho histórico. A resposta foi um sonoro não.

O formato `.woff2` (Web Open Font Format 2.0) utiliza o algoritmo de compressão Brotli nativo e é suportado por praticamente 100% dos navegadores modernos em circulação no mundo há muitos anos. Apaguei todos os formatos antigos da pasta de fontes e deixei exclusivamente os arquivos `.woff2` leves, mantendo as declarações limpas em `_sass/base/_typography.scss`:

```scss
/* Declaração enxuta em _sass/base/_typography.scss */
@font-face {
  font-family: 'Source Serif 4';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/assets/fonts/source-serif-4-regular.woff2') format('woff2');
}

@font-face {
  font-family: 'Source Code Pro';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/assets/fonts/source-code-pro-regular.woff2') format('woff2');
}
```
*Fontes 100% locais: carregamento ultra-rápido sem depender de servidores alheios.*

A mesma postura rigorosa foi aplicada aos ícones do FontAwesome: nada de carregar folhas de estilo mastodônticas de meio megabyte com milhares de ícones que o blog jamais usaria. Isolamos apenas os vetores e classes essenciais para as redes sociais e marcadores em `assets/fonts/` e `_sass/`.

Hoje, se você desligar o cabo de rede ou ativar o modo avião, o blog compila perfeitamente, renderiza com fidelidade absoluta no navegador e não dispara uma única requisição para fora do servidor local.

Autonomia de verdade é isso.

## Tipografia e ritmo vertical: o design para leitura imersiva

Se o layout do site é o seu esqueleto, a tipografia é a sua respiração. Você pode ter a melhor arquitetura do mundo, mas se a tipografia for apertada, o contraste for deficiente ou a largura das linhas for exagerada, o leitor vai cansar os olhos e fechar a aba em menos de três minutos de leitura.

Para um blog focado em ensaios e artigos aprofundados com milhares de palavras, a legibilidade é uma prioridade inegociável.

A escolha da serifa (`Source Serif 4`) para o corpo do texto foi uma decisão consciente contra a tendência contemporânea de colocar fontes sem serifa em tudo quanto é canto. Fontes serifadas clássicas bem desenhadas criam uma linha de base imaginária sutil que guia o olhar com suavidade ao longo dos períodos, reduzindo o esforço cognitivo em leituras longas.

Para acompanhar, travamos o contêiner do post em `760px`, garantindo uma média saudável entre 65 e 75 caracteres por linha (a zona áurea do design editorial clássico) com um entrelinhas generoso de `1.75`.

A hierarquia de títulos também foi aliviada: no tema antigo, os títulos H1 vinham em negrito ultrapesado (`font-weight: 800`), parecendo uma manchete gritada de tabloide sensacionalista. Reduzimos o peso do H1 para `500` com um leve ajuste de aproximação de caracteres (`letter-spacing: -0.5px`), complementando com o subtítulo em `<p class="post-subtitle">` logo abaixo para contextualizar o tom do artigo sem competir com o cabeçalho.

Outro ajuste detalhado foi a calibração dos blocos de código Rouge em `_sass/_syntax.scss`. O realce de sintaxe herdado embutia regras que aplicavam negrito em quase todas as palavras-chave de linguagens como Java, Python e Rust, transformando trechos longos em festivais de manchas escuras.

Nivelamos palavras-chave, variáveis, funções e operadores no peso regular (`font-weight: 400`), fazendo o código renderizar de forma plana, limpa e confortável, exatamente como nos editores modernos.

Na página Sobre ([`about.md`](/about/)), preservamos a nossa tradicional marca visual: o caractere em escrita vertical japonesa flutuando na lateral direita da tela. Ajustamos o elemento `.jp-float` com opacidade suave para atuar como textura visual sem obstruir o texto corrido, e adicionamos `aria-hidden="true"` para garantir acessibilidade e evitar que leitores de tela tentem pronunciar o caractere decorativo.

```scss
/* O kanji vertical na página Sobre */
.jp-float {
  writing-mode: vertical-rl;
  text-orientation: upright;
  opacity: 0.15;
  user-select: none;
}
```
*Tipografia vertical japonesa com acessibilidade: atributo aria-hidden garante silêncio aos leitores de tela.*

Por fim, resolvemos o clássico bug do rodapé flutuante (o famoso *Sticky Footer*).

Em páginas curtas, como a de erro 404 ou em listagens de tags com apenas um post, o rodapé teimava em subir e ficar flutuando no meio da tela como uma faixa perdida. A cura veio em dez linhas de Flexbox moderno em `_sass/layout/_footer.scss`:

```scss
/* A cura definitiva para rodapés flutuantes */
body {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

main.container {
  flex: 1 0 auto;
}

.site-footer {
  margin-top: auto;
}
```
*Comportamento de mola: o container principal empurra o rodapé para o piso em qualquer resolução.*

O `body` assume altura mínima de `100vh`, o contêiner principal preenche todo o espaço vertical livre com `flex: 1 0 auto`, e o rodapé recebe `margin-top: auto`. Seja em uma página com vinte parágrafos ou em uma tela com uma única frase de aviso, o rodapé repousa com firmeza no chão da janela, sem uma linha sequer de JavaScript.

## A saga da matemática: KaTeX local sem nós cegos

Para quem escreve sobre ciência da computação, criptografia, sistemas distribuídos e física, ter suporte de primeira classe à renderização de equações matemáticas em LaTeX é mandatório. Mas aqui mora uma das maiores armadilhas de performance da web técnica: o MathJax.

Embora venerável e completo, o MathJax é colossal. Ele despeja megabytes de scripts no navegador do leitor, demora preciosos segundos para inicializar e redesenha a árvore DOM várias vezes até conseguir formatar uma fórmula simples. Em conexões móveis, a página inteira engasga.

A alternativa consagrada é o **KaTeX**, mantido pela equipe do Khan Academy, que desenha equações de forma síncrona, leve e sem refazer o layout da página.

Nossa primeira ideia foi tentar a gem `kramdown-math-katex`, que prometia interceptar os delimitadores `$$` durante a compilação do site e gerar o HTML estático das equações diretamente no servidor. No papel soava perfeito, mas na prática foi um desastre silencioso.

A gem depende de uma ponte de comunicação com o Node.js no sistema operacional via ExecJS, e no meu ambiente essa amarração falhou de forma opaca: o build do Jekyll passava sem acusar erro no terminal, mas as fórmulas apareciam na página como blocos de texto cru com barras invertidas escapadas (`\[ \mathcal{F} ... \]`).

Parei de brigar com a compilação no servidor e adotei a abordagem pragmática: o KaTeX oficial rodando no client-side sob demanda.

Criamos um include inteligente no arquivo `_includes/head.html` que injeta os scripts e folhas de estilo exclusivamente se o post declarar `math: true` no front matter:

```html
{% raw %}{% if page.math %}
  <link rel="stylesheet" href="{{ '/assets/katex/katex.min.css' | relative_url }}">
  <script defer src="{{ '/assets/katex/katex.min.js' | relative_url }}"></script>
  <script defer src="{{ '/assets/katex/contrib/auto-render.min.js' | relative_url }}"
          onload="renderMathInElement(document.body);"></script>
{% endif %}{% endraw %}
```
*Injeção condicional por demanda: quem lê tutoriais sem fórmulas baixa zero bytes de matemática.*

Se o artigo que você está lendo é uma crônica ou um tutorial de Linux, a variável `page.math` não existe e o Jekyll nem sequer inclui essas tags no HTML compilado; zero scripts adicionais são trafegados.

E na pasta de fontes da biblioteca, aplicamos a mesma faxina: deletamos todos os formatos legados `.ttf` e `.woff`, deixando estritamente os vinte arquivos `.woff2` necessários para símbolos AMS e alfabetos gregos. A pasta de fontes despencou de 1.2 MB para meros 250 KB, garantindo a renderização instantânea de fórmulas como a transformada de Fourier:

$$
\mathcal{F}\{f\}(\omega) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} f(t) e^{-i\omega t} \, dt
$$

> [!NOTE] Que equação é essa?
> Para quem ficou curioso: essa é a boa e velha **Transformada de Fourier** para fazer mágica na área de processamento de sinais. Eu poderia entrar nos detalhes matemáticos, mas sou uma pessoa que quer evitar a fadiga, e a internet já tem material de sobra sobre isso. E olha que bonito, o KaTeX renderizou como se fosse uma drag queen se maquiando, com direito a brilho, contorno e cílios postiços. Um luxo!

O resultado é uma matemática com nitidez vetorial absoluta, sem atrasos de carregamento e sem saltos de layout na rolagem da página. Rápido, previsível e leve como deve ser.

## Sumários dinâmicos e componentes modulares: o poder do Kramdown nativo

Quem escreve artigos extensos sabe que um sumário funcional no início do texto não é um luxo decorativo, mas uma ferramenta essencial de navegação para o leitor. No meu artigo sobre a {% include post-ref.html slug="historia-internet" text="História da Internet" %}, por exemplo, o texto é tão longo que navegar sem um índice de seções é como viajar em uma rodovia sem placas.

Durante muito tempo eu mantinha uma lista manual de tópicos no começo dos artigos, o que invariavelmente gerava links quebrados toda vez que eu renomeava um subtítulo.

Quando pesquisei como automatizar a geração do índice de seções (TOC - *Table of Contents*), a recomendação habitual da comunidade foi instalar o plugin `jekyll-toc`. Em vez de adicionar mais uma dependência ao `Gemfile`, fui consultar a documentação do Kramdown [^4], o conversor padrão de Markdown do Jekyll.

Descobri que o Kramdown já possui um gerador nativo de sumários integrado desde as suas primeiras versões, dispensando qualquer gem auxiliar. Basta configurar o comportamento dos níveis de captura no arquivo `_config.yml` para ignorar o H1 do título principal e capturar estritamente os subtítulos H2 e H3:

```yaml
# Configuração nativa no _config.yml
kramdown:
  input: GFM
  smart_quotes: ["apos", "apos", "quot", "quot"]
  toc_levels: 2..3
```
*Ajuste do Kramdown: o índice ignora o H1 do título e captura estritamente os subtítulos H2 e H3.*

No corpo do artigo, envolvemos a diretiva semântica `{:toc}` dentro de uma tag nativa `<details class="toc-box" markdown="1" open>`. O atributo `markdown="1"` é fundamental para que o Kramdown processe o conteúdo interno da tag HTML, varrendo os cabeçalhos do documento e gerando uma lista aninhada com identificadores de âncora funcionais automaticamente.

Para completar, estilizamos a caixa retrátil no arquivo `_sass/components/_toc.scss`:

```scss
/* Estilo semântico da caixa de sumário */
.toc-box {
  background-color: var(--pico-card-background-color);
  border: 1px solid var(--pico-muted-border-color);
  border-radius: 6px;
  padding: 1rem 1.25rem;
  margin: 2rem 0;

  summary {
    cursor: pointer;
    font-size: 1.05rem;
    color: var(--pico-color);
  }

  ul {
    margin-top: 0.75rem;
    padding-left: 1.5rem;

    li a {
      color: var(--pico-primary);
      text-decoration: none;

      &:hover {
        text-decoration: underline;
      }
    }
  }
}
```
*Sumário dinâmico, elegante e retrátil sem uma linha sequer de JavaScript.*

A mesma disciplina de modularidade e reaproveitamento de código (DRY - *Don't Repeat Yourself*) guiou a reconstrução dos demais componentes do blog. O include `_includes/card.html` unificou a renderização dos cartões de categorias e trilhas com contadores dinâmicos de posts; o `_includes/post-list.html` centralizou a exibição de metadados e paginação entre a Home e as taxonomias; o modal de apoio ao criador (`_includes/pix-modal.html`) foi reconstruído com travamento suave de scroll; e os diagramas dinâmicos do **Mermaid.js** foram desacoplados em um componente próprio (`_sass/components/_mermaid.scss` e `_includes/mermaid.html`), renderizando fluxogramas e diagramas de sequência com adaptação automática aos temas claro e escuro.

Menos código duplicado, mais coerência visual em cada recanto do site.

## O teste de fogo: compilando 101 páginas e domando o HTMLProofer

Depois de mexer na fundação inteira do blog, renomear variáveis de ponta a ponta, excluir centenas de linhas de código antigo e refatorar cada template HTML, qualquer desenvolvedor é assaltado pela dúvida natural: o que foi que quebrou sem que eu percebesse?

Em um site pessoal com mais de cem páginas publicadas ao longo de anos, fazer uma checagem visual clicando em cada link pelo navegador é humanamente inviável. Fatalmente você esquecerá um link antigo, deixará uma âncora órfã ou esquecerá de fechar uma tag semântica.

Para auditar o site com rigor de engenharia, convoquei o auditor definitivo: o **HTMLProofer** [^5], adicionando a ferramenta ao `Gemfile` dentro do grupo de testes. O utilitário compila o site estático completo e realiza uma varredura minuciosa em cada arquivo gerado na pasta `_site`, inspecionando links internos, imagens ausentes, scripts inexistentes e marcações malformadas.

Ao disparar o teste pela primeira vez, tomei de cara um erro seco de biblioteca C ausente:

```text
/home/debian/.gem/ruby/3.3.0/gems/ffi-1.17.4/lib/ffi/dynamic_library.rb:94:in `load_library':
Could not open library 'libcurl': libcurl: cannot open shared object file: No such file or directory. (LoadError)
Could not open library 'libcurl.so.4': libcurl.so.4: cannot open shared object file: No such file or directory.
```
*O susto clássico de ambiente Linux: dependência C dinâmica ausente no host.*

O HTMLProofer utiliza a gem `typhoeus` para disparar verificações HTTP paralelas de alta velocidade, conversando diretamente com a biblioteca nativa `libcurl` do sistema via FFI em linguagem C. Em instalações limpas e minimalistas do Debian no WSL, a biblioteca `libcurl4` não vem pré-instalada.

Um rápido `sudo apt update && sudo apt install -y libcurl4` resolveu a pendência no host, mas ao reexecutar o comando esbarrei nas mudanças arquiteturais da versão 5.2.2 do auditor.

As antigas flags `--check-html` e `--check-images` foram descontinuadas porque no v5 essas checagens rodam ativadas por padrão em todas as execuções. Além disso, a versão 5 força a validação estrita de HTTPS em links externos, o que quebrava a auditoria em posts históricos antigos que citam papers acadêmicos e repositórios de universidades que ainda operam sob HTTP tradicional.

Com as opções ajustadas para o nosso cenário, o terminal processou todo o acervo sem travar em servidores acadêmicos externos:

```bash
$ bundle exec htmlproofer ./_site --disable-external --no-enforce-https
Running 3 checks (Images, Links, Scripts) in ["./_site"] on *.html files ...

Checking 287 internal links
Checking internal link hashes in 41 files
Ran on 104 files!

HTML-Proofer finished successfully.
Finished in 12.34 seconds
```
*Certidão de nascimento do novo tema: 104 páginas auditadas e zero inconsistências.*

Cento e quatro páginas estáticas compiladas, duzentos e oitenta e sete links internos auditados e quarenta e um arquivos com sumários e âncoras validados em profundidade com zero falhas. A nova arquitetura estava oficialmente homologada e pronta para produção.

## Conclusão e o prazer do jardim digital

Existe uma satisfação indescritível e genuína em abrir o próprio blog no navegador e conhecer o motivo de cada pixel desenhado na tela. Saber exatamente por que cada margem foi posicionada daquela forma, entender por que cada família tipográfica foi escolhida e ter a certeza de que nenhuma requisição secreta está sendo feita pelas costas do leitor para servidores de publicidade ou telemetria é uma forma rara de paz de espírito.

Este blog deixou de ser um inquilino assustado morando de favor em um tema genérico do GitHub Pages. Ele se transformou naquilo que a cultura do software livre convencionou chamar de *digital garden* [^6]: um pedaço acolhedor de terra na internet que você cultiva com as suas próprias mãos, com as suas preferências estéticas, cuidando das podas, adubando a tipografia e garantindo que quem passe por aqui tenha uma experiência de leitura confortável, leve e segura.

Há uma importância quase terapêutica em cuidar do seu espaço digital como quem cuida de um jardim (afinal de contas, como já defendi por aqui, não somos todos jardineiros de software [^7]?).

Se você ficou curioso para ver como todos esses elementos visuais se comportam juntos na prática, convido você a visitar o nosso laboratório vivo no {% include post-ref.html slug="showcase" text="Showcase de Elementos & Design System" %}. Lá você encontrará a escala tipográfica completa, os cinco tipos de callouts personalizados, as amostras de código em múltiplas linguagens de programação, as matrizes matemáticas do KaTeX e os detalhes expansíveis reunidos em uma única página de testes.

A casa está arrumada. O chassi está calibrado. As ferramentas estão no lugar.

Agora, o único trabalho restante é o mais prazeroso de todos: sentar na cadeira e voltar a escrever.

## Referências

[^1]: **Pico CSS v2: Semantic CSS Framework** {*Pico CSS Documentation*} ([Link](https://picocss.com/))
[^2]: **Monokai Pro: Color scheme & custom UI theme** {*Wimer Hazenberg*} ([Link](https://monokai.pro/))
[^3]: **Solarized: Precision colors for machines and people** {*Ethan Schoonover*} ([Link](https://ethanschoonover.com/solarized/))
[^4]: **kramdown: Fast, pure-Ruby Markdown-to-HTML converter** {*Thomas Leitner*} ([Link](https://kramdown.gettalong.org/))
[^5]: **HTML-Proofer: Test your HTML files to make sure they're accurate** {*Garen Torikian*} ([Link](https://github.com/gjtorikian/html-proofer))
[^6]: **A Brief History & Ethos of the Digital Garden** {*Maggie Appleton*} ([Link](https://maggieappleton.com/garden-history))
[^7]: **Você não é um Engenheiro de Software** {*Eduardo N. S. R., Ago/2024*} ({% include post-ref.html slug="jardineiro-software" text="Link" %})

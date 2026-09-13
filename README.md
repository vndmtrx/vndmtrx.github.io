# Vndmtrx Blog

> *Vi Veri Vniversum Vivvs Vici* — Blog pessoal sobre engenharia de software, Linux, DevOps, computação distribuída, privacidade e reflexões técnicas.

[![Jekyll 4.4](https://img.shields.io/badge/Jekyll-4.4-CC0000.svg?logo=jekyll&logoColor=white)](https://jekyllrb.com/)
[![Pico CSS v2](https://img.shields.io/badge/Pico%20CSS-v2-1095c1.svg)](https://picocss.com/)
[![KaTeX](https://img.shields.io/badge/KaTeX-LaTeX%20Math-329894.svg)](https://katex.org/)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](LICENSE)
[![Deploy](https://github.com/vndmtrx/vndmtrx.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/vndmtrx/vndmtrx.github.io/actions)

---

## 🧭 Visão Geral & Filosofia

Este repositório contém o código-fonte e o conteúdo do blog [vndmtrx.github.io](https://vndmtrx.github.io). 

O projeto passou por um **rework arquitetural completo**, abandonando o tema clássico Minima e o ecossistema Open Props em favor de uma integração limpa com o **Pico CSS v2**, estruturada em **Sass modular (Dart Sass `@use`)** com foco em:

1. **HTML 100% Semântico:** Aproveitamento nativo dos elementos HTML5 (`<article>`, `<header>`, `<hgroup>`, `<section>`, `<nav>`, `<details>`, `<dialog>`).
2. **Offline-First & Zero Dependências Externas em Runtime:** Fontes e bibliotecas são servidas estática e localmente pelo próprio repositório, garantindo total privacidade, imunidade a bloqueios de CDNs e renderização instantânea.
3. **Tipografia Editorial Imersiva:** Calibração tipográfica refinada com ritmo vertical agradável, escalas fluidas e leitura confortável tanto no modo claro quanto no modo escuro.
4. **Desempenho Estático Extremo:** Construção estática com Jekyll e deploy automatizado no GitHub Pages via GitHub Actions.

---

## ✨ Recursos & Funcionalidades

### 🎨 Design System & Estilização
- **Pico CSS v2 Customizado:** Integração com o framework semântico Pico CSS v2, adaptado com tokens de cores e temas definidos em `_sass/base/_variables.scss`.
- **Modos Claro & Escuro Nativos:** Suporte automático ao esquema de cores do sistema (`prefers-color-scheme`) e alternância via atributos sem quebras visuais.
- **Tipografia Local Otimizada:** Fontes *Source Serif 4* (corpo de texto e títulos) e *Source Code Pro* (código e monospace) servidas estritamente em formato `.woff2` para máxima compressão e performance.
- **Syntax Highlighting Editorial:** Esquema de cores customizado para o Rouge em `_sass/_syntax.scss`, com blocos de código formatados com respiro vertical harmonizado.

### 📐 Matemática & LaTeX (KaTeX Local)
- **Renderização de Fórmulas Matemáticas:** Suporte completo a equações LaTeX inline (`$$ ... $$`) e em bloco (`$$`), processadas pelo KaTeX.
- **Carregamento Sob Demanda:** O CSS e os scripts JS do KaTeX (armazenados localmente em `assets/katex/`) só são injetados no `<head>` quando a página define `math: true` no front matter.
- **Fontes WOFF2 Otimizadas:** Apenas 20 arquivos `.woff2` estritamente necessários (~250 KB no total), cobrindo integrais, matrizes, delimitadores gigantes e símbolos AMS.

### 📚 Arquitetura de Conteúdo & Taxonomias
- **Trilhas e Séries de Tutoriais:** Suporte a séries temáticas (configuradas em `_data/series.yml`) com layout dedicado ([`_layouts/serie.html`](_layouts/serie.html)), hero cards informativos e timeline ordenada de capítulos.
- **Hubs de Navegação Dinâmicos:**
  - **Categorias:** Página com cards descritivos em grade responsiva ([`categorias.html`](categorias.html)).
  - **Trilhas:** Hub visual listando todas as séries de tutoriais disponíveis ([`tutoriais.html`](tutoriais.html)).
  - **Tags:** Nuvem de tags categorizada por popularidade com navegação alfabética rápida ([`tags.html`](tags.html)).
- **Paginação Automática (`jekyll-paginate-v2`):** Geração automática de páginas de arquivo para cada categoria e tag via `autopages`, com paginação calibrada para 5 posts por página na Home.
- **Sumários Automáticos (TOC Nativo):** Geração automática de sumários dinâmicos com hierarquia de títulos e links âncora através do recurso nativo `{:toc}` do Kramdown, com estilização responsiva em `_sass/components/_toc.scss`.
- **Callouts GFM (Admonitions):** Suporte nativo aos 5 tipos de avisos do GitHub Flavored Markdown (`NOTE`, `TIP`, `IMPORTANT`, `WARNING`, `CAUTION`) estilizados com as cores do tema.

### 🧩 Componentes DRY Reutilizáveis
- [`_includes/card.html`](_includes/card.html): Componente genérico para cards de categorias e trilhas com suporte a ícones FontAwesome e emojis.
- [`_includes/post-list.html`](_includes/post-list.html): Componente padronizado para listagem de artigos, resumos, metadados e controles de paginação.
- [`_includes/pix-modal.html`](_includes/pix-modal.html): Modal nativo HTML5 `<dialog>` para apoio financeiro via Pix com cópia de chave e QR Code.
- [`_posts/2024/03/2024-03-22-showcase.md`](_posts/2024/03/2024-03-22-showcase.md): Página de showcase completa (`/showcase/`) para testes e validação visual de todos os elementos do tema.

---

## 📁 Estrutura de Diretórios

```
.
├── _data/                   # Dados estruturados (ex: series.yml)
├── _includes/               # Componentes parciais Liquid (head, header, card, post-list, etc.)
├── _layouts/                # Templates de layout (default, post, serie, category, tag, page)
├── _posts/                  # Artigos em Markdown organizados por ano/mês
├── _sass/                   # Arquitetura modular de estilos Sass
│   ├── base/                # Variáveis, paleta de cores, tipografia e reset
│   ├── components/          # Cards, pílulas, admonitions, paginação, modal pix, etc.
│   ├── layout/              # Header/navbar, fluxo do post, sticky footer
│   ├── _syntax.scss         # Realce de sintaxe Rouge
│   └── main.scss            # Entrypoint Sass compilado via Dart Sass
├── assets/                  # Arquivos estáticos servidos pelo site
│   ├── css/                 # Pico CSS v2 e style.scss
│   ├── fonts/               # Fontes locais (Source Serif 4, Source Code Pro)
│   ├── images/              # Imagens e ilustrações
│   └── katex/               # Biblioteca KaTeX offline (CSS, JS, auto-render, fonts woff2)
├── tutoriais/               # Páginas base das séries e trilhas
├── _config.yml              # Configuração global do Jekyll e plugins
├── Gemfile                  # Dependências Ruby gerenciadas pelo Bundler
└── handoff_pico_css.md      # Registro técnico detalhado de todas as alterações do rework
```

---

## 🚀 Como Executar Localmente

### Pré-requisitos
- **Ruby:** 3.x+
- **Bundler:** `gem install bundler`
- **Libcurl (necessário para o HTMLProofer no Linux/WSL):** `sudo apt install -y libcurl4`

### Instalação & Execução

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/vndmtrx/vndmtrx.github.io.git
   cd vndmtrx.github.io
   ```

2. **Instale as dependências Ruby:**
   ```bash
   bundle install
   ```

3. **Inicie o servidor de desenvolvimento do Jekyll:**

   - **Modo Padrão (com recarregamento contínuo no Windows):**
     ```bash
     bundle exec jekyll serve --host 0.0.0.0 --force_polling --incremental
     ```

   - **Modo de Escrita & Redação (Rascunhos e Posts Futuros):**
     ```bash
     bundle exec jekyll serve --host 0.0.0.0 --force_polling --incremental --drafts --future
     ```

   > **💡 Explicação das flags:**
   > - `--host 0.0.0.0`: Libera o acesso para outros dispositivos na rede local ou via WSL/VM.
   > - `--force_polling`: Garante a detecção imediata de arquivos modificados em sistemas Windows/WSL.
   > - `--incremental`: Compila apenas as páginas e componentes alterados, acelerando muito o recarregamento.
   > - `--drafts`: Publica localmente os arquivos contidos na pasta `_drafts/`.
   > - `--future`: Renderiza posts agendados para datas futuras (essencial durante a escrita de novos artigos).

4. **Acesse no navegador:**
   - **Site:** [http://localhost:4000](http://localhost:4000)
   - **Showcase de Elementos:** [http://localhost:4000/showcase/](http://localhost:4000/showcase/)

---

## 🧪 Qualidade & Auditoria (HTMLProofer)

O projeto inclui o **HTMLProofer** para validar a integridade de todo o HTML gerado pelo Jekyll antes de publicar.

Para auditar o site e checar **links quebrados**, caminhos de imagens e integridade HTML:

1. **Gere o build estático:**
   ```bash
   bundle exec jekyll build
   ```

2. **Execute o HTMLProofer:**

   - **Auditoria rápida (links internos, âncoras e imagens locais):**
     ```bash
     bundle exec htmlproofer ./_site --disable-external --no-enforce-https
     ```

   - **Auditoria completa (incluindo validação de URLs externas na web):**
     ```bash
     bundle exec htmlproofer ./_site --no-enforce-https
     ```

O auditor verifica:
- 🔗 Links internos ou âncoras quebradas (erro 404).
- 🖼️ Imagens com caminhos inexistentes ou sem o atributo `alt` (acessibilidade).
- 🏷️ Fechamento e integridade estrutural das tags HTML5.

---

## ✍️ Guia de Escrita de Posts

Para criar uma nova postagem, crie um arquivo em `_posts/AAAA/MM/AAAA-MM-DD-titulo-do-post.md`:

```yaml
---
layout: post
title: "Título do Seu Post"
date: 2026-09-13 18:00:00 -0300
excerpt: "Breve resumo que aparecerá nas listagens e no SEO."
categories: [Programação]
tags: [Linux, DevOps, Kubernetes]
math: true           # Habilita o KaTeX se o post contiver equações matemáticas
# serie: k8s-local   # Opcional: vincula o post a uma trilha definida em _data/series.yml
# serie_order: 1     # Ordem do capítulo dentro da trilha
---

Seu conteúdo em Markdown aqui...

### Exemplo de Equação Matemática
A fórmula inline $$e^{i\pi} + 1 = 0$$ ou em bloco:

$$
\mathcal{F}\{f\}(\omega) = \int_{-\infty}^{\infty} f(t) e^{-i\omega t} \, dt
$$

> [!NOTE]
> Nota explicativa utilizando GitHub Flavored Markdown Admonitions.
```

---

## 📄 Licença

Distribuído sob a licença **GPL-3.0**. Consulte o arquivo [`LICENSE`](LICENSE) para mais informações.
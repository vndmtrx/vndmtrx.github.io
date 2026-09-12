# Blog vndmtrx.github.io

Este é o repositório do meu blog pessoal. O site é gerado estaticamente usando Jekyll e hospedado via GitHub Pages.

## Tecnologias

- **Gerador de Site Estático:** Jekyll 4.4
- **Estilização:** Sass (Dart Sass via `@use`) customizado (originalmente um fork do Minima v3, mas totalmente descolado e independente)
- **Hospedagem:** GitHub Pages
- **Deploy:** GitHub Actions

## Estrutura do Projeto

- `_layouts/`: Templates HTML base (home, post, page, category, tag)
- `_includes/`: Componentes modulares (head, header, footer, pix-modal)
- `_sass/`: Folhas de estilo modularizadas (variáveis, fontes, layout, componentes)
- `_posts/`: Artigos do blog escritos em Markdown
- `assets/`: Arquivos estáticos (imagens, favicons, css compilado)

## Como rodar localmente

### Pré-requisitos

- Ruby (versão compatível com o Jekyll)
- Bundler (`gem install bundler`)
- Jekyll

### Passo a passo

1. Instale as dependências:
   ```bash
   bundle install
   ```

2. Rode o servidor de desenvolvimento:
   ```bash
   bundle exec jekyll serve
   ```

3. Acesse no navegador: `http://localhost:4000`

## Workflow de Deploy

O deploy é feito automaticamente via GitHub Actions. Qualquer push na branch principal engatilha a action definida em `.github/workflows/deploy.yml` que compila o site e publica no GitHub Pages.
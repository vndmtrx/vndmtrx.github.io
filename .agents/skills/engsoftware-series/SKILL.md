---
name: engsoftware-series
description: >
  Convenções, metadados e diretrizes da série "Engenharia de Software Essencial" (28 módulos) do blog vndmtrx.github.io. Use quando o usuário pedir para escrever, rascunhar ou revisar módulos desta série.
---

# Skill: Série Engenharia de Software Essencial

Diretrizes técnicas e estruturais para os posts da série **Engenharia de Software Essencial -- Da Demanda à Arquitetura** baseada no SWEBOK v4.0 e no projeto piloto **SGCF (Sistema de Gestão e Controle de Frotas)**.

---

## 1. Convenções Editoriais da Série

- **Front Matter Obrigatório:**
  ```yaml
  category: Artigos # ou Tutoriais conforme o módulo
  series: Engenharia de Software Essencial
  title: "Engenharia de Software, Módulo XX - [Tema]"
  subtitle: "[Tagline ou frase de efeito técnica]"
  tags: [Engenharia de Software, Arquitetura, SWEBOK, Modelagem, Qualidade]
  ```
- **Página de Coleção / Trilha:** Cadastrada em `tutoriais/engsoftware.md` e metadados em `_data/series.yml`.
- **Estudo de Caso Contínuo:** Todos os módulos aplicam a teoria ao **SGCF** (Mobile-First Web PWA com QR Code no painel de veículos, GPS via Geolocation API e prestação de contas de combustível).

---

## 2. Metas de Extensão e Calibração por Tiers

- **Tier 1 (Fundacional):** ~3.600 a 4.200 palavras (M01-M03, M07, M13, M26).
- **Tier 2 (Padrão):** ~4.500 a 5.000 palavras (M04-M05, M08-M11, M14-M17, M19, M22, M24-M25, M27-M28).
- **Tier 3 (Alta Densidade):** ~5.400 a 6.500 palavras (M06, M12, M18, M20, M21, M23).

---

## 3. Roteiro e Ementa sob Demanda

O roteiro detalhado de todos os 28 módulos está em [references/roteiro.md](file:///home/rolim/du/dev/github/vndmtrx.github.io/.agents/skills/engsoftware-series/references/roteiro.md).

> [!TIP] Eficiência de Tokens
> **NÃO leia o roteiro inteiro.** Ao redigir ou revisar o Módulo X, faça a leitura exclusiva do Módulo X em `references/roteiro.md` utilizando `view_file` com slice de linhas (`StartLine`/`EndLine`).

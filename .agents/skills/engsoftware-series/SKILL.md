---
name: engsoftware-series
description: >
  Convenções, metadados, tiers de extensão e roteiro da série "Engenharia de Software Essencial" (28 módulos, SWEBOK v4.0 + SGCF) no blog vndmtrx.github.io. Ative ao escrever, rascunhar ou revisar módulos desta série.
---

# Skill: Série Engenharia de Software Essencial

Herda integralmente voz, antipadrões, ritmo, invariantes e validação (`scripts/lint_post.py`) de [blog-posts](../blog-posts/SKILL.md). Baseada no **SWEBOK v4.0** e no projeto piloto **SGCF (Sistema de Gestão e Controle de Frotas)**.

---

## 1. Convenções da Série

- **Front Matter Obrigatório:**
  ```yaml
  category: Artigos # ou Tutoriais conforme o módulo
  series: Engenharia de Software Essencial
  title: "Engenharia de Software, Módulo XX - [Tema]"
  subtitle: "[Tagline técnica]"
  tags: [Engenharia de Software, Arquitetura, SWEBOK, Modelagem, Qualidade]
  ```
- **Trilha:** Página em `tutoriais/engsoftware.md` e metadados em `_data/series.yml`.
- **Estudo de Caso Contínuo:** Todos os módulos aplicam a teoria ao **SGCF** (Mobile-First Web PWA com QR Code no painel de veículos, GPS via Geolocation API e prestação de contas de combustível).
- **Override de Exercícios (Obrigatório):** Todo módulo exige `## Exercícios` aplicados ao contexto do SGCF, seguindo estritamente [formatacao-avancada.md](../blog-posts/references/formatacao-avancada.md).

---

## 2. Metas de Extensão por Tier

- **Tier 1 (Fundacional):** ~3.600 a 4.200 palavras (M01-M03, M07, M13, M26).
- **Tier 2 (Padrão):** ~4.500 a 5.000 palavras (M04-M05, M08-M11, M14-M17, M19, M22, M24-M25, M27-M28).
- **Tier 3 (Alta Densidade):** ~5.400 a 6.500 palavras (M06, M12, M18, M20, M21, M23).

---

## 3. Roteiro sob Demanda

O roteiro completo dos 28 módulos está em [references/roteiro.md](references/roteiro.md).

> [!TIP] Eficiência de Tokens e Anti-Bleed
> **Não leia o roteiro inteiro.** Inspecione apenas o intervalo de linhas do Módulo X em `references/roteiro.md` e transforme os tópicos estruturados em prosa fluida (sem copiar listas simétricas `- **Negrito:**` para o texto final).

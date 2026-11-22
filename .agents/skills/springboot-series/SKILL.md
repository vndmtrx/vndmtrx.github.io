---
name: springboot-series
description: >
  Convenções, metadados, stack e roteiro da série "Spring Boot Tutorial" (17 partes, tarefas-api) no blog vndmtrx.github.io. Ative ao escrever, rascunhar ou revisar posts desta série.
---

# Skill: Série Spring Boot Tutorial

Herda integralmente voz, antipadrões, ritmo, invariantes e validação (`scripts/lint_post.py`) de [blog-posts](../blog-posts/SKILL.md).

---

## 1. Convenções da Série

- **Front Matter Obrigatório:**
  ```yaml
  category: Tutoriais
  series: Spring Boot Tutorial
  title: "Spring Boot Tutorial, Parte X - [Tema]"
  subtitle: "[Tagline técnica marcante]"
  tags: [Spring Boot, Java, Backend, DevOps, Infraestrutura, Arquitetura]
  ```
- **Trilha e Repositório:** Página em `tutoriais/spring-boot.md` (`/tutoriais/spring-boot/`), metadados em `_data/series.yml` e código por capítulo (`capitulo-02/`, `capitulo-03/`, ...) em [vndmtrx/estudos_springboot](https://github.com/vndmtrx/estudos_springboot).
- **Callout de Abertura (na introdução, antes do primeiro `##`):**
  ```markdown
  > [!NOTE] Nota da Série
  > Este post faz parte da série **"Spring Boot Tutorial"**, onde construímos do zero uma API backend de produção com **Spring Boot**, explorando boas práticas de arquitetura, contratos, persistência, resiliência, observabilidade e nuvem. O código-fonte de apoio e os projetos de cada capítulo estão organizados no repositório parceiro [vndmtrx/estudos_springboot](https://github.com/vndmtrx/estudos_springboot).
  ```
- **Override de Exercícios (Obrigatório):** Posts práticos da série incluem `## Exercícios` com desafios de código e testes na `tarefas-api`, seguindo [formatacao-avancada.md](../blog-posts/references/formatacao-avancada.md).

---

## 2. Roteiro sob Demanda

O roteiro das 17 partes está em [references/roteiro.md](references/roteiro.md).

> [!TIP] Eficiência de Tokens e Anti-Bleed
> **Não leia o roteiro inteiro.** Inspecione apenas o intervalo de linhas da Parte X em `references/roteiro.md` e converta os tópicos do roteiro em prosa fluida (sem copiar listas simétricas `- **Negrito:**` para o post).

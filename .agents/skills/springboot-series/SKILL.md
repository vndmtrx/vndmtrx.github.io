---
name: springboot-series
description: >
  Convenções, metadados e stack para a série "Spring Boot Tutorial" do blog vndmtrx.github.io. Use quando o usuário pedir para escrever, rascunhar ou revisar posts especificamente desta série.
---

# Skill: Série Spring Boot Tutorial

Diretrizes técnicas e convenções para os posts da série **Spring Boot Tutorial** (`tarefas-api`) no blog `vndmtrx.github.io`.

---

## 1. Convenções Editoriais da Série

- **Front Matter Obrigatório:**
  ```yaml
  category: Tutoriais
  series: Spring Boot Tutorial
  title: "Spring Boot Tutorial, Parte X - [Tema]"
  subtitle: "[Tagline técnica marcante]"
  tags: [Spring Boot, Java, Backend, DevOps, Infraestrutura, Arquitetura]
  ```
- **Página de Coleção / Trilha:** Cadastrada em `tutoriais/spring-boot.md` (`/tutoriais/spring-boot/`) e metadados centralizados em `_data/series.yml`.
- **Repositório Parceiro:** `[vndmtrx/estudos_springboot](https://github.com/vndmtrx/estudos_springboot)` organizado por capítulos (`capitulo-02/`, `capitulo-03/`, etc.).
- **Callout de Abertura:**
  ```markdown
  > [!NOTE] Nota da Série
  > Este post faz parte da série **"Spring Boot Tutorial"**, onde construímos do zero uma API backend de produção com **Spring Boot**, explorando boas práticas de arquitetura, contratos, persistência, resiliência, observabilidade e nuvem. O código-fonte de apoio e os projetos de cada capítulo estão organizados no repositório parceiro [vndmtrx/estudos_springboot](https://github.com/vndmtrx/estudos_springboot).
  ```

---

## 2. Roteiro e Ementa sob Demanda

O roteiro completo com as 17 partes está em [references/roteiro.md](references/roteiro.md).

> [!TIP] Eficiência de Tokens
> **NÃO leia o roteiro inteiro.** Ao trabalhar no capítulo X, inspecione exclusivamente a seção da Parte X em `references/roteiro.md` utilizando `view_file` com `StartLine` e `EndLine`.

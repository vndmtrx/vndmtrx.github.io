---
name: k8sbox-series
description: >
  Convenções, metadados e roteiro da série "Kubernetes in a Box" (25 posts, Kubernetes the hard way com Ansible) no blog vndmtrx.github.io. Ative ao escrever, rascunhar ou revisar posts desta série.
---

# Skill: Série Kubernetes in a Box

Herda integralmente voz, antipadrões, ritmo, invariantes e validação (`scripts/lint_post.py`) de [blog-posts](../blog-posts/SKILL.md). Baseada no repositório parceiro [vndmtrx/k8s-in-a-box](https://github.com/vndmtrx/k8s-in-a-box).

---

## 1. Convenções da Série

- **Front Matter Obrigatório:**
  ```yaml
  category: Tutoriais
  series: Kubernetes in a Box
  title: "Kubernetes in a Box, Parte X - [Tema]"
  subtitle: "[Tagline técnica sobre o componente abordado]"
  tags: [Kubernetes, Ansible, DevOps, Infraestrutura, Linux]
  ```
- **Seção de Diagnóstico Obrigatória:** Todo post exige `## Diagnóstico e Troubleshooting` com comandos reais de validação (`etcdctl`, `kubectl`, `crictl`, `openssl`, `sysctl`).
- **Sem Exercícios:** Esta série **não** usa `## Exercícios`. A fixação prática acontece em `## Diagnóstico e Troubleshooting` e no laboratório em `vndmtrx/k8s-in-a-box`.
- **Repositório Parceiro:** Referencie sempre as tasks/roles Ansible correspondentes na branch principal de `vndmtrx/k8s-in-a-box`.

---

## 2. Roteiro sob Demanda

O roteiro dos 25 posts (Cluster Base, Integração, Operações e Extras) está em [references/roteiro.md](references/roteiro.md).

> [!TIP] Eficiência de Tokens e Anti-Bleed
> **Não leia o roteiro inteiro.** Inspecione apenas o intervalo de linhas da Parte X em `references/roteiro.md` e converta os tópicos do roteiro em narrativa técnica (sem copiar listas simétricas para o post).

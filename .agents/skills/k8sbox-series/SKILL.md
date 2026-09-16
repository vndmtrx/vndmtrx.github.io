---
name: k8sbox-series
description: >
  Convenções, metadados e diretrizes da série "Kubernetes in a Box" (24 posts) do blog vndmtrx.github.io. Use quando o usuário pedir para escrever, rascunhar ou revisar posts desta série sobre infraestrutura e Kubernetes the hard way.
---

# Skill: Série Kubernetes in a Box

Diretrizes técnicas e estruturais para os posts da série **Kubernetes in a Box**, baseada no repositório parceiro [vndmtrx/k8s-in-a-box](https://github.com/vndmtrx/k8s-in-a-box).

---

## 1. Convenções Editoriais da Série

- **Front Matter Obrigatório:**
  ```yaml
  category: Tutoriais
  series: Kubernetes in a Box
  title: "Kubernetes in a Box, Parte X - [Tema]"
  subtitle: "[Tagline técnica sobre o componente abordado]"
  tags: [Kubernetes, Ansible, DevOps, Infraestrutura, Linux]
  ```
- **Seção de Diagnóstico Obrigatória:** Todo post deve conter uma seção `## Diagnóstico e Troubleshooting` com comandos reais de validação (`etcdctl`, `kubectl`, `crictl`, `openssl`, `sysctl`).
- **Repositório Parceiro:** Referenciar tasks/roles Ansible correspondentes em `vndmtrx/k8s-in-a-box`.

---

## 2. Roteiro e Ementa sob Demanda

O roteiro detalhado dos 24 posts (Cluster Base, Integração, Operações e Extras) está em [references/roteiro.md](references/roteiro.md).

> [!TIP] Eficiência de Tokens
> **NÃO leia o roteiro inteiro.** Ao redigir ou revisar a Parte X, consulte exclusivamente o bloco da Parte X em `references/roteiro.md` utilizando `view_file` com slice de linhas (`StartLine`/`EndLine`).

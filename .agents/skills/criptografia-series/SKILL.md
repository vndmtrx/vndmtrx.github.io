---
name: criptografia-series
description: >
  Convenções, metadados, elenco, roteiro e catálogo de referências da série "Criptografia na Prática" (PKI/X.509 com OpenSSL, OpenPGP/GnuPG) no blog vndmtrx.github.io. Ative ao escrever, rascunhar ou revisar posts desta série.
---

# Skill: Série Criptografia na Prática

Herda integralmente voz, antipadrões, ritmo, invariantes e validação (`scripts/lint_post.py`) de [blog-posts](../blog-posts/SKILL.md).

---

## 1. Convenções da Série

- **Front Matter Obrigatório:**
  ```yaml
  category: Tutoriais
  series: Criptografia na Prática
  tags: [Criptografia, Segurança, ...] # 2 a 6 tags, sempre incluindo Criptografia e Segurança
  mermaid: true # Trilogia PKI utiliza diagramas Mermaid
  ```
- **Override de Exercícios (Obrigatório):** Todo post exige `## Exercícios` imediatamente antes de `## Conclusão`, no padrão de [formatacao-avancada.md](../blog-posts/references/formatacao-avancada.md).
- **Seção de Diagnóstico Obrigatória:** Incluir `## Diagnóstico e Troubleshooting` com comandos reais (`openssl`, `gpg`, `gpgsm`, `ssh-keygen -L`, `curl -v`).
- **Fio Comparativo Contínuo:** Manter ao menos um ponto de comparação explícito com Certificados SSH (via `` {% include post-ref.html slug="certificados-ssh" %} ``) e ganchos para a teia de confiança do OpenPGP.
- **Elenco e Cenário Fixos:** João (dev), Maria (DBA), Antônio (QA / pentester curioso, quem tenta e falha ou tem certificado revogado), Carlos (consultor externo com acesso temporário), servidores `php-01` e `db-01`, domínio `example.com`.
- **Saídas de Terminal Reais:** Use exclusivamente saídas validadas em OpenSSL 3.5.x registradas em [references/laboratorio-validado.md](references/laboratorio-validado.md). Nunca invente saídas de terminal.
- **Links Internos Seguros:** Referencie via `post-ref.html` apenas posts já publicados no blog (nunca posts futuros como Partes 5 e 6 do `k8sbox`).

---

## 2. Roteiro e Referências sob Demanda

- **Roteiro dos Posts:** [references/roteiro.md](references/roteiro.md) (leia apenas o intervalo de linhas da parte em questão; converta os tópicos do roteiro em prosa sem copiar listas simétricas).
- **Catálogo de Referências Canônicas:** [references/referencias.md](references/referencias.md) (IDs R01 a R84 com status de validação).
- **Laboratório Validado (OpenSSL 3.5.7):** [references/laboratorio-validado.md](references/laboratorio-validado.md) (configs `openssl.cnf`, chaves, certificados e comandos testados).

---
name: criptografia-series
description: >
  Convenções, metadados, roteiro e catálogo de referências da série "Criptografia na Prática"
  do blog vndmtrx.github.io (PKI/X.509 com OpenSSL, OpenPGP/GnuPG e afins). Use quando o usuário
  pedir para escrever, rascunhar ou revisar posts desta série.
---

# Skill: Série Criptografia na Prática

Diretrizes técnicas, convenções editoriais e estrutura de referência para os posts da série **Criptografia na Prática**.

---

## 1. Convenções Editoriais da Série

- **Front Matter Obrigatório:**
  ```yaml
  category: Tutoriais
  series: Criptografia na Prática
  tags: [Criptografia, Segurança, ...] # 2 a 6 tags, sempre incluindo Criptografia e Segurança
  mermaid: true # Todos os posts da trilogia PKI utilizam diagramas Mermaid
  ```
- **Override de Exercícios:** Esta série EXIGE a seção `## Exercícios` (no formato padrão documentado em `blog-posts/references/formatacao-avancada.md`), posicionada imediatamente antes de `## Conclusão`.
- **Seção de Diagnóstico Obrigatória:** Todo post deve conter uma seção `## Diagnóstico e Troubleshooting` com comandos reais e opções do ecossistema (`openssl`, `gpg`, `gpgsm`, `ssh-keygen -L`, `curl -v`).
- **Fio Comparativo Contínuo:** Todo post deve ter ao menos um ponto de comparação explícito com Certificados SSH (post {% raw %}{% include post-ref.html slug="certificados-ssh" %}{% endraw %}) e ganchos/pontes para a teia de confiança do OpenPGP.
- **Elenco e Cenário Fixos:** João (dev), Maria (DBA), Antônio (QA / pentester curioso, o que tenta e falha / tem certificado revogado), Carlos (consultor externo com acesso temporário), servidores `php-01` e `db-01`, domínio corporativo fictício `example.com`.
- **Saídas de Terminal Reais:** Usar estritamente saídas reais validadas no ambiente local com OpenSSL 3.5.x, catalogadas em [references/laboratorio-validado.md](references/laboratorio-validado.md). NUNCA inventar ou alucinar saídas de terminal.
- **Links Internos Seguros:** Nunca criar links internos via `post-ref.html` para posts que ainda não foram publicados (como as Partes 5 e 6 do `k8sbox`). O roteiro do `k8sbox` aponta para cá; esta trilogia só aponta para posts já existentes no blog.

---

## 2. Roteiro e Referências sob Demanda

- **Roteiro dos Posts:** Consulte [references/roteiro.md](references/roteiro.md) (leia SOMENTE o bloco da parte em questão com slice de linhas).
- **Catálogo de Referências Canônicas:** Consulte [references/referencias.md](references/referencias.md) (IDs R01 a R84 com status de validação).
- **Laboratório Validado (OpenSSL 3.5.7):** Consulte [references/laboratorio-validado.md](references/laboratorio-validado.md) para configs `openssl.cnf`, chaves, certificados e comandos testados na prática.

# Segurança Defensiva e POLP (*Principle of Least Privilege*)

Critérios fundamentais de integridade, controle de acesso e delimitação de superfície de ataque.

---

## ⚫ Acusação (Chapéu Preto - O Auditor Metódico)
* **Fronteiras Não Confiáveis:** Aceitação de dados ou instruções externas sem validação estrita na borda do sistema.
* **Privilégios Excessivos (Violação de POLP):** Componentes ou processos operando com permissões, capacidades ou acessos superiores ao estritamente necessário para sua função.
* **Exposição de Informações Sensíveis:** Vazamento de credenciais, dados protegidos ou estados internos confidenciais em canais inseguros ou registros de execução.
* **Ausência de Limites de Proteção:** Vulnerabilidade a esgotamento de recursos, operações descontroladas ou abuso operacional.

---

## 🟢 Resolução (Chapéu Verde)
* Validação rigorosa e sanitização em todas as fronteiras de entrada com tipos seguros e contratos explícitos.
* Isolamento e concessão estrita do menor escopo operacional viável por padrão (*Least Privilege*).
* Proteção, externalização e não-exposição de credenciais e dados sensíveis em artefatos rastreáveis.
* Definição de limites formais de tempo, volume e consumo para conter anomalias e falhas em cascata.

---

## 🔵 Veredito (Chapéu Azul)
* Violações que exponham dados confidenciais ou permitam quebra de integridade operacional não admitem tolerância a débito:
  - Voto obrigatório: **`[VETADO: brecha de segurança ou violação de privilégio com mitigação mandatória]`**.

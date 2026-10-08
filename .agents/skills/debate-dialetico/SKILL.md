---
name: debate-dialetico
description: >-
  Deliberação dialética e teste de estresse de decisões/código baseada nos Seis Chapéus do Pensamento
  (Edward de Bono) e Posturas Críticas (OCEAN/Big Five). Use esta skill quando o usuário solicitar
  explicitamente um debate dialético, contraditório formal, teste de estresse de ideias/código,
  ou avaliação pelos Seis Chapéus. Não ative para tarefas comuns de edição de código ou dúvidas triviais.
---

# Skill: Debate Dialético (Seis Chapéus & Posturas Críticas)

Metodologia deliberativa em dois níveis com contraditório calibrado por posturas críticas.

---

## 1. Modos de Operação

* **Nível 1: Tríade Ágil (90% do tempo):** `⚪ Branco (Fatos)` + `⚫ Preto (Riscos)` ➔ `🔵 Azul (Juiz/Veredito)`.
* **Nível 2: Plenário dos Seis Chapéus (Decisões Críticas):** Convocação completa (`⚪ Fatos`, `⚫ Riscos`, `🟡 Ganhos/ROI`, `🟢 Alternativas`, `🔴 DX/UX` e `🔵 Síntese`).
  * Detalhamento dos chapéus em [refs/seis-chapeus.md](refs/seis-chapeus.md).
* **Sequências Táticas:** [Ideação, Alternativas, Feedback Rápido, Incidentes, Estratégia, Processos](refs/programas-sequencias.md).
* **Gatilhos de Intenção Naturais:**
  * *"me dê alternativas", "qual escolher?"* ➔ Sequência [Escolha entre Alternativas](refs/programas-sequencias.md).
  * *"debugue esse erro", "incidente", "post-mortem"* ➔ Sequência [Solução de Problemas / Incidentes](refs/programas-sequencias.md).
  * *"revisão rápida", "o que acha?", "pente fino"* ➔ Sequência [Feedback Rápido](refs/programas-sequencias.md) ou Tríade Ágil.
  * *"ideias para", "como conceber do zero?"* ➔ Sequência [Ideação Inicial](refs/programas-sequencias.md).

---

## 2. Catálogo de Posturas Críticas

O Chapéu Azul escolhe autonomamente a postura conforme o domínio técnico (ou adota o padrão *Auditor Metódico + Pragmatista* se genérico). Os resumos abaixo são autossuficientes para deliberação imediata; acesse os arquivos de referência apenas se houver ambiguidade crítica ou solicitação expressa de aprofundamento:

* 🛡️ [Guardião do Status Quo](refs/posturas/status-quo.md): Preservação de estabilidade comprovada e aversão ao risco de regressão.
* 🔍 [Auditor Metódico](refs/posturas/auditor-metodico.md): Verificação empírica, estabilidade de contratos e cobertura de cenários de falha.
* ⚡ [Pragmatista](refs/posturas/pragmatista.md): Navalha de Occam, simplicidade de primeira ordem e eliminação de esforço desperdiçado.
* 🚀 [Inovador Radical](refs/posturas/inovador-radical.md): Superação de paradigmas obsoletos e viabilização de evolução arquitetural futura.
* 🐧 [Sysadmin de Bare-Metal](refs/posturas/sysadmin-bare-metal.md): Autonomia operacional, resiliência de baixo nível e controle sobre recursos físicos.
* ☁️ [Arquiteto Cloud-Native](refs/posturas/arquiteto-cloud-native.md): Escalabilidade elástica, processos descartáveis e desacoplamento de infraestrutura.
* 🏛️ [Auditor Público](refs/posturas/auditor-publico.md): Conformidade regulatória, auditabilidade irrevogável e governança formal de dados.
* 🧠 [Cético de IA](refs/posturas/cetico-ia.md): Priorização de abordagens determinísticas e econômicas sobre inferência probabilística.
* 📖 [Redator Didático](refs/posturas/redator-didatico.md): Clareza conceitual, ergonomia cognitiva e redução do atrito de manutenção (DX).
* 👤 [Usuário do Mundo Real](refs/posturas/usuario-mundo-real.md): Usabilidade intuitiva, tolerância a erros e acessibilidade universal (UX).

*Heurísticas de engenharia:* [DRY](refs/principios/dry-vs-aha.md) | [KISS/YAGNI](refs/principios/kiss-e-yagni.md) | [SOLID](refs/principios/solid.md) | [12-Factor](refs/principios/12-factor.md) | [Segurança/POLP](refs/principios/seguranca-polp.md).

---

## 3. Diretrizes e Veredito

1. **Anti-Teatralização e Densidade:** Zero drama, sem personas de RPG. Resposta direta em tópicos técnicos.
2. **Anti-Sycophancy:** Foco estrito em arestas, vulnerabilidades e débitos técnicos. Proibido validar por complacência.
3. **Formato Obrigatório de Voto:** Abrir manifestações com uma das taxonomias:
   * `[APROVADO: justificativa curta]`
   * `[APROVADO COM RESSALVAS: mitigações obrigatórias]`
   * `[REPROVADO: inconsistência ou falha conceitual]`
   * `[VETADO: brecha de segurança ou risco crítico]`

---

## 4. Circuit Breakers (Anti-Looping)

1. **Budget de Coleta (Default = 3):** Máximo de 3 tentativas semânticas para achar dados (customizável no prompt). Erros de sintaxe de comando não contam no teto.
2. **Escalação HITL:** Ao esgotar o budget, interrompe o debate e emite `[ESCALAÇÃO HITL]` solicitando o caminho ou comando ao usuário.
3. **Single-Pass e Terminalidade:** Deliberação em rodada única sequencial (`Branco -> Preto -> Azul`). O Chapéu Azul encerra com veredito; em caso de empate, aplica desempate conservador (`[APROVADO COM RESSALVAS]` ou `[REPROVADO]`).
4. **Anti-Hiperfoco e Retorno Decrescente:** Interrompa a análise no momento em que detalhes adicionais não alterarem o veredito prático ou quando o custo analítico superar o valor da decisão (noção de prejuízo/ROI analítico). Priorize soluções pragmáticas e acionáveis sobre minúcias teóricas.

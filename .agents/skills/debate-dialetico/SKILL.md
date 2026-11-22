---
name: debate-dialetico
description: >-
  Deliberação dialética e teste de estresse de decisões ou código via Seis Chapéus do Pensamento
  (Edward de Bono) e Posturas Críticas (OCEAN/Big Five). Ative apenas quando o usuário pedir
  explicitamente debate dialético, contraditório formal, teste de estresse ou avaliação pelos Seis Chapéus.
  Não ative para edições comuns de código ou dúvidas triviais.
---

# Skill: Debate Dialético (Seis Chapéus & Posturas Críticas)

Deliberação técnica em rodada única com contraditório calibrado por posturas críticas e saída compacta.

---

## 1. Modos de Operação

- **Nível 1 (Padrão, 90% dos casos) — Tríade Ágil:** `⚪ Branco (Fatos)` -> `⚫ Preto (Riscos)` -> `🔵 Azul (Veredito)`.
- **Nível 2 (Decisões Críticas) — Plenário Completo:** `⚪ Fatos`, `⚫ Riscos`, `🟡 Ganhos/ROI`, `🟢 Alternativas`, `🔴 DX/UX`, `🔵 Síntese`. Detalhamento sob demanda em [refs/seis-chapeus.md](refs/seis-chapeus.md).
- **Sequências Táticas (com a skill já ativa):** selecione a sequência em [refs/programas-sequencias.md](refs/programas-sequencias.md) conforme o objetivo do pedido:
  - Comparação/escolha de alternativas -> *Escolha entre Alternativas*.
  - Diagnóstico de falha/incidente/post-mortem -> *Solução de Problemas / Incidentes*.
  - Pente-fino pontual -> *Feedback Rápido* ou *Tríade Ágil*.
  - Concepção do zero -> *Ideação Inicial*.

---

## 2. Catálogo de Posturas Críticas

O Chapéu Azul escolhe a postura pelo domínio técnico (padrão genérico: *Auditor Metódico + Pragmatista*). Os resumos de 1 linha abaixo bastam para deliberar; abra o arquivo em `refs/` apenas diante de ambiguidade crítica ou pedido expresso:

- 🛡️ [Guardião do Status Quo](refs/posturas/status-quo.md): Estabilidade comprovada e aversão a risco de regressão.
- 🔍 [Auditor Metódico](refs/posturas/auditor-metodico.md): Verificação empírica, contratos estáveis e cobertura de cenários de falha.
- ⚡ [Pragmatista](refs/posturas/pragmatista.md): Navalha de Occam, simplicidade de primeira ordem e corte de esforço desperdiçado.
- 🚀 [Inovador Radical](refs/posturas/inovador-radical.md): Superação de paradigmas obsoletos e evolução arquitetural.
- 🐧 [Sysadmin de Bare-Metal](refs/posturas/sysadmin-bare-metal.md): Autonomia operacional, resiliência de baixo nível e controle sobre recursos físicos.
- ☁️ [Arquiteto Cloud-Native](refs/posturas/arquiteto-cloud-native.md): Escalabilidade elástica, processos descartáveis e desacoplamento de infra.
- 🏛️ [Auditor Público](refs/posturas/auditor-publico.md): Conformidade regulatória, auditabilidade e governança formal de dados.
- 🧠 [Cético de IA](refs/posturas/cetico-ia.md): Soluções determinísticas e econômicas acima de inferência probabilística.
- 📖 [Redator Didático](refs/posturas/redator-didatico.md): Clareza conceitual, ergonomia cognitiva e baixo atrito de manutenção (DX).
- 👤 [Usuário do Mundo Real](refs/posturas/usuario-mundo-real.md): Usabilidade intuitiva, tolerância a erros e acessibilidade (UX).

*Heurísticas sob demanda:* [DRY](refs/principios/dry-vs-aha.md) | [KISS/YAGNI](refs/principios/kiss-e-yagni.md) | [SOLID](refs/principios/solid.md) | [12-Factor](refs/principios/12-factor.md) | [Segurança/POLP](refs/principios/seguranca-polp.md).

---

## 3. Formato de Saída, Rigor e Veredito

1. **Zero Preâmbulo e Alta Densidade:** Em vez de introduções teatrais ou personas de RPG, abra direto no primeiro chapéu usando **2 a 4 bullets objetivos por chapéu** (foco em evidência, causa raiz e ação).
2. **Anti-Sycophancy:** Em vez de validar por complacência, ataque arestas reais, vulnerabilidades e débitos técnicos; só aprove quando os riscos estiverem mitigados.
3. **Esqueleto Obrigatório de Saída (Tríade Ágil):**
   ```markdown
   **⚪ Branco (Fatos):**
   - [Evidência ou restrição verificável]

   **⚫ Preto ([Postura]):**
   - [Risco concreto + mecanismo de falha]

   **🔵 Azul (Veredito):** `[APROVADO | APROVADO COM RESSALVAS | REPROVADO | VETADO]: justificativa curta`
   - **Próxima ação:** [Passo executável único e direto]
   ```

---

## 4. Circuit Breakers (Anti-Looping)

1. **Budget de Coleta (Default = 3):** Máximo de 3 buscas semânticas para coletar fatos (customizável no prompt); erros de sintaxe de comando não consomem budget.
2. **Escalação HITL:** Esgotado o budget, interrompa e emita `[ESCALAÇÃO HITL]` pedindo o caminho ou comando ao usuário.
3. **Single-Pass e Terminalidade:** Deliberação em rodada única (`Branco -> Preto -> Azul`). Em empate, o Azul aplica desempate conservador (`[APROVADO COM RESSALVAS]` ou `[REPROVADO]`).
4. **Retorno Decrescente:** Encerre a análise assim que detalhes extras não alterarem o veredito prático ou o custo analítico superar o valor da decisão.

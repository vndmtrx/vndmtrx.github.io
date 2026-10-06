# 12-Factor (Arquitetura Desacoplada e Escalável)

Auditoria de conformidade com ambientes dinâmicos, descartabilidade de processos e escalabilidade elástica.

---

## ⚫ Acusação (Chapéu Preto - O Auditor Metódico & Sysadmin)
* **Acoplamento a Ambiente:** Configurações ou endereçamentos fixos incorporados ao artefato em vez de injetados dinamicamente pelo ambiente de execução.
* **Persistência Volátil Imprópria:** Processos retendo estado local que impeça replicação concorrente ou recuperação transparente de falhas.
* **Encerramento Não-Gracioso:** Ausência de tratamento de sinais de encerramento, gerando interrupções abruptas e corrupção de operações em andamento.
* **Gerenciamento Local de Registros:** Tentativa de controlar rotação ou armazenamento de logs internamente, em vez de tratá-los como fluxo contínuo de eventos.
* **Divergência entre Ambientes:** Diferenças estruturais relevantes entre o contexto de validação e o contexto real de operação.

---

## 🟢 Resolução (Chapéu Verde)
* Externalização completa de parâmetros operacionais para injeção via ambiente.
* Transformação de processos em unidades descartáveis e stateless, delegando estado durável a serviços persistentes desacoplados.
* Implementação de encerramento gracioso para finalizar trabalhos pendentes com segurança.
* Emissão de registros estruturados em fluxos padronizados de saída.

---

## 🔵 Veredito (Chapéu Azul)
* Violações que impeçam replicação elástica ou automação de ciclo de vida:
  - Voto de referência: `[APROVADO COM RESSALVAS: desacoplar parâmetros de ambiente e estado volátil antes da homologação final]`.

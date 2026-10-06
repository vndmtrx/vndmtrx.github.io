# Postura: O Arquiteto Cloud-Native

* **Perfil OCEAN:** `Abertura: Alta | Conscienciosidade: Moderada | Alavancagem: Alta`
* **Foco:** Escalabilidade elástica, processos descartáveis, descentralização e aproveitamento de serviços especializados.

---

## Vetores de Ataque no Chapéu Preto (Exemplos)
* *"Essa solução escala horizontalmente sob demanda ou depende de gargalos centralizados e nós únicos?"*
* *"Estamos gastando esforço para gerenciar infraestrutura operacional em vez de focar no valor do negócio?"*
* *"Como a arquitetura se comporta perante a falha inevitável de componentes individuais distribuídos?"*
* *"O estado da aplicação é desacoplado do ciclo de vida dos processos de execução?"*

---

## Gatilho de Veto Imediato
* Acoplamento rígido a estado volátil local ou dependência de pontos únicos de falha que inviabilizem redundância, escalabilidade e recuperação automática.

## Critério de Pacificação (Aprovação)
* Processos desacoplados e efêmeros, configuração externalizada, resiliência projetada para falhas parciais e observabilidade integrada.

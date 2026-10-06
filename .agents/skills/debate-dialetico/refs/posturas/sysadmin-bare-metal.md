# Postura: O Sysadmin de Bare-Metal

* **Perfil OCEAN:** `Abertura: Baixa | Conscienciosidade: Máxima | Risco: Averso | Foco: Baixo Nível`
* **Foco:** Autonomia operacional, resiliência de baixo nível, controle sobre recursos físicos e facilidade de diagnóstico sob estresse.

---

## Vetores de Ataque no Chapéu Preto (Exemplos)
* *"Qual é o comportamento do sistema quando recursos fundamentais (memória, armazenamento, I/O) se esgotarem?"*
* *"A solução consegue operar e ser diagnosticada autonomamente sem depender de intermediários ou plataformas externas?"*
* *"O estado interno e as falhas são inspecionáveis diretamente por ferramentas nativas em caso de emergência?"*
* *"Como o sistema se recupera de interrupções abruptas ou reinicializações não planejadas?"*

---

## Gatilho de Veto Imediato
* Dependência mandatória de camadas opacas para diagnóstico básico, ausência de limites explícitos de consumo de recursos ou falha catastrófica silenciosa sob contenção.

## Critério de Pacificação (Aprovação)
* Comportamento determinístico e delimitado de consumo de recursos, rastreabilidade operacional direta e capacidade comprovada de sobrevivência a falhas de ambiente.

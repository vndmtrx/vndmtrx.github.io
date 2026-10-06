# DRY (*Don't Repeat Yourself*) vs. AHA (*Avoid Hasty Abstractions*)

O princípio DRY visa eliminar a duplicação de **conhecimento e regras essenciais de domínio**, enquanto AHA alerta contra o acoplamento artificial gerado por abstrações prematuras.

---

## ⚫ Acusação (Chapéu Preto - O Auditor Metódico)
* **Onde ataca:** Identifica duplicação de regras essenciais de negócio e invariantes de domínio.
* **Risco apontado:** Divergência silenciosa de comportamento quando uma das instâncias for alterada e a outra esquecida.

---

## ⚫ Contraditório Pragmático (Chapéu Preto - O Pragmatista)
* **Onde ataca:** Identifica abstrações apressadas criadas para evitar mera repetição incidental de estrutura.
* **Risco apontado:** Acoplamento artificial entre contextos independentes que compartilham formato semelhante por coincidência (*"Duplicação é muito mais barata que a abstração errada"*).
* **Regra de Julgamento:** Aplica a **Regra dos Três** (tolerar repetições locais até que a convergência semântica seja indubitável).

---

## 🟢 Resolução (Chapéu Verde)
* Propõe unificação em contratos limpos onde há identidade conceitual real, ou preservação consciente de independência onde os ciclos de vida forem distintos.

---

## 🔵 Diretriz de Veredito (Chapéu Azul)
* **Inconsistência em regras de domínio essenciais:** `[REPROVADO: risco de divergência comportamental; unificar fonte da verdade]`.
* **Semelhança estrutural isolada entre fluxos independentes:** `[APROVADO: tolerar repetição local para evitar acoplamento prematuro]`.

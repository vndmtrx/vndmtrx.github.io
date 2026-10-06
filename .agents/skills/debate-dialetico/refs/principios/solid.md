# Princípios SOLID (Design Modular e Extensibilidade)

Auditoria estrutural de acoplamento, responsabilidade e estabilidade de contratos.

---

## Matriz Dialética dos 5 Princípios

| Princípio | Acusação do Chapéu Preto (Onde ataca) | Proposta do Chapéu Verde (Como resolve) |
| :--- | :--- | :--- |
| **SRP** *(Single Responsibility)* | Módulos acumulando múltiplos eixos de mudança (regras, persistência, apresentação). | Quebra em componentes coesos com responsabilidade única bem definida. |
| **OCP** *(Open/Closed)* | Necessidade de alterar código consolidado a cada novo requisito incorporado. | Extensão por composição, parametrização ou contratos plugáveis. |
| **LSP** *(Liskov Substitution)* | Especializações que alteram pressupostos ou quebram garantias do contrato base. | Substituição de acoplamento rígido por composição de comportamentos. |
| **ISP** *(Interface Segregation)* | Contratos sobrecarregados que impõem dependências desnecessárias aos consumidores. | Segregação em interfaces granulares e orientadas ao uso estrito de quem consome. |
| **DIP** *(Dependency Inversion)* | Lógica central acoplada diretamente a detalhes voláteis de infraestrutura ou I/O. | Inversão de controle via contratos abstratos estáveis. |

---

## 🔵 Diretriz de Veredito (Chapéu Azul)
* **Violação estrutural que comprometa integridade de contratos ou testabilidade:** `[REPROVADO: segregar responsabilidades ou desacoplar dependências]`.
* **Modularidade coesa com contratos estáveis e baixo acoplamento:** `[APROVADO: design modular e sustentável]`.

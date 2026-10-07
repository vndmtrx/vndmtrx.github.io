# Catálogo dos Seis Chapéus do Pensamento (Edward de Bono)

Os chapéus definem **modos de raciocínio temporários e neutros**. Nenhuma persona "é" um chapéu; qualquer agente calça e descalça o chapéu sob demanda do Juiz (Chapéu Azul).

---

## ⚪ Chapéu Branco (Fatos, Dados e Ground Truth)
* **Função:** Extrair a realidade factual estrita, restrições e dados observáveis sem interpretação subjetiva.
* **Vetores de Análise (Exemplos):**
  - Quais são as métricas, evidências e dados observáveis comprovados no estado atual?
  - Quais restrições de arquitetura, contratos e versões são fatos formalmente verificados?
  - Quais informações vitais ainda estão ausentes antes que uma decisão fundamentada possa ser tomada?
* **Regra estrita:** Proibido propor soluções ou julgar riscos; relata exclusivamente evidências literais, dados brutos e fatos verificáveis.

---

## ⚫ Chapéu Preto (O Contraditório / Riscos e Cautela)
* **Função:** Promotor do teste de estresse. Caçar vulnerabilidades, falhas conceituais e cenários de quebra.
* **Vetores de Análise (Exemplos):**
  - Onde e sob quais condições de estresse, carga ou casos limítrofes essa solução vai falhar?
  - Quais são as dependências frágeis, pontos únicos de falha e superfícies de risco introduzidas?
  - Qual é o custo oculto de manutenção, débito técnico e complexidade acumulada?
* **Regra estrita:** Críticas devem ser fundamentadas em causalidade técnica e evidências, nunca mero pessimismo retórico.

---

## 🟡 Chapéu Amarelo (Otimismo Lógico e Valor Agregado)
* **Função:** Identificar o melhor cenário, os ganhos reais de produtividade e o retorno sobre o investimento (ROI).
* **Vetores de Análise (Exemplos):**
  - Quais são os benefícios diretos e mensuráveis em eficiência, estabilidade ou clareza?
  - Como essa abordagem simplifica o ecossistema ou economiza esforço operacional contínuo?
  - Qual é a proposta de valor que justifica o custo de implementação e adoção?
* **Regra estrita:** Otimismo obrigatoriamente justificado; proibido validações complacentes ou elogios vagos sem comprovação.

---

## 🟢 Chapéu Verde (Criatividade, Alternativas e Refatoração Lateral)
* **Função:** Pensar fora da caixa, propor alternativas mais simples e refatorações pragmáticas.
* **Vetores de Análise (Exemplos):**
  - Existe forma de resolver a maior parte desse problema com uma fração do esforço/código proposto?
  - Se descartássemos a abordagem atual, qual seria a alternativa lateral mais elegante?
  - Como podemos recombinar recursos já disponíveis sem adicionar dependências externas?
* **Regra estrita:** Proibido propor soluções puramente especulativas; toda alternativa deve ser concreta, aplicável e testável.

---

## 🔴 Chapéu Vermelho (Intuição, Ergonomia e UX / DX)
* **Função:** Capturar o feeling imediato, a intuição visceral e a ergonomia de uso (UX do usuário e DX do desenvolvedor).
* **Vetores de Análise (Exemplos):**
  - A interação é fluida e intuitiva ou causa atrito desnecessário e cospe jargões (UX)?
  - A solução é ergonômica de manter ou exige esforço interpretativo excessivo (DX)?
  - Em situações de anomalia, o comportamento do sistema é compreensível para quem estiver operando?
* **Regra estrita:** Foco estrito em atrito cognitivo e reação intuitiva; não requer justificativa matemática formal.

---

## 🔵 Chapéu Azul (O Juiz / Metaprocesso e Veredito)
* **Função:** Orquestrar o debate, selecionar posturas/programas, cortar hiperfoco e emitir o veredito oficial executável.
* **Vetores de Análise (Exemplos):**
  - Os dados coletados já são suficientes para decidir ou caímos em retornos decrescentes (anti-hiperfoco)?
  - Os riscos apontados pelo Preto superam os ganhos do Amarelo e a simplicidade proposta pelo Verde?
  - Qual é o plano de ação imediato para destravar a implementação com a menor fricção possível?
* **Regra estrita:** Proibido veredito ambíguo; deve fechar com taxonomia obrigatória (`[APROVADO]`, `[APROVADO COM RESSALVAS]`, `[REPROVADO]`, `[VETADO]`).

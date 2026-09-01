---
layout: post
title: "Vinte Minutos para Explicar Meio Século de Aprendizado de Máquina"
subtitle: "Notas de sobrevivência para apresentar aprendizado supervisionado e por reforço sem surtar no palco"
author:
  - "Eduardo N. S. R."
date: 2026-09-01 14:37:00 GMT-3
permalink: /posts/banca-ia-aprendizado-supervisionado/
tags: [Inteligência Artificial, Machine Learning, Algoritmos, Faculdade, Opinião]
---

Botar um cronômetro de vinte minutos na sua frente e ter que explicar aprendizado supervisionado e aprendizado por reforço é um exercício de síntese homérico, na melhor definição que consigo pensar agora (e olha que eu gosto de uma boa dose de masoquismo). Estamos falando de duas áreas monumentais da computação que consumiram décadas de pesquisas, acumularam centenas de variações algorítmicas e hoje sustentam quase tudo o que chamamos de IA moderna.

Na aula dos próximos dias, o passador de slides estará na minha mão. A plateia é a mesma turma que vem acompanhando os seminários da disciplina, e o desafio é passar pelos capítulos 19 e 23 do Russell e Norvig [^1], costurando com os fundamentos clássicos do livro de Sutton e Barto [^2] (que eu mesmo coloquei porque aparentemente não tenho amor à vida), sem parecer um papagaio recitando índices de livros ou um leitor de tela acelerado em duas vezes.

O perigo clássico desse tipo de apresentação é cair na tentação de colocar todas as fórmulas no slide para parecer erudito. O resultado disso todo mundo conhece: o apresentador se perde nos subscritos das matrizes, o tempo estoura no terceiro slide e ninguém na sala consegue pescar o fio da meada.

Para colocar ordem na minha própria cabeça e criar uma bússola de apresentação, organizei estas notas. Elas funcionam como o meu roteiro de estudo e reflexão: a história técnica de como ensinamos máquinas a reconhecer padrões em dados do passado e como damos autonomia para que elas aprendam a agir no futuro.

> [!NOTE] Disclaimer
> Este texto é o meu ensaio pessoal de preparação para a arguição da banca. O foco aqui não é a demonstração formal de teoremas, mas a intuição por trás das decisões de engenharia e os motivos que levaram a comunidade a criar cada uma dessas abordagens.

## O desafio da síntese: escolher as brigas certas

Vinte minutos passam como um estalar de dedos quando você está falando em público. Se você gastar cinco minutos deduzindo uma regressão linear, faltará tempo para explicar por que o Q-Learning se diferencia do SARSA ou como o truque do kernel salvou as máquinas de vetores de suporte.

O segredo de uma apresentação curta não é correr com a fala, mas ter clareza absoluta sobre o papel de cada bloco:

1. **A base conceitual:** O que é indução estatística e por que o equilíbrio entre viés e variância governa tudo.
2. **O cardápio supervisionado:** Como árvores, modelos lineares, SVMs e comitês de modelos resolvem problemas com dados rotulados.
3. **A virada para o reforço:** Por que a supervisão direta falha em problemas sequenciais e como a interação com o ambiente substitui o professor.
4. **O controle ótimo e a generalização:** Como estimar utilidades no tempo e o que acontece quando colocamos redes neurais dentro do loop de decisão.

Com essa estrutura na cabeça, fica muito mais fácil cortar o excesso de detalhes sem perder a espinha dorsal do assunto.

## O problema da indução: caçando funções no escuro

Todo aprendizado supervisionado parte de uma premissa simples: você tem um conjunto de treino com pares de entrada e saída `(x_i, y_i)`. Alguma regra desconhecida da natureza gerou essas respostas, e o seu objetivo é encontrar uma função candidata `h` (a hipótese) que aproxime essa regra para qualquer dado que aparecer depois.

A primeira bifurcação clássica desse caminho:

* **Classificação:** O objetivo é prever uma categoria discreta (identificar se uma transação bancária é legítima ou fraude, se uma imagem contém um gato ou um cachorro).
* **Regressão:** O objetivo é prever um valor numérico contínuo (estimar o tempo de resposta de um servidor com base na carga, prever o consumo de memória de um processo).

Toda a matemática repousa sobre a suposição de estacionariedade (`i.i.d.`): assume-se que os dados futuros seguirão a mesma distribuição probabilística dos dados passados. No mundo real da infraestrutura e dos sistemas isso é uma meia-verdade constante (o tráfego muda, o perfil dos usuários evolui, o comportamento de ataque se transforma), mas sem essa âncora inicial, nenhum modelo consegue sair do lugar.

### Viés contra variância: o equilíbrio entre a teimosia e o exagero

Qualquer modelo de aprendizado supervisionado vive sob a tensão de duas forças opostas:

* **Viés (*Bias*):** Representa a rigidez do modelo. Se o espaço de hipóteses for limitado demais (como insistir em passar uma linha reta sobre dados que descrevem uma curva acentuada), o modelo falha em capturar o padrão essencial. É o chamado *underfitting*.
* **Variância:** Representa a sensibilidade excessiva aos dados de treino. Se o modelo for flexível demais, ele passa a memorizar o ruído estatístico e as peculiaridades daquela amostra específica. Ele acerta tudo no treino, mas desaba diante de qualquer dado inédito. É o clássico *overfitting*.

A Navalha de Ockham entra aqui como princípio orientador: entre duas explicações que justificam igualmente bem as observações, a mais simples costuma ser a mais confiável para generalizar.

### O papel das perdas e a geometria da regularização

Para calibrar os parâmetros de um modelo, usamos funções de perda. A perda quadrática (`L2`) penaliza desvios grandes com muito mais rigor, sendo a escolha natural quando assumimos ruído Gaussiano. A perda absoluta (`L1`) é mais estável na presença de dados discrepantes (*outliers*), pois não eleva os erros ao quadrado.

Para evitar que os pesos cresçam descontroladamente e gerem sobreajuste, aplicamos técnicas de regularização:

```text
Custo = Perda nos Dados + lambda * Penalidade dos Pesos
```

A escolha da penalidade altera completamente a natureza do modelo:

* **Regularização L1 (Lasso):** Penaliza a magnitude absoluta dos coeficientes. Devido à sua geometria em formato de losango, cujos vértices coincidem com os eixos cartesianos, ela força vários coeficientes a se tornarem exatamente zero durante a otimização. Na prática, funciona como uma seleção automática de variáveis, descartando o que não tem relevância.
* **Regularização L2 (Ridge):** Penaliza o quadrado dos coeficientes. Com sua geometria esférica e suave, ela puxa todos os pesos para valores próximos de zero de maneira uniforme, mas raramente anula qualquer parâmetro por completo.

## Quatro pilares do aprendizado supervisionado

Para cobrir a diversidade de abordagens nos vinte minutos, escolhi quatro famílias conceituais que mostram como a área evoluiu.

### 1. Árvores de decisão e a medida da desordem

Árvores de decisão organizam o espaço de busca como uma sequência hierárquica de testes condicionais. A grande vantagem é a interpretabilidade direta: cada caminho da raiz até a folha pode ser lido como uma regra lógica compreensível.

Para construir a árvore sem testar todas as combinações possíveis (o que seria computacionalmente inviável), usa-se uma estratégia gulosa guiada pela **Entropia de Shannon**, que mede a incerteza dos dados:

```text
H(V) = - somatorio( P(v_k) * log2(P(v_k)) )
```

A cada nó, o algoritmo escolhe a variável que proporciona o maior **Ganho de Informação** (a maior redução líquida de incerteza após a divisão).

Como árvores profundas decoram os dados com facilidade, a poda é essencial. Parar o crescimento antes da hora (*early stopping*) é arriscado porque o algoritmo não enxerga interações complexas entre atributos (em um problema de porta lógica XOR, por exemplo, nenhum atributo sozinho parece informativo no primeiro corte). A melhor prática é deixar a árvore crescer por completo e aplicar a **Poda Chi-quadrado (`chi^2`)** retrospectivamente, eliminando nós cujas divisões não apresentem relevância estatística.

### 2. Modelos lineares: do Perceptron à Regressão Logística

A regressão linear busca o hiperplano que minimiza o erro quadrático médio em relação aos dados. Pode ser calculada de forma exata pela Equação Normal quando a matriz cabe na memória, ou otimizada iterativamente via Gradiente Descendente quando lidamos com grandes volumes de informação.

Na classificação, o **Perceptron** histórico utilizava um limiar rígido: se a combinação linear ultrapassasse zero, a resposta era 1; caso contrário, 0. A limitação é evidente: se os dados não forem perfeitamente separáveis por uma reta, o algoritmo nunca se estabiliza.

A **Regressão Logística** contorna essa fragilidade aplicando a função sigmoide sobre a saída linear:

```text
h(x) = 1 / (1 + e^(-w . x))
```

Em vez de tomar uma decisão binária abrupta, o modelo entrega uma probabilidade contínua e bem calibrada entre 0 e 1. Por ser suave e derivável, sua superfície de custo permite uma otimização convexa e robusta mesmo quando as classes apresentam sobreposição natural.

### 3. Support Vector Machines (SVM) e o salto dimensional

O conceito central das Máquinas de Vetores de Suporte é a busca pela **Margem Máxima**: entre todos os hiperplanos capazes de separar duas classes, o algoritmo escolhe aquele que mantém a maior distância possível em relação aos pontos mais próximos de cada categoria.

Esses pontos críticos que determinam a fronteira são os **vetores de suporte**. Qualquer outro ponto distante da margem pode ser alterado ou removido do conjunto de dados sem afetar a decisão final.

Quando os dados não possuem separação linear no espaço original, entra em cena o **Kernel Trick**: uma formulação matemática fundamentada no Teorema de Mercer que calcula o produto escalar das amostras em um espaço de características de alta dimensão sem precisar projetar os dados explicitamente. É o equivalente a desembolar pontos misturados em uma mesa bidimensional elevando-os em diferentes alturas para conseguir passar um plano reto entre eles.

### 4. Métodos de Ensemble: a força da combinação

Nenhum modelo precisa carregar todo o peso da decisão sozinho. Os métodos de comitê combinam múltiplos aprendizes base para produzir estimativas mais robustas:

* **Bagging:** Treina instâncias do mesmo algoritmo em diferentes amostras aleatórias com reposição (*bootstrapping*) e agrega os votos por maioria ou média. Seu principal efeito é a redução drástica de **variância** em modelos instáveis.
* **Random Forests:** Sofistica o Bagging ao introduzir aleatoriedade também na escolha das variáveis avaliadas a cada divisão de nó (usando tipicamente a raiz quadrada do total de atributos). Isso quebra a correlação entre as árvores da floresta, gerando um conjunto muito mais diverso.
* **Boosting (AdaBoost e Gradient Boosting):** Opera de forma sequencial. Cada novo modelo é construído com foco prioritário nas instâncias que os modelos anteriores classificaram incorretamente. O Gradient Boosting refina essa ideia ajustando os novos modelos diretamente aos resíduos (o gradiente negativo da função de perda), reduzindo progressivamente o **viés**.

## A fronteira: por que o aprendizado por reforço é diferente

Até este ponto, o paradigma foi sempre o mesmo: existia um conjunto de dados anotado, com entradas e respostas corretas fornecidas por um agente externo. O aprendizado supervisionado é essencialmente um processo de inferência passiva sobre amostras prévias.

O **Aprendizado por Reforço (RL)** quebra essa estrutura:

```text
             ┌─────────────────────────┐
             │         Agente          │
             └───────────┬─────────────┘
                         │ Ação (A_t)
                         ▼
             ┌─────────────────────────┐
             │        Ambiente         │
             └───────────┬─────────────┘
                         │ Estado (S_t+1) e Recompensa (R_t+1)
                         ▼
```

Não há um professor dizendo qual era a ação ótima a cada instante. O agente interage ativamente com um mundo estocástico, toma decisões e recebe apenas sinais escalares de **recompensa** ou punição ao longo do tempo.

O problema central passa a ser a **atribuição de crédito temporal**: quando o agente alcança um resultado relevante após centenas de ações consecutivas, como determinar quais decisões intermediárias foram realmente determinantes para aquele desfecho?

Formalizamos esse ambiente através de um **Processo de Decisão de Markov (MDP)**, definido pela quádrupla `(S, A, P, R, gamma)`:
* `S`: Espaço de estados do ambiente.
* `A`: Conjunto de ações disponíveis.
* `P(s' | s, a)`: Dinâmica de transição do mundo.
* `R(s, a, s')`: Função de recompensa imediata.
* `gamma`: Fator de desconto no tempo (entre 0 e 1), que pondera o valor de retornos futuros em relação a ganhos imediatos.

O objetivo do agente é encontrar uma política `pi(s)` que mapeie estados em ações de modo a maximizar o retorno acumulado esperado:

```text
G_t = R_t+1 + gamma * R_t+2 + gamma^2 * R_t+3 + ...
```

## RL Passivo: estimando valores no tempo

Antes de aprender a agir, o agente precisa aprender a avaliar a qualidade dos estados sob uma política fixa `pi`. A literatura clássica divide essa tarefa em três abordagens fundamentais:

```text
Métodos de Avaliação de Políticas
├── Direct Utility Estimation (Monte Carlo puro, sem modelo, sem bootstrapping)
├── Adaptive Dynamic Programming (Model-based, aprende transições P, resolve Bellman)
└── Temporal-Difference TD(0) (Model-free, com bootstrapping local)
```

1. **Direct Utility Estimation (Monte Carlo):** O agente executa trajetórias completas até o estado terminal, soma os retornos observados a partir de cada estado e calcula médias amostrais. O problema é que essa abordagem trata cada estado de forma isolada, ignorando que o valor de um estado está estruturalmente amarrado ao valor de seus sucessores pelas equações de Bellman.
2. **Adaptive Dynamic Programming (ADP):** O agente adota uma postura *model-based*. Ele conta as frequências de transição observadas para construir uma estimativa explícita de `P(s' | s, a)` e resolve o sistema de equações de Bellman por programação dinâmica. É a abordagem com maior eficiência amostral, mas se torna computacionalmente intratável quando o número de estados cresce exponencialmente.
3. **Temporal-Difference Learning (TD(0)):** Proposto por Rich Sutton em 1988, o método TD une o melhor dos dois mundos. Ele dispensa o modelo de transição do ambiente e atualiza a estimativa de utilidade logo no passo seguinte:

```text
U(s) <- U(s) + alpha * [ R + gamma * U(s') - U(s) ]
```

A mágica reside no conceito de **bootstrapping**: o algoritmo usa a sua própria estimativa do estado seguinte `U(s')` para atualizar a estimativa do estado anterior `U(s)`, sem precisar esperar o final do episódio e sem precisar calcular matrizes de transição completas.

## RL Ativo: o controle e o equilíbrio da exploração

Quando o agente precisa escolher ativamente as ações para maximizar o retorno, ele se depara imediatamente com o conflito entre **Exploração** e **Explotação**:

* **Explotação (*Exploitation*):** Escolher a ação que o agente atualmente acredita ser a melhor para garantir recompensas a curto prazo.
* **Exploração (*Exploration*):** Tomar ações com retornos incertos na tentativa de descobrir rotas e estratégias potencialmente superiores.

Um agente puramente guloso (*greedy*) costuma convergir para políticas medíocres: ele descobre um caminho razoável nas primeiras tentativas e passa a repeti-lo indefinidamente, sem jamais explorar caminhos vizinhos que poderiam ser ordens de magnitude melhores.

Para contornar isso, usamos estratégias como o **epsilon-greedy**, onde o agente escolhe a melhor ação com probabilidade `1 - epsilon` e seleciona uma ação aleatória com probabilidade `epsilon`. Ao reduzir gradualmente o valor de `epsilon` ao longo do tempo, o sistema atende à condição de exploração infinita (GLIE), garantindo convergência para a política ótima.

### Q-Learning contra SARSA: duas filosofias de controle

No controle livre de modelo (*model-free*), aprendemos a função de valor de ação `Q(s, a)`, que representa o retorno esperado ao tomar a ação `a` no estado `s`. Dois algoritmos clássicos dominam essa categoria:

**Q-Learning (Watkins, 1989 - Off-Policy):**
```text
Q(s, a) <- Q(s, a) + alpha * [ R + gamma * max_a'( Q(s', a') ) - Q(s, a) ]
```

**SARSA (Rummery & Niranjan, 1994 - On-Policy):**
```text
Q(s, a) <- Q(s, a) + alpha * [ R + gamma * Q(s', a') - Q(s, a) ]
```

A distinção entre as duas fórmulas é sutil no índice, mas fundamental no comportamento:

* O **Q-Learning** atualiza a estimativa assumindo que a próxima ação será a melhor teoricamente possível (`max_a' Q`), independentemente da ação que o agente realmente venha a executar durante a fase exploratória. Por ser *off-policy*, ele aprende diretamente a política ótima, mas pode ser arriscado durante a fase de treino se o ambiente contiver armadilhas severas.
* O **SARSA** atualiza a estimativa utilizando a ação `a'` que foi **efetivamente sorteada** pela política do agente no passo seguinte. Sendo *on-policy*, ele leva em consideração os próprios desvios exploratórios. Em ambientes com penalidades catastróficas próximas da borda, o SARSA aprende uma rota mais conservadora e segura para evitar quedas acidentais.

## A Tríade Mortal e a escalabilidade no mundo real

Em problemas reais de grande porte, o espaço de estados é infinito ou excessivamente vasto para caber em uma tabela de memória. A solução é usar aproximadores de função (como redes neurais) para estimar `Q(s, a)` a partir de vetores de características.

No livro canônico de Sutton e Barto, os autores destacam um alerta fundamental para a engenharia de sistemas de IA: a **Tríade Mortal** (*The Deadly Triad*). A combinação simultânea de três fatores pode tornar o treinamento matematicamente instável e levar à divergência:

1. **Aproximação de funções:** Uso de modelos não lineares parametrizados no lugar de representações tabulares.
2. **Bootstrapping:** Atualização de estimativas baseada em estimativas seguintes (como no TD e Q-Learning).
3. **Treinamento Off-policy:** Aprender sobre uma política enquanto os dados são coletados por outra política de exploração.

O marco do algoritmo Deep Q-Network (DQN) da DeepMind em 2015 foi justamente conseguir estabilizar essa tríade ao jogar títulos do Atari a partir de pixels puros. A solução central foi o mecanismo de **Experience Replay**: as transições observadas são armazenadas em um buffer de memória e o modelo é atualizado a partir de mini-lotes sorteados aleatoriamente, quebrando a correlação temporal dos dados e restaurando a estabilidade do aprendizado.

## Roteiro cronometrado para a apresentação

Para garantir que os vinte minutos cubram toda essa trajetória sem atropelos, estruturei a apresentação nos seguintes marcos de tempo:

* **[00:00 a 03:00] Fundamentos da Aprendizagem e Indução:**
  * O problema de aproximar a função desconhecida `f` via hipótese `h`.
  * A fronteira entre classificação e regressão.
  * O dilema central de viés contra variância e a parcimônia da Navalha de Ockham.
  * O papel das funções de perda e o contraste geométrico entre regularização `L1` (esparsidade) e `L2` (suavização).

* **[03:00 a 11:00] Quatro Pilares do Aprendizado Supervisionado:**
  * Árvores de Decisão: Entropia de Shannon, ganho de informação e por que a poda Chi-quadrado é superior ao corte precoce em problemas como XOR.
  * Modelos Lineares: O Perceptron com limiar rígido versus a Regressão Logística com sigmoide contínua e probabilística.
  * Máquinas de Vetores de Suporte (SVM): O princípio da Margem Máxima, vetores de suporte e a projeção implícita do Kernel Trick.
  * Ensembles: A redução de variância com Bagging/Random Forests e a redução de viés com Boosting sequencial.

* **[11:00 a 18:00] A Transição para o Aprendizado por Reforço:**
  * A ausência de gabarito e a dinâmica de tentativa e erro nos Processos de Decisão de Markov.
  * O problema da atribuição de crédito em sequências longas de ação.
  * Avaliação passiva: o salto conceitual do Monte Carlo para o TD(0) com bootstrapping.
  * Controle ativo: o equilíbrio da exploração (*epsilon-greedy*) e o contraste entre o otimismo do Q-Learning e o realismo do SARSA.
  * A Tríade Mortal de Sutton & Barto e o papel do Experience Replay no DQN.

* **[18:00 a 20:00] Síntese e Fechamento:**
  * O arco evolutivo: da indução passiva de padrões estruturados para o controle autônomo em ambientes dinâmicos.
  * Conclusão aberta para a arguição da banca.

## Considerações finais

Apresentar um panorama denso em uma janela curta de tempo é um exercício de foco naquilo que realmente importa. Não adianta tentar transformar vinte minutos em uma leitura apressada de enciclopédia; o objetivo é guiar a banca através das grandes ideias que moldaram o aprendizado de máquina nas últimas décadas.

Entender a intuição por trás do compromisso entre viés e variância, a elegância do cálculo de margem no SVM, a ousadia do *bootstrapping* nas diferenças temporais e os limites teóricos da aproximação de funções em reforço é o que dá sustentação a qualquer discussão técnica séria. Se esses fundamentos ficarem claros para quem está assistindo, o tempo terá sido muito bem investido.

## Referências

[^1]: **Artificial Intelligence: A Modern Approach (4th Edition)** {*Stuart Russell & Peter Norvig, Pearson, 2020*} ([Link](https://aima.cs.berkeley.edu/))

[^2]: **Reinforcement Learning: An Introduction (2nd Edition)** {*Richard S. Sutton & Andrew G. Barto, MIT Press, 2018*} ([Link](http://incompleteideas.net/book/the-book.html))

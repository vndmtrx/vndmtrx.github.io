---
layout: post
title: "Gradiente Descendente em 6 atos"
subtitle: "O conto de terror de um profissional de infraestrutura assombrado por buscas em grafos, hipercubos de 23 dimensões e o temido OOM Killer"
author:
  - "Eduardo N. S. R."
date: 2026-11-01 00:00:00 GMT-3
permalink: /posts/gradiente-descendente-em-6-atos/
category: Crônicas
tags: [Inteligência Artificial, Faculdade, PyTorch, Algoritmos]
math: true
published: false
---

Existe uma sensação muito peculiar em olhar para os lados em uma sala de aula de pós-graduação e perceber, com razoável grau de certeza estatística, que você é a pessoa mais velha da turma. O povo ao redor parece ter nascido sabendo calcular autovalores de cabeça, enquanto o meu cérebro passou décadas condicionado pela lida crua da infraestrutura: acostumado ao cheiro de poeira dos racks, ao zumbido frio das ventoinhas nos data centers e à certeza quase religiosa de que o mundo funciona melhor quando a gente entende os próprios logs antes de dormir.

Só que quando alguém abre um colchete de matriz e começa a falar sobre derivadas parciais em superfícies não lineares, o meu instinto de sobrevivência apita na hora. Eu travo. Travo feio, como um computador antigo tentando renderizar vídeo sem placa aceleradora. Álgebra linear e otimização contínua sempre foram a minha criptonita em qualquer coisa que encarei na vida. E saber que os próximos projetos da disciplina vão descambar para redes neurais profundas só ativa um alarme silencioso no fundo da mente: AAAAAAAAAA!

Quando o professor colocou o trabalho no Teams, o Mini-Projeto 1 parecia uma provocação em duas partes complementares. Na primeira, você recebe uma fita binária de 23 bits, `00001001000011001100111`, e precisa encontrar a sequência ótima de inversões de bits individuais e de blocos contíguos até transformar tudo em zeros usando buscas clássicas em grafos. Na segunda, ele joga o conforto dos inteiros no lixo e exige que você trate esses mesmos bits como coordenadas contínuas no intervalo real entre zero e um, descendo a encosta da função de custo na base do puro gradiente descendente.

Aqui vale um alinhamento honesto de bastidor. No meu {% include post-ref.html slug="ensaio-sobre-dois-cegos" text="Ensaio sobre dois cegos" %}, eu defendi com unhas e dentes a escrita a quatro mãos com inteligência artificial para o blog, onde a máquina e o autor dividem o texto sem falsa vergonha. Só que aquilo era sobre literatura e ensaios pessoais. Aqui é mestrado. No mestrado, a regra do jogo é outra: se a IA escrever uma linha de código por você ou mastigar o relatório, você não aprendeu nada e virou apenas um papagaio caro de tecnologia.

O meu pacto com a máquina foi radicalmente inverso. Sentei diante do terminal e decretei: *"Você não vai gerar o trabalho para mim. Você será o meu tutor digital. Eu vou formular a minha intuição, vou tentar explicar com a minha linguagem tosca e por várias vezes incorreta, vou quebrar a cara, e você vai me fazer perguntas difíceis para apontar onde a minha lógica furou. Aí eu vou lá, leio o livro, repito tudo novamente, e vou implementando com as minhas próprias mãos no teclado e testo até passar"*.

O que se seguiu nas semanas seguintes não foi um fluxo de trabalho corporativo elegante. Foi uma comédia de erros, humilhações computacionais e pequenas epifanias que merecem ser contadas em seis atos.

## Ato I: A Batalha dos Bits

Todo programador que se preza carrega um vício secreto: a vontade incontrolável de complicar coisas simples para parecer inteligente.

Quando li que a fita tinha 23 posições e que podíamos inverter bits isolados ou blocos de tamanho arbitrário com custo unitário, a minha primeira reação foi montar uma arquitetura. Criei uma classe toda bonitinha chamada `FitaBits`, decorei com dataclasses, inventei métodos de parsing, coloquei validações de integridade e cheguei a pensar em abstrações funcionais com tuplas imutáveis. Estava lindo. Parecia um módulo de biblioteca corporativa pronta para ir a leilão.

Aí parei, olhei para o código e me perguntei o que diabos eu estava fazendo.

Eu estava gastando cem linhas de abstração orientada a objetos para virar zeros e uns. Chamei a máquina para o debate e ela foi impiedosa: se o seu objetivo é explorar milhões de estados em grafos de busca, criar instâncias de classes e alocar memória heap a cada nó filho vai transformar o seu garbage collector em uma fornalha.

Joguei a classe no lixo.

Voltei para o chão de fábrica do qual nunca deveria ter saído. Uma fita binária de tamanho $L$ cabe perfeitamente dentro de um inteiro comum do Python. Para evitar dores de cabeça com alinhamento, inverti o *endianness*: a posição zero fica no bit menos significativo, crescendo da direita para a esquerda. A inversão de um bit na posição $p$ virou um simples operador XOR com deslocamento: `estado ^ (1 << p)`. A inversão de um bloco de tamanho $k$ na posição $p$ virou uma máscara direta:

```python
mascara = ((1 << tamanho_bloco) - 1) << posicao
novo_estado = estado ^ mascara
```

Duas linhas. Zero alocações de objetos. Nenhuma cerimônia.

O alívio durou pouco. Às três da manhã, quando fui rodar a primeira suíte no terminal dentro do contêiner do Jupyter, tomei na cara um singelo `bash: pytest: command not found`. Respirei fundo, tomei um gole de café gelado e lembrei: a simplicidade não te livra de configurar o ambiente direito.

## Ato II: A Ilusão do Multicore

Com as operações básicas testadas e blindadas, passei para o algoritmo canônico de Busca em Largura (BFS), retirado diretamente do livro do Russell e Norvig [^1].

O BFS não tem segredo teórico. É uma busca cega: você põe a raiz na fila, expande todos os vizinhos do nível atual, coloca na fila FIFO e avança nível por nível. O problema é que o fator de ramificação dessa brincadeira é da ordem de $O(L^2)$. Para $L = 20$, cada nó gera mais de duzentos sucessores. A árvore explode como uma supernova.

Foi aí que a soberba de infraestrutura falou mais alto. Olhei para a minha estação de trabalho com dezesseis núcleos e trinta e dois gigabytes de memória RAM e pensei com os meus botões: *"Eu não vou rodar isso em um núcleo só como se estivesse em 1995. Vou meter concorrência pesada. Vou fazer um MapReduce aqui e dividir a fronteira entre os núcleos da máquina e ver essa árvore evaporar!"*

O resultado foi um dos momentos mais humilhantes desse processo.

| Estratégia de Execução | Mecanismo Interno | Tempo no Pior Caso ($L = 20$) |
| :--- | :--- | :---: |
| **Multi-Processos** | `multiprocessing` / Pool | **105,42 s** |
| **Pool de Threads** | `ThreadPoolExecutor` | **44,56 s** |
| **Sequencial Puro** | 1 Core CPU (Cache L1) | **18,92 s** |
| **PyTorch SIMD** | Tensores / Operações C++ | **4,03 s** |

Dezesseis núcleos levaram quase dois minutos para resolver o que um único núcleo fez em dezoito segundos.

O motivo é tão óbvio quanto doloroso: para operações atômicas que custam dois nanossegundos de CPU (um XOR bitwise), o custo do sistema operacional para serializar tuplas no `pickle`, empurrar dados por pipes de IPC (*Inter-Process Communication*) e gerenciar concorrência custa ordens de grandeza a mais do que o cálculo em si. Nas threads, o temido GIL (*Global Interpreter Lock*) do Python ficou apenas assistindo aos núcleos brigarem entre si por migalhas de sincronização.

O núcleo solitário, rodando em um loop seco e mantendo as máscaras pré-computadas inteiramente dentro do cache L1 da CPU, humilhou o paralelismo ingênuo.

A salvação do paralelismo só veio quando trocamos a estratégia: em vez de concorrência no nível do Python, usamos PyTorch, o que inclusive foi uma sugestão do professor para a feitura do trabalho. Pegamos a fronteira inteira do nível, empilhamos em um tensor matricial e disparamos um broadcasting bidimensional contra o tensor de máscaras. A expansão de cem mil nós ocorreu de uma vez só em C++ nativo com instruções vetoriais SIMD. O tempo despencou para quatro segundos no pior caso, e na fita oficial de 23 bits caiu de 21 segundos para míseros 1,2 segundo.

Mais do que o ganho de tempo, ficou a lição: ter núcleos de sobra não substitui a disciplina de entender a localidade dos seus dados.

## Ato III: A Parede dos 4096 Bits e o OOM Killer

O BFS resolve o problema da fita de 23 bits encontrando a solução ótima com cinco operações. O problema é que ele esgota os recursos logo em seguida.

Para fitas alternadas (`101010...`), o BFS visita mais de um milhão de estados em $L=20$. Em $L=23$, ele passa de 2,7 milhões. Se o professor pedisse para rodar em $L=30$, a máquina não terminaria antes do final do semestre. E o enunciado exigia testar a escalabilidade até $L = 4096$.

Entramos no terreno das buscas heurísticas: o Algoritmo Guloso (*Greedy Best-First Search*).

Primeiro, testamos a óbvia Distância de Hamming ($h_1$), que simplesmente conta quantos bits 1 ainda restam na fita. Parecia uma excelente ideia, mas na prática ela é míope. Para ela, uma sequência com cinco bits 1 espalhados pela fita tem exatamente a mesma distância estimada até o alvo que um bloco sólido de cinco bits 1 contíguos. Só que pelas regras do problema, o bloco sólido pode ser eliminado inteiro com uma única inversão de bloco (custo 1), enquanto os bits espalhados vão exigir pelo menos cinco operações. A heurística de Hamming não enxerga essa vantagem dos blocos, calcula custos distorcidos, expande caminhos desnecessários e sofre para convergir.

Foi quando implementamos a heurística de blocos contíguos ($h_2$), que conta quantos agrupamentos contíguos de bits 1 existem.

O efeito dessa heurística foi comparável a ligar os faróis em uma estrada escura. O fator de ramificação efetivo despencou para exatamente $b^* = 1,00$. A busca cega que antes tateava 750 mil nós no escuro colapsou em uma linha reta perfeita: cinco nós expandidos, custo cinco, resolução em 0,54 milissegundos. Foi trinta e nove mil vezes mais rápido que o BFS.

A euforia foi tão grande que até achei que tinha feito alguma coisa errada, ou que tinha implementado algum cheat sem querer no processo. Parecia bom demais para ser verdade.

Mas os testes continuavam passando. E se rodou $L=23$ em meio milissegundo, a tentação imediata foi ligar o modo turbo e rodar os testes de escala em potências de dois até 4096. Subi para 32, 64, 128, 256, 512, 1024, 2048. Os tempos iam subindo, mas tudo parecia sob controle.

Até que chamei o teste para $L = 4096$.

Para uma fita desse comprimento, o número de ações possíveis a cada passo é dado pela combinação $4096 \times 4097 / 2$, totalizando exatamente **8.390.656 operações possíveis por nó**. Cada inteiro de 4096 bits consome cerca de 570 bytes. Pré-computar as máscaras de ação devorou cinco gigabytes de cara.

Abri o monitor do sistema no terminal para acompanhar. Vi a barra de memória RAM de 32 GB subir em linha reta, devorando vinte, vinte e quatro, vinte e oito gigabytes. Meu notebook não usa partição de swap no disco, ele usa zswap na própria memória RAM, o que nessa hora só significa uma coisa: o processador fritando a 100% tentando compactar páginas de memória em desespero enquanto os coolers pareciam turbinas de avião decolando.

Dois segundos depois, o terminal cuspiu uma única palavra seca:

```text
Morto
```

O famoso *Out-of-Memory Killer* do Linux entrou na sala com uma espingarda de caça e abateu o meu processo sem direito a despedida.

> [!CAUTION] Aviso de Hardware
> Trinta e dois gigabytes de memória parecem uma quantidade infinita de espaço até você encontrar um problema combinatório de ordem quadrática que decide gerar milhões de estados filhos no primeiro nível de expansão.

## Ato IV: A Fita da Colega e a Proibição da Cola

Dias depois, no auge das minhas batalhas contra a exaustão de memória, uma colega de turma avisou no grupo que já tinha finalizado o relatório dela e compartilhou o repositório.

A tentação foi imediata.

Qualquer um que já tenha passado aperto na faculdade conhece a voz que sussurra no ouvido: *"Dá uma espiada. Não custa nada. Olha como ela modelou os testes, vê que estrutura ela usou no BFS e poupa dois dias de dor de cabeça. Ninguém vai saber"*.

Mas eu saberia. E isso pesa muito pra mim.

Botei uma regra de ferro para mim mesmo. Eu até baixei o repositório, dei uma olhada no relatório dela, comentei com o meu tutor digital sobre o que tinha visto, mas dei uma ordem categórica no terminal: *"Não use nada do conhecimento ou do código dela como base. Vamos nos basear estritamente no que eu construí até aqui no meu próprio repositório"*. Não era purismo moral de santinho de barro; era pragmatismo de aprendizado. Se eu pegasse o atalho antes de fechar o meu próprio raciocínio, eu perderia a oportunidade de construir a minha própria musculatura mental.

Só depois que a minha suíte inteira de testes estava rodando perfeitamente e o meu código estava blindado é que me dei ao luxo de abrir o trabalho dela para comparar os resultados.

E tomei um susto: o BFS dela tinha rodado a fita oficial de 23 bits em vinte e seis segundos, com números ligeiramente diferentes dos meus, e sem estourar a memória.

Fiquei intrigado. Como o algoritmo dela tinha passado com tanta tranquilidade pelos 23 bits se o meu BFS quase derreteu a máquina quando testei as fitas do pior caso?

Fui olhar o código dela com carinho e entendi a intuição: a fita canônica do professor (`00001001000011001100111`) é na verdade uma fita extremamente rasa. Ela tem apenas cinco blocos de bits 1. A solução ótima mora na profundidade cinco. O BFS dela fazia o teste de objetivo na geração e parava assim que encontrava a primeira resposta viável, além de colocar uma trava rígida de segurança limitando a busca a três milhões de nós visitados.

Foi uma sacada prática e muito inteligente para o enunciado específico. Se eu tivesse olhado o trabalho dela antes, eu certamente teria copiado a mesma estratégia, teria ficado feliz com os 23 bits resolvidos e jamais teria me dado ao trabalho de estressar o pior caso em fitas alternadas onde o algoritmo falha invariavelmente.

Não havia um código "melhor" ou "pior". Havia duas intuições complementares diante da mesma folha de papel: ela foi certeira no alvo pedido; eu fui paranóico com os limites da máquina. Ter respeitado o meu próprio tempo me permitiu apreciar a inteligência da solução dela sem me sentir inferior nem superior.

## Ato V: O Tutor Socrático

Quando achei que o pior tinha passado, virei a página do exercício e entrei na Parte 2: Otimização Contínua com Gradiente Descendente.

O pânico voltou em ondas gigantescas.

Até aquele momento, que já tinha passado quase um mês desde o começo dessa odisséia, tudo estava confortável dentro da lógica booleana: bits são zero ou um, estados são inteiros, transições são XOR. De repente, o enunciado exige que a fita binária seja tratada como um ponto contínuo $\mathbf{x} \in [0, 1]^L$ dentro de um hipercubo euclidiano de 23 dimensões, atraído por uma bacia de potencial quadrática até o vetor nulo.

Sentei diante da máquina e mandei a real: *"Eu não entendi nada do que é pra fazer. Sou de infraestrutura. Matrizes e cálculo são o meu calcanhar de Aquiles. Seja meu professor. Não me cuspa fórmulas prontas. Me faça perguntas conceituais, teste minhas analogias, me teste os conhecimentos e vamos construindo a intuição do zero"*.

O que se seguiu foi uma das sessões mais fascinantes de tutoria que já experimentei.

A IA começou me perguntando o que acontecia se o erro fosse definido pela soma dos quadrados dos valores da fita, $E(\mathbf{x}) = \sum x_i^2$, e como a derivada nos ajudava a descer a ladeira. Fui respondendo do meu jeito, tateando o escuro. Lembrei do paradoxo de Zenão e soltei: *"O gradiente descendente é como a corrida do coelho contra a tartaruga, onde a cada passo ele pula uma fração da distância restante e vai diminuindo o salto?"*

Ela confirmou: a derivada nos dá a direção de subida; se subtrairmos o gradiente multiplicado por uma taxa de aprendizado $\eta$, damos um passo ladeira abaixo.

Aí veio o pulo do gato conceitual. A derivada de $x^2$ é $2x$. O novo ponto é calculado por $x - \eta \cdot 2x = x(1 - 2\eta)$.

Fiz a conta de cabeça no susto: se a taxa de aprendizado for $\eta = 0.5$, a equação vira $x(1 - 2 \cdot 0.5) = x(1 - 1) = 0$.

O erro zera em exatamente um único passo milagroso.

Se $\eta < 0.5$, o algoritmo dá passos cautelosos e precisa de dezenas de iterações para chegar ao fundo do vale. Se $\eta > 0.5$, a derivada empurra com força excessiva, o ponto ultrapassa a origem (*overshoot*) e atinge valores negativos no hipercubo. Discutindo ali no terminal, fui provocando a máquina e deduzimos juntos o caso extremo: se o passo passar de 1.0, o módulo $|1 - 2\eta|$ fica maior que um e vira uma catapulta geométrica. Em vez de descer a encosta, cada salto fica maior que o anterior e o sistema explode para o infinito. Quando mais tarde abrimos o clássico *Dive into Deep Learning*, de Alex Smola e Aston Zhang [^2], para conferir a bibliografia, o sorriso foi inevitável: aquela mesma dinâmica que tínhamos acabado de destrinchar no diálogo socrático era exatamente a prova matemática formal do livro. Testamos isso na prática com PyTorch, plotamos as curvas de nível, e a teoria matemática tomou forma física diante dos meus olhos.

A coisa ficou ainda mais bonita quando adicionamos a função de regularização para simular a inversão de blocos vizinhos:

$$C(\mathbf{x}) = \sum_{i=1}^{L-1} (x_{i+1} - x_i)^2$$

A intuição que construímos foi puramente física: é como se cada bit estivesse preso ao chão pela gravidade (atraído para o zero) e amarrado aos vizinhos imediatos por elásticos. O parâmetro $\lambda$ (lambda) entrou nessa equação como o botão que regula a espessura desse elástico.

Se $\lambda = 0$, não existe elástico nenhum: cada bit cai sozinho na sua própria velocidade em direção ao chão. Se $\lambda = 0.5$, a tensão é suave e os blocos contíguos descem juntos pelo meio, enquanto as pontas do bloco sofrem o cisalhamento das bordas. Se um bit 1 está isolado entre dois zeros, ele sofre a atração do chão e a puxada dupla dos vizinhos, sendo jogado para baixo com força dobrada. O gradiente descendente estava desfazendo os blocos de forma contínua, exatamente como um filtro de desfoque gaussiano age sobre os pixels de uma imagem.

Só que havia um perigo oculto. Quando aumentamos o elástico para um valor agressivo como $\lambda = 20.0$, a corda ficou tão rígida que qualquer empurrãozinho em um bit catapultava os vizinhos para o lado oposto, fazendo o sistema inteiro oscilar em desespero e explodir para o infinito.

Para o elástico não arrebentar, o passo do algoritmo ($\eta$) precisa ser calibrado em função da rigidez da corda: quanto mais tenso o elástico ($\lambda$ maior), mais curto e medroso precisa ser o passo ($\eta$ menor). Ao analisar o autovalor máximo da matriz desse sistema acoplado, chegamos à cota de estabilidade clássica:

$$\eta \le \frac{1}{2 + 4\lambda}$$

Pela primeira vez em quarenta e quatro anos de vida, as matrizes e derivadas começaram a deixar de ser símbolos incompreensíveis em um quadro negro e viraram molas, elásticos e amortecedores que eu conseguia enxergar e tocar. Ok, ainda não é o ideal, mas é o ferramental que consegui construir por conta própria.

## Ato VI: A Conversa no WhatsApp e a Epifania do set()

Alguns dias após a entrega dos resultados, recebi uma mensagem de outro colega de turma.

Ele estava em desespero legítimo com a complexidade combinatória do problema. Conversamos em sala de aula e ele me mandou um vídeo de maratona de programação competitiva tratando sobre *Xor Hashing* e detecção de permutações em subarrays de alta performance, que até aquele momento eu não conhecia. O colega estava quebrando a cabeça para calcular limites teóricos de $N^N$ transições e se perguntando se havia algum algoritmo exótico de hashing polinomial que ele deveria ter implementado.

Eu nem sequer tinha estofo para tentar bancar o teórico ali.

Respondi com a mais pura humildade de quem passou a vida inteira trocando cabo de rede e configurando memória de servidor e tava sofrendo com toda aquela prosopopéia abstrata:

> *"Cara, a sua intuição com o vídeo foi show. Mas eu resolvi esse problema do jeito mais tosco que você pode imaginar: usei uma fila `deque` para pegar os nós por ordem de chegada e enfiei cada fita já vista dentro de um `set()` nativo do Python. Como o `set` usa tabela hash interna com busca em $O(1)$, a busca nunca visitou o mesmo estado duas vezes e a memória não explodiu."*

Ele respondeu concordando. Trocamos mais algumas mensagens sobre como duas pessoas diante do mesmíssimo enunciado podem enxergar caminhos completamente distintos: uma enxerga a sofisticação teórica dos hashes probabilísticos; a outra enxerga o consumo prático de cache e memória de uma estrutura embutida da linguagem.

Essa, no fim das contas, é a verdadeira graça de voltar para a universidade depois de velho. Não é sobre provar quem sabe mais ou quem tira a maior nota. É sobre o privilégio de passar perrengue junto, comparar intuições díspares sem vaidade e descobrir que, com paciência e método, até as nossas criptonitas mais antigas podem ser domadas.

O Mini-Projeto 1 está entregue e devidamente commitado no repositório [^3], com oitenta testes automatizados passando no `pytest` e uma sensação deliciosa de dever cumprido.

Agora só me resta respirar fundo e preparar para o enunciado dos Mini-Projetos 2 e do 3, onde as redes neurais profundas, matrizes de pesos densas e tensores multidimensionais certamente estarão me esperando na próxima esquina para cobrar a fatura com juros.

Segura na mão de Zeus e vai.

## Referências

[^1]: **Artificial Intelligence: A Modern Approach (4th Edition)** {*Stuart Russell & Peter Norvig, Pearson, 2020*} ([Link](https://aima.cs.berkeley.edu/))

[^2]: **Dive into Deep Learning** {*Aston Zhang, Zachary C. Lipton, Mu Li, & Alexander J. Smola, Cambridge University Press, 2023*} ([Link](https://d2l.ai/))

[^3]: **ppgco-pgc112-ia: Mini-Projeto 1** {*Repositório GitHub, vndmtrx*} ([Link](https://github.com/vndmtrx/ppgco-pgc112-ia))

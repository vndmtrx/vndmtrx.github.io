---
layout: post
title: "Ensaio da Banca de 20 Minutos: Agentes e Busca em IA"
author:
  - "Eduardo N. S. R."
date: 2026-08-17 07:19:00 GMT-3
permalink: /posts/banca-ia-agentes-e-busca/
tags: [Inteligência Artificial, Agentes, Algoritmos, Faculdade, Opinião]
---

Hoje mais tarde eu tenho aula de Tópicos em Inteligência Artificial, e o professor resolveu implementar uma daquelas dinâmicas que colocam a minha ansiedade em órbita: bancas avaliadoras compostas pelos próprios alunos. Funciona assim: enquanto um grupo vai para a frente da sala defender o tema da semana, outro grupo senta na primeira fila com a nobre e ingrata missão de fazer perguntas, avaliar o conteúdo e fingir pleno controle da própria vida acadêmica.

Para uma jovem idozah de 44 anos que já carrega uma preguiça quase divina de fazer qualquer obrigação fora da minha bolha de hiperfoco, a situação beira o tragicômico. Eu sou uma contradição ambulante: tenho uma resistência física a qualquer estudo que venha com carimbo de 'tarefa obrigatória', mas quando finalmente crio vergonha na cara, abro o PDF e a curiosidade bate, eu fico completamente absorvido pelas ideias. O problema é que isso só aconteceu no sábado e no domingo.

O detalhe que eleva o desespero a níveis pouco saudáveis é simples: o meu grupo é a primeiríssima banca do semestre. Não temos nenhum histórico prévio de apresentações para balizar o rigor, nenhum exemplo do professor sobre o que ele considera uma arguição justa e absolutamente nenhum parâmetro de comparação. Não sabemos se a postura esperada é a de um revisor implacável de conferência internacional ou a de um colega compreensivo que entende o perrengue de condensar tópicos densos em uma janela minúscula. Haja Sertralina para hoje!

E a pauta de hoje é daquelas pesadas. Dois grupos de colegas vão apresentar temas fundamentais e complementares da base clássica e moderna de IA: o primeiro grupo falará sobre agentes racionais, percepção, ação, ambiente e a fronteira entre comportamento reativo e planejado; o segundo grupo entrará de cabeça na resolução de problemas como busca em espaço de estados, representação em grafos e a temida maldição da dimensionalidade.

O desafio deles não é trivial: tiveram apenas uma semana para digerir capítulos inteiros do clássico livro de IA do Russell e Norvig [^1], cruzar com a visão moderna de arquiteturas autônomas do LeCun [^2], e montar algo palatável para vinte minutos de fala. E o meu lado na banca também não é nada confortável. Na teoria, a turma teve uma semana; na prática da vida real, eu só consegui sentar para ler e tentar entender esse caminhão de conceitos no fim de semana. Não tenho como fingir um domínio narrativo enciclopédico ou bancar a especialista em algo que li anteontem à base de café, coca-cola e joguinhos.

Como forma de acalmar meus próprios nervos e criar uma bússola prática para a aula de logo mais, decidi colocar no papel o que eu consegui pescar como a espinha dorsal desses textos. No fim das contas, este texto é um desabafo honesto e um guia pessoal sobre o que considero obrigatório ver em cada apresentação e o que é perfeitamente compreensível relevar quando todo mundo teve pouco tempo e o relógio está correndo contra você.

> 🔔 **Disclaimer**: Este texto reflete as anotações de alguém que passou o fim de semana tentando digerir leituras densas de IA para não passar vergonha na aula. Não domino nenhum detalhe formal desses papers, e estou usando a escrita justamente para organizar a minha intuição antes da apresentação.

## A angústia do primeiro grupo avaliador

Avaliar colegas quando você mesmo teve apenas sábado e domingo de leitura intensiva para absorver uma montanha de teoria é um exercício de pura empatia. Se você exige cada detalhe formal do livro, você se torna o hipócrita pedante que finge ter nascido sabendo o que leu quarenta e oito horas atrás, entre jogar fazendinha no *Palia* e assistir *Boku no Hero* no *Crunchyroll*, para ir aliviando a cabeça de tempos em tempos, tipo se levantar para relaxar as pernas; se você não cobra nada e só balança a cabeça concordando com tudo, a dinâmica perde qualquer propósito.

O segredo, pelo menos para a minha sanidade mental, é focar no feijão com arroz bem feito em vez de caçar tecnicalidades de rodapé. Uma apresentação de vinte minutos não serve para recitar a documentação da disciplina. Ela serve para contar uma história técnica coesa: qual é o problema que estamos tentando resolver, qual é a intuição das soluções e onde as coisas começam a complicar.

Com essa régua pé no chão, dividi o que vou prestar atenção nas apresentações em dois blocos: o que eu acho que não pode faltar (até para quem leu de última hora como eu) e o que pode ficar de fora sem peso na consciência.

## Apresentação 1: Agentes, a ilusão da onisciência e o salto para o planejamento

O primeiro grupo tem em mãos um conceito que parece simples no dia a dia, mas que tem nuances conceituais importantes: o que é um agente inteligente. A tentação aqui é encher o quadro de desenhos com sensores e atuadores sem explicar a ideia por trás.

### O que eu consegui pescar e vou prestar atenção

A primeira coisa básica que me marcou na leitura do Russell e Norvig foi a definição de racionalidade. Racionalidade não é perfeição e nem adivinhar o futuro (onisciência). Um agente racional é apenas aquele que toma a melhor decisão possível com base no que ele percebeu até ali e no que sabe do ambiente. O exemplo anedótico do livro é maravilhoso: se você olha para os dois lados, atravessa na faixa e uma porta de Boeing 747 despenca do céu e te esmaga, você não foi irracional; você apenas não era vidente.

Depois, tem a formalização do ambiente pelo acrônimo `PEAS` (*Performance, Environment, Actuators, Sensors*). O ponto aqui não é decorar a sigla, mas entender que a complexidade do agente depende do mundo onde ele vive: uma coisa é um robô num tabuleiro estático e previsível; outra completamente diferente é um táxi autônomo numa rua cheia de pedestres e chuva.

Mas o que realmente me chamou atenção nos textos foi a diferença entre duas formas de agir:

1. **O comportamento puramente reativo**: O agente age no reflexo imediato (regras simples do tipo `se vir sujeira então aspire`), sem pensar no amanhã. Se o ambiente tiver qualquer ponto cego, ele entra em crise existencial e fica preso em loops infinitos, como o aspirador de pó do livro que perde o sensor de localização e fica patinando para sempre entre duas salas limpas.
2. **O comportamento planejado (com modelo)**: O agente guarda um estado interno (uma memória de como o mundo funciona) e pensa antes de agir, ponderando as consequências das ações em direção a um objetivo ou utilidade.

E se o grupo quiser brilhar de verdade, pode puxar a ponte com o texto do LeCun: a distinção entre o Modo-1 (o reflexo rápido, tipo os LLMs de hoje que só cospem o próximo *token* sem planejar) e o Modo-2 (o raciocínio deliberado, onde um modelo de mundo simula o que vai acontecer antes de tomar a decisão). Se falarem disso, já ganharam a banca.

### O que o grupo pode deixar de lado

Não precisa ficar dez minutos lendo tabelas intermináveis de regras do aspirador de pó de duas salas ou dissecando pseudocódigo linha por linha. Todo mundo entende a ideia de que guardar todas as combinações de ações numa tabela é impossível. O valor está no conceito, não no código do livro.

Também não espero que entrem em detalhes matemáticos pesados das funções de custo ou nas fórmulas de redes neurais do LeCun. Eu mesmo considerei aquilo como paisagem. Entender a intuição de que o agente precisa de um modelo do mundo para prever o futuro já é mais do que suficiente.

## Apresentação 2: O labirinto dos estados e o muro da dimensionalidade

Se o primeiro grupo fala sobre quem decide, o segundo fala sobre como decidir quando você precisa encontrar um caminho. Entrar em busca em espaço de estados é basicamente transformar problemas do mundo real em labirintos ou grafos (e torcer para o computador não explodir a memória RAM no processo).

### O que eu consegui pescar e vou prestar atenção

Aqui, o básico que até eu, que li correndo no fim de semana, percebo é a necessidade de *abstração*. Para encontrar uma rota entre duas cidades (como no clássico exemplo de Arad a Bucareste), a gente não coloca no grafo o modelo do carro, a música do rádio ou as poças d'água na pista. A gente abstrai a realidade em pontos (estados) e conexões (ações). Sem simplificar, o computador simplesmente morre abraçado à falta de memória antes mesmo de dar o primeiro passo.

Outro ponto que eu espero que fique nítido é a diferença entre o **espaço de estados** (o mapa completo e conceitual do problema) e a **árvore de busca** (os caminhos que o algoritmo realmente abre na memória para tentar achar a saída).

E aí vem o tema central: a **maldição da dimensionalidade**. Se a cada passo você tem várias opções e o objetivo está longe, o número de caminhos possíveis explode exponencialmente ($O(b^d)$). É por isso que buscas cegas (como olhar tudo em largura ou profundidade) não servem para problemas reais: a memória ou o tempo acabam muito rápido.

Para resolver isso, entram as heurísticas e a busca informada com o algoritmo `A*`, que usa a conhecida função:

```text
f(n) = g(n) + h(n)
```

*Onde `g(n)` é o custo do que você já andou e `h(n)` é o chute educado (heurística) do quanto falta para chegar.*

O grupo só precisa explicar a ideia intuitiva: uma boa heurística funciona como uma bússola que nunca mente para cima (admissível/otimista), permitindo que o algoritmo corte caminhos inúteis sem perder a melhor rota.

Se sobrarem dois minutos e quiserem amarrar com o LeCun de novo, falar de como o ser humano planeja em múltiplos níveis (planejar a viagem em blocos grandes em vez de pensar em cada músculo da perna) fecha o tema com chave de ouro.

### O que o grupo pode deixar de lado

Não faz sentido ficar desenhando o passo a passo de cada cidadezinha da Romênia abrindo na fila de nós, nem demonstrar provas formais de teoremas matemáticos de consistência. Entender por que a busca cega quebra e como a heurística guia o algoritmo já resolve a apresentação.

Variações super avançadas de controle de memória (como `SMA*` ou bancos de dados de padrões disjuntos) também podem ficar de fora. Nem eu entendi isso direito. Saber que a memória é o maior gargalo do `A*` clássico já cobre o essencial.

## O filtro dos vinte minutos: saber o que cortar

A maior armadilha de uma apresentação de vinte minutos é o desespero de querer falar absolutamente tudo o que está no texto. Quando o tempo é curto, tentar cobrir cada parágrafo faz a apresentação virar uma leitura corrida de texto sem qualquer profundidade.

Saber escolher o que enfatizar e o que cortar é sinal de clareza. Para quem está assistindo (especialmente quem passou o fim de semana alternando entre ler paper e cuidar de plantações virtuais, tentando não surtar com a quantidade de conteúdo), vale muito mais entender por que a reatividade pura falha ou por que o espaço de estados explode do que ver vinte slides abarrotados de texto passados a jato.

> 💡 **Nota de Bancada**: Uma boa apresentação de vinte minutos foca nas perguntas certas: "qual é o gargalo aqui?" e "por que inventaram essa solução?".

## A listinha de checagem para a hora da apresentação

Para me ajudar na hora da aula e servir de roteiro mental enquanto os colegas apresentam, montei este resumo prático do que vou tentar pescar:

**Na apresentação de Agentes:**
- Explicaram que racionalidade é tomar a melhor decisão com o que se percebe, e não ser perfeito ou onisciente?
- Citaram a ideia do `PEAS` e como o ambiente afeta a dificuldade do agente?
- Mostraram a diferença entre o agente puramente reativo (que só responde ao susto do momento) e o agente que planeja/usa modelo interno?
- Conseguiram dar uma pincelada na ponte moderna (Modo-1 dos reflexos vs. Modo-2 do raciocínio com modelo de mundo)?

**Na apresentação de Busca:**
- Falaram sobre como a abstração é necessária para transformar um problema real em estados e ações?
- Ficou clara a diferença entre o grafo do problema e a árvore que o algoritmo percorre?
- Explicaram o que é a maldição da dimensionalidade (por que a busca cega explode em tempo e memória)?
- Deram a intuição básica do `A*` e de como a heurística serve de bússola para podar o espaço de busca?

## Um parêntese pessoal: fantasmas de um TCC inacabado

Ficar pensando em espaços de busca, explosão de estados e decisões de agentes me trouxe um *déjà-vu* curioso. Na minha segunda graduação, em Sistemas de Informação, cheguei a desenhar o meu TCC dentro de um laboratório de pesquisa que estava montando um braço mecânico para jogar damas. A minha parte era programar a inteligência que decidia as jogadas no tabuleiro.

Foi ali que senti na pele o desespero de encarar um espaço amostral gigantesco. Na época, devorei o livro de Sutton e Barto [^4] para tentar aplicar aprendizado por reforço (que, ironicamente, é o tema que eu mesmo vou apresentar daqui a duas semanas).

Sem usar redes neurais nem nada sofisticado, tentei resolver com programação dinâmica e um algoritmo de *one-armed bandit* aprendendo partida a partida.

No fim das contas, acabei jubilando daquele curso e o TCC nunca foi entregue, mas o aprendizado colou na mente. Até hoje, a lógica do *epsilon-greedy* (`e-greedy`) me assombra de vez em quando.

## Considerações Finais: Calibrando o julgamento

Escrever estas anotações me ajudou a colocar a cabeça no lugar e a dissipar boa parte daquela ansiedade inicial. Para quem leu tudo às pressas no sábado e no domingo, tentar bancar o examinador erudito seria pura presunção. Estar na primeira banca não significa fingir onisciência técnica; significa saber ouvir com atenção e conferir se os conceitos fundamentais foram bem articulados.

O meu objetivo na aula mais tarde não será encurralar ninguém com pegadinhas de rodapé ou detalhes obscuros de algoritmos. O que eu realmente quero ver é se eles conseguiram capturar e transmitir a essência da discussão: como passamos da reação cega para o planejamento deliberado, como a abstração nos salva de sermos engolidos pela realidade e de que maneira a computação lida com a assustadora imensidão dos espaços de busca.

Se esses alicerces forem defendidos com clareza e honestidade técnica, os vinte minutos terão valido cada segundo. E, com sorte, a nossa estreia como banca deixará um precedente razoável para as próximas semanas do semestre.

## Referências

[^1]: **Artificial Intelligence: A Modern Approach (4th Edition)** {*Stuart Russell & Peter Norvig, Pearson, 2020*} ([Link](https://aima.cs.berkeley.edu/))

[^2]: **A Path Towards Autonomous Machine Intelligence (Version 0.9.2)** {*Yann LeCun, Meta AI & NYU, 2022*} ([Link](https://openreview.net/forum?id=BZ5a1r-kVsf))

[^3]: **Thinking, Fast and Slow** {*Daniel Kahneman, Farrar, Straus and Giroux, 2011*} ([Link](https://www.amazon.com.br/Thinking-Fast-Slow-Daniel-Kahneman/dp/0374533555))

[^4]: **Reinforcement Learning: An Introduction (2nd Edition)** {*Richard S. Sutton & Andrew G. Barto, MIT Press, 2018*} ([Link](http://incompleteideas.net/book/the-book.html))

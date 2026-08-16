---
layout: post
title: "E se a gente refatorasse o Cálculo?"
author:
- "Eduardo N. S. R."
date: 2026-08-16 14:18:00 GMT-3
modified_date: 2026-08-16 20:09:00 GMT-3
permalink: /posts/refatorando-calculo/
tags: [Matemática, Cálculo, Educação, Opinião]
---

Eu desisti de fazer faculdade de Matemática por causa de cálculo, e definitivamente não foi por falta de interesse na disciplina como um todo. Pelo contrário: matemática discreta, teoria de números, teoria de conjuntos, axiomas de Peano, a incompletude de Gödel, a cardinalidade de infinitos e a hipótese do continuum sempre me fascinaram de um jeito quase obsessivo. Eu lia sobre essas estruturas por puro prazer, porque achava bonito ver cada peça lógica se encaixar com elegância. O problema era quando chegava em cálculo: ali a matéria virava um muro intransponível de regras mecânicas, e durante muitos anos eu me convenci de que a limitação era exclusivamente minha.

A sensação era de estar diante de um assunto que todo mundo parecia assimilar no piloto automático (ou fingir com muita convicção que estava assimilando), menos eu. Derivadas pareciam apenas uma lista de macetes para decorar, limites surgiam do nada para burocratizar contas simples sem explicar o porquê de existirem, e integrais eram aquela caixa-preta de "calcular a área sob a curva" sem qualquer aplicação palpável.

Aí, esses dias, eu esbarrei em um artigo de 2018 chamado *"Simplifying and Refactoring Introductory Calculus"* [^1], do Jonathan Bartlett, e tive uma daquelas epifanias libertadoras. O autor coloca o dedo na ferida e propõe uma reformulação profunda no ensino de cálculo usando um conceito que qualquer pessoa de computação conhece na pele: a ideia de *refactoring*.

> 🔔 *Disclaimer*: Este post reflete a minha experiência pessoal com o ensino de cálculo e a leitura do artigo. Não sou matemático, não pretendo ser, e se eu errar alguma tecnicalidade aqui, fiquem à vontade para me corrigir nos comentários.

## Dívida técnica, mas na matemática

O artigo começa com uma analogia que me acertou em cheio, justamente porque vem do mundo do software. Bartlett compara o estado atual do ensino de cálculo com *code debt*, a dívida técnica que se acumula quando novas funcionalidades são adicionadas a um programa sem reorganizar o que já existia. No código, isso significa duplicação, confusão sobre qual é a "forma certa" de fazer algo e um sistema que só fica mais difícil de manter com o tempo.

O ensino de cálculo, segundo o artigo, sofre do mesmo problema. Ao longo de mais de cem anos, conceitos foram sendo empilhados em uma sequência que fez sentido em algum momento, mas nunca foi reorganizada para refletir o entendimento moderno. O resultado é um curso onde o aluno precisa memorizar processos diferentes para problemas que, no fundo, são variações da mesma coisa. E quando o aluno não consegue, a culpa cai nele.

O que Bartlett propõe é fazer com o cálculo o que programadores fazem com código legado: refatorar. Pegar as peças, reorganizar, eliminar redundâncias e apresentar os conceitos de uma forma que exija menos memorização mecânica e mais compreensão real.

## Limites: a solução que aparece antes do problema

Embora a integral fosse o meu verdadeiro nêmesis (já chego nela), limites sempre foram algo estranho de entrar na minha cabeça. O motivo é simples: limite não é uma "aritmética direta" onde você pega valores, faz uma conta pontual e cospe um resultado estático. É muito mais um teste sobre o comportamento daquela situação, quase um *probe* para inspecionar como a função reage quando você se aproxima de um ponto proibido sem necessariamente encostar nele.

O artigo aponta algo que eu nunca tinha conseguido articular direito: limites são ensinados *antes* de o aluno ter qualquer noção de por que eles seriam necessários. Você chega no primeiro semestre, sabe resolver equações, tá confortável com álgebra, e de repente te jogam uma notação completamente nova para resolver problemas que você já resolvia com tranquilidade. Se eu sei que o valor de `f(x) = x²` quando `x = 3` é 9, por que eu preciso inventar uma notação de limite para expressar isso?

A resposta é que limites existem para resolver uma categoria muito específica de problemas: funções que têm descontinuidades ou "buracos", pontos onde a avaliação direta quebra ou resulta em algo indefinido. Mas essa motivação raramente vem primeiro. O que aparece é a sopa de letrinhas, as regras de manipulação e uma pilha de exercícios que parecem apenas burocratizar o que já era simples.

O Bartlett propõe inverter a ordem: limites deveriam vir no *final* do curso, e não no começo. O aluno passaria um bom tempo trabalhando com derivadas e integrais, desenvolvendo intuição prática, e só depois veria a justificativa formal por trás de tudo isso. Ele compara com aprender um idioma: crianças aprendem a falar muito antes de aprenderem regras de análise sintática. A imersão vem antes da formalização.

Quando eu finalmente entendi limites, foi justamente através dessa ideia de sonda: entender o comportamento de uma expressão perto de um ponto crítico. Tipo avaliar `1/x` com `x` crescendo indefinidamente em direção ao infinito, observando a curva tender a zero sem nunca precisar encostar no infinito (que sequer é um número definido). Essa imagem mental fez infinitamente mais sentido para mim do que qualquer demonstração prematura com épsilons e deltas.

## O momento em que derivadas finalmente fizeram sentido

Derivadas foram outro monstro para mim. Durante um bom tempo, eu só sabia aplicar a regra da potência no piloto automático: você pega o expoente, joga ele multiplicando na frente da variável e subtrai 1 do expoente original, tipo pegar `y = x³` e transformar mecanicamente em `y' = 3x²` (a famosa "regra do tombo", que no meu caso era só a minha dignidade acadêmica levando um tombo mesmo). Eu decorava o algoritmo do cálculo, mas não entendia o *porquê* daquilo de um jeito que eu pudesse sentir de verdade.

O clique veio quando alguém me explicou o conceito de taxa de variação. Não como uma definição abstrata, mas de forma concreta: a derivada é a inclinação da reta tangente a um ponto específico de uma curva. É a taxa com que as coisas estão mudando *naquele instante*. E o exemplo que fez tudo se encaixar pra mim foi a aceleração.

Velocidade é o quanto a posição muda ao longo do tempo. Aceleração é o quanto a velocidade muda ao longo do tempo. Ou seja, aceleração é a derivada da velocidade. Quando alguém me disse isso, eu finalmente consegui conectar o conceito abstrato com algo que eu podia visualizar. O carro acelerando na estrada. A curva ficando mais íngreme ou mais suave.

O artigo de Bartlett sugere exatamente esse tipo de abordagem: começar com exemplos concretos de inclinação entre dois pontos, aproximar os pontos progressivamente, e deixar que o aluno perceba por conta própria que, no limite, a inclinação entre dois pontos infinitamente próximos é a inclinação *no* ponto. Só depois disso vem a formalização.

## Diferenciais em vez de derivadas: uma unificação elegante

Uma das propostas mais interessantes do artigo é a ideia de ensinar *diferenciais* em vez de *derivadas* como ferramenta principal. Quando bati o olho nisso, confesso que me deu até um frio na espinha: para mim, a palavra "diferencial" só lembrava a temida matéria de equações diferenciais da licenciatura em Matemática que abandonei no primeiro semestre, só para ressaltar. Mas o que Bartlett estava propondo era algo muito mais pé no chão: usar diretamente aqueles símbolos `dx` e `dy` que a gente sempre vê soltos no cálculo (pra mim estavam soltos, não me julguem), mas que o ensino tradicional trata quase como enfeites de notação em vez de ferramentas que você pode manipular de verdade.

No ensino tradicional, o processo muda dependendo de como a função é apresentada. Se a função é explícita (tipo `y = x³`), o processo é direto. Mas se a equação for implícita (tipo um círculo `x² + y² = 25`), de repente entram regras adicionais de derivação implícita: você precisa lembrar de multiplicar termos por `dy/dx` pela regra da cadeia (como eu lembro disso... enfim), como se fosse um truque à parte. Essa assimetria entre variáveis confunde qualquer estudante.

A proposta de Bartlett é resgatar a abordagem original de Leibniz: separar a operação em duas etapas universais. Primeiro, você calcula o diferencial da equação inteira, tratando todas as variáveis com perfeita simetria. Depois, se você precisar de uma taxa de variação específica, você apenas resolve a álgebra básica.

Olha como isso funciona na prática para a equação `x² + y² = 25`:

1. Aplica o diferencial em todos os termos: `2x dx + 2y dy = 0`
2. Quer achar `dy/dx`? Basta isolar algebricamente: `2y dy = -2x dx` -> `dy/dx = -x/y`

E se você quisesse `dx/dy` em vez de `dy/dx`? A mesmíssima coisa: `2x dx = -2y dy` -> `dx/dy = -y/x`.

Dois passos. Sempre os mesmos dois passos, seja para funções diretas ou equações implícitas. Sem casos especiais ou regras *ad-hoc*.

O artigo mostra que esse processo não é apenas mais simétrico e fácil de memorizar: é exatamente a forma como o cálculo foi originalmente concebido por Leibniz. Durante séculos a matemática mudou de abordagem pedagógica para se blindar formalmente, e o ensino nunca voltou atrás para avaliar se a abordagem original não era, na verdade, muito mais clara para quem está aprendendo.

Isso me lembrou algo que eu já sabia do mundo do software: a primeira implementação nem sempre é a melhor, mas às vezes a primeira *arquitetura* é mais limpa que as refatorações posteriores. Não é que Leibniz estivesse "errado" e depois "consertaram". É que a formalização posterior complicou algo que já funcionava, e ninguém se deu ao trabalho de refatorar o currículo.

## A integral como soma infinita

Se limites causavam estranheza, a integral era o meu maior pesadelo: de todos os ramos da matemática que já tive contato, cálculo integral é de longe aquele com o qual menos tenho afinidade. O que eu sempre soube sobre ela era algo extremamente rudimentar: serve para calcular a área delimitada por uma curva e, em vez de me perder na notação mágica da cobrinha (o símbolo da integral), eu conseguia no máximo visualizá-la como um somatório contínuo. Mas parava por aí. Eu nunca entendi aplicações práticas daquilo além de calcular áreas de formatos abstratos em folhas de prova (porque aparentemente o mundo real estava desesperado para saber a área sob uma parábola aleatória).

O artigo propõe justamente uma mudança de definição que teria feito diferença pra mim. Em vez de definir a integral como "a área sob a curva", definir como "a soma infinita de pedaços infinitamente pequenos". Parece a mesma coisa, mas não é.

Quando você define como área, fica difícil entender por que a mesma ferramenta serve pra calcular comprimento de arco, volume de sólidos de revolução, ou qualquer outra aplicação. Parece que estão forçando a barra. Mas quando você define como "soma de pedacinhos", de repente faz sentido intuitivo: o que muda é a *forma* de cada pedacinho que você está somando. Para área, são retângulos ultrafinos. Para comprimento de arco, são segmentos de reta. Para volume, são cilindros ultracurtos.

A integral, nessa visão, é uma máquina de somar. O que está do lado direito do símbolo descreve a forma de cada peça individual, e o operador junta todas elas. Eu consigo visualizar isso perfeitamente. A definição estática de "área sob a curva", não.

## Um parêntese sobre infinitos e infinitesimais

O artigo também toca em um ponto sobre o qual eu só tinha uma noção muito abstrata e teórica: a nossa relação com o infinito e com os *infinitesimais*.

O pouco que eu conhecia sobre o infinito vinha do meu hiperfoco em conceitos matemáticos absurdos que não têm a menor utilidade prática na vida real: ZFC, os cortes de Dedekind, a cardinalidade de Cantor e o paradoxo de Banach-Tarski (a contradição ambulante: adoro perder o sono vendo uma esfera abstrata virar duas, mas fico puto com a área sob a parábola da prova porque "não tem aplicação no mundo real"). Mas tirando essa loucura teórica, no cálculo real da faculdade eu não fazia a menor ideia de como aplicar ou enxergar um "infinitesimal" na prática.

E foi aí que o artigo de Bartlett me deu outro clique. Ele explica que, no início do cálculo com Leibniz e Newton, o infinitesimal não era esse bicho de sete cabeças: era simplesmente a intuição de pegar uma curva, dar um passinho infinitamente pequeno para o lado e ver como a equação reagia. Era algo direto, quase geométrico.

Segundo o artigo, foi no século XIX que a matemática resolveu se blindar contra qualquer risco de contradição e inventou a pesada definição formal de limites. A intenção de dar rigor era nobre, mas o efeito colateral para quem aprende foi péssimo: jogaram no lixo a intuição visual e direta de Leibniz que tornava o cálculo compreensível.

O que o paper defende é que resgatar essa noção prática de infinitesimais (que a lógica matemática moderna já provou ser perfeitamente rigorosa) torna tudo mais palpável. Em vez de decorar malabarismos de limite no primeiro dia de aula, você apenas pensa: "vou somar uma variação infinitamente pequena aqui, simplificar a álgebra e ver o resultado". A intuição vem primeiro; a burocracia das provas formais fica para quando você já domina o terreno.

## Refatorar é uma atitude, não uma técnica

O que mais me pegou nesse artigo não foi nenhuma proposta técnica isoladamente (até porque a matemática mais densa do paper eu preferi admirar de longe, como quem admira um leão atrás do vidro reforçado do zoológico). Foi a atitude de fundo. A ideia de que um corpo de conhecimento, assim como um código legado, pode e deve ser reorganizado periodicamente. Que a forma como algo é ensinado não é sagrada só porque "sempre foi assim". Que se gerações inteiras de alunos tropeçam nos mesmos pontos, talvez o problema não esteja nos alunos.

Eu passei anos achando que eu não tinha aptidão para cálculo. Que as áreas da matemática que eu gostava, as discretas, as fundacionais, as lógicas, eram de alguma forma "separadas" do cálculo, e que a dificuldade era uma limitação minha. Lendo o artigo de Bartlett, eu percebo que o que me faltou não foi aptidão, foi um ensino que fizesse sentido. Os conceitos estavam lá. As conexões estavam lá. Mas a ordem de apresentação, a sequência pedagógica, o acúmulo de processos redundantes e a ausência de motivação concreta antes da formalização criaram uma barreira artificial.

E é a mesma coisa que a gente vê em sistemas de software que crescem sem refatoração: não é que o código seja impossível de entender. É que as camadas de complexidade acidental tornam impossível *querer* entender.

## Conclusão: não era eu, era o onboarding

Se eu fosse resumir o que senti lendo esse artigo, seria algo como descobrir que aquele sistema legado com o qual você brigou por anos não era tão impossível assim, era só mal documentado e mal organizado. O cálculo em si não é meu inimigo. O cálculo, no fundo, é sobre entender como coisas mudam. E isso é bonito.

O que me afastou foi a forma como ele foi empacotado e servido: limites antes da motivação, regras antes da intuição, formalismo antes da compreensão. A proposta de Bartlett não simplifica o cálculo no sentido de torná-lo menos rigoroso. Ela reorganiza a apresentação para que o rigor venha *depois* da compreensão, e não no lugar dela.

Vale deixar claro um detalhe importante: a ideia aqui não é desmerecer o método tradicional moderno. Para muita gente no mundo inteiro, essa estrutura clássica funciona perfeitamente bem (e que bom que funciona!). O meu ponto é que, para uma parcela enorme de estudantes, ela simplesmente não encaixa.

Como já pontuava Seymour Papert em *Mindstorms* [^2] sobre "matofobia" e como estudos como esse sobre a aversão à matemática também destacam [^3], a aversão e o bloqueio quase nunca nascem de uma incapacidade real do aluno, mas sim de um ensino dissociado de qualquer construção intuitiva. Variar as abordagens e criar caminhos onde o estudante possa construir o próprio entendimento pode dar mais trabalho para quem ensina, mas garante que mais pessoas consigam cruzar a linha de chegada, mesmo que a gente pareça aquele coelho do paradoxo de Zenão pulando metade da distância a cada pulo até finalmente alcançar o limite.

Se a matemática é uma das construções mais elegantes do pensamento humano (e eu genuinamente acredito que é), talvez a gente devesse cuidar do seu "código" com o mesmo carinho com que cuida de um bom repositório: revisando, refatorando e garantindo que quem chegar depois consiga, de fato, navegar.

## Referências

[^1]: **Simplifying and Refactoring Introductory Calculus** {*Jonathan Bartlett, 2018*} ([Link](https://arxiv.org/abs/1811.03459))

[^2]: **Mindstorms: Children, Computers, and Powerful Ideas** {*Seymour Papert, Basic Books, 1980, Cap. 2, pp. 38–54*} ([Link](https://www.amazon.com.br/Mindstorms-Children-Computers-Powerful-Ideas/dp/1541675126))

[^3]: **Aversão Matemática ou Matofobia: Causas, Efeitos e Superação** {*Cybelle Travassos & José Joelson de Almeida, EduCAPES / UEPB, 2019*} ([Link](https://educapes.capes.gov.br/handle/capes/567904))

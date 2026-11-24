---
layout: post
title: "E se a gente refatorasse o Cálculo?"
subtitle: "Como a dívida técnica na matemática transformou derivadas e limites em pesadelos de decoreba"
author:
- "Eduardo N. S. R."
date: 2026-08-16 14:18:00 GMT-3
modified_date: 2026-11-24 09:49:12 GMT-3
permalink: /posts/refatorando-calculo/
tags: [Educação, Faculdade, Matemática, Opinião]
category: Ensaios
---

Eu desisti de fazer faculdade de Matemática por causa de cálculo, e garanto que não foi por falta de interesse na disciplina como um todo. Pelo contrário: matemática discreta, teoria de números, teoria de conjuntos, axiomas de Peano, a incompletude de Gödel, a cardinalidade de infinitos e a hipótese do continuum sempre me fascinaram de um jeito quase obsessivo. Eu lia sobre essas estruturas por puro prazer, porque achava bonito ver cada peça lógica se encaixar com elegância. O problema era quando chegava em cálculo: ali a matéria virava um muro intransponível de regras mecânicas, e durante muitos anos eu me convenci de que a limitação era só minha.

A sensação era de estar diante de um assunto que todo mundo parecia assimilar no piloto automático (ou fingir com muita convicção que estava assimilando), menos eu. Derivadas pareciam apenas uma lista de macetes para decorar, limites surgiam do nada para burocratizar contas simples sem explicar o porquê de existirem, e integrais eram aquela caixa-preta de "calcular a área sob a curva" sem qualquer aplicação palpável.

Aí, esses dias, eu esbarrei em um artigo de 2018 chamado *"Simplifying and Refactoring Introductory Calculus"* [^1], do Jonathan Bartlett, e tive uma daquelas epifanias libertadoras. O autor coloca o dedo na ferida e propõe uma reformulação profunda no ensino de cálculo usando um conceito que qualquer pessoa de computação conhece na pele: a ideia de *refactoring*.

> [!NOTE] Disclaimer
> Este post reflete a minha experiência pessoal com o ensino de cálculo e a leitura do artigo. Não sou matemático, não pretendo ser, e se eu errar alguma tecnicalidade aqui, fiquem à vontade para me corrigir nos comentários.

{% include toc.html %}

## Dívida técnica, mas na matemática

Logo de saída, o artigo puxa uma analogia que me acertou em cheio por vir do software: Bartlett compara o ensino atual de cálculo com *code debt*, a dívida técnica acumulada quando novas funcionalidades se empilham num programa sem reorganizar o que já existia. No código, isso gera duplicação, confusão sobre o jeito certo de fazer e manutenção cada vez mais penosa.

Segundo o autor, o cálculo sofre do mesmo mal. Ao longo de mais de cem anos, conceitos foram empilhados numa sequência que fez sentido lá atrás, sem nunca serem reorganizados para o entendimento moderno. O aluno acaba obrigado a decorar processos diferentes para variações da mesma ideia, e quando trava, a culpa cai nas costas dele.

A proposta de Bartlett é tratar o cálculo como programadores tratam código legado: refatorar. Reorganizar peças, cortar redundâncias e trocar decoreba mecânica por compreensão real.

## Limites: a solução que aparece antes do problema

Embora a integral fosse meu verdadeiro nêmesis (já chego nela), limites sempre entraram atravessados na minha cabeça. Em vez de aritmética direta que cospe um resultado pontual, o limite opera como um *probe* para sondar como a função se comporta perto de um ponto proibido, sem encostar nele.

O artigo aponta algo que eu nunca tinha conseguido articular direito: limites são ensinados *antes* de o aluno ter qualquer noção de por que eles seriam necessários. Você chega no primeiro semestre, sabe resolver equações, tá confortável com álgebra, e de repente te jogam uma notação completamente nova para resolver problemas que você já resolvia com tranquilidade. Se eu sei que o valor de `f(x) = x²` quando `x = 3` é 9, por que eu preciso inventar uma notação de limite para expressar isso?

Limites existem para funções com descontinuidades ou "buracos", onde a conta direta quebra. Só que essa motivação quase nunca vem antes da sopa de letrinhas e da pilha de exercícios.

O Bartlett propõe inverter a ordem: limites deveriam vir no *final* do curso, e não no começo. O aluno passaria um bom tempo trabalhando com derivadas e integrais, desenvolvendo intuição prática, e só depois veria a justificativa formal por trás de tudo isso. Ele compara com aprender um idioma: crianças aprendem a falar muito antes de aprenderem regras de análise sintática. A imersão vem antes da formalização.

Quando entendi limites de verdade, foi por essa imagem de sonda: testar o comportamento de uma expressão perto de um ponto crítico, como avaliar `1/x` com `x` crescendo sem teto, vendo a curva tender a zero sem precisar encostar no infinito (que nem número é). Essa imagem visual fez muito mais sentido do que qualquer demonstração prematura com épsilons e deltas.

## O momento em que derivadas finalmente fizeram sentido

Derivadas foram outro monstro para mim. Durante um bom tempo, eu só sabia aplicar a regra da potência no piloto automático: você pega o expoente, joga ele multiplicando na frente da variável e subtrai 1 do expoente original, tipo pegar `y = x³` e transformar mecanicamente em `y' = 3x²` (a famosa "regra do tombo", que no meu caso era só a minha dignidade acadêmica levando um tombo mesmo). Eu decorava o algoritmo do cálculo, mas não entendia o *porquê* daquilo de um jeito que eu pudesse sentir de verdade.

O clique veio com taxa de variação: a derivada como inclinação da reta tangente naquele instante exato. O exemplo que destravou tudo foi a aceleração.

Velocidade é o quanto a posição muda ao longo do tempo. Aceleração é o quanto a velocidade muda ao longo do tempo. Ou seja, aceleração é a derivada da velocidade. Quando alguém me disse isso, eu finalmente consegui conectar o conceito abstrato com algo que eu podia visualizar. O carro acelerando na estrada. A curva ficando mais íngreme ou mais suave.

O artigo de Bartlett defende esse caminho: começar com inclinação entre dois pontos concretos, aproximá-los aos poucos e deixar o aluno perceber sozinho que, quando a distância entre eles zera, sobra a inclinação *no* ponto. Só depois entra a formalização.

## Diferenciais em vez de derivadas: uma unificação elegante

Uma das propostas mais interessantes do artigo é a ideia de ensinar *diferenciais* em vez de *derivadas* como ferramenta principal. Quando bati o olho nisso, confesso que me deu até um frio na espinha: para mim, a palavra "diferencial" só lembrava a temida matéria de equações diferenciais da licenciatura em Matemática que abandonei no primeiro semestre, só para ressaltar. Mas o que Bartlett estava propondo era algo muito mais pé no chão: usar diretamente aqueles símbolos `dx` e `dy` que a gente sempre vê soltos no cálculo (pra mim estavam soltos, não me julguem), mas que o ensino tradicional trata quase como enfeites de notação em vez de ferramentas que você pode manipular de verdade.

No ensino tradicional, o processo muda dependendo de como a função é apresentada. Se a função é explícita (tipo `y = x³`), o processo é direto. Mas se a equação for implícita (tipo um círculo `x² + y² = 25`), de repente entram regras adicionais de derivação implícita: você precisa lembrar de multiplicar termos por `dy/dx` pela regra da cadeia (como eu lembro disso... enfim), como se fosse um truque à parte. Essa assimetria entre variáveis confunde qualquer estudante.

A proposta de Bartlett é resgatar a abordagem original de Leibniz: separar a operação em duas etapas universais. Primeiro, você calcula o diferencial da equação inteira, tratando todas as variáveis com perfeita simetria. Depois, se você precisar de uma taxa de variação específica, você apenas resolve a álgebra básica.

Olha como isso funciona na prática para a equação `x² + y² = 25`:

1. Aplica o diferencial em todos os termos: `2x dx + 2y dy = 0`
2. Quer achar `dy/dx`? Basta isolar algebricamente: `2y dy = -2x dx` -> `dy/dx = -x/y`

E se você quisesse `dx/dy` em vez de `dy/dx`? A mesmíssima coisa: `2x dx = -2y dy` -> `dx/dy = -y/x`.

Dois passos. Sempre os mesmos dois passos, seja para funções diretas ou equações implícitas. Sem casos especiais ou regras *ad-hoc*.

O artigo mostra que esse processo, além de mais simétrico e fácil de lembrar, corresponde ao jeito como Leibniz concebeu o cálculo na origem. Durante séculos a matemática mudou a pedagogia para ganhar blindagem formal, sem nunca voltar atrás para checar se o caminho original era muito mais claro para quem aprende.

Isso me lembrou algo conhecido no software: a primeira implementação nem sempre é a melhor, mas às vezes a primeira *arquitetura* é mais limpa que as camadas posteriores. Leibniz não estava "errado" esperando conserto; a formalização posterior é que complicou algo funcional sem ninguém refatorar o currículo.

## A integral como soma infinita

Se limites causavam estranheza, a integral era meu maior pesadelo: de todos os ramos da matemática com que tive contato, cálculo integral é de longe o que menos conversa comigo. Tudo o que eu sabia era bem rudimentar: calcula a área sob uma curva e, em vez de me perder na cobrinha da notação, eu via aquilo no máximo como um somatório contínuo. Só que nunca enxerguei utilidade além de calcular áreas abstratas em folha de prova (como se o mundo real estivesse desesperado pela área sob uma parábola aleatória).

O artigo traz a virada de definição que teria mudado tudo pra mim: trocar "área sob a curva" por "soma infinita de pedaços infinitesimais". Parece detalhe, mas não é.

Quando você define como área, fica difícil entender por que a mesma ferramenta serve pra calcular comprimento de arco, volume de sólidos de revolução, ou qualquer outra aplicação. Parece que estão forçando a barra. Mas quando você define como "soma de pedacinhos", de repente faz sentido intuitivo: o que muda é a *forma* de cada pedacinho que você está somando. Para área, são retângulos ultrafinos. Para comprimento de arco, são segmentos de reta. Para volume, são cilindros ultracurtos.

A integral, nessa visão, é uma máquina de somar. O que está do lado direito do símbolo descreve a forma de cada peça individual, e o operador junta todas elas. Eu consigo visualizar isso perfeitamente. A definição estática de "área sob a curva", não.

## Um parêntese sobre infinitos e infinitesimais

O artigo também toca em um ponto sobre o qual eu só tinha uma noção muito abstrata e teórica: a nossa relação com o infinito e com os *infinitesimais*.

O pouco que eu conhecia sobre o infinito vinha do meu hiperfoco em conceitos matemáticos absurdos que não têm a menor utilidade prática na vida real: ZFC, os cortes de Dedekind, a cardinalidade de Cantor e o paradoxo de Banach-Tarski (a contradição ambulante: adoro perder o sono vendo uma esfera abstrata virar duas, mas fico puto com a área sob a parábola da prova porque "não tem aplicação no mundo real"). Mas tirando essa loucura teórica, no cálculo real da faculdade eu não fazia a menor ideia de como aplicar ou enxergar um "infinitesimal" na prática.

Foi aí que Bartlett me deu outro clique: na origem, com Leibniz e Newton, o infinitesimal era só dar um passinho minúsculo na curva e olhar a reação da equação.

Segundo o artigo, foi no século XIX que a matemática resolveu se blindar contra qualquer risco de contradição e inventou a pesada definição formal de limites. A intenção de dar rigor era nobre, mas o efeito colateral para quem aprende foi péssimo: jogaram no lixo a intuição visual e direta de Leibniz que tornava o cálculo compreensível.

O paper defende resgatar essa noção prática de infinitesimais (que a lógica moderna já provou ser rigorosa) para deixar tudo palpável. Em vez de decorar malabarismos de limite no primeiro dia, você pensa: "somo uma variação minúscula aqui, simplifico a álgebra e vejo o resultado". Intuição primeiro; provas formais depois que você domina o terreno.

## Refatorar é uma atitude, não uma técnica

O que mais me pegou no artigo não foi nenhuma proposta técnica sozinha (até porque a matemática mais densa do paper eu admirei de longe, como leão atrás do vidro reforçado do zoológico), e sim a atitude de fundo: um corpo de conhecimento, como código legado, precisa de revisão de tempos em tempos. A forma de ensinar não é sagrada só porque "sempre foi assim", e quando gerações inteiras tropeçam nos mesmos degraus, talvez a falha não esteja nos alunos.

Eu passei anos achando que eu não tinha aptidão para cálculo. Que as áreas da matemática que eu gostava, as discretas, as fundacionais, as lógicas, eram de alguma forma "separadas" do cálculo, e que a dificuldade era uma limitação minha. Lendo o artigo de Bartlett, eu percebo que o que me faltou não foi aptidão, foi um ensino que fizesse sentido. Os conceitos estavam lá. As conexões estavam lá. Mas a ordem de apresentação, a sequência pedagógica, o acúmulo de processos redundantes e a ausência de motivação concreta antes da formalização criaram uma barreira artificial.

Acontece o mesmo em software que cresce sem refatoração: camadas de complexidade acidental acabam matando qualquer vontade de entender o código.

## Conclusão: não era eu, era o onboarding

Resumindo o que senti lendo esse artigo: foi como descobrir que o sistema legado com o qual briguei por anos era só mal organizado. O cálculo fala sobre como coisas mudam, e isso é bonito.

O que me afastou foi a forma como ele foi empacotado e servido: limites antes da motivação, regras antes da intuição, formalismo antes da compreensão. A proposta de Bartlett não simplifica o cálculo no sentido de torná-lo menos rigoroso. Ela reorganiza a apresentação para que o rigor venha *depois* da compreensão, e não no lugar dela.

Um detalhe justo: a ideia aqui não é desmerecer o método tradicional moderno. Para muita gente no mundo inteiro, essa estrutura clássica funciona muito bem (e que bom!). Só que, para uma parcela enorme de estudantes, ela trava na largada.

Como já pontuava Seymour Papert em *Mindstorms* [^2] sobre "matofobia" e como estudos como esse sobre a aversão à matemática também destacam [^3], a aversão e o bloqueio quase nunca nascem de uma incapacidade real do aluno, mas sim de um ensino dissociado de qualquer construção intuitiva. Variar as abordagens e criar caminhos onde o estudante possa construir o próprio entendimento pode dar mais trabalho para quem ensina, mas garante que mais pessoas consigam cruzar a linha de chegada, mesmo que a gente pareça aquele coelho do paradoxo de Zenão pulando metade da distância a cada pulo até finalmente alcançar o limite.

Se a matemática é uma das construções mais elegantes do pensamento humano (e eu genuinamente acredito que é), talvez a gente devesse cuidar do seu "código" com o mesmo carinho com que cuida de um bom repositório: revisando, refatorando e garantindo que quem chegar depois consiga, de fato, navegar.

## Referências

[^1]: **Simplifying and Refactoring Introductory Calculus** {*Jonathan Bartlett, 2018*} ([Link](https://arxiv.org/abs/1811.03459))

[^2]: **Mindstorms: Children, Computers, and Powerful Ideas** {*Seymour Papert, Basic Books, 1980, Cap. 2, pp. 38–54*} ([Link](https://www.amazon.com.br/Mindstorms-Children-Computers-Powerful-Ideas/dp/1541675126))

[^3]: **Aversão Matemática ou Matofobia: Causas, Efeitos e Superação** {*Cybelle Travassos & José Joelson de Almeida, EduCAPES / UEPB, 2019*} ([Link](https://educapes.capes.gov.br/handle/capes/567904))

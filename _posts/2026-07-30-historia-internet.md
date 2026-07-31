---
layout: post
title: "Uma Breve História da Internet"
author:
- "Eduardo N. S. R."
date: 2026-07-31 12:40:00 GMT-3
permalink: /posts/historia-internet/
tags: [Internet, Web, História, Redes]
---

A internet é uma dessas coisas que a gente usa o dia inteiro sem parar pra pensar no que tem por baixo. A gente acorda, olha o celular, entra no Instagram, assiste um vídeo no YouTube, manda mensagem no WhatsApp, pede comida, carro e até hospedagem por aplicativo, e tudo isso acontece em cima de uma rede que levou décadas pra chegar onde está. E a história de como isso tudo foi construído é das mais interessantes da computação.

A ideia desse post é contar essa história de uma forma razoavelmente acessível, passando pelos momentos que eu considero mais marcantes na trajetória da internet. Não é um tratado acadêmico e nem pretende ser exaustivo. É mais um passeio cronológico que vai das redes militares dos anos 60 até o streaming e a Internet das Coisas. Considere esse texto como um mapa de onde as coisas vieram e de como essa infraestrutura que usamos todos os dias foi construída.

> *💡 Nota de mea culpa:* Ok, admito que no fim das contas a história não ficou tão breve assim. Quando comecei a juntar as peças, percebi que resumir seis décadas de evolução sem perder os detalhes importantes ia exigir bem mais do que um post rápido. Tive um trabalho considerável de pesquisa para compilar, organizar e cruzar dezenas de fontes em uma linha do tempo única, tentando entregar tudo de forma direta pra você (claro, com uma ajudinha de IA para ajudar a localizar fontes e organizar as ideias). Aliás, não deixe de conferir as referências no final.

## Linha do Tempo e Estrutura do Post

Para ajudar a guiar a leitura por essa jornada mais longa, organizei os principais marcos da internet em ordem cronológica. Você pode usar a tabela abaixo para navegar diretamente para a seção ou período que mais te interessar:

| Seção | Período / Década |
| :--- | :--- |
| [As Raízes da Internet: Comutação de Pacotes e a Guerra Fria](#as-raízes-da-internet) | Anos 60 |
| [ARPANET: A Primeira Rede](#arpanet-a-primeira-rede) | 1969 - Anos 70 |
| [O Surgimento do TCP/IP](#o-surgimento-do-tcpip) | 1974 - 1983 |
| [A Internet Chega ao Brasil](#a-internet-chega-ao-brasil) | 1988 - 1995 |
| [A World Wide Web](#a-world-wide-web) | 1989 - 1993 |
| [Os Primeiros Buscadores](#os-primeiros-buscadores) | 1990 - 1998 |
| [A Guerra dos Navegadores](#a-guerra-dos-navegadores) | 1994 - Anos 2000 |
| [A Bolha Pontocom (e o seu estouro)](#a-bolha-pontocom-e-o-seu-estouro) | 1995 - 2002 |
| [A Era da Web 2.0](#a-era-da-web-20) | Anos 2000 |
| [O Fenômeno das Redes Sociais](#o-fenômeno-das-redes-sociais) | 1997 - Presente |
| [Smartphones e a Revolução Mobile](#smartphones-e-a-revolução-mobile) | 2007 - Presente |
| [A Computação em Nuvem](#a-computação-em-nuvem) | 2003 - Presente |
| [O Surgimento do Streaming](#o-surgimento-do-streaming) | 1999 - Presente |
| [A Internet das Coisas](#a-internet-das-coisas) | 1999 - Presente |


## As Raízes da Internet: Comutação de Pacotes e a Guerra Fria

Antes de qualquer coisa, a gente precisa voltar ao início dos anos 1960, em plena Guerra Fria. Nessa época, uma das preocupações dos militares americanos era bastante prática: como manter uma rede de comunicação funcionando caso parte dela fosse destruída por um ataque nuclear? As redes de telecomunicação existentes eram baseadas em comutação de circuitos, ou seja, quando duas pontas se comunicavam, existia um circuito dedicado entre elas. Se alguém cortasse aquele circuito, a comunicação morria.

É nesse cenário que Paul Baran, um engenheiro da RAND Corporation, começou a pensar em uma alternativa. Ele publicou uma série de relatórios entre 1960 e 1964 chamada *"On Distributed Communications"* [^1], onde propôs um modelo de rede distribuída. A ideia era que a mensagem fosse quebrada em pedaços menores (que ele chamou de "message blocks") e que esses pedaços pudessem trafegar por caminhos diferentes dentro de uma rede em formato de malha, se reorganizando dinamicamente ao redor de pontos danificados ou sobrecarregados.

Do outro lado do Atlântico, de forma totalmente independente, o cientista da computação Donald Davies chegava a conclusões parecidas no National Physical Laboratory (NPL), na Inglaterra, em 1965 [^2]. Em vez de motivações militares, seu objetivo era otimizar a troca de dados entre computadores de tempo compartilhado. Foi ele, inclusive, quem cunhou os termos **"packet"** (pacote) e **"packet switching"** (comutação de pacotes), terminologia que usamos até hoje [^3].

Os dois pesquisadores trabalharam de forma independente, mas quando suas pesquisas se cruzaram, a comunidade percebeu que tinha em mãos um conceito poderoso. Lawrence Roberts, que viria a ser uma figura central no projeto da ARPANET, incorporou a terminologia e os conceitos de Davies no projeto americano [^2].

## ARPANET: A Primeira Rede

A ARPANET foi o primeiro grande experimento prático de rede de comutação de pacotes. O projeto foi financiado pela Advanced Research Projects Agency (ARPA) [^4], uma agência do Departamento de Defesa dos Estados Unidos que tinha o papel de investir em projetos de pesquisa de longo prazo. O arquiteto principal da rede foi Lawrence Roberts, que acabamos de falar no tópico anterior.

A primeira conexão da ARPANET aconteceu em **29 de outubro de 1969** [^5], entre um computador na Universidade da Califórnia em Los Angeles (UCLA) e outro no Stanford Research Institute (SRI). A equipe era liderada pelo professor Leonard Kleinrock na UCLA, e o estudante Charley Kline ficou responsável por enviar a primeira mensagem. O plano era digitar "LOGIN" para se conectar remotamente ao computador de Stanford.

O resultado? O sistema caiu depois de transmitir apenas as duas primeiras letras. A primeira mensagem da história enviada pela ARPANET foi **"LO"** [^5]. Em cerca de uma hora, a equipe conseguiu restabelecer a conexão e completar o comando. É um início humilde para algo que mudaria o mundo.

Até o final de 1969, a rede já tinha quatro nós: UCLA, SRI, UC Santa Barbara e a Universidade de Utah [^4]. A conexão entre esses computadores usava equipamentos chamados Interface Message Processors (IMPs), desenvolvidos pela empresa Bolt, Beranek and Newman (BBN) [^6]. Os IMPs são, na prática, os ancestrais dos roteadores modernos.

## O Surgimento do TCP/IP

A ARPANET cresceu, e com ela o problema de interoperabilidade. Cada rede que surgia usava seus próprios protocolos, e elas simplesmente não conseguiam conversar entre si. A ARPANET usava um protocolo chamado NCP (*Network Control Protocol*), que funcionava bem dentro da própria rede mas não tinha sido pensado para interconectar redes diferentes.

Em 1974, Vint Cerf e Bob Kahn publicaram um paper que seria um marco na história das redes: *"A Protocol for Packet Network Intercommunication"* [^7]. Nesse artigo, eles propuseram um protocolo de "arquitetura aberta" que pudesse conectar redes heterogêneas através de gateways. O protocolo foi batizado inicialmente de Transmission Control Program (TCP).

Com o tempo, ficou claro que o TCP monolítico precisava ser dividido. Em 1978, o protocolo foi separado em duas camadas: o **TCP** (*Transmission Control Protocol*), responsável pela entrega confiável e ordenada dos dados, e o **IP** (*Internet Protocol*), responsável pelo roteamento dos pacotes até o destino correto. Nascia o **TCP/IP**.

O momento decisivo veio em **1º de janeiro de 1983**, data conhecida como o "Flag Day" [^8]. Nesse dia, a ARPANET migrou de NCP para TCP/IP de uma vez, sem período de transição. Quem não migrasse, ficava fora da rede. Essa data é frequentemente citada como o nascimento da internet como a conhecemos, porque a partir dali tínhamos um protocolo universal que permitia que qualquer rede se conectasse a qualquer outra rede. O nome "internet" vem justamente disso: uma rede de redes interconectadas (*inter-net*).

## A Internet Chega ao Brasil

No Brasil, a internet chegou um pouco mais tarde. Em 1988, a FAPESP (em São Paulo) e o LNCC (no Rio de Janeiro) fizeram as primeiras conexões internacionais do país, usando a rede Bitnet para troca de e-mails e arquivos [^9]. Era o início, mas ainda bem distante do que a gente entende por "internet" hoje.

Em 1989, o Ministério da Ciência e Tecnologia criou a **RNP** (Rede Nacional de Pesquisa) [^10], com o objetivo de construir um backbone nacional que interligasse universidades e centros de pesquisa. A primeira conexão TCP/IP brasileira aconteceu em 1991, pela FAPESP. Mas até esse ponto, a internet no Brasil era coisa restrita ao mundo acadêmico.

A abertura para uso comercial veio em **1995**, com a criação do **CGI.br** (Comitê Gestor da Internet no Brasil) [^11] e a liberação do acesso para o público geral. A Embratel iniciou os primeiros projetos de acesso discado, e a partir daí surgiram os provedores comerciais que levariam a internet para dentro das casas dos brasileiros.

## A World Wide Web

Ter uma rede global funcionando é uma coisa. Torná-la utilizável para pessoas comuns é outra bem diferente. A internet existia nos anos 80, mas era usada quase que exclusivamente por pesquisadores e militares, através de ferramentas como e-mail, FTP e Usenet. Faltava uma camada que tornasse a informação fácil de publicar, encontrar e navegar.

Essa camada foi criada por Tim Berners-Lee [^12], um cientista do CERN, o Laboratório Europeu de Física de Partículas, na Suíça. Em março de 1989, Berners-Lee escreveu uma proposta chamada *"Information Management: A Proposal"*, onde ele descrevia um sistema para conectar documentos através de links, usando a infraestrutura da internet. A ideia era juntar hipertexto com rede de computadores, criando algo que ele inicialmente chamou de "Mesh" e depois batizou de World Wide Web.

Até o final de 1990, Berners-Lee já tinha desenvolvido os componentes fundamentais da Web: o primeiro servidor web, o primeiro navegador (chamado WorldWideWeb) e os protocolos base (HTML, HTTP e URIs). O primeiro site da história ficava no endereço info.cern.ch [^13] e ainda pode ser acessado nos dias de hoje. Em agosto de 1991, Berners-Lee fez o anúncio público da Web no newsgroup alt.hypertext [^14], convidando qualquer pessoa a acessar e contribuir.

Eu escrevi com mais detalhes sobre a evolução técnica do HTTP e da Web no meu post sobre [Evolução do Protocolo HTTP e da World Wide Web](/posts/evolucao-http/), se você quiser se aprofundar na evolução do protocolo.

Um fator que não dá pra ignorar na expansão da Web foi a decisão do CERN, em **30 de abril de 1993**, de liberar o software da World Wide Web para o domínio público [^15]. Se o CERN tivesse decidido cobrar licenças ou patentear a tecnologia, é provável que a Web como conhecemos simplesmente não existisse. Essa decisão garantiu que a tecnologia fosse aberta, e qualquer pessoa ou instituição pudesse construir em cima dela.

Pouco tempo depois, em 1993, surgiu o **NCSA Mosaic** [^16], o primeiro navegador com interface gráfica que rodava em Windows e Mac. Desenvolvido por Marc Andreessen e sua equipe na Universidade de Illinois, o Mosaic foi o responsável por popularizar a Web com o público geral. Até então, navegar na internet era coisa de terminal de texto. O Mosaic abriu as portas para milhões de pessoas.

## Os Primeiros Buscadores

Com a Web crescendo rapidamente, um novo problema apareceu: como encontrar alguma coisa? Nos primeiros anos, se você não soubesse o endereço exato de um site, tinha que trocar e-mails, ler listas de discussão ou pedir referências para outras pessoas. Conforme o número de páginas crescia, ficava claro que era necessário algum mecanismo de busca.

O primeiro a resolver esse problema (antes mesmo da Web) foi o **Archie**, criado em 1990 [^17]. O Archie não era um buscador da Web, porque a Web nem existia ainda no formato que conhecemos. O que ele fazia era indexar os nomes de arquivos disponíveis em servidores FTP públicos. Era basicamente um banco de dados de diretórios de arquivos.

Quando a Web apareceu e o volume de páginas explodiu, surgiram soluções voltadas especificamente para a Web. O **Yahoo!**, lançado em 1994, funcionava como um diretório curado por humanos [^18]. As páginas eram organizadas manualmente em categorias, como um catálogo de biblioteca. Funcionava bem enquanto o número de sites era administrável, mas com o crescimento da Web, uma abordagem manual passou a ser inviável.

No Brasil, o equivalente do Yahoo! foi o **Cadê?**, criado em 1995 por Gustavo Viberti e Fábio de Oliveira [^19]. O Cadê? funcionava da mesma forma: uma catalogação manual de sites brasileiros, organizada por categorias. Para quem usava internet no Brasil nessa época, o Cadê? era o ponto de partida para encontrar qualquer coisa em português na Web. O serviço foi vendido para a StarMedia em 1999 e depois comprado pelo Yahoo! Brasil em 2002, desaparecendo gradualmente com a chegada do Google.

Em 1995, o **AltaVista** representou um salto técnico [^20]. Ele foi um dos primeiros buscadores a usar um crawler (um programa que navega automaticamente de página em página, seguindo links) para indexar o conteúdo das páginas e não só seus títulos ou diretórios. Isso permitia buscas por palavras-chave em um volume enorme de páginas.

O **Google** surgiu em 1998, fundado por Larry Page e Sergey Brin, dois doutorandos de Stanford [^21]. O diferencial do Google foi o algoritmo **PageRank** [^22], que em vez de ranquear páginas apenas pelo conteúdo textual, ranqueava pela quantidade e qualidade de links que apontavam para elas. A lógica era que uma página referenciada por muitas outras páginas relevantes provavelmente era mais confiável. Enquanto os concorrentes se transformavam em portais cheios de notícias, horóscopo e propaganda, o Google manteve uma interface limpa e focada na busca. Essa combinação de qualidade de resultado com simplicidade de uso definiu a era da busca na internet.

## A Guerra dos Navegadores

Enquanto os buscadores disputavam a atenção dos usuários, outra guerra acontecia em paralelo. A chamada "Guerra dos Navegadores" (ou *Browser War*) foi um dos episódios mais marcantes dos anos 90 na internet.

O protagonista inicial era o **Netscape Navigator**, que surgiu em 1994 e rapidamente dominou o mercado, chegando a ter entre 70% e 90% de participação [^23]. O Netscape era o navegador que a maioria das pessoas usava para acessar a Web. Marc Andreessen, o mesmo criador do Mosaic, era cofundador da Netscape Communications.

A Microsoft, por sua vez, demorou a perceber a importância da internet. Isso mudou em 1995, quando Bill Gates escreveu o famoso memorando interno *"The Internet Tidal Wave"* [^24], onde ele reconhecia que a internet era a coisa mais importante desde o IBM PC. A partir dali, a Microsoft redirecionou a empresa para a Web.

A estratégia da Microsoft foi criar o **Internet Explorer** e embutí-lo diretamente no Windows. Dessa forma, todo computador com Windows já vinha com um navegador instalado, sem que o usuário precisasse baixar nada. O IE era gratuito, o que minava o modelo de negócio da Netscape, que vendia licenças do seu navegador [^25]. A Microsoft também pressionou fabricantes de computadores e provedores de internet para priorizarem o IE e limitarem a distribuição do Netscape.

Em 1998, o Departamento de Justiça dos Estados Unidos moveu um processo antitruste contra a Microsoft [^26], acusando a empresa de usar seu monopólio no mercado de sistemas operacionais para eliminar a concorrência no mercado de navegadores. Os tribunais confirmaram que a Microsoft tinha agido de forma anticompetitiva. Uma proposta inicial de desmembrar a empresa foi derrubada, mas a Microsoft aceitou mudar algumas práticas de negócio.

A Netscape não sobreviveu. Foi comprada pela AOL em 1999. Mas antes de desaparecer, fez algo que teria consequências profundas: liberou o código-fonte do seu navegador como software de código aberto [^27]. Desse código nasceu o projeto **Mozilla**, que anos depois daria origem ao **Firefox**. A Guerra dos Navegadores terminou com a Microsoft vencendo a batalha, mas semeou o terreno para o movimento de código aberto nos navegadores que culminaria, anos depois, na diversidade de navegadores que temos hoje, com Chrome, Firefox, Safari e outros.

## A Bolha Pontocom (e o seu estouro)

A rápida expansão da Web nos anos 90 criou uma euforia no mercado financeiro. Investidores de risco despejaram quantidades enormes de dinheiro em qualquer startup que tivesse ".com" no nome. A lógica era que a internet ia mudar tudo (e de fato mudou), e que portanto qualquer empresa conectada à internet valeria muito dinheiro (aí a lógica falhava).

O índice Nasdaq, fortemente concentrado em ações de tecnologia, subiu cerca de 600% entre 1995 e 2000 [^28]. Empresas eram avaliadas não por lucro, receita ou fluxo de caixa, mas por métricas como "cliques", "eyeballs" (quantas pessoas olhavam para o site) e "market share" (participação de mercado). A estratégia dominante era o "Get Big Fast": gastar agressivamente para crescer rápido, mesmo operando no prejuízo.

A bolha estourou em março de 2000. A Nasdaq começou a cair e não parou. Até outubro de 2002, o índice tinha perdido mais de 75% do seu valor, evaporando algo em torno de 5 trilhões de dólares em capitalização de mercado [^28]. Empresas emblemáticas como a Pets.com queimaram centenas de milhões de dólares e desapareceram da noite para o dia.

No Brasil, o cenário tinha suas particularidades. O **UOL** (Universo Online), lançado em 1996 pelo Grupo Folha [^29], era o grande portal brasileiro: provedor de acesso, conteúdo, e-mail, chat, tudo num lugar só. O **iG** (Internet Group) apareceu em janeiro de 2000 e mexeu bastante o mercado ao oferecer acesso gratuito à internet [^30]. O usuário pagava apenas a ligação telefônica, o que democratizou o acesso em um momento em que a assinatura mensal dos provedores ainda era cara para muita gente.

O **Submarino** surgiu como um dos primeiros grandes e-commerces brasileiros, sobreviveu à bolha e anos depois se juntou a outras operações para formar a B2W [^29]. Assim como nos Estados Unidos, a crise filtrou quem tinha um modelo de negócio sustentável e quem estava apenas surfando a euforia.

E para quem viveu essa época no Brasil, a experiência da internet tinha um ritual particular: o modem 56k discando, a linha telefônica ocupada enquanto você navegava (e a família reclamando), e a espera até meia-noite para conectar pagando um único pulso telefônico.

A parte interessante dessa história é que, apesar da destruição, a bolha não foi um desperdício completo. Ela financiou a construção de infraestrutura de rede (fibra óptica, data centers) que seria aproveitada pelas empresas que sobreviveram. E entre as sobreviventes estavam a Amazon e o Google, que saíram do outro lado da crise e se tornaram duas das maiores empresas do mundo.

## A Web 2.0 e o Conteúdo Gerado pelo Usuário

Depois que a poeira da bolha baixou, a Web mudou de cara. Em 2004, Tim O'Reilly popularizou o termo **"Web 2.0"** [^31] para descrever uma mudança que já estava em andamento: a Web deixava de ser um lugar onde você ia para ler informação e passava a ser um lugar onde você também criava conteúdo.

Na Web dos anos 90 (que retroativamente passou a ser chamada de "Web 1.0"), a maioria dos sites era estática. Alguém publicava uma página e você lia. A interação era mínima. Já existiam sinais de participação, como o **GeoCities** (1994) [^32], que permitia a qualquer pessoa criar sua própria página web dentro de "bairros" temáticos, mas a estrutura ainda era de publicação unidirecional. Com a Web 2.0, a dinâmica mudou de vez. Os usuários passaram a ser produtores de conteúdo, não apenas consumidores.

Os blogs se espalharam como forma de publicação pessoal. O **WordPress** (2003) e o Blogger (comprado pelo Google em 2003) colocaram a publicação na web ao alcance de qualquer pessoa. A **Wikipedia** [^33] foi lançada em 2001 e se tornou o maior exemplo de criação colaborativa de conteúdo da história, com voluntários do mundo inteiro escrevendo e editando artigos em dezenas de idiomas.

O próprio Tim Berners-Lee criticou o termo "Web 2.0", argumentando que a Web sempre foi pensada para ser colaborativa [^31]. E ele tem razão. A diferença não foi conceitual, foi prática: as tecnologias ficaram maduras o suficiente para que essa participação acontecesse em escala.

## O Fenômeno das Redes Sociais

Se a Web 2.0 transformou a internet em um lugar de criação de conteúdo, as redes sociais transformaram a internet em um lugar de conexão entre pessoas. A ideia de perfis, amigos e redes de contatos na internet não é tão nova quanto parece.

O **SixDegrees**, lançado em 1997, é considerado uma das primeiras redes sociais [^34]. O nome faz referência à teoria dos seis graus de separação [^35]. Ele permitia criar perfis, listar amigos e navegar pelas conexões dos seus contatos. Chegou a ter milhões de usuários, mas não conseguiu se manter e fechou em 2000.

O **Friendster** apareceu em 2002 com uma proposta de conectar pessoas através de amigos em comum [^34]. Cresceu rápido, mas sofreu com problemas técnicos na medida em que a base de usuários aumentou.

O **MySpace** (2003) foi um fenômeno cultural, especialmente entre a cena musical e o público adolescente. A possibilidade de customizar o perfil com HTML e CSS (muitas vezes gerando verdadeiras aberrações visuais) e a integração com música fizeram do MySpace a maior rede social do mundo entre 2005 e 2008 [^36].

O **Orkut** foi lançado pelo Google em janeiro de 2004 [^37], criado pelo engenheiro turco Orkut Büyükkökten como um projeto do "20% time" do Google (a política que permitia funcionários dedicarem parte do tempo a projetos pessoais). O Orkut virou um fenômeno no Brasil e na Índia. No Brasil, em especial, a rede se tornou sinônimo de internet para uma geração inteira: comunidades, depoimentos, scraps e a eterna disputa por "quem te adicionou". No auge, a maioria esmagadora do tráfego do Orkut vinha de usuários brasileiros. O Google chegou a transferir a operação do Orkut para o Brasil em 2008. Mas com a ascensão do Facebook, o Orkut perdeu usuários progressivamente e foi encerrado em setembro de 2014.

O **Facebook** surgiu em fevereiro de 2004 [^38], criado por Mark Zuckerberg e colegas na Universidade de Harvard. Começou restrito a estudantes universitários e foi expandindo gradualmente até abrir para o público geral. A introdução do News Feed, a interface limpa e a rede de identidade real foram fatores que fizeram o Facebook ultrapassar o MySpace e se tornar a rede social dominante do planeta.

O **Twitter** apareceu em 2006 [^39], criado por Jack Dorsey e equipe. O conceito de microblogging em tempo real criou uma dinâmica nova: mensagens curtas, públicas, em um fluxo contínuo de informação. O Twitter se tornou uma ferramenta de comunicação instantânea para jornalismo, política e movimentos sociais.

A história das redes sociais também é uma história de fracassos. Para cada Facebook ou Twitter que sobreviveu, dezenas de redes desapareceram. O próprio Google, apesar do sucesso do Orkut no Brasil, nunca conseguiu replicar isso globalmente: o **Google Buzz** (2010) e o **Google+** (2011) foram tentativas de competir com o Facebook que não emplacaram. O **Vine** (2013), que popularizou vídeos de 6 segundos, foi encerrado pelo Twitter em 2017. O **Path** (2010) apostou em uma rede limitada a 150 amigos e não escalou. Redes sociais dependem de efeito de rede: quanto mais gente usa, mais útil fica. E o inverso também é verdade: quando os usuários começam a sair, o êxodo se acelera.

## Smartphones e a Revolução Mobile

Até meados dos anos 2000, acessar a internet significava sentar na frente de um computador. Existiam celulares com acesso à internet (WAP, lembram?), mas a experiência era precária: telas minúsculas, navegadores limitados e conexões lentas.

Em **9 de janeiro de 2007**, Steve Jobs apresentou o iPhone [^40]. Jobs o descreveu como três dispositivos em um: um iPod com tela widescreen, um telefone e um "dispositivo de comunicação com a internet". A tela multi-touch, sem teclado físico nem stylus, mudou a forma como as pessoas interagiam com tecnologia. O Safari do iPhone oferecia uma experiência de navegação na web que era utilizável pela primeira vez em um dispositivo móvel.

Mas o que mudou o jogo de verdade foi a **App Store**, lançada em 2008. De repente, o celular deixou de ser um aparelho para fazer ligações e mandar SMS. Ele virou uma plataforma. Desenvolvedores do mundo inteiro passaram a criar aplicativos que iam de jogos a bancos, de GPS a delivery de comida. A internet saiu do escritório e entrou no bolso.

O Android, do Google, expandiu essa revolução para faixas de preço mais acessíveis, acelerando a adoção global de smartphones. Em poucos anos, para bilhões de pessoas ao redor do mundo, o smartphone se tornou o **primeiro** dispositivo de acesso à internet, e não o computador. Isso é especialmente verdade em países em desenvolvimento, onde o celular chegou antes do PC com acesso à banda larga.

No Brasil, essa transição teve um capítulo próprio. Nos anos 2000, antes da explosão dos smartphones, as **lan houses** foram o principal ponto de acesso à internet para uma enorme parcela da população [^41], especialmente nas periferias. Elas não eram apenas locais de conexão: eram espaços de socialização, jogos em rede e auxílio para trabalhos escolares. Entre 2005 e 2008, as lan houses chegaram a ser a forma mais comum de acesso à internet no Brasil para quem não tinha computador em casa.

Quando o smartphone chegou com preços acessíveis e planos de dados baratos, muitos brasileiros simplesmente pularam a era do PC com banda larga e foram direto para o celular. Não houve aquela transição gradual de desktop para laptop para smartphone que aconteceu em outros países. Para muita gente, o primeiro contato com a internet pessoal foi móvel.

Hoje, cerca de 99% dos internautas brasileiros se conectam pelo celular, e para uma parcela significativa da população o smartphone é o único dispositivo de acesso à rede.

## A Computação em Nuvem

A computação em nuvem parece um conceito abstrato, mas a história da sua criação é bem concreta. A Amazon, no início dos anos 2000, estava lutando para escalar sua infraestrutura de e-commerce [^42]. A empresa percebeu que poderia padronizar e modularizar seus serviços internos de computação e, eventualmente, oferecê-los para terceiros.

Em 2003, Chris Pinkham e Benjamin Black, executivos da Amazon, propuseram a visão de uma infraestrutura automatizada e padronizada que pudesse ser vendida como serviço [^42]. O primeiro bloco dessa visão foi o **Amazon Simple Queue Service (SQS)**, lançado em preview em 2004.

Os dois marcos que realmente inauguraram a era da computação em nuvem vieram em 2006:

- **Amazon S3** (*Simple Storage Service*), lançado em março de 2006 [^43], que resolveu o problema de armazenar grandes volumes de dados de forma confiável e escalável.
- **Amazon EC2** (*Elastic Compute Cloud*), lançado em agosto de 2006 [^43], que permitiu que qualquer pessoa alugasse computadores virtuais sob demanda, pagando apenas pelo que usasse.

A combinação de S3 e EC2 foi o que hoje chamamos de "nuvem". Startups que antes precisavam comprar servidores físicos e montar data centers agora podiam lançar seus produtos com investimento inicial mínimo em infraestrutura. Isso democratizou o acesso a poder computacional de uma forma que antes era restrita a grandes corporações.

Anos depois a Microsoft respondeu com o **Azure**, o Google com o **Google Cloud Platform**, e hoje essas três empresas dominam o mercado de nuvem pública. Em 2014, a Amazon lançou o **AWS Lambda**, popularizando o conceito de computação serverless, onde o desenvolvedor roda código sem nem precisar pensar em servidores.

Para quem está começando na computação, vale o lembrete que o pessoal gosta de brincar: "não existe nuvem, existe o computador de outra pessoa" [^44]. E é verdade. A "nuvem" nada mais é do que data centers enormes espalhados pelo mundo, com milhares de servidores físicos rodando o tempo todo. O que a abstração da nuvem faz é esconder essa complexidade do desenvolvedor e do usuário final.

## O Surgimento do Streaming

A internet não mudou só a forma como acessamos informação. Ela mudou a forma como consumimos música, filmes e séries. E essa história começa com um garoto de 18 anos.

Em 1999, Shawn Fanning lançou o **Napster** [^45]. O Napster permitia que usuários compartilhassem arquivos MP3 diretamente entre si, em um modelo peer-to-peer. Ele não hospedava nenhuma música; apenas mantinha um índice centralizado dos arquivos que cada usuário estava compartilhando. Chegou a 80 milhões de usuários registrados [^45] e provocou um caos na indústria da música.

A RIAA (*Recording Industry Association of America*) processou o Napster por violação de direitos autorais, e o serviço foi fechado em julho de 2001 [^45]. Mas o estrago (do ponto de vista da indústria) já estava feito. O Napster provou que as pessoas queriam acesso instantâneo à música digital. A indústria poderia ter se adaptado mais cedo, mas preferiu brigar na justiça. Isso abriu espaço para serviços sucessores como Gnutella, LimeWire e BitTorrent.

A primeira resposta efetiva mesmo veio com a **iTunes Store** da Apple em 2003, que oferecia músicas individuais por US$0,99. E a resposta definitiva veio com o **Spotify**, fundado em 2006 [^46] e lançado em 2008. O Spotify oferecia um modelo freemium: acesso gratuito com anúncios ou assinatura mensal sem anúncios. A ideia era ser uma alternativa legal e conveniente à pirataria. E funcionou.

No campo do vídeo, existem duas histórias que se entrelaçam. O **YouTube**, que foi lançado em 2005 [^47] e democratizou a publicação de vídeos na internet. Qualquer pessoa com uma câmera (e depois com um celular) podia publicar conteúdo para o mundo inteiro. O Google comprou o YouTube em 2006 por 1,65 bilhão de dólares.

E tem a **Netflix**, que tem uma trajetória diferente. Fundada em 1997 [^48], ela começou como um serviço de aluguel de DVDs pelo correio. Em 2007, deu o salto para streaming de vídeo online. E em 2013, com o lançamento da série *House of Cards*, a Netflix fez algo que ninguém esperava: passou a produzir conteúdo original, competindo diretamente com os estúdios de Hollywood. Essa mudança forçou empresas de mídia tradicionais a lançar suas próprias plataformas de streaming (como Disney+, HBO Max, Apple TV+), o que gerou a "guerra do streaming" que vivemos até hoje.

A Netflix chegou ao Brasil em **setembro de 2011** [^48], com uma assinatura inicial de R$15 por mês. O Brasil foi um dos primeiros mercados da expansão latino-americana da empresa. Em 2016, a Netflix produziu *3%*, sua primeira série original brasileira. Do lado nacional, a TV Globo respondeu com o **Globoplay** em 2015 [^49], digitalizando seu enorme acervo de novelas e jornalismo e apostando na identidade cultural brasileira como diferencial frente às plataformas estrangeiras.

## A Internet das Coisas

Claro que a internet não se limitou a computadores e celulares. Progressivamente, ela foi entrando em objetos que antes não tinham nenhuma conexão com a rede.

O termo **"Internet of Things"** (Internet das Coisas, ou IoT) foi cunhado por Kevin Ashton em 1999 [^49], enquanto trabalhava no MIT. Mas exemplos de dispositivos conectados existem desde antes. Nos anos 80, um grupo de programadores da Carnegie Mellon University modificou uma máquina de Coca-Cola para reportar pela internet se ela ainda tinha latas e se elas estavam geladas [^49]. Era uma solução prática para evitar a frustração de andar até a máquina e descobrir que ela estava vazia.

O conceito ganhou tração de verdade na segunda metade dos anos 2000, quando o número de dispositivos conectados à internet ultrapassou o número de pessoas no planeta [^50]. Termostatos inteligentes como o Nest, pulseiras de atividade como o Fitbit, assistentes de voz como Alexa e Google Home, câmeras de segurança, lâmpadas, geladeiras... a lista de objetos que hoje se conectam à internet é enorme.

A computação em nuvem foi o que viabilizou a IoT em escala. Esses dispositivos geralmente têm capacidade computacional limitada e dependem de serviços na nuvem para processar dados, armazenar informações e tomar decisões.

Mais recentemente, o conceito de *edge computing* (computação na borda) vem ganhando espaço, permitindo que parte do processamento aconteça próximo ao dispositivo, sem precisar enviar tudo para a nuvem, utilizando servidores instalados em centrais regionais de telecomunicações, por exemplo. Isso reduz a latência e aumenta a segurança dos dados. Um exemplo são os veículos autônomos, que precisam tomar decisões em milissegundos e não podem depender de uma conexão de internet para isso.

## Conclusão

De quatro computadores conectados em 1969 para bilhões de dispositivos interconectados hoje. Essa é a trajetória da internet, resumida.

O que chama atenção nessa história é que nenhuma pessoa ou empresa sozinha "inventou" a internet. Ela foi construída em camadas, ao longo de décadas, por pesquisadores, engenheiros, cientistas e programadores em universidades, laboratórios, empresas e garagens ao redor do mundo. Paul Baran pensou em redes distribuídas. Vint Cerf e Bob Kahn criaram o TCP/IP. Tim Berners-Lee inventou a Web. Marc Andreessen trouxe o navegador gráfico. Larry Page e Sergey Brin organizaram a busca. E milhões de outras pessoas contribuíram com código, padrões, infraestrutura e conteúdo.

Cada geração construiu em cima do que a geração anterior deixou. E o que é mais importante: boa parte dessas contribuições foi feita de forma aberta, com protocolos públicos, padrões abertos e software livre. Se a Web tivesse sido patenteada pelo CERN, se o TCP/IP fosse proprietário da DARPA, se o código do Mosaic não tivesse sido acessível, a internet seria algo completamente diferente do que é hoje (se é que existiria).

Hoje estamos entrando em uma nova era, com inteligência artificial generativa, computação quântica e novos desafios de privacidade e governança. Mas a lição das últimas seis décadas é que a internet prospera quando é aberta, distribuída e colaborativa. Toda vez que alguém tentou fechar, centralizar ou monopolizar, a rede encontrou um caminho ao redor.

Para quem lê essa história hoje: tudo isso foi construído em menos de uma vida humana. O que será construído nas próximas décadas ainda está sendo escrito, mas a história mostra que as maiores transformações acontecem quando a tecnologia permite que mais pessoas se conectem, compartilhem e criem juntas.

## Referências

[^1]: **On Distributed Communications** {*Paul Baran, RAND Corporation, 1964*} ([Link](https://www.rand.org/pubs/research_memoranda/RM3420.html))

[^2]: **Packet switching** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Packet_switching))

[^3]: **Donald Davies** {*Internet Hall of Fame*} ([Link](https://www.internethalloffame.org/inductees/donald-davies/))

[^4]: **ARPANET** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/ARPANET))

[^5]: **The first message sent over the ARPANET** {*UCLA*} ([Link](https://www.lk.cs.ucla.edu/internet_first_words.html))

[^6]: **A Brief History of the Internet** {*ICANN*} ([Link](https://www.icann.org/en/history))

[^7]: **A Protocol for Packet Network Intercommunication** {*Cerf & Kahn, IEEE Transactions on Communications, 1974*} ([Link](https://ieeexplore.ieee.org/document/1092259))

[^8]: **TCP/IP - Flag Day** {*Living Internet*} ([Link](https://www.livinginternet.com/i/ii_tcpip.htm))

[^9]: **História da internet no Brasil** {*RNP*} ([Link](https://www.rnp.br/institucional/nossa-historia))

[^10]: **Rede Nacional de Ensino e Pesquisa** {*Wikipedia*} ([Link](https://pt.wikipedia.org/wiki/Rede_Nacional_de_Ensino_e_Pesquisa))

[^11]: **Sobre o CGI.br** {*CGI.br*} ([Link](https://cgi.br/sobre/))

[^12]: **A Short History of the Web** {*CERN*} ([Link](https://home.cern/science/computing/the-birth-of-the-web/short-history-web/))

[^13]: **O primeiro site da Web** {*CERN*} ([Link](https://info.cern.ch/))

[^14]: **Anúncio público da WWW** {*Tim Berners-Lee, 1991*} ([Link](https://www.w3.org/People/Berners-Lee/1991/08/art-6484.txt))

[^15]: **Putting the Web in the public domain** {*CERN, 1993*} ([Link](https://timeline.web.cern.ch/cern-puts-world-wide-web-public-domain))

[^16]: **NCSA Mosaic** {*Living Internet*} ([Link](https://web.archive.org/web/20070702183017/http://www.livinginternet.com/w/wi_mosaic.htm))

[^17]: **Archie search engine** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Archie_(search_engine)))

[^18]: **History of search engines** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Web_search_engine))

[^19]: **Cadê?** {*Wikipedia*} ([Link](https://pt.wikipedia.org/wiki/Cad%C3%AA%3F))

[^20]: **AltaVista** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/AltaVista))

[^21]: **Google** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Google_Search))

[^22]: **The PageRank Citation Ranking: Bringing Order to the Web** {*Larry Page & Sergey Brin, Stanford, 1998*} ([Link](http://infolab.stanford.edu/~page/papers/pagerank/index.htm))

[^23]: **Browser wars** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Browser_wars))

[^24]: **The Internet Tidal Wave** {*Computer History Museum*} ([Link](https://www.computerhistory.org/tdih/may/26/))

[^25]: **The Browser Wars: How Netscape and IE Changed the Internet** {*The History of the Web*} ([Link](https://thehistoryoftheweb.com/))

[^26]: **United States v. Microsoft Corporation** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/United_States_v._Microsoft_Corp.))

[^27]: **The History of Firefox** {*Mozilla*} ([Link](https://www.mozilla.org/en-US/firefox/browsers/browser-history/))

[^28]: **Dot-com bubble** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Dot-com_bubble))

[^29]: **A história da internet no Brasil** {*Revista Ciência & Cultura*} ([Link](https://revistacienciaecultura.org.br/?p=7699))

[^30]: **iG** {*Wikipedia*} ([Link](https://pt.wikipedia.org/wiki/IG))

[^31]: **Web 2.0** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Web_2.0))

[^32]: **GeoCities** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/GeoCities))

[^33]: **Wikipedia** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Wikipedia))

[^34]: **The History of Social Networking** {*Britannica*} ([Link](https://www.britannica.com/topic/social-network))

[^35]: **Six degrees of separation** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Six_degrees_of_separation))

[^36]: **MySpace** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Myspace))

[^37]: **Orkut** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Orkut))

[^38]: **Facebook** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Facebook))

[^39]: **Twitter** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Twitter,_Inc.))

[^40]: **iPhone at 10: How Steve Jobs Transformed the World** {*The Guardian, 2017*} ([Link](https://www.theguardian.com/technology/2017/jun/29/iphone-at-10-how-it-changed-everything))

[^41]: **Pesquisa TIC Domicílios** {*NIC.br / CETIC.br*} ([Link](https://cetic.br/pt/pesquisa/domicilios/))

[^42]: **Amazon Web Services** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Amazon_Web_Services))

[^43]: **Timeline of Amazon Web Services** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Timeline_of_Amazon_Web_Services))

[^44]: **Napster** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Napster))

[^45]: **About Spotify** {*Spotify*} ([Link](https://newsroom.spotify.com/company-info/))

[^46]: **YouTube** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/YouTube))

[^47]: **Netflix** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Netflix))

[^48]: **Globoplay** {*Wikipedia*} ([Link](https://pt.wikipedia.org/wiki/Globoplay))

[^49]: **A Brief History of the Internet of Things** {*Dataversity*} ([Link](https://www.dataversity.net/brief-history-internet-things/))

[^50]: **The history of IoT: From concept to reality** {*Thales Group*} ([Link](https://www.thalesgroup.com/en/news-centre/insights/enterprise/mobile-communications/history-iot-concept-reality))

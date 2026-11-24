---
layout: post
title: "Uma Breve História da Internet"
subtitle: "Das redes militares da ARPANET nos anos 60 à era do streaming e da computação em nuvem"
author:
- "Eduardo N. S. R."
date: 2026-07-31 12:40:00 GMT-3
modified_date: 2026-11-24 19:27:44 GMT-3
permalink: /posts/historia-internet/
tags: [Internet, Web, História, Redes]
category: Artigos
---

A internet é uma dessas coisas que a gente usa o dia inteiro sem parar pra pensar no que tem por baixo. A gente acorda, olha o celular, entra no Instagram, assiste um vídeo no YouTube, manda mensagem no WhatsApp, pede comida, carro e até hospedagem por aplicativo, e tudo isso acontece em cima de uma rede que levou décadas pra chegar onde está. E a história de como isso tudo foi construído é das mais interessantes da computação.

A ideia desse post é contar essa história de uma forma razoavelmente acessível, passando pelos momentos que eu considero mais marcantes na trajetória da internet. Não é um tratado acadêmico e nem pretende ser exaustivo. É mais um passeio cronológico que vai das redes militares dos anos 60 até o streaming e a Internet das Coisas. Considere esse texto como um mapa de onde as coisas vieram e de como essa infraestrutura que usamos todos os dias foi construída.

> [!NOTE] Nota de Mea Culpa
> Ok, admito que no fim das contas a história não ficou tão breve assim. Quando comecei a juntar as peças, percebi que resumir seis décadas de evolução sem perder os detalhes importantes ia exigir bem mais do que um post rápido. Tive um trabalho considerável de pesquisa para compilar, organizar e cruzar dezenas de fontes em uma linha do tempo única, tentando entregar tudo de forma direta pra você (claro, com uma ajudinha de IA para ajudar a localizar fontes e organizar as ideias). Aliás, não deixe de conferir as referências no final.

{% include toc.html title="Linha do Tempo & Sumário das Fases" %}


## As Raízes da Internet: Comutação de Pacotes e a Guerra Fria

Volte aos anos 1960, em plena Guerra Fria: o problema militar era manter comunicações de pé num ataque nuclear, já que redes de circuitos dedicados morriam com um único fio cortado.

Foi aí que Paul Baran, engenheiro da RAND Corporation, publicou entre 1960 e 1964 a série *"On Distributed Communications"* [^1], propondo quebrar mensagens em blocos menores (*message blocks*) trafegando por caminhos distintos numa malha que se reorganizava sozinha ao redor de pontos danificados ou congestionados.

Do outro lado do Atlântico, sem saber de Baran, Donald Davies chegou às mesmas conclusões no NPL (Inglaterra, 1965) [^2] e cunhou **"packet"** e **"packet switching"** [^3].

Os dois pesquisadores trabalharam de forma independente, mas quando suas pesquisas se cruzaram, a comunidade percebeu que tinha em mãos um conceito poderoso. Lawrence Roberts, que viria a ser uma figura central no projeto da ARPANET, incorporou a terminologia e os conceitos de Davies no projeto estadunidense [^2].

## ARPANET: A Primeira Rede

A ARPANET foi o primeiro grande experimento prático de comutação de pacotes, financiado pela ARPA [^4] (agência de pesquisa do Departamento de Defesa dos EUA) sob arquitetura de Lawrence Roberts.

A primeira conexão aconteceu em **29 de outubro de 1969** [^5], entre um computador na Universidade da Califórnia em Los Angeles (UCLA) e outro no Stanford Research Institute (SRI). A equipe era liderada pelo professor Leonard Kleinrock na UCLA, e o estudante Charley Kline ficou responsável por enviar a primeira mensagem. O plano era digitar "LOGIN" para se conectar remotamente ao computador de Stanford.

O sistema caiu na segunda letra. A primeira mensagem da ARPANET foi **"LO"** [^5] (uma hora depois eles restabeleceram o link e completaram o comando).

Até o final de 1969, a rede já tinha quatro nós: UCLA, SRI, UC Santa Barbara e a Universidade de Utah [^4]. A conexão entre esses computadores usava equipamentos chamados Interface Message Processors (IMPs), desenvolvidos pela empresa Bolt, Beranek and Newman (BBN) [^6]. Os IMPs são, na prática, os ancestrais dos roteadores modernos.

## O Surgimento do TCP/IP

A ARPANET cresceu e esbarrou na interoperabilidade: cada rede falava um dialeto próprio e o protocolo NCP não fora feito para ligar redes distintas.

Em 1974, Vint Cerf e Bob Kahn publicaram um paper que seria um marco na história das redes: *"A Protocol for Packet Network Intercommunication"* [^7]. Nesse artigo, eles propuseram um protocolo de "arquitetura aberta" que pudesse conectar redes heterogêneas através de gateways. O protocolo foi batizado inicialmente de Transmission Control Program (TCP).

O design de Cerf e Kahn bebeu fundo na rede francesa **CYCLADES**, liderada por Louis Pouzin nos anos 1970 [^8]. A CYCLADES trouxe o conceito de **datagrama**, jogando a responsabilidade pela entrega confiável para os computadores das pontas (o princípio fim-a-fim, ou *end-to-end*). O mecanismo de janela deslizante para controle de fluxo, criado pela equipe de Pouzin, entrou direto no desenho do TCP/IP.

Em 1978, o TCP monolítico foi separado em duas camadas: **TCP** (entrega confiável e ordenada) e **IP** (roteamento até o destino). Nascia o **TCP/IP**.

A virada definitiva veio em **1º de janeiro de 1983**, o "Flag Day" [^9]: a ARPANET migrou de NCP para TCP/IP de uma tacada só, sem transição. Quem não migrou ficou de fora. É essa data que muita gente marca como o nascimento real da internet (*inter-net*, rede de redes interconectadas sob um protocolo comum).

## A Internet Chega ao Brasil

No Brasil, o pontapé foi em 1988: FAPESP (São Paulo) e LNCC (Rio de Janeiro) fecharam as primeiras conexões internacionais via Bitnet para e-mail e arquivos [^10].

Em 1989, o Ministério da Ciência e Tecnologia criou a **RNP** (Rede Nacional de Pesquisa) [^11] para erguer um backbone nacional ligando universidades e centros de pesquisa. A primeira conexão TCP/IP brasileira veio em 1991, pela FAPESP, ainda restrita ao meio acadêmico.

A abertura comercial chegou em **1995**, com a criação do **CGI.br** (Comitê Gestor da Internet no Brasil) [^12] e os primeiros projetos de acesso discado da Embratel, abrindo caminho para os provedores comerciais nas casas brasileiras.

## A World Wide Web

Ter uma rede global de pé é uma coisa; deixá-la usável para pessoas comuns é outra. Nos anos 80, a internet era território de pesquisadores e militares (e-mail, FTP, Usenet).

Essa camada faltante nasceu das mãos de Tim Berners-Lee [^13], no CERN (Suíça). Em março de 1989, ele escreveu *"Information Management: A Proposal"*, descrevendo um sistema de documentos ligados por hiperlinks sobre a internet, batizado primeiro de "Mesh" e depois de World Wide Web.

No fim de 1990, já rodavam o primeiro servidor web, o navegador WorldWideWeb e a tríade HTML, HTTP e URIs. O primeiro site da história (`info.cern.ch` [^14]) ainda está no ar, e em agosto de 1991 Berners-Lee anunciou a Web no newsgroup `alt.hypertext` [^15], convidando o mundo a construir em cima.

Detalhei essa evolução técnica em {% include post-ref.html slug="evolucao-http" text="Evolução do Protocolo HTTP e da World Wide Web" %}.

Um fator que não dá pra ignorar na expansão da Web foi a decisão do CERN, em **30 de abril de 1993**, de liberar o software da World Wide Web para o domínio público [^16]. Se o CERN tivesse decidido cobrar licenças ou patentear a tecnologia, é provável que a Web como conhecemos simplesmente não existisse. Essa decisão garantiu que a tecnologia fosse aberta, e qualquer pessoa ou instituição pudesse construir em cima dela.

Pouco tempo depois, em 1993, surgiu o **NCSA Mosaic** [^17], o primeiro navegador com interface gráfica que rodava em Windows e Mac. Desenvolvido por Marc Andreessen e sua equipe na Universidade de Illinois, o Mosaic foi o responsável por popularizar a Web com o público geral. Até então, navegar na internet era coisa de terminal de texto. O Mosaic abriu as portas para milhões de pessoas.

## Os Primeiros Buscadores

Com a Web crescendo em ritmo acelerado, bateu uma pergunta óbvia: como achar qualquer coisa ali dentro?

Antes mesmo da Web existir nesse formato, o **Archie** (1990) [^18] resolveu uma ponta do problema indexando nomes de arquivos em servidores FTP públicos. Era um catálogo de diretórios de arquivos, simples e útil.

Quando a Web explodiu, vieram soluções feitas pra ela. O **Yahoo!**, lançado em 1994, operava como diretório curado por humanos [^19]: páginas organizadas na mão em categorias, tipo catálogo de biblioteca. Funcionou enquanto a Web cabia na prateleira; depois, escalar curadoria manual ficou inviável.

No Brasil, o equivalente do Yahoo! foi o **Cadê?**, criado em 1995 por Gustavo Viberti e Fábio de Oliveira [^20]. O Cadê? funcionava da mesma forma: uma catalogação manual de sites brasileiros, organizada por categorias. Para quem usava internet no Brasil nessa época, o Cadê? era o ponto de partida para encontrar qualquer coisa em português na Web. O serviço foi vendido para a StarMedia em 1999 e depois comprado pelo Yahoo! Brasil em 2002, desaparecendo gradualmente com a chegada do Google.

Em 1995, o **AltaVista** representou um salto técnico [^21]. Ele foi um dos primeiros buscadores a usar um crawler (um programa que navega automaticamente de página em página, seguindo links) para indexar o conteúdo das páginas e não só seus títulos ou diretórios. Isso permitia buscas por palavras-chave em um volume enorme de páginas.

O **Google** surgiu em 1998, fundado por Larry Page e Sergey Brin, dois doutorandos de Stanford [^22]. O diferencial do Google foi o algoritmo **PageRank** [^23], que em vez de ranquear páginas apenas pelo conteúdo textual, ranqueava pela quantidade e qualidade de links que apontavam para elas. A lógica era que uma página referenciada por muitas outras páginas relevantes provavelmente era mais confiável. Enquanto os concorrentes se transformavam em portais cheios de notícias, horóscopo e propaganda, o Google manteve uma interface limpa e focada na busca. Essa combinação de qualidade de resultado com simplicidade de uso definiu a era da busca na internet.

## A Guerra dos Navegadores

Enquanto os buscadores disputavam a atenção dos usuários, outra guerra acontecia em paralelo. A chamada "Guerra dos Navegadores" (ou *Browser War*) foi um dos episódios mais marcantes dos anos 90 na internet.

O protagonista inicial era o **Netscape Navigator**, que surgiu em 1994 e rapidamente dominou o mercado, chegando a ter entre 70% e 90% de participação [^24]. O Netscape era o navegador que a maioria das pessoas usava para acessar a Web. Marc Andreessen, o mesmo criador do Mosaic, era cofundador da Netscape Communications.

A Microsoft demorou a acordar para a internet. A virada veio em 1995, com o memorando interno de Bill Gates *"The Internet Tidal Wave"* [^25], reconhecendo a rede como a maior mudança desde o IBM PC.

A resposta foi criar o **Internet Explorer** e embutir o navegador direto no Windows. Como todo PC já saía de fábrica com o IE de graça, o modelo de licenças pagas da Netscape desabou [^26], agravado pela pressão da Microsoft sobre fabricantes e provedores para limitar a distribuição do rival.

Em 1998, o Departamento de Justiça dos Estados Unidos processou a Microsoft por práticas antitruste [^27], acusando-a de usar o monopólio do Windows para esmagar a concorrência nos navegadores. Os tribunais confirmaram a conduta anticompetitiva; a proposta de fatiar a empresa caiu, mas a Microsoft teve que recuar em várias práticas comerciais.

A Netscape não sobreviveu. Foi comprada pela AOL em 1999. Mas antes de desaparecer, fez algo que teria consequências profundas: liberou o código-fonte do seu navegador como software de código aberto [^28]. Desse código nasceu o projeto **Mozilla**, que anos depois daria origem ao **Firefox**. A Guerra dos Navegadores terminou com a Microsoft vencendo a batalha, mas semeou o terreno para o movimento de código aberto nos navegadores que culminaria, anos depois, na diversidade de navegadores que temos hoje, com Chrome, Firefox, Safari e outros.

## A Bolha Pontocom (e o seu estouro)

A expansão da Web nos anos 90 disparou uma euforia cega no mercado financeiro: se tivesse ".com" no nome, o dinheiro dos fundos jorrava.

O índice Nasdaq, pesado em tecnologia, disparou cerca de 600% entre 1995 e 2000 [^29]. Em vez de lucro ou fluxo de caixa, o mercado precificava "cliques", "eyeballs" e participação de mercado sob o mantra "Get Big Fast": queimar caixa sem freio para crescer antes dos rivais, mesmo no prejuízo.

Em março de 2000, a bolha estourou. Até outubro de 2002, a Nasdaq perdeu mais de 75% do valor, evaporando cerca de 5 trilhões de dólares [^29] e enterrando símbolos da época como a Pets.com da noite para o dia.

No Brasil, o cenário tinha suas particularidades. O **UOL** (Universo Online), lançado em 1996 pelo Grupo Folha [^30], era o grande portal brasileiro: provedor de acesso, conteúdo, e-mail, chat, tudo num lugar só. O **iG** (Internet Group) apareceu em janeiro de 2000 e mexeu bastante o mercado ao oferecer acesso gratuito à internet [^31]. O usuário pagava apenas a ligação telefônica, o que democratizou o acesso em um momento em que a assinatura mensal dos provedores ainda era cara para muita gente.

O **Submarino** surgiu como um dos primeiros grandes e-commerces brasileiros, sobreviveu à bolha e anos depois se juntou a outras operações para formar a B2W [^30]. Assim como nos Estados Unidos, a crise filtrou quem tinha um modelo de negócio sustentável e quem estava apenas surfando a euforia.

No Brasil daquela época, conectar tinha ritual: modem 56k chiando, telefone ocupado com a família reclamando e a espera pela meia-noite pra pagar um único pulso.

Mesmo com a quebradeira, a bolha deixou herança útil: fibra óptica e data centers já pagos, que serviram de pista para sobreviventes como Amazon e Google virarem gigantes.

## A Web 2.0 e o Conteúdo Gerado pelo Usuário

Depois que a poeira da bolha baixou, a Web mudou de cara. Em 2004, Tim O'Reilly popularizou o termo **"Web 2.0"** [^32] para descrever uma mudança que já estava em andamento: a Web deixava de ser um lugar onde você ia para ler informação e passava a ser um lugar onde você também criava conteúdo.

Na Web dos anos 90 (que retroativamente passou a ser chamada de "Web 1.0"), a maioria dos sites era estática. Alguém publicava uma página e você lia. A interação era mínima. Já existiam sinais de participação, como o **GeoCities** (1994) [^33], que permitia a qualquer pessoa criar sua própria página web dentro de "bairros" temáticos, mas a estrutura ainda era de publicação unidirecional. Com a Web 2.0, a dinâmica mudou de vez. Os usuários passaram a ser produtores de conteúdo, não apenas consumidores.

Os blogs se espalharam como forma de publicação pessoal. O **WordPress** (2003) e o Blogger (comprado pelo Google em 2003) colocaram a publicação na web ao alcance de qualquer pessoa. A **Wikipedia** [^34] foi lançada em 2001 e se tornou o maior exemplo de criação colaborativa de conteúdo da história, com voluntários do mundo inteiro escrevendo e editando artigos em dezenas de idiomas.

O próprio Tim Berners-Lee criticou o termo "Web 2.0", argumentando que a Web sempre foi pensada para ser colaborativa [^32]. E ele tem razão. A diferença não foi conceitual, foi prática: as tecnologias ficaram maduras o suficiente para que essa participação acontecesse em escala.

## O Fenômeno das Redes Sociais

Se a Web 2.0 transformou a internet em um lugar de criação de conteúdo, as redes sociais transformaram a internet em um lugar de conexão entre pessoas. A ideia de perfis, amigos e redes de contatos na internet não é tão nova quanto parece.

Lançado em 1997, o **SixDegrees** é considerado uma das primeiras redes sociais [^35], inspirado nos seis graus de separação [^36]. Permitia perfis, lista de amigos e navegação por contatos; bateu milhões de usuários, mas fechou em 2000.

O **Friendster** apareceu em 2002 conectando pessoas via amigos em comum [^35], cresceu rápido e travou nos próprios problemas técnicos de escala.

Em 2003 veio o **MySpace**, fenômeno cultural entre bandas e adolescentes: perfis customizados em HTML e CSS (muitas vezes aberrações visuais memoráveis) o mantiveram como maior rede social do mundo entre 2005 e 2008 [^37].

Em janeiro de 2004, o Google lançou o **Orkut** [^38], nascido no "20% time" do engenheiro turco Orkut Büyükkökten. No Brasil e na Índia virou febre: comunidades, depoimentos, scraps e a novela de "quem visitou seu perfil" fizeram os brasileiros dominarem o tráfego da rede. O Google chegou a mover a operação para o Brasil em 2008, mas com a ascensão do Facebook o serviço foi definhando até fechar em setembro de 2014.

No mês seguinte (fevereiro de 2004), Mark Zuckerberg e colegas lançaram o **Facebook** em Harvard [^39]. Começou restrito a universitários, abriu ao público e, com News Feed, interface limpa e identidade real, atropelou o MySpace para dominar o planeta.

Dois anos depois (2006), Jack Dorsey e equipe tiraram do forno o **Twitter** [^40], criando o microblogging em tempo real que mudou a dinâmica do jornalismo, da política e dos movimentos sociais.

A história das redes sociais também é uma história de fracassos. Para cada Facebook ou Twitter que sobreviveu, dezenas de redes desapareceram. O próprio Google, apesar do sucesso do Orkut no Brasil, nunca conseguiu replicar isso globalmente: o **Google Buzz** (2010) e o **Google+** (2011) foram tentativas de competir com o Facebook que não emplacaram. O **Vine** (2013), que popularizou vídeos de 6 segundos, foi encerrado pelo Twitter em 2017. O **Path** (2010) apostou em uma rede limitada a 150 amigos e não escalou. Redes sociais dependem de efeito de rede: quanto mais gente usa, mais útil fica. E o inverso também é verdade: quando os usuários começam a sair, o êxodo se acelera.

## Smartphones e a Revolução Mobile

Até meados dos anos 2000, acessar a internet significava sentar na frente de um computador. Existiam celulares com acesso à internet (WAP, lembram?), mas a experiência era precária: telas minúsculas, navegadores limitados e conexões lentas.

Em **9 de janeiro de 2007**, Steve Jobs apresentou o iPhone [^41]: um iPod widescreen, um telefone e um "dispositivo de comunicação com a internet". A tela multi-touch sem teclado nem stylus, somada a um Safari realmente navegável, virou a chave do mercado móvel.

Mas o golpe decisivo veio em 2008, com a **App Store**: o celular virou plataforma e a internet saiu do escritório pro bolso.

O Android, do Google, levou essa onda a faixas de preço acessíveis e fez do smartphone o **primeiro** acesso à internet para bilhões de pessoas (principalmente em países em desenvolvimento, onde o celular chegou antes do PC com banda larga).

No Brasil, essa transição teve um capítulo próprio. Nos anos 2000, antes da explosão dos smartphones, as **lan houses** foram o principal ponto de acesso à internet para uma enorme parcela da população [^42], especialmente nas periferias. Elas não eram apenas locais de conexão: eram espaços de socialização, jogos em rede e auxílio para trabalhos escolares. Entre 2005 e 2008, as lan houses chegaram a ser a forma mais comum de acesso à internet no Brasil para quem não tinha computador em casa.

Quando o smartphone chegou com preços acessíveis e planos de dados baratos, muitos brasileiros simplesmente pularam a era do PC com banda larga e foram direto para o celular. Não houve aquela transição gradual de desktop para laptop para smartphone que aconteceu em outros países. Para muita gente, o primeiro contato com a internet pessoal foi móvel.

Hoje, cerca de 99% dos internautas brasileiros se conectam pelo celular, e para uma parcela significativa da população o smartphone é o único dispositivo de acesso à rede.

## A Computação em Nuvem

A computação em nuvem parece um conceito abstrato, mas a história da sua criação é bem concreta. A Amazon, no início dos anos 2000, estava lutando para escalar sua infraestrutura de e-commerce [^43]. A empresa percebeu que poderia padronizar e modularizar seus serviços internos de computação e, eventualmente, oferecê-los para terceiros.

Em 2003, Chris Pinkham e Benjamin Black, executivos da Amazon, propuseram a visão de uma infraestrutura automatizada e padronizada que pudesse ser vendida como serviço [^43]. O primeiro bloco dessa visão foi o **Amazon Simple Queue Service (SQS)**, lançado em preview em 2004.

Os dois marcos que realmente inauguraram a era da computação em nuvem vieram em 2006:

- **Amazon S3** (*Simple Storage Service*), lançado em março de 2006 [^44], que resolveu o problema de armazenar grandes volumes de dados de forma confiável e escalável.
- **Amazon EC2** (*Elastic Compute Cloud*), lançado em agosto de 2006 [^44], que permitiu que qualquer pessoa alugasse computadores virtuais sob demanda, pagando apenas pelo que usasse.

S3 e EC2 inauguraram o que hoje chamamos de "nuvem": startups passaram a subir produtos sem comprar servidores físicos nem montar data center próprio.

Anos depois a Microsoft respondeu com o **Azure**, o Google com o **Google Cloud Platform**, e hoje essas três empresas dominam o mercado de nuvem pública. Em 2014, a Amazon lançou o **AWS Lambda**, popularizando o conceito de computação serverless, onde o desenvolvedor roda código sem nem precisar pensar em servidores.

Para quem está começando na computação, vale o lembrete que o pessoal gosta de brincar: "não existe nuvem, existe o computador de outra pessoa" [^45]. E é verdade. A "nuvem" nada mais é do que data centers enormes espalhados pelo mundo, com milhares de servidores físicos rodando o tempo todo. O que a abstração da nuvem faz é esconder essa complexidade do desenvolvedor e do usuário final.

## O Surgimento do Streaming

A internet não mudou só a forma como acessamos informação. Ela mudou a forma como consumimos música, filmes e séries. E essa história começa com um garoto de 18 anos.

Em 1999, Shawn Fanning lançou o **Napster** [^46], permitindo compartilhar MP3 em peer-to-peer sem hospedar música nenhuma (só mantinha o índice central). Bateu 80 milhões de usuários [^46] e virou a indústria fonográfica de cabeça para baixo.

A RIAA (*Recording Industry Association of America*) processou o Napster e derrubou o serviço em julho de 2001 [^46]. Tarde demais: o público já tinha provado acesso instantâneo à música digital, e a teimosia judicial da indústria só abriu caminho para Gnutella, LimeWire e BitTorrent.

A resposta comercial começou na **iTunes Store** (2003, faixas a US$0,99) e se firmou com o **Spotify** (2006 [^47], lançado em 2008), vencendo a pirataria pela conveniência.

No campo do vídeo, existem duas histórias que se entrelaçam. O **YouTube**, que foi lançado em 2005 [^48] e democratizou a publicação de vídeos na internet. Qualquer pessoa com uma câmera (e depois com um celular) podia publicar conteúdo para o mundo inteiro. O Google comprou o YouTube em 2006 por 1,65 bilhão de dólares.

E tem a **Netflix**, que tem uma trajetória diferente. Fundada em 1997 [^49], ela começou como um serviço de aluguel de DVDs pelo correio. Em 2007, deu o salto para streaming de vídeo online. E em 2013, com o lançamento da série *House of Cards*, a Netflix fez algo que ninguém esperava: passou a produzir conteúdo original, competindo diretamente com os estúdios de Hollywood. Essa mudança forçou empresas de mídia tradicionais a lançar suas próprias plataformas de streaming (como Disney+, HBO Max, Apple TV+), o que gerou a "guerra do streaming" que vivemos até hoje.

A Netflix chegou ao Brasil em **setembro de 2011**, com uma assinatura inicial de R$15 por mês. O Brasil foi um dos primeiros mercados da expansão latino-americana da empresa. Em 2016, a Netflix produziu *3%*, sua primeira série original brasileira. Do lado nacional, a TV Globo respondeu com o **Globoplay** em 2015 [^50], digitalizando seu enorme acervo de novelas e jornalismo e apostando na identidade cultural brasileira como diferencial frente às plataformas estrangeiras.

## A Internet das Coisas

Claro que a internet não se limitou a computadores e celulares. Progressivamente, ela foi entrando em objetos que antes não tinham nenhuma conexão com a rede.

O termo **"Internet of Things"** (Internet das Coisas, ou IoT) foi cunhado por Kevin Ashton em 1999 [^51], enquanto trabalhava no MIT. Mas exemplos de dispositivos conectados existem desde antes. Nos anos 80, um grupo de programadores da Carnegie Mellon University modificou uma máquina de Coca-Cola para reportar pela internet se ela ainda tinha latas e se elas estavam geladas [^52]. Era uma solução prática para evitar a frustração de andar até a máquina e descobrir que ela estava vazia.

O conceito ganhou tração de verdade na segunda metade dos anos 2000, quando o número de dispositivos conectados à internet ultrapassou o número de pessoas no planeta [^53]. Termostatos inteligentes como o Nest, pulseiras de atividade como o Fitbit, assistentes de voz como Alexa e Google Home, câmeras de segurança, lâmpadas, geladeiras... a lista de objetos que hoje se conectam à internet é enorme.

A computação em nuvem foi o que viabilizou a IoT em escala. Esses dispositivos geralmente têm capacidade computacional limitada e dependem de serviços na nuvem para processar dados, armazenar informações e tomar decisões.

Mais recentemente, o conceito de *edge computing* (computação na borda) [^54] vem ganhando espaço, permitindo que parte do processamento aconteça próximo ao dispositivo, sem precisar enviar tudo para a nuvem, utilizando servidores instalados em centrais regionais de telecomunicações, por exemplo. Isso reduz a latência e aumenta a segurança dos dados. Um exemplo são os veículos autônomos, que precisam tomar decisões em milissegundos e não podem depender de uma conexão de internet para isso.

## Conclusão

De quatro computadores conectados em 1969 para bilhões de dispositivos interconectados hoje. Essa é a trajetória da internet, resumida.

O que chama atenção nessa história é que nenhuma pessoa ou empresa sozinha "inventou" a internet. Ela foi construída em camadas, ao longo de décadas, por pesquisadores, engenheiros, cientistas e programadores em universidades, laboratórios, empresas e garagens ao redor do mundo. Paul Baran pensou em redes distribuídas. Vint Cerf e Bob Kahn criaram o TCP/IP. Tim Berners-Lee inventou a Web. Marc Andreessen trouxe o navegador gráfico. Larry Page e Sergey Brin organizaram a busca. E milhões de outras pessoas contribuíram com código, padrões, infraestrutura e conteúdo.

Cada geração construiu em cima do que a geração anterior deixou. E o que é mais importante: boa parte dessas contribuições foi feita de forma aberta, com protocolos públicos, padrões abertos e software livre. Se a Web tivesse sido patenteada pelo CERN, se o TCP/IP fosse proprietário da DARPA, se o código do Mosaic não tivesse sido acessível, a internet seria algo irreconhecível (se é que existiria).

Hoje entramos em outra virada, com IA generativa, computação quântica e novas disputas de privacidade e governança. Ainda assim, a lição de seis décadas continua de pé: toda vez que alguém tentou cercar ou monopolizar a rede, ela deu a volta.

Tudo isso aconteceu em menos de uma vida humana. O resto ainda está em aberto.

## Referências

[^1]: **On Distributed Communications** {*Paul Baran, RAND Corporation, 1964*} ([Link](https://www.rand.org/pubs/research_memoranda/RM3420.html))

[^2]: **Packet switching** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Packet_switching))

[^3]: **Donald Davies** {*Internet Hall of Fame*} ([Link](https://www.internethalloffame.org/inductees/donald-davies/))

[^4]: **ARPANET** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/ARPANET))

[^5]: **The first message sent over the ARPANET** {*UCLA*} ([Link](https://www.lk.cs.ucla.edu/internet_first_words.html))

[^6]: **A Brief History of the Internet** {*ICANN*} ([Link](https://www.icann.org/en/history))

[^7]: **A Protocol for Packet Network Intercommunication** {*Cerf & Kahn, IEEE Transactions on Communications, 1974*} ([Link](https://ieeexplore.ieee.org/document/1092259))

[^8]: **Inventing the Internet** {*Janet Abbate, MIT Press, 1999, p. 125*} ([Link](https://books.google.com.br/books?id=E2BdY6WQo4AC&pg=PA125))

[^9]: **TCP/IP - Flag Day** {*Living Internet*} ([Link](https://www.livinginternet.com/i/ii_tcpip.htm))

[^10]: **História da internet no Brasil** {*RNP*} ([Link](https://www.rnp.br/institucional/nossa-historia))

[^11]: **Rede Nacional de Ensino e Pesquisa** {*Wikipedia*} ([Link](https://pt.wikipedia.org/wiki/Rede_Nacional_de_Ensino_e_Pesquisa))

[^12]: **Sobre o CGI.br** {*CGI.br*} ([Link](https://cgi.br/sobre/))

[^13]: **A Short History of the Web** {*CERN*} ([Link](https://home.cern/science/computing/the-birth-of-the-web/short-history-web/))

[^14]: **O primeiro site da Web** {*CERN*} ([Link](https://info.cern.ch/))

[^15]: **Anúncio público da WWW** {*Tim Berners-Lee, 1991*} ([Link](https://www.w3.org/People/Berners-Lee/1991/08/art-6484.txt))

[^16]: **Putting the Web in the public domain** {*CERN, 1993*} ([Link](https://timeline.web.cern.ch/cern-puts-world-wide-web-public-domain))

[^17]: **NCSA Mosaic** {*Living Internet*} ([Link](https://web.archive.org/web/20070702183017/http://www.livinginternet.com/w/wi_mosaic.htm))

[^18]: **Archie search engine** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Archie_%28search_engine%29))

[^19]: **History of search engines** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Web_search_engine))

[^20]: **Cadê?** {*Wikipedia*} ([Link](https://pt.wikipedia.org/wiki/Cad%C3%AA%3F))

[^21]: **AltaVista** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/AltaVista))

[^22]: **Google** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Google_Search))

[^23]: **The PageRank Citation Ranking: Bringing Order to the Web** {*Larry Page & Sergey Brin, Stanford, 1998*} ([Link](http://infolab.stanford.edu/~page/papers/pagerank/index.htm))

[^24]: **Browser wars** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Browser_wars))

[^25]: **The Internet Tidal Wave** {*Computer History Museum*} ([Link](https://www.computerhistory.org/tdih/may/26/))

[^26]: **The Browser Wars: How Netscape and IE Changed the Internet** {*The History of the Web*} ([Link](https://thehistoryoftheweb.com/))

[^27]: **United States v. Microsoft Corporation** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/United_States_v._Microsoft_Corp.))

[^28]: **The History of Firefox** {*Mozilla*} ([Link](https://www.mozilla.org/en-US/firefox/browsers/browser-history/))

[^29]: **Dot-com bubble** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Dot-com_bubble))

[^30]: **A história da internet no Brasil** {*Revista Ciência & Cultura*} ([Link](https://revistacienciaecultura.org.br/?p=7699))

[^31]: **iG** {*Wikipedia*} ([Link](https://pt.wikipedia.org/wiki/IG))

[^32]: **Web 2.0** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Web_2.0))

[^33]: **GeoCities** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/GeoCities))

[^34]: **Wikipedia** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Wikipedia))

[^35]: **The History of Social Networking** {*Britannica*} ([Link](https://www.britannica.com/topic/social-network))

[^36]: **Six degrees of separation** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Six_degrees_of_separation))

[^37]: **MySpace** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Myspace))

[^38]: **Orkut** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Orkut))

[^39]: **Facebook** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Facebook))

[^40]: **Twitter** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Twitter,_Inc.))

[^41]: **iPhone at 10: How Steve Jobs Transformed the World** {*The Guardian, 2017*} ([Link](https://www.theguardian.com/technology/2017/jun/29/iphone-at-10-how-it-changed-everything))

[^42]: **Pesquisa TIC Domicílios** {*NIC.br / CETIC.br*} ([Link](https://cetic.br/pt/pesquisa/domicilios/))

[^43]: **Amazon Web Services** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Amazon_Web_Services))

[^44]: **Timeline of Amazon Web Services** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Timeline_of_Amazon_Web_Services))

[^45]: **There is no cloud, it's just someone else's computer** {*Chris Watterston*} ([Link](https://www.chriswatterston.com/article/success-of-my-there-is-no-cloud-sticker))

[^46]: **Napster** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Napster))

[^47]: **About Spotify** {*Spotify*} ([Link](https://newsroom.spotify.com/company-info/))

[^48]: **YouTube** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/YouTube))

[^49]: **Netflix** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Netflix))

[^50]: **Globoplay** {*Wikipedia*} ([Link](https://pt.wikipedia.org/wiki/Globoplay))

[^51]: **A Brief History of the Internet of Things** {*Dataversity*} ([Link](https://www.dataversity.net/brief-history-internet-things/))

[^52]: **Decoding the Internet of Things** {*Carnegie Mellon University, School of Computer Science*} ([Link](https://csd.cmu.edu/news/decoding-the-internet-of-things))

[^53]: **The history of IoT: From concept to reality** {*Thales Group*} ([Link](https://www.thalesgroup.com/en/news-centre/insights/enterprise/mobile-communications/history-iot-concept-reality))

[^54]: **History of edge computing** {*TechRepublic*} ([Link](https://www.techrepublic.com/article/edge-computing-history/))

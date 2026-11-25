---
layout: post
title: "Não Somos Ninguém Porque Ninguém é Perfeito"
subtitle: "De quando a gente achava que a internet ia libertar o mundo até a distopia cyberpunk que ela acabou virando"
author:
  - "Eduardo N. S. R."
date: 2026-11-20 22:36:00 GMT-3
modified_date: 2026-11-25 07:54:29 GMT-3
permalink: /posts/ensaio-hacktivismo/
category: Ensaios
tags: [Segurança, Hacktivismo, Engenharia Social, Ciberguerra, Conhecimento Livre]
---

Outro dia eu estava jogando conversa fora com um colega sobre gente que embarca de cabeça em teoria da conspiração. No meio da risada, ele soltou uma frase que ficou martelando na minha cabeça: "tenho que falar que é brincadeira, né, vai que tem gente que realmente acredita em QAnon". A fala era pra ser só piada, mas me puxou pra um buraco de coelho.

Fui pesquisar sobre o QAnon e esbarrei num detalhe que arrancou um sorriso cansado: gente passando horas caçando esteganografia em foto aleatória de político.

Eu sorri porque, mais de uma década antes, a esteganografia em fóruns como o 4chan existia de verdade. Só que ninguém estava decodificando foto de político. Era gente trocando mensagem criptografada dentro de foto de gatinho, usando um mar de memes descartáveis como camuflagem operacional.

Ver o QAnon hoje é uma tristeza, de ver alguém encontrar uma ideologia jogada na calçada, vestir ela do avesso e acreditar que herdou uma revolução.

> [!NOTE] Disclaimer de Saudosismo
> Antes que você siga lendo, vale o aviso honesto: este autor que vos fala é assumidamente saudosista daquela época. Tenho um carinho difícil de esconder pelas máscaras de Guy Fawkes, pelos chats de IRC que caíam a cada cinco minutos e por *mottos* que misturavam filosofia de boteco com subcultura digital, tipo o título deste post. Também não escondo de onde eu falo: sou uma pessoa de esquerda e acredito que o conhecimento, em todas as suas formas, deveria ser livre, sempre.
>
> E, só pra tranquilizar o senhor agente federal que porventura cair aqui: isso é história, tá? Pode guardar o mandado e poupar a planilha de *doxxing*, que meu nome já está ali no cabeçalho de graça. Se eu tivesse algo pra esconder, não estaria publicando num blog no GitHub Pages. Qualquer semelhança com madrugadas reais é mera coincidência literária (e, na dúvida, já prescreveu faz tempo).

Aquela lembrança acabou me puxando pra uma pergunta bem mais pesada. Como é que a gente saiu de uma internet que parecia promessa de emancipação e conhecimento aberto pra acordar em 2026, num cenário onde ataques cibernéticos drenam bilhões de dólares em minutos e servem de artilharia pra guerras reais?

A resposta curta dói um pouco: o hacktivismo clássico acabou esmagado entre o Estado e o crime profissionalizado, mesmo sem que as defesas tenham ficado invencíveis.

E, de ponta a ponta dessa história, existe um fio que nunca se rompeu desde os anos 80: o elo mais fraco raramente é o algoritmo. É sempre a pessoa sentada na frente da tela.

{% include toc.html title="Roteiro da Viagem" %}

## Antes da máscara: Kevin Mitnick e a virada política

Antes de o hacking virar bandeira política, ele era um ofício solitário de curiosidade e ego. Se você precisa de um marco zero pra entender a cabeça de quem veio antes do hacktivismo, o nome é Kevin Mitnick [^1].

Mitnick não estava tentando derrubar governos nem socializar o conhecimento do mundo. Nos anos 80 e 90, começou no *phreaking* (explorando centrais telefônicas) e escalou para invasões na Motorola, Nokia e Sun Microsystems pela simples adrenalina de provar que conseguia entrar.

O detalhe técnico que muita gente esquece, porque o cinema prefere uma tela preta cheia de código verde descendo rápido, é que a arma principal dele era o telefone, muito mais do que qualquer *exploit* mágico. Mitnick era um mestre de *social engineering* (engenharia social, ou SEing): ligava para funcionários, falava o jargão interno da empresa com naturalidade e convencia quem estava do outro lado a entregar senhas e códigos-fonte sem desconfiar (padrão que vai atravessar toda essa história).

A virada entre o hacker curioso e o ativista político começa de verdade nos anos 90. Na Alemanha, o *Chaos Computer Club* (CCC) já misturava técnica pesada com defesa de liberdades civis desde a década anterior. Nos Estados Unidos, em 1996, um coletivo chamado *Cult of the Dead Cow* (cDc) cunhou oficialmente o termo "hacktivismo" [^2].

A proposta deles mudou o horizonte: usar invasão, vazamento e desobediência civil digital como ferramenta política e de direitos humanos. O *Back Orifice*, software criado por eles, virou símbolo dessa era, junto com o trabalho ajudando dissidentes a furar censura estatal. A internet estava crescendo rápido (como eu já contei em {% include post-ref.html slug="historia-internet" text="Uma Breve História da Internet" %}), e pela primeira vez a rede deixava de ser infraestrutura acadêmica pra virar arena de disputa política.

## A cultura dos bastidores: gatinhos, chaves e túneis

Nos porões do 4chan em meados dos anos 2000, o Anonymous brota sem solenidade nenhuma, movido a piada interna, caos coletivo e *lulz*.

Em julho de 2006, centenas de usuários invadiram o jogo virtual *Habbo Hotel* com avatares idênticos de terno cinza e cabelo *afro* só pra formar uma barreira humana impedindo a entrada na piscina digital, entupindo o chat com a frase *"Pool's closed"* [^3].

No mundo físico, rolavam anúncios falsos no Craigslist despachando dezenas de estranhos ao mesmo ponto da Times Square pra assistir todo mundo perdido ao vivo numa webcam pública da EarthCam (como faria anos depois na *Operation Card Stand* de 2011).

Antes de qualquer manifesto, já era engenharia social coletiva testando o quanto um bando de anônimos conseguia dobrar a realidade.

A virada política veio em 2008 com o *Project Chanology*, contra a Igreja da Cientologia, depois que a instituição tentou tirar do ar à força um vídeo promocional interno vazado em que Tom Cruise fazia um discurso bizarro sobre a seita [^4]. De repente, aquela mesma horda sem rosto descobriu que tinha músculo pra sair dos fóruns e encher praças pelo mundo real de máscara.

Nos bastidores, não existia sede, CNPJ nem organograma: tudo rodava em clientes de IRC, fóruns efêmeros e canais que sumiam da noite pro dia.

Em células menores, a identidade de cada participante costumava ser reduzida a um recorte do hash da própria chave pública, algo no formato `#XXXXXX`. Sem nome real, sem ego inflado, sem crachá. Apenas uma assinatura verificável provando que a mensagem vinha da mesma pessoa de ontem.

Pra passar recados em campo aberto, entrava a esteganografia: bloco PGP escondido num JPEG de gatinho no `/b/` passava batido entre milhões de memes.

E nem tudo era barulho ou ataque. Tinha um lado bem mais quieto dessa cultura que quase nunca aparecia no jornal: gente virando a madrugada ensinando jornalistas, ativistas e pessoas comuns em regiões sob censura ou crise política a limpar rastros digitais e configurar túneis no Tor e na rede I2P (*Invisible Internet Project*).

Em lugares com infraestrutura destruída ou monitoramento estatal pesado, manter uma conexão anônima de pé significava conseguir tirar uma denúncia de dentro de um território isolado. Era uma mistura estranha de paranoia técnica, solidariedade sincera e molecagem de internet. Não era perfeito (ninguém ali fingia que era), mas tinha uma ética própria.

## Payback, Free Assange e a defesa do conhecimento livre

O momento em que empresas e governos pararam de rir do Anonymous chegou em 2010, com a *Operation Payback* e o seu desdobramento mais famoso, a *Operation Avenge Assange* (que muita gente lembra como a onda do *Free Assange*) [^5].

A *Operation Payback* nasceu em defesa do *The Pirate Bay*, em resposta ao cerco judicial das associações da indústria fonográfica e cinematográfica (RIAA e MPAA). Ali já estava desenhada uma briga que nunca acabou: de um lado, quem trata cultura e informação como propriedade trancada; do outro, quem entende que a rede existe pra circular conhecimento.

Logo depois, quando o WikiLeaks vazou milhares de telegramas diplomáticos confidenciais das embaixadas dos Estados Unidos e gigantes financeiros como PayPal, Visa, Mastercard e bancos suíços bloquearam as doações para Julian Assange, o conflito subiu de escala. A censura deixou de ser só jurídica e virou asfixia financeira. Em resposta, o Anonymous virou os canhões pro sistema bancário global.

> [!NOTE] Sobre o lado da trincheira
> Eu sei que muita gente torce o nariz quando se defende WikiLeaks e *The Pirate Bay* na mesma frase. Eu não torço. Os dois atacavam, cada um no seu terreno, o mesmo cercamento: o monopólio de quem decide o que o público pode ver, ler, ouvir ou saber sobre os próprios governos. Numa sociedade desigual, propriedade intelectual absoluta e segredo de Estado irrestrito nunca serviram pra proteger quem está embaixo. Serviram pra blindar quem já manda.

Tecnicamente falando, boa parte dos ataques daquela fase era quase artesanal. Ferramentas como o LOIC (*Low Orbit Ion Cannon*) deixavam qualquer pessoa com um computador doméstico e vontade de protestar apontar um fluxo contínuo de requisições HTTP/TCP contra um servidor alvo. Era um DDoS voluntário, quase uma versão corporativa de bloquear a piscina do Habbo Hotel: em vez de avatares travando uma entrada virtual, milhares de requisições sentadas na porta do PayPal e da Mastercard pra ninguém passar. (E, convenhamos, muita gente rodou o LOIC sem nem ligar uma VPN ou Tor antes, entregando o próprio IP residencial de bandeja pra polícia.)

Na virada para 2011, com a Primavera Árabe e o vazamento humilhante da consultoria de segurança HBGary Federal (cujo CEO se gabou na imprensa de ter identificado os líderes e acordou com os e-mails da empresa vazados), o movimento chegou ao pico de força. Por um breve instante, pareceu que um coletivo sem orçamento conseguia peitar impérios de igual pra igual.

## As dissidências: LulzSec, AntiSec e os rachas internos

O preço de virar fenômeno global sem porta de entrada nem filtro é que todo mundo resolve entrar. Depois de *Payback* e *Avenge Assange*, os canais de IRC ficaram lotados de gente nova, barulhenta e sem nenhuma noção de segurança operacional.

Uma parte dos operadores mais técnicos começou a se cansar do excesso de discurso, das brigas de ego e dos novatos baixando LOIC achando que estavam dentro de um filme. A consequência natural foi o racha em células menores, fechadas e bem mais agressivas.

A mais barulhenta delas nasceu em maio de 2011 com o nome de **LulzSec** (*Lulz Security*) [^6]. Formado por um punhado de veteranos saídos do ataque à HBGary, o grupo chutou o discurso idealista pro alto e decretou uma temporada de "50 dias de *lulz*", invadindo Sony Pictures, Fox, PBS, o site do Senado dos EUA e até derrubando a página pública da CIA. Nada de DDoS amador: o LulzSec combinava *SQL injection* clássico, senhas reutilizadas e uma conta debochada no Twitter que tirava o sono de diretorias inteiras.

Na mesma época surgiram outras ramificações com agendas próprias. Quando o LulzSec anunciou o fim da campanha, parte dos seus membros se juntou à ala mais radical do Anonymous na operação **AntiSec**, voltada a vazar documentos de governos, polícias e consultorias privadas de inteligência como a Stratfor.

Em paralelo, brotaram coletivos menores como o **CabinCr3w** e dezenas de células regionais que carregavam a mesma bandeira sem responder umas às outras. O guarda-chuva continuava chamando atenção na mídia. Por baixo dele, porém, o que existia já era uma colcha de retalhos de grupos competindo por espaço e técnica.

E o detalhe mais melancólico dessa cronologia é que metade dessa festa já estava rolando com o FBI sentado dentro da sala.

## O elo mais fraco não é o algoritmo: o caso Sabu

Se você estuda criptografia, aprende cedo a confiar na matemática. Uma chave RSA longa ou uma curva elíptica bem implementada não vai ceder na força bruta antes da morte térmica do universo.

O problema é que ninguém precisa quebrar a sua chave quando pode quebrar você.

A queda do núcleo duro do LulzSec e da AntiSec gira em torno de um nome nos chats: **Sabu** [^7] [^8].

Em 7 de junho de 2011, bem no meio dos "50 dias de *lulz*", agentes do FBI bateram à porta do apartamento dele em Nova York. Não precisaram de um supercomputador pra vencer os algoritmos que ele usava: um deslize operacional (uma conexão sem proteção de anonimato num momento de descuido) ligou o apelido ao endereço real.

Mas o golpe definitivo não foi a prisão em si. Sabu era o guardião legal de duas crianças, filhas de uma prima que estava presa. Diante da chance real de passar décadas na cadeia e deixar as meninas sozinhas no sistema de acolhimento, ele fez o acordo que quase qualquer pai faria no lugar dele: virou informante do FBI no dia seguinte.

Isso significa que a reta final do LulzSec (incluindo os ataques ao Senado e à página da CIA) já rolou sob supervisão direta de agentes federais. O mesmo vale pra quase toda a campanha da AntiSec, até o vazamento gigante da Stratfor em dezembro, durante os nove meses em que Sabu seguiu logando no IRC como se nada tivesse mudado. Quando a rede fechou em março de 2012, nomes de peso como Jeremy Hammond, Topiary, Kayla e Tflow caíram em efeito dominó.

A partir dali, o feitiço quebrou. A descentralização, que era a maior força do Anonymous, mostrou sua fraqueza fatal: sem estrutura de confiança real, a paranoia tomou conta dos canais. Qualquer pessoa no chat podia ser um agente infiltrado ou um colega virado pelo pescoço.

Pra quem acompanhou aquilo de perto, essa talvez tenha sido a parte mais triste de toda a história. Ver, madrugada após madrugada, canais de IRC que chegavam a juntar centenas de pessoas cheias de ideias genuinamente revolucionárias pra época irem se esvaziando aos poucos. Primeiro sumiam os veteranos. Depois sumiam as discussões sérias. Por fim, sobravam o silêncio, alguns *bots* e a desconfiança.

> [!IMPORTANT] O peso real por trás da tela
> Existe um momento em que o romantismo da internet bate de frente com o concreto do mundo real. Enquanto a coisa fica no terminal, nos apelidos e nos hashes, parece que todo mundo é intocável. Mas do outro lado da tela sempre existe gente de carne e osso, com família, boleto, medo real e consequência real. Entender isso muda a forma como você olha pra cada linha de comando que digita.

O movimento não desapareceu do mapa, mas perdeu a alma e o centro de gravidade.

## A década perdida, Parte 1: Snowden, brigas internas e o novo 4chan

O que aconteceu entre 2013 e 2020 foi o desmanche lento de uma utopia.

Em junho de 2013, Edward Snowden vazou o arquivo de vigilância em massa da NSA [^9]. Foi a confirmação de tudo que a comunidade de privacidade e criptografia denunciava fazia anos, mas veio num formato oposto ao do Anonymous: um *whistleblower* solitário entregando documentos curados pra jornalistas investigativos, sem máscara, sem DDoS e sem teatro em fórum.

Enquanto isso, sem o núcleo técnico de 2011, a bandeira do Anonymous virou terra de ninguém. Ainda houve campanhas barulhentas ligadas a crises reais: a *OpFerguson* em 2014 (nos protestos pela morte de Michael Brown e contra a Ku Klux Klan), a *OpISIS* em 2015 (após os atentados ao *Charlie Hebdo* e em Paris, derrubando milhares de contas de propaganda do Estado Islâmico) e um retorno relâmpago em maio de 2020 durante os protestos por George Floyd, quando o site da polícia de Minneapolis saiu do ar [^10].

Nos bastidores, porém, o clima era de desgaste e briga interna. Contas gigantes de Twitter e canais de YouTube disputavam pra dizer quem falava "em nome do movimento", enquanto alas progressistas batiam de frente com alas libertárias e trolls antigos.

E o golpe mais amargo veio do próprio berço cultural de tudo aquilo. Ao longo da década de 2010, o 4chan (em especial o `/pol/`) migrou da anarquia dos anos 2000 pra virar incubadora da extrema-direita estadunidense. Junto com seu primo ainda mais radical e sem moderação, o **8chan** (depois renomeado 8kun) [^11], acabou parindo o QAnon lá do começo desse texto.

Ver o mesmo terreno que gerou protestos contra censura corporativa se transformar em fábrica de teoria conspiratória reacionária é uma das viradas mais tristes da história recente da internet.

> [!NOTE] O luto pelo que virou aquele espaço
> Dói admitir, mas parte do luto que eu carrego dessa história vem justamente daí. A gente olhava pros fóruns anônimos e achava que a ausência de filtros ia servir pra desmontar autoritarismos e abrir a informação pro mundo. Ver a mesma linguagem, os mesmos códigos e o mesmo ecossistema serem sequestrados pela extrema-direita pra fabricar pânico moral e teorias como o QAnon é uma daquelas decepções que não passam fácil.

## A década perdida, Parte 2: o crime vira franquia e caos adolescente

Enquanto o hacktivismo se esfarelava em disputas internas, o vácuo foi ocupado rápido por gente que nunca teve nenhum interesse em mudar o mundo. Só em faturar em cima dele.

Entre 2018 e 2021, o crime digital abandonou o amadorismo e copiou o modelo do Vale do Silício. Nascia a indústria do **Ransomware-as-a-Service (RaaS)**: cartéis como REvil, Conti, LockBit e DarkSide operando como franquias corporativas, com divisão de lucros pra afiliados, atendimento 24/7 pra ensinar a vítima a comprar criptomoeda e pagar o resgate, e até departamento de RH.

O cartão de visitas desse novo mundo chegou em maio de 2021, quando o DarkSide paralisou o oleoduto **Colonial Pipeline** nos Estados Unidos, provocando filas quilométricas em postos de combustível e estado de emergência nacional [^12]. Não havia manifesto. Só fatura vencida.

No fim daquele mesmo ano, ainda surgiu uma anomalia sem ideologia nem disciplina de cartel: ego puro, extorsão e gosto por ver o circo pegar fogo.

O melhor exemplo dessa virada foi o **Lapsus$** [^13]. Entre o final de 2021 e 2022, esse grupo formado em boa parte por adolescentes (com lideranças no Reino Unido e conexões fortes no Brasil) humilhou gigantes de tecnologia como Nvidia, Microsoft, Samsung, Okta, Uber e Rockstar Games.

Aqui no Brasil, o estrago ficou famoso na madrugada de 10 de dezembro de 2021, quando a infraestrutura em nuvem do Ministério da Saúde e do DATASUS na AWS foi varrida do mapa, tirando do ar o ConecteSUS e os registros nacionais de vacinação em plena pandemia [^14]. Quem olhou de perto os rastros técnicos daquela invasão percebeu rápido que não se tratava de um *zero-day* alienígena saído de filme de espionagem. A entrada veio por credenciais administrativas comprometidas, seguida de automação destrutiva pra apagar recursos em massa na nuvem (no estilo de scripts como o *AWS-Bomb*) e tráfego mascarado pulando por *proxies* espalhados pela Ásia.

E como o Lapsus$ entrava nas *big techs*? De volta às raízes de Kevin Mitnick, só que adaptado pra era do trabalho remoto: **SEing puro**. Eles compravam credenciais de funcionários direto em canais do Telegram, faziam *SIM swapping* pra sequestrar códigos de SMS, disparavam fadiga de MFA (*MFA bombing*) até o funcionário aceitar o aviso no celular pra parar o barulho, e ligavam pro *helpdesk* fingindo ser técnicos internos.

De novo, milhões de dólares em *firewalls* e criptografia de ponta vencidos por uma conversa fiada bem aplicada.

## A era dos Estados: de Sony e WannaCry à ciberguerra de 2026

Se os cartéis de *ransomware* e o Lapsus$ mostram o lado mercenário e caótico desse novo mundo, o que realmente domina o tabuleiro hoje é muito mais frio. O hacking saiu de vez do porão e entrou na folha de pagamento de forças armadas e serviços de inteligência.

Esse roteiro começou a ficar escancarado ainda em novembro de 2014, quando o ataque devastador à Sony Pictures (assinado por um suposto grupo chamado *Guardians of Peace* e atribuído à Coreia do Norte) inaugurou a era de Estados vestindo fantasia de grupo independente pra intimidação política [^15].

Entre 2016 e 2017, o patamar mudou de vez quando o misterioso grupo *The Shadow Brokers* vazou o arsenal de ferramentas da própria NSA, incluindo o *exploit* **EternalBlue** [^16]. Em maio de 2017, o **WannaCry** (ligado à Coreia do Norte) usou essa brecha pra paralisar hospitais e empresas no planeta inteiro [^17]. Um mês depois, em junho, o **NotPetya** (atribuído à inteligência militar russa) se disfarçou de *ransomware* mas agiu como arma de sabotagem mirando a Ucrânia, travando gigantes globais de logística como a Maersk e deixando cerca de 10 bilhões de dólares de prejuízo [^18].

Hoje, em 2026, aquela escalada virou rotina.

Quem acompanha segurança já conhece bem o **Lazarus Group** (ligado ao escritório de inteligência militar norte-coreano, o RGB), que virou na prática o departamento de financiamento externo de um Estado sancionado. Depois de Sony e WannaCry, entre 2025 e 2026 eles mudaram a escala do jogo: em fevereiro de 2025 drenaram 1,5 bilhão de dólares da corretora Bybit e, em outubro de 2026, bateram o recorde histórico do setor ao levar 6,3 bilhões de dólares da Binance [^19] [^20].

E sabe qual foi a porta de entrada no golpe bilionário da Binance? A mesma de quarenta anos atrás. Engenharia social. Só que agora no formato da campanha *Contagious Interview*: recrutadores falsos no LinkedIn, entrevistas de emprego forjadas usando IA generativa e *deepfakes* em vídeo, mirando desenvolvedores e funcionários internos pra plantar código malicioso em ambientes legítimos. Mitnick fazia isso com um orelhão e cara de pau; o Lazarus faz com orçamento militar e modelos generativos.

E a Coreia do Norte não está sozinha nessa:

No tabuleiro de 2026, três frentes estatais dominam o palco:

Do lado chinês, grupos como **Salt Typhoon** e **Volt Typhoon** passaram ao pré-posicionamento silencioso: o Salt Typhoon invadiu operadoras de telecomunicações nos Estados Unidos e comprometeu sistemas de interceptação legal (*lawful intercept*) usados pelo próprio governo [^21], ficando quieto dentro de telecoms, redes elétricas e água esperando uma crise militar real. Do lado russo, unidades militares como o **Sandworm** (ligado ao GRU, os mesmos do NotPetya) operam sabotagem cinética contra sistemas industriais (OT/ICS), energia e logística ocidental.

E há ainda o **faketivism**, a parte mais cínica de 2026: agências de inteligência usando a fantasia do hacktivismo como **negação plausível**. Grupos como KillNet, NoName(057)16 e Cyber Army of Russia Reborn se pintam de "hacktivistas independentes" pra fazer DDoS barulhento e guerra psicológica sob cobertura silenciosa de Estados [^22]. É hacktivismo de fachada.

No meio disso tudo, a técnica também mudou de roupa. Os operadores modernos evitam ao máximo soltar *malware* barulhento que acende o painel do antivírus; preferem *Living-off-the-Land* (LotL), usando ferramentas nativas do próprio sistema operacional, credenciais válidas e roteadores de borda sem *patch* pra se misturar ao tráfego normal de administração.

### A corrida de IA: achando bugs mais rápido do que a gente consegue atualizar

E como se esse cenário já não fosse pesado o bastante, a IA entrou dos dois lados do balcão e quebrou o equilíbrio que existia há trinta anos. Antes, achar um *zero-day* sério num projeto maduro custava meses de auditoria humana e *fuzzing* pesado. Hoje, agentes autônomos varrem bases inteiras de código aberto em velocidade de máquina e desenterram falhas que estavam dormindo há décadas.

Não é exagero de palestra de segurança: em ciclos recentes do OpenSSL, pipelines autônomos de IA chegaram a descobrir todas as vulnerabilidades de uma leva inteira de correções, incluindo erros complexos de memória que tinham escapado de anos de revisão humana [^23]. A mesma enxurrada bateu em tudo que segura a internet de pé, de {% include post-ref.html slug="copy-fail" text="falhas críticas no kernel Linux descobertas com ajuda de IA, como o Copy Fail" %}, até bugs remotos no PHP.

Quem cuida de servidor sabe bem a exaustão que virou viver de janela de manutenção em janela de manutenção, tentando aplicar *patch* de emergência antes que algum bot transforme o CVE da manhã em *exploit* funcional no mesmo dia.

Do lado ofensivo, a IA encurta a janela entre a divulgação do bug e a exploração ativa de semanas pra horas, além de automatizar o reconhecimento e o encadeamento de falhas menores. Do lado defensivo, as equipes já precisam usar IA pra fazer triagem, gerar correções e tentar segurar o dilúvio de atualizações sem derrubar produção (o que, sejamos honestos, nem sempre dá certo).

Máquina caçando falha em código escrito por gente, máquina explorando, máquina sugerindo o *patch* e a gente no meio perdendo o sono. Se isso não é o retrato acabado de uma distopia cyberpunk, eu não sei mais o que é.

## O que ainda resiste: Sci-Hub, Anna's Archive e o retorno dos torrents

Seria fácil terminar esse texto aqui, fechar o caderno com gosto amargo na boca e decretar que o idealismo hacker morreu de vez. Mas não seria verdade.

Ele não morreu. Ele mudou de endereço e baixou o volume.

Muito antes de 2026, em 2008, um jovem programador chamado **Aaron Swartz** escreveu o *Guerilla Open Access Manifesto* [^24] [^25]. A tese dele era tão simples quanto incômoda pra quem lucra com escassez artificial: informação é poder, e trancar pesquisa científica financiada com dinheiro público atrás de *paywalls* bilionários de editoras privadas é um cercamento inaceitável. Compartilhar conhecimento, dizia ele, não era crime. Era um dever moral.

Aaron pagou com a própria vida pela perseguição desproporcional da Justiça dos EUA depois de baixar artigos do JSTOR, em 2011. Mas a semente que ele jogou no chão não secou.

Ela floresceu no **Sci-Hub**, criado pela neurocientista cazaque Alexandra Elbakyan em 2011 [^26]. Num mundo onde conglomerados editoriais cobram quarenta dólares por um único PDF que foi escrito por pesquisadores pagos com verba pública e revisado de graça por outros cientistas, o Sci-Hub abriu as portas de dezenas de milhões de artigos pra estudantes, médicos e universidades do Sul Global. Sem máscara, sem vídeo com voz distorcida, sem show no Twitter. Apenas um corvo segurando uma chave e a recusa teimosa de aceitar que a ciência pertença a acionistas.

A mesma linhagem reapareceu mais recentemente no **Anna's Archive** [^27]. Nascido no final de 2022 depois das investidas policiais contra a Z-Library, o projeto assumiu uma missão quase romântica no meio dessa distopia toda: construir um *backup* aberto e distribuído da memória escrita da humanidade. Livros, periódicos, metadados e acervos inteiros catalogados e replicados em *torrents* públicos, pra que nenhuma editora, tribunal ou governo consiga apagar uma biblioteca inteira com uma ordem judicial.

E, nos últimos anos, algo parecido começou a acontecer na cultura cotidiana com o ressurgimento silencioso dos ***torrents***.

Durante uma década, as plataformas de *streaming* convenceram quase todo mundo de que a pirataria tinha ficado obsoleta porque a conveniência era barata. Só que a lua de mel acabou. No processo que o escritor Cory Doctorow batizou com precisão de *enshittification* [^28], o oligopólio dos *streamings* fatiou filmes, séries e músicas em uma dúzia de assinaturas caras, enfiou propaganda dentro de plano pago, restringiu o compartilhamento familiar e passou a sumir com obras inteiras dos catálogos por conveniência fiscal. Você paga todo mês e não é dono de nada.

Diante disso, voltar pro *BitTorrent* deixou de ser apenas um jeito de economizar no fim do mês. Virou um gesto de preservação cultural e recusa política. Se um filme some do catálogo oficial e ninguém estiver fazendo *seeding* dele em algum canto do mundo, ele simplesmente deixa de existir.

> [!TIP] Posição assumida, sem rodeio
> Aqui eu não faço média: defender Sci-Hub, Anna's Archive e *torrents* não é "romantizar pirataria", é se recusar a aceitar o cercamento privado da cultura e da ciência. Pesquisa paga com dinheiro público não tem que dar margem de lucro obscena pra editora gringa, assim como a memória do cinema e da literatura não pode depender da boa vontade de meia dúzia de CEOs de *streaming*. Se a lei protege o monopólio em vez do acesso, a desobediência civil digital continua sendo legítima.

Esse é o hacktivismo que ainda respira em 2026. Menos barulhento, mais paciente e muito menos preocupado com fama, mas fiel à única coisa que realmente valia a pena salvar lá dos anos 2000: a convicção de que o conhecimento humano é bem público.

## O que sobrou quando a poeira baixou

Quando eu olho pra essa linha do tempo inteira, fica uma mistura difícil de nomear: tristeza pelo que a internet poderia ter sido e um fio teimoso de carinho pelo que ainda não se rendeu.

O hacktivismo da minha juventude tinha mil defeitos. Era caótico, às vezes irresponsável, cheio de ego disfarçado de anonimato e capaz de cometer injustiças no calor do momento. Mas tinha uma faísca genuína de contra-poder: a ideia um pouco ingênua de que a rede pertencia a quem sabia construí-la e de que o cidadão comum podia usar a técnica pra devolver o olhar de quem vigia.

Quase tudo aquilo se dissolveu entre teorias conspiratórias, *faketivism* estatal e cartéis bilionários.

Os algoritmos ficaram mais fortes, as nuvens ficaram mais complexas e os *firewalls* ganharam IA. Mas se tem uma lição que atravessa intacta do telefone do Kevin Mitnick, passa pela queda do Sabu, derruba servidores na AWS e chega até um golpe de seis bilhões de dólares no LinkedIn, é uma só: você pode empilhar toda a criptografia do mundo em volta de um sistema, que a fechadura principal continua sendo humana.

Talvez seja justamente por isso que, apesar de toda a distopia, alguma coisa ainda resiste. Porque do mesmo jeito que a vulnerabilidade mora nas pessoas, a solidariedade também mora. Em algum servidor discreto, alguém continua mantendo um *seed* de pé de madrugada pra que um livro ou um artigo científico continue acessível pra quem não pode pagar.

E, convenhamos, ninguém é perfeito.

## Referências

[^1]: **Kevin Mitnick** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Kevin_Mitnick))
[^2]: **Cult of the Dead Cow** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Cult_of_the_Dead_Cow))
[^3]: **Anonymous (hacker group): Early raids and Habbo Hotel** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Anonymous_%28hacker_group%29))
[^4]: **Project Chanology** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Project_Chanology))
[^5]: **Operation Payback** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Operation_Payback))
[^6]: **LulzSec** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/LulzSec))
[^7]: **Operation AntiSec** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Operation_AntiSec))
[^8]: **Sabu (LulzSec / AntiSec)** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Hector_Monsegur))
[^9]: **Edward Snowden** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Edward_Snowden))
[^10]: **Timeline of events associated with Anonymous** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Timeline_of_events_associated_with_Anonymous))
[^11]: **8chan** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/8chan))
[^12]: **DarkSide Ransomware: Best Practices for Preventing Business Disruption (AA21-131A)** {*CISA Advisory*} ([Link](https://www.cisa.gov/news-events/cybersecurity-advisories/aa21-131a))
[^13]: **Review of the Attacks Associated with Lapsus$ and Related Threat Groups** {*Cyber Safety Review Board / CISA*} ([Link](https://www.cisa.gov/resources-tools/resources/review-attacks-associated-lapsus-and-related-threat-groups-report))
[^14]: **Sites e aplicativo do Ministério da Saúde sofrem ataque cibernético** {*Agência Brasil / EBC*} ([Link](https://agenciabrasil.ebc.com.br/saude/noticia/2021-12/sites-e-aplicativo-do-ministerio-da-saude-sofrem-ataque-cibernetico))
[^15]: **2014 Sony Pictures hack** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/2014_Sony_Pictures_hack))
[^16]: **The Shadow Brokers** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/The_Shadow_Brokers))
[^17]: **WannaCry ransomware attack** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/WannaCry_ransomware_attack))
[^18]: **2017 Ukraine ransomware attacks (NotPetya)** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/2017_Ukraine_ransomware_attacks))
[^19]: **North Korea Responsible for $1.5 Billion Bybit Hack** {*FBI Public Service Announcement*} ([Link](https://www.ic3.gov/PSA/2025/PSA250226))
[^20]: **Significant Cyber Incidents** {*CSIS*} ([Link](https://www.csis.org/programs/strategic-technologies-program/significant-cyber-incidents))
[^21]: **Joint Statement from FBI and CISA on People's Republic of China (PRC) Targeting of Commercial Telecommunications Infrastructure (Salt Typhoon)** {*CISA*} ([Link](https://www.cisa.gov/news-events/news/joint-statement-fbi-and-cisa-peoples-republic-china-prc-targeting-commercial-telecommunications))
[^22]: **Pro-Russia Hacktivists Conduct Opportunistic Attacks Against US and Global Critical Infrastructure (AA25-343A)** {*CISA Advisory*} ([Link](https://www.cisa.gov/news-events/cybersecurity-advisories/aa25-343a))
[^23]: **AI Found Twelve New Vulnerabilities in OpenSSL** {*Bruce Schneier / Schneier on Security*} ([Link](https://www.schneier.com/blog/archives/2026/02/ai-found-twelve-new-vulnerabilities-in-openssl.html))
[^24]: **Aaron Swartz** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Aaron_Swartz))
[^25]: **Guerilla Open Access Manifesto** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Guerilla_Open_Access_Manifesto))
[^26]: **Sci-Hub** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Sci-Hub))
[^27]: **Anna's Archive** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Anna%27s_Archive))
[^28]: **Enshittification** {*Wikipedia*} ([Link](https://en.wikipedia.org/wiki/Enshittification))

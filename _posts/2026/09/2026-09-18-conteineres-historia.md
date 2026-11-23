---
layout: post
title: "A História dos Contêineres"
subtitle: "De uma chamada de sistema dos anos 70 a uma palestra de cinco minutos que mudou a indústria"
author:
  - "Eduardo N. S. R."
date: 2026-09-18 14:08:00 GMT-3
modified_date: 2026-11-23 18:46:37 GMT-3
permalink: /posts/conteineres-historia/
tags: [Docker, Contêineres, Linux, História]
series: Contêineres de Cabo a Rabo
category: Artigos
---

Tenho um amigo que usa Slackware no trabalho. Não por nostalgia, não por teimosia, não por falta de opção. Por escolha técnica deliberada, com a convicção serena de quem conhece o sistema até a raiz e não quer camadas de abstração que ele não pediu. É o tipo de pessoa que abre um `man 8 chroot` por lazer, tem opinião formada sobre hierarquia de processo em *BSD e consegue passar horas discutindo as diferenças filosóficas entre o modelo de jails do FreeBSD e o isolamento de processos do OpenBSD. Um entusiasta no sentido mais verdadeiro da palavra: aquele que estuda porque gosta, e não porque a certificação exige.

Numa conversa sobre Docker e Kubernetes, num desses papos técnicos que não tem hora pra acabar, ele fez uma observação que ficou martelando na minha cabeça. Disse que entendia a utilidade das ferramentas, mas que sentia que estava aprendendo conceitos novos. Que o mundo dos contêineres parecia um universo próprio, com vocabulário e princípios específicos que ele ainda estava assimilando.

Fiquei olhando pra ele por um segundo.

Eu mesmo não vim do nada. Passei por Mandrake, Conectiva e Kurumin nos anos das instalações que levavam três horas e uma reza. Depois Slackware, Gentoo, Arch. Fiz RHEL em ambiente corporativo. Hoje uso Debian. No meio do caminho, fui fundo o suficiente para montar um sistema do zero com o LFS e o BLFS, inclusive em contextos de sistemas embarcados, só para entender o que estava acontecendo debaixo do capô. `chroot`? Eu conhecia. Usava com menos frequência que meu amigo, que compila os próprios pacotes no Slackware dele até hoje, mas conhecia.

Ele estava começando a se aventurar pelo mundo dos contêineres agora. Experiências simples por aqui e por ali, e aquela conversa era parte do processo de entrar de cabeça no assunto. Eu já tinha um bom caminho percorrido nesse terreno: Docker, Compose, Kubernetes, o ecossistema todo.

A dúvida dele era direta: hipervisor + SO convidado + contêiner no topo não viram três camadas mais pesadas do que uma VM?

Faz todo sentido a pergunta vir de quem pensa em hardware real, latência e overhead: é um engenheiro de infra levantando uma objeção legítima contra o mito de que contêineres são VMs mais leves. Esse modelo mental é falso, e é ele que confunde tudo.

A conversa que se seguiu inspirou esta série. Ficou claro ali que o nó está na narrativa da indústria que faz parecer que o Docker caiu do céu em 2013 inventando isolamento de processos. Não inventou: só continuou uma história bem mais antiga.

> [!NOTE] Nota da Série
> Este post abre a série **"Contêineres de Cabo a Rabo"**, que explora os contêineres desde a história até a prática avançada. Se você já conhece bem a linha do tempo e quer ir direto ao mecanismo interno, pule para a {% include post-ref.html slug="conteineres-fundamentos" text="Parte 1: Fundamentos e Anatomia" %}. Se quiser entender as ferramentas do dia a dia, vai para a {% include post-ref.html slug="conteineres-pratica" text="Parte 2: Contêineres na Prática" %}.

{% include toc.html %}

## O que o Docker realmente fez

Solomon Hykes não inventou o isolamento de processos. Não inventou namespaces, não inventou cgroups, não inventou sistemas de arquivos em camadas.

O que ele fez foi pegar uma série de tecnologias que existiam espalhadas no ecossistema Linux, que qualquer administrador de sistemas experiente conhecia individualmente mas que eram trabalhosas de configurar juntas, e empacotou tudo isso numa experiência de usuário tão fluida que mudou a maneira como a indústria pensa sobre entrega de software. É a diferença entre saber que existe motor a combustão, suspensão e sistema de freios e ter um carro na garagem pronto pra usar.

A história dos contêineres é, nesse sentido, uma história de convergência. Tecnologias desenvolvidas em contextos diferentes, por equipes sem coordenação direta, ao longo de décadas, que foram gradualmente se encontrando até o momento em que alguém teve o discernimento de perceber que elas podiam andar juntas.

## 1979: A Primeira Jaula

Tudo começa em 1979, durante o desenvolvimento da versão 7 do Unix. Bill Joy e outros pioneiros adicionaram ao sistema a chamada de sistema `chroot` [^1]. A ideia era simples: alterar o diretório raiz aparente para um processo e todos os seus filhos. Se você rodasse um programa sob `chroot /jail`, para aquele programa a barra (`/`) passava a ser a pasta `/jail`.

O caso de uso original era pragmático. Compilar pacotes de software em um ambiente limpo sem riscos de afetar o sistema principal. Testar instalações sem estragar a máquina. A lógica faz sentido até hoje.

O problema é que o `chroot` isolava *apenas* o sistema de arquivos. A aplicação enjaulada ainda enxergava todos os processos do sistema operacional, abria conexões de rede sem restrição e consumia memória livremente até derrubar a máquina. E escapar de uma jaula `chroot` sendo `root` sempre foi, no Linux, um truque de entrada de manual: um passo, três linhas, pronto.

A primeira jaula existia. Mas as paredes tinham buracos por todos os lados.

## 2000: A Primeira Prisão de Verdade

A solução veio de fora do Linux, no ano 2000, quando o sistema FreeBSD introduziu as **FreeBSD Jails** [^2], desenvolvidas por Poul-Henning Kamp. Meu amigo do Slackware, se estiver lendo isso, está provavelmente assentindo nesse ponto.

As Jails foram a primeira tecnologia real de virtualização em nível de sistema operacional. Elas isolavam não só o sistema de arquivos, mas a árvore de processos completa, o endereço IP e os privilégios administrativos. Cada jail tinha seu próprio hostname, sua própria tabela de processos e seu próprio usuário `root` restrito ao escopo daquela jaula. O `root` da jail não era o `root` da máquina.

Isso era filosoficamente diferente do `chroot`: em vez de uma pasta cercada, era um compartimento com porta, teto e vigilância.

O modelo influenciou o restante do ecossistema Unix. Se você usa *BSD por escolha técnica, sabe exatamente por quê essa abordagem é elegante: é isolamento sem hipervisor, sem emulação, sem overhead. É o sistema operacional fazendo o que deveria fazer desde o começo.

## 2001-2004: O Linux Tenta Acompanhar

O Linux tentou acompanhar com **Linux-VServer** (2001) e **OpenVZ** (2005): ótimo desempenho, mas presos a patches pesados fora da árvore oficial do kernel.

Como esses patches nunca foram aceitos por Linus Torvalds, rodar contêineres em Linux exigia manter kernels customizados de terceiros, um pesadelo logístico para equipes corporativas que precisam de suporte e correções de segurança previsíveis.

Em 2004, a Sun Microsystems deu um passo diferente com o Solaris 10 e as **Solaris Zones** [^3]. As Zones combinaram isolamento de processos com o inovador sistema de arquivos ZFS, permitindo criar clones e snapshots instantâneos de sistemas inteiros com custo ínfimo de disco. Foi a demonstração de que isolamento e gerenciamento de artefatos podiam andar juntos com elegância.

O Linux precisava de uma resposta que não exigisse patches externos. E ela viria de um lugar inesperado.

## 2006: O Google Resolve Seu Próprio Problema

Por volta de 2006, os engenheiros do Google enfrentavam um problema de escala que poucos outros times no mundo podiam compreender. Dezenas de milhares de servidores rodando a busca, o Gmail e outros serviços, todos competindo por recursos de CPU e memória sem nenhum mecanismo formal de governança. Um processo mal comportado podia afetar serviços vizinhos. A telemetria era imprecisa. A previsibilidade era uma ilusão bem disfarçada.

Paul Menage e Rohit Seth batizaram a solução interna de *Process Containers* [^4]: um mecanismo para agrupar processos e impor limites duros de CPU, memória e disco que o kernel faria cumprir não importasse o que o processo tentasse.

Para evitar confusão com o termo "contêineres", o recurso virou **cgroups** (*control groups*) e entrou no kernel Linux 2.6.24 em 2008.

Diferente do Linux-VServer e do OpenVZ, os cgroups entraram no kernel oficial. Qualquer distribuição Linux que rodasse um kernel moderno tinha acesso a essa tecnologia sem patches, sem customização, sem dependência de repositórios externos.

A fundação estava pronta.

## 2008: LXC e o Problema da Ergonomia

Com os cgroups no kernel e os namespaces sendo gradualmente maturados, o **LXC** (*Linux Containers*) surgiu em 2008 combinando essas primitivas em um conjunto de utilitários de linha de comando. Era possível subir contêineres completos sem modificar o kernel, sem aplicar patches, sem depender de projetos externos.

O problema era que fazer isso funcionava, mas não era divertido. Configurar redes virtuais, pontos de montagem, permissões e limites de recursos no LXC exigia conhecimento profundo de administração de sistemas e uma dose generosa de paciência. Não era uma ferramenta que você recomendaria para um desenvolvedor que queria rodar sua aplicação localmente.

Era a tecnologia certa, mas ainda faltava a interface certa.

## 2013: Cinco Minutos que Mudaram a Indústria

Em março de 2013, uma pequena empresa de plataforma como serviço chamada dotCloud decidiu abrir o código de uma ferramenta interna. Solomon Hykes subiu ao palco da PyCon [^5] para uma palestra relâmpago. Cinco minutos. Sem slides elaborados. Sem demo preparada com horas de ensaio.

A sala era pequena e ninguém esperava revolução: em segundos, Hykes baixou uma imagem, subiu um processo isolado e destruiu tudo num comando por vez.

A plateia entendeu na hora o que estava vendo: LXC com interface acessível, imagens em camadas reutilizáveis e um repositório central para compartilhamento. A combinação, apresentada com aquela fluência operacional, virou o mercado em tempo real.

O Docker não ganhou por ser a tecnologia mais sofisticada, mas por chegar no momento certo, com a embalagem certa, para um mercado pronto que não sabia por onde começar.

## 2015: A Indústria Faz as Pazes

O sucesso do Docker trouxe um risco óbvio: toda a cadeia de entrega (Kubernetes, nuvens públicas, CI/CD) passou a depender de um formato controlado por uma única empresa.

Para evitar esse aprisionamento tecnológico, em 2015 as grandes empresas do ecossistema se uniram sob a Linux Foundation e criaram a **Open Container Initiative (OCI)** [^6]. Docker, Red Hat, Google, IBM, Microsoft. O objetivo era padronizar tanto o formato de imagem quanto o mecanismo de execução de contêineres em especificações abertas e neutras.

O Docker doou seu motor central (`libcontainer`), que virou o independente `runc`, e a especificação OCI abriu o ecossistema para ferramentas intercambiáveis.

A guerra de formatos que poderia ter fragmentado o ecossistema foi evitada antes de começar.

## 2017 em diante: O Ecossistema Adulto

Nos anos seguintes, a padronização abriu espaço para uma diversidade saudável de implementações. O projeto `containerd` foi doado para a Cloud Native Computing Foundation (CNCF) e virou o runtime de referência. A Red Hat desenvolveu o **Podman** e o **CRI-O** para ambientes corporativos e Kubernetes, resolvendo preocupações reais de segurança com o modelo de daemon centralizado do Docker.

Implementações alternativas de runtime de baixo nível surgiram com objetivos específicos: o `crun` em C puro, mais rápido e com menor pegada de memória; o `youki` em Rust, com garantias de segurança de memória; o `gVisor` da Google, interceptando chamadas de sistema em espaço de usuário para isolamento extremo. O Kata Containers integrou micro-máquinas virtuais para os casos onde o compartilhamento de kernel era inaceitável.

```
1979        2000        2004        2006-2008        2008        2013        2015        2017+
 │           │           │              │             │           │           │           │
 ▼           ▼           ▼              ▼             ▼           ▼           ▼           ▼
chroot    FreeBSD     Solaris        cgroups         LXC       Docker        OCI      containerd
(Unix)     Jails       Zones       (Google no      (Kernel    (dotCloud/   (Padrão     Podman
             │       (com ZFS)     mainline)       nativo)      Hykes)     aberto)     CRI-O
             │                                                   │
        Linux-VServer                                       libcontainer
           (2001)                                             -> runc
```

## O que a história diz sobre como a indústria funciona

Existe um padrão aqui.

As tecnologias fundamentais raramente surgem prontas. Elas emergem em contextos distintos, resolvendo problemas específicos de suas épocas, e passam anos existindo em paralelo sem se encontrar. O `chroot` era uma ferramenta de build. As Jails eram uma resposta de segurança do ecossistema *BSD. Os cgroups nasceram de uma necessidade operacional do Google. Os union filesystems existiam para gerenciamento de sistemas de arquivos em live CDs.

O Docker não inventou nenhuma dessas coisas. O Docker percebeu que elas podiam funcionar juntas.

Meu amigo do Slackware conhecia `chroot`, conhecia jails, tinha até experimentado LXC em algum momento. O que ele não havia conectado era que o Docker era, essencialmente, uma interface para os mesmos conceitos que ele já dominava. A terminologia mudou. A experiência de uso ficou polida. A abstração ganhou uma camada de marketing pesada. Mas o kernel debaixo continuava fazendo o mesmo trabalho que sempre fez.

É uma lição que vale além do universo dos contêineres. A inovação real raramente é *ex nihilo*. Quase sempre é síntese, integração, timing.

E às vezes é uma palestra de cinco minutos na hora certa.

## Conclusão

Na {% include post-ref.html slug="conteineres-fundamentos" text="Parte 1 da série" %}, vamos descer ao nível do kernel Linux para entender exatamente o que acontece quando você digita `docker run`: namespaces, cgroups v2, OverlayFS e a especificação OCI. Se você é o tipo de pessoa que prefere entender o mecanismo antes de usar a ferramenta, é pra lá que você vai querer ir.

## Referências

[^1]: **chroot(2) Linux Manual Page** {*Michael Kerrisk, man7.org*} ([Link](https://man7.org/linux/man-pages/man2/chroot.2.html))

[^2]: **Jails: Confining the omnipotent root** {*Poul-Henning Kamp e Robert N. M. Watson, Proceedings of the 2nd International SANE Conference, 2000*} ([Link](https://papers.freebsd.org/2000/phk-jails/))

[^3]: **Solaris Zones: System Administration Guide: Solaris Containers-Resource Management and Solaris Zones** {*Sun Microsystems / Oracle Documentation*} ([Link](https://docs.oracle.com/cd/E19253-01/817-1592/))

[^4]: **Process containers** {*Jonathan Corbet sobre patches de Paul Menage (Google), LWN.net, 2007*} ([Link](https://lwn.net/Articles/236038/))

[^5]: **The Future of Linux Containers** {*Solomon Hykes, PyCon US Lightning Talks, 2013*} ([Link](https://www.youtube.com/watch?v=wW9CAH9nSLs))

[^6]: **Open Container Initiative (OCI) Specifications** {*The Linux Foundation, OpenContainers GitHub*} ([Link](https://opencontainers.org/))

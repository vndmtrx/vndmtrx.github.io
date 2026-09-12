---
layout: post
title: "Fundamentos e Anatomia de Contêineres"
subtitle: "De namespaces a cgroups v2: tudo que o kernel faz quando você digita docker run"
author:
  - "Eduardo N. S. R."
date: 2026-09-25 14:00:00 GMT-3
permalink: /posts/conteineres-fundamentos/
tags: [Docker, Podman, Contêineres, Linux, DevOps, Infraestrutura]
series: Contêineres de Cabo a Rabo
published: false
---

Você já rodou `docker run` centenas de vezes. Digita o comando, aperta enter, um punhado de letrinhas corre pelo terminal e, em questão de meio segundo, você tem uma aplicação inteira rodando em um ambiente isolado com rede, disco e variáveis próprias. Mas se eu te perguntar exatamente o que o kernel Linux fez naquele exato instante de meio segundo, você sabe responder?

A maioria dos desenvolvedores e operadores de infraestrutura aprendeu a usar contêineres como se fossem "máquinas virtuais mais leves e rápidas". Essa metáfora quebra galho para começar, mas ela é conceitualmente falsa. Contêineres não são máquinas virtuais. Não existe um hipervisor emulando placa-mãe, processador ou controladora SCSI. Não existe um segundo kernel dando *boot* silencioso no fundo da sua máquina. O que existe é um processo comum, rodando no mesmo kernel que o seu editor de texto e o seu navegador, só que usando uma coleira extremamente sofisticada fornecida pelo próprio sistema operacional.

Entender essa coleira é o divisor de águas entre o profissional que só sabe colar comandos do Stack Overflow e aquele que realmente resolve problemas quando o bicho pega em produção. Quando uma aplicação estoura o limite de memória e é abatida sem piedade pelo sistema operacional, quando duas instâncias brigam pela mesma porta de rede, ou quando você precisa projetar um cluster distribuído com Kubernetes, a abstração bonitinha do Docker desaparece. O que sobra é o kernel puro.

Este conhecimento também é o alicerce fundamental para a nossa série sobre criação de clusters locais com o projeto {% include post-ref.html slug="k8sbox-visao-geral" text="Kubernetes in a Box" %} e para a etapa de empacotamento que veremos na Parte 14 da série {% include post-ref.html slug="spring-boot-tutorial-parte-1-ambiente" text="Spring Boot Tutorial" %}. Sem dominar o que é um contêiner por baixo do capô, tentar entender a arquitetura de *Pods*, *Container Network Interface* (CNI) ou *Container Runtime Interface* (CRI) vira mero exercício de decoreba.

> [!NOTE] Nota da Série
> Este post é a Parte 1 da série **"Contêineres de Cabo a Rabo"**. Se você quer entender como chegamos até aqui, leia primeiro o {% include post-ref.html slug="conteineres-historia" text="Post Zero: A História dos Contêineres" %}. Aqui vamos dissecar a anatomia interna dos contêineres e explorar as três tecnologias fundamentais do kernel Linux: *namespaces*, *cgroups* e *union filesystems*, fechando com a construção de um mini-contêiner do zero em apenas 50 linhas de shell script. Na Parte 2, vamos subir o nível para as ferramentas de produção: Dockerfiles avançados, Docker Compose, arquitetura sem daemon do Podman, segurança e o caminho para a orquestração.

## Estrutura do Post

Para facilitar o estudo e permitir que você use este texto como guia de consulta rápida, dividi a anatomia dos contêineres em tópicos estruturados. A tabela a seguir lista o roteiro do post:

| Seção | Tema Principal |
| :--- | :--- |
| [Contêiner Não é VM: A Distinção que Muda Tudo](#contêiner-não-é-vm-a-distinção-que-muda-tudo) | Comparativo real entre hipervisores e isolamento de processos |
| [Namespaces: Os Muros de Isolamento do Kernel](#namespaces-os-muros-de-isolamento-do-kernel) | Como fatiar a visão de processos, rede, montagens e usuários |
| [Cgroups: O Guarda de Recursos](#cgroups-o-guarda-de-recursos) | Limites de memória, CPU e processos com a hierarquia unificada v2 |
| [Union Filesystems: Imagens em Camadas](#union-filesystems-imagens-em-camadas) | Anatomia do OverlayFS, Copy-on-Write e montagens na mão |
| [A Especificação OCI e o Ecossistema de Runtimes](#a-especificação-oci-e-o-ecossistema-de-runtimes) | Runtimes de alto e baixo nível: dockerd, containerd, runc e crun |
| [Grand Finale: Construindo um Mini-Contêiner do Zero](#grand-finale-construindo-um-mini-contêiner-do-zero) | Script bash executável integrando namespaces, cgroups e OverlayFS |
| [Exercícios](#exercícios) | Desafios práticos para consolidar namespaces, cgroups e OverlayFS |
| [O Que Vem na Parte 2](#o-que-vem-na-parte-2) | O passo seguinte: ferramentas, ciclo de vida e orquestração |
| [Referências](#referências) | Documentação oficial, papers e especificações do kernel |

## Contêiner Não é VM: A Distinção que Muda Tudo

Para consolidar o funcionamento prático, precisamos sepultar de vez a ideia de que um contêiner é uma máquina virtual em miniatura.

Imagine a estrutura física de moradia. Uma máquina virtual é como uma **casa isolada em seu próprio lote de terreno**. Essa casa tem fundações de concreto próprias, caixa d'água exclusiva, gerador elétrico individual e seu próprio quadro de disjuntores. Se o encanamento dessa casa arrebentar, o problema fica restrito a ela. Em contrapartida, construir essa estrutura exige muito material, ocupa um espaço físico enorme e custa caro para manter aquecida.

Um contêiner é como um **apartamento dentro de um edifício moderno**. O apartamento tem paredes sólidas, fechadura na porta e total privacidade interior: os vizinhos não enxergam o que você faz dentro da sua sala. Porém, o apartamento compartilha toda a infraestrutura estrutural do edifício: a fundação de sustentação, os prumadas hidráulicas e as colunas de cabos elétricos. Essa infraestrutura compartilhada é o **kernel Linux**. Se a fundação de concreto do prédio sofrer um abalo estrutural gravíssimo (uma falha catastrófica de pânico no kernel), todos os apartamentos sentem o impacto imediatamente.

Em termos de arquitetura de computadores, a virtualização tradicional funciona por meio de um **hipervisor** (*hypervisor*). Em hipervisores do Tipo 1 (como VMware ESXi, KVM e Xen) ou do Tipo 2 (como VirtualBox e VMware Workstation), o software cria uma camada de emulação de hardware completa. Cada máquina virtual convidada (*guest*) acredita piamente que tem processadores x86 exclusivos, barramentos PCI, placas de rede Realtek ou Intel e controladoras de disco dedicadas. Por conta disso, cada máquina virtual precisa carregar um sistema operacional convidado completo: rodar o processo de inicialização (*bootloader*), subir um kernel próprio, inicializar serviços de sistema (como o *systemd*) e carregar drivers. Isso consome centenas de megabytes de memória RAM apenas para manter a máquina em espera, além de exigir minutos preciosos para reiniciar.

```
        VIRTUALIZAÇÃO (VM)                           CONTÊINERES

┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│  App A   │   App B   │   App C  │       │  App A   │   App B   │   App C  │
├──────────┼───────────┼──────────┤       ├──────────┼───────────┼──────────┤
│ Libs /   │  Libs /   │  Libs /  │       │ Libs /   │  Libs /   │  Libs /  │
│ Bins     │  Bins     │  Bins    │       │ Bins     │  Bins     │  Bins    │
├──────────┼───────────┼──────────┤       ├──────────┴───────────┴──────────┤
│ Guest OS │ Guest OS  │ Guest OS │       │        Container Runtime        │
│ (Kernel) │ (Kernel)  │ (Kernel) │       │     (containerd, runc, crun)    │
├──────────┴───────────┴──────────┤       ├─────────────────────────────────┤
│           Hypervisor            │       │       Sistema Operacional       │
│       (KVM, Xen, VMware)        │       │       Host (Kernel Linux)       │
├─────────────────────────────────┤       ├─────────────────────────────────┤
│         Hardware Físico         │       │         Hardware Físico         │
└─────────────────────────────────┘       └─────────────────────────────────┘
```

Nos contêineres, essa camada de emulação de hardware simplesmente não existe. Quando você inicia um contêiner, o runtime não pede para uma CPU virtual dar boot. Ele simplesmente faz chamadas de sistema normais do Linux (como `clone` e `execve`) para criar um novo processo comum no sistema hospedeiro. 

A diferença reside no fato de que esse novo processo recebe restrições estritas do kernel sobre o que ele pode visualizar e quantos recursos ele pode consumir. O tempo de inicialização cai de quarenta segundos para dez milissegundos porque criar um contêiner tem exatamente o mesmo custo computacional que iniciar qualquer programa na linha de comando.

| Característica | Máquina Virtual Tradicional | Contêiner Linux |
| :--- | :--- | :--- |
| **Tempo de Inicialização** | Dezenas de segundos a minutos | Poucos milissegundos |
| **Overhead de Memória** | Alto (kernel próprio + daemons do SO convidado) | Mínimo (apenas o consumo real da aplicação) |
| **Arquitetura de Isolamento** | Hardware emulado por hipervisor | Recursos isolados e limitados pelo mesmo kernel |
| **Tamanho dos Artefatos** | Gigabytes (imagens de disco completas) | Megabytes (apenas binários e bibliotecas extras) |
| **Densidade Operacional** | Dezenas de VMs por servidor físico | Centenas a milhares de contêineres por servidor |
| **Heterogeneidade de Kernel** | Total (Linux roda sobre Windows, BSD sobre Linux) | Inexistente (compartilha estritamente o kernel host) |
| **Superfície de Ataque** | Menor (barreira física de hardware emulado) | Maior (compartilhamento direto de chamadas ao kernel) |

Essa tabela deixa claro o que um contêiner realmente é: o resultado de três tecnologias nativas do kernel Linux trabalhando em uníssono. Os **namespaces** criam as paredes visuais de isolamento, os **cgroups** agem como o medidor de consumo de recursos, e os **union filesystems** estruturam o sistema de arquivos em camadas. Vamos analisar detalhadamente cada uma dessas peças.

## Namespaces: Os Muros de Isolamento do Kernel

Se um contêiner é apenas um processo comum rodando no mesmo kernel do hospedeiro, surge a pergunta inevitável: como uma aplicação dentro do contêiner não enxerga os outros processos do servidor, não escuta conexões nas interfaces de rede de outras aplicações e não acessa os arquivos das outras pastas?

A resposta atende pelo nome de **namespaces** [^1].

Um *namespace* é uma camada de abstração do kernel Linux que envelopa recursos globais do sistema em partições isoladas. Quando um processo é colocado dentro de um namespace, ele passa a enxergar uma visão filtrada e privativa daquele recurso específico. Para todos os efeitos práticos, aquele processo tem a ilusão completa de que é a única entidade existente em toda a máquina.

O kernel Linux disponibiliza atualmente oito tipos diferentes de namespaces, cada um responsável por fatiar um subsistema específico:

| Namespace | Flag no Kernel | Recurso Isolado | Kernel Inicial | Ano de Introdução |
| :--- | :--- | :--- | :--- | :--- |
| **MNT** | `CLONE_NEWNS` | Pontos de montagem do sistema de arquivos | 2.4.19 | 2002 |
| **UTS** | `CLONE_NEWUTS` | Nome da máquina (*hostname*) e domínio NIS | 2.6.19 | 2006 |
| **IPC** | `CLONE_NEWIPC` | Filas de mensagens POSIX/SysV e memória compartilhada | 2.6.19 | 2006 |
| **PID** | `CLONE_NEWPID` | Árvore de identificadores de processos | 2.6.24 | 2008 |
| **NET** | `CLONE_NEWNET` | Interfaces de rede, rotas, regras de firewall e portas | 2.6.29 | 2009 |
| **USER** | `CLONE_NEWUSER` | Mapeamento de identificadores de usuário e grupo (UID/GID) | 3.8 | 2013 |
| **CGROUP** | `CLONE_NEWCGROUP`| Visão da própria hierarquia do pseudo-sistema cgroup | 4.6 | 2016 |
| **TIME** | `CLONE_NEWTIME` | Relógios de inicialização e contadores de tempo monotônico | 5.6 | 2020 |

A criação e manipulação desses muros é realizada por três chamadas de sistema fundamentais: `clone()` (que aceita as flags `CLONE_NEW*` para criar um processo filho já nascido em novos namespaces), `unshare()` (que desconecta o processo atual de seus namespaces herdados) e `setns()` (que anexa um processo em execução a um namespace preexistente).

Vamos deixar a teoria de lado e exercitar essas chamadas diretamente no terminal.

### Isolamento de Processos: O Namespace PID

No Linux, todo processo possui um número identificador único chamado PID. O primeiro processo inicializado pelo kernel ao ligar a máquina recebe o PID 1 (tradicionalmente o `/sbin/init` ou o `systemd`). Todos os outros processos do sistema são descendentes diretos ou indiretos dele.

Quando você isola o namespace PID, o primeiro processo disparado dentro do novo ambiente recebe o PID 1 privativo. Ele se torna o processo pai de todas as tarefas daquele espaço. Ao mesmo tempo, ele perde totalmente a capacidade de enxergar ou enviar sinais de encerramento (`kill`) para qualquer processo que esteja no hospedeiro.

Vamos abrir uma sessão isolada usando o comando utilitário `unshare` [^2]:

```bash
# No host: conferir a quantidade massiva de processos normais
$ ps aux | head -n 5
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0 169592 13092 ?        Ss   09:00   0:01 /sbin/init
root         2  0.0  0.0      0     0 ?        S    09:00   0:00 [kthreadd]
root         3  0.0  0.0      0     0 ?        I<   09:00   0:00 [rcu_gp]
root         4  0.0  0.0      0     0 ?        I<   09:00   0:00 [rcu_par_gp]

# Criar um namespace PID isolado disparando um novo shell bash
$ sudo unshare --pid --fork --mount-proc bash

# Dentro do novo ambiente: listar os processos ativos
$ ps aux
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.0  0.0   8536  5312 pts/0    S    14:00   0:00 bash
root         2  0.0  0.0  10072  3456 pts/0    R+   14:00   0:00 ps aux
```
*A flag `--mount-proc` remonta o sistema de arquivos `/proc` no novo contexto; sem ela, o utilitário ps continuaria lendo a tabela de processos do host.*

Repare no detalhe da chamada: a flag `--fork` é estritamente necessária porque a chamada de sistema `unshare(CLONE_NEWPID)` afeta apenas os processos filhos criados posteriormente. Para que o seu shell assuma o papel de PID 1 dentro do novo espaço, o utilitário precisa criar um processo filho bifurcado (*forked*).

### Isolamento de Rede: O Namespace NET

O namespace de rede isola todos os artefatos relacionados à comunicação: tabelas de roteamento, regras de filtragem (*iptables* e *nftables*), sockets abertos e interfaces de rede físicas ou lógicas.

Quando um novo namespace NET é instanciado, ele nasce como um deserto digital:

```bash
# No hospedeiro: listar interfaces existentes
$ ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
    link/ether bc:24:11:43:82:aa brd ff:ff:ff:ff:ff:ff
3: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default
    link/ether 02:42:1a:de:99:11 brd ff:ff:ff:ff:ff:ff

# Disparar um namespace de rede isolado
$ sudo unshare --net bash

# Verificar as interfaces disponíveis no novo contexto
$ ip link
1: lo: <LOOPBACK> mtu 65536 qdisc noop state DOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00

# Tentar consultar tabelas de roteamento
$ ip route
# (absolutamente nada retornado)
```
*O namespace de rede nasce isolado do mundo exterior, contendo exclusivamente a interface de loopback em estado desligado.*

É exatamente por essa razão que um contêiner Docker recém-criado não interfere nas portas do seu computador hospedeiro. Se uma aplicação subir escutando na porta 80 dentro do contêiner, essa porta fica aberta apenas dentro do seu namespace de rede privativo. Para expô-la ao mundo exterior, ferramentas como o Docker criam pares de interfaces virtuais conectadas por um cabo de rede virtual imaginário (*veth pair*), plugando uma ponta dentro do contêiner e a outra em uma ponte de rede (*bridge*) no hospedeiro.

### Isolamento de Hostname: O Namespace UTS

O namespace UTS (cujo nome histórico vem de *UNIX Timesharing System*) permite que um grupo de processos tenha seu próprio nome de máquina (*hostname*) e domínio de rede sem impactar o resto do sistema.

```bash
# Consultar nome original do host
$ hostname
meu-servidor-producao

# Criar namespace UTS e trocar o nome localmente
$ sudo unshare --uts bash
$ hostname container-temporario
$ hostname
container-temporario

# Sair da sessão isolada e conferir o host original
$ exit
$ hostname
meu-servidor-producao
```
*O hostname configurado dentro da sessão isolada desaparece ao sair, mantendo a configuração do hospedeiro intacta.*

### Inspecionando os Namespaces no Próprio Linux

Toda essa mágica não fica escondida em estruturas de dados misteriosas. O Linux expõe os namespaces de qualquer tarefa em execução através do pseudo-sistema de arquivos `/proc`.

Se você listar a pasta `/proc/<PID>/ns/`, verá apontadores simbólicos especiais:

```bash
# Inspecionar os namespaces do seu próprio terminal
$ ls -la /proc/self/ns/
total 0
dr-x--x--x 2 rolim rolim 0 set  8 14:00 .
dr-xr-xr-x 9 rolim rolim 0 set  8 14:00 ..
lrwxrwxrwx 1 rolim rolim 0 set  8 14:00 cgroup -> 'cgroup:[4026531835]'
lrwxrwxrwx 1 rolim rolim 0 set  8 14:00 ipc -> 'ipc:[4026531839]'
lrwxrwxrwx 1 rolim rolim 0 set  8 14:00 mnt -> 'mnt:[4026531841]'
lrwxrwxrwx 1 rolim rolim 0 set  8 14:00 net -> 'net:[4026531840]'
lrwxrwxrwx 1 rolim rolim 0 set  8 14:00 pid -> 'pid:[4026531836]'
lrwxrwxrwx 1 rolim rolim 0 set  8 14:00 pid_for_children -> 'pid:[4026531836]'
lrwxrwxrwx 1 rolim rolim 0 set  8 14:00 time -> 'time:[4026531834]'
lrwxrwxrwx 1 rolim rolim 0 set  8 14:00 time_for_children -> 'time:[4026531834]'
lrwxrwxrwx 1 rolim rolim 0 set  8 14:00 user -> 'user:[4026531837]'
lrwxrwxrwx 1 rolim rolim 0 set  8 14:00 uts -> 'uts:[4026531838]'
```
*Os números entre colchetes representam o identificador de inode do namespace no kernel; dois processos compartilham o mesmo namespace se os números de inode forem idênticos.*

Agora veja a prova cabal. Vamos subir um contêiner com o Docker e inspecionar os mesmos apontadores a partir do sistema operacional hospedeiro:

{% raw %}
```bash
# Subir um contêiner alpine dormindo em segundo plano
$ docker run -d --name teste-namespaces alpine sleep 3600

# Descobrir o PID do processo sleep no hospedeiro
$ CONTAINER_PID=$(docker inspect -f '{{.State.Pid}}' teste-namespaces)
$ echo "O PID real no hospedeiro é: $CONTAINER_PID"
O PID real no hospedeiro é: 28419

# Comparar os namespaces do contêiner com os do hospedeiro
$ ls -l /proc/$CONTAINER_PID/ns/net /proc/1/ns/net
lrwxrwxrwx 1 root root 0 set  8 14:05 /proc/1/ns/net -> 'net:[4026531840]'
lrwxrwxrwx 1 root root 0 set  8 14:05 /proc/28419/ns/net -> 'net:[4026532455]'
```
{% endraw %}
*Os números de inode são completamente diferentes, comprovando que o processo do contêiner vive em um namespace de rede próprio.*

### O Segredo do Comando docker exec: nsenter

Quando você roda `docker exec -it teste-namespaces sh`, o Docker não cria um contêiner novo nem faz conexões remotas via SSH. Ele simplesmente descobre o PID do processo principal do contêiner no hospedeiro e executa a chamada de sistema `setns()` para colocar um novo terminal dentro dos mesmos namespaces já utilizados por aquele contêiner.

O utilitário de linha de comando que faz isso diretamente no Linux chama-se `nsenter` [^3]:

```bash
# Entrar nos namespaces do contêiner usando apenas ferramentas padrão do Linux
$ sudo nsenter --target $CONTAINER_PID --pid --net --mount --uts --ipc sh

# Agora estamos dentro da visão do contêiner
/ # hostname
teste-namespaces
/ # ps aux
PID   USER     TIME  COMMAND
    1 root      0:00 sleep 3600
    7 root      0:00 sh
    8 root      0:00 ps aux
/ # exit
```
*O comando nsenter anexa o terminal aos namespaces do processo alvo sem depender do daemon do Docker.*

> [!TIP] Dica de Bastidor
> Da próxima vez que o daemon do Docker travar e não responder aos comandos convencionais, você não precisa ficar desesperado. Se o processo do contêiner ainda estiver vivo na tabela de processos do Linux, você pode usar `nsenter` para entrar diretamente no ambiente, diagnosticar arquivos de log e salvar seus dados sem depender de reiniciar serviço algum.

## Cgroups: O Guarda de Recursos

Os *namespaces* resolvem com brilhantismo a questão da visibilidade: eles garantem que os processos não enxerguem o que não devem. Mas imagine a seguinte situação: você cria um contêiner em um namespace isolado, mas uma linha de código maliciosa ou mal implementada dispara um laço infinito que aloca memória sem parar ou cria milhares de threads simultâneas.

Se dependêssemos apenas de namespaces, esse contêiner solitário consumiria 100% da CPU do computador, esgotaria toda a memória física do hospedeiro e causaria o travamento total do sistema operacional, derrubando todos os outros contêineres que dividem o mesmo servidor.

Para resolver o problema do consumo desenfreado de hardware, entram em cena os **Control Groups** ou simplesmente **cgroups** [^4].

Se o namespace representa a **parede de alvenaria do seu apartamento**, o cgroup é a **caixa de disjuntores e o hidrômetro**: ele determina rigidamente quanta corrente elétrica e quantos litros de água aquele cômodo tem permissão para puxar da rede principal.

No Linux, os cgroups não são configurados por meio de interfaces obscuras ou comandos mágicos. Eles são implementados como um pseudo-sistema de arquivos montado tradicionalmente no caminho `/sys/fs/cgroup/`. Isso significa que, para criar um grupo de controle, limitar recursos e associar processos a ele, basta usar operações básicas de sistema de arquivos: criar pastas com `mkdir` e escrever valores numéricos em arquivos de texto com comandos simples como `echo`.

### A Grande Mudança: Cgroups v1 versus Cgroups v2

Durante muitos anos, o Linux utilizou a primeira versão dos grupos de controle (cgroups v1). No modelo v1, cada recurso (CPU, memória, entrada e saída de disco, identificadores de processo) vivia em uma hierarquia de diretórios totalmente separada e independente dentro de `/sys/fs/cgroup/`. Um processo podia pertencer ao grupo `limite-baixo` na hierarquia de memória, mas pertencer ao grupo `prioridade-alta` na hierarquia de CPU.

Na prática, gerenciar essa matriz multidimensional virou um pesadelo de complexidade para os desenvolvedores de sistemas operacionais. Além disso, surgiam inconsistências graves: o controlador de memória não conversava direito com o controlador de gravação em disco (*writeback cache*), gerando bloqueios misteriosos de I/O.

Para solucionar essas dores, o engenheiro Tejun Heo liderou a reestruturação que deu origem aos **cgroups v2** (também conhecida como *Unified Hierarchy* ou hierarquia unificada) [^5]. No cgroups v2, existe apenas uma árvore de diretórios unificada. Um processo pertence a exatamente um cgroup, e todos os controladores de recursos habilitados para aquele grupo são aplicados de forma consistente sobre os mesmos processos.

Você pode verificar qual versão está em operação no seu sistema inspecionando as montagens:

```bash
# Verificar o tipo de montagem ativa em /sys/fs/cgroup
$ mount | grep cgroup
cgroup2 on /sys/fs/cgroup type cgroup2 (rw,nosuid,nodev,noexec,relatime,nsdelegate)
```
*Se a saída indicar o tipo cgroup2, seu sistema já opera com a moderna hierarquia unificada adotada por padrão em distribuições recentes como Debian 12+, Ubuntu 22.04+ e Fedora.*

Os principais controladores de recursos disponíveis no cgroups v2 e seus arquivos correspondentes são apresentados na tabela a seguir:

| Controlador | O que gerencia | Arquivos Chave no cgroup v2 | Exemplo de Valor Aplicado |
| :--- | :--- | :--- | :--- |
| **memory** | Consumo de RAM física e área de swap | `memory.max`, `memory.current`, `memory.events` | `536870912` (limite estrito de 512 MB) |
| **cpu** | Tempo de processamento e cotas em milissegundos | `cpu.max`, `cpu.weight`, `cpu.stat` | `150000 100000` (limita a 1.5 núcleos de CPU) |
| **pids** | Quantidade máxima de processos simultâneos | `pids.max`, `pids.current` | `50` (evita ataques de fork bomb) |
| **io** | Largura de banda e operações por segundo em disco | `io.max`, `io.stat` | `8:0 rbps=10485760` (limite de leitura a 10 MB/s) |
| **cpuset** | Fixação de processos em núcleos específicos | `cpuset.cpus`, `cpuset.mems` | `0,2` (amarra execução apenas nos núcleos 0 e 2) |

### Criando e Testando um Cgroup Manualmente

Vamos construir um grupo de controle na mão, sem recorrer ao Docker, para ver a mecânica pura do kernel em ação.

Primeiro, garantimos que os controladores desejados estejam habilitados para delegação na raiz dos cgroups:

```bash
# Habilitar controladores de memória e processos para os subdiretórios
$ echo "+memory +pids" | sudo tee /sys/fs/cgroup/cgroup.subtree_control
+memory +pids

# Criar um novo grupo de controle chamado laboratorio-cgroup
$ sudo mkdir /sys/fs/cgroup/laboratorio-cgroup

# Inspecionar os arquivos gerados automaticamente pelo kernel dentro da nova pasta
$ ls /sys/fs/cgroup/laboratorio-cgroup/
cgroup.controllers      cgroup.procs            memory.high             memory.stat
cgroup.events           cgroup.stat             memory.max              pids.current
cgroup.freeze           cgroup.subtree_control  memory.min              pids.events
cgroup.kill             memory.current          memory.oom.group        pids.max
```
*O simples fato de criar um diretório faz o kernel popular instantaneamente a pasta com as interfaces de controle do cgroup v2.*

Agora vamos estabelecer limites rígidos para este grupo: um teto de 50 megabytes de memória RAM e um limite de no máximo 20 processos simultâneos:

```bash
# Definir o limite de memória em bytes (50 MB = 52428800 bytes)
$ echo "52428800" | sudo tee /sys/fs/cgroup/laboratorio-cgroup/memory.max
52428800

# Definir o limite máximo de processos (pids)
$ echo "20" | sudo tee /sys/fs/cgroup/laboratorio-cgroup/pids.max
20

# Conferir se as configurações foram gravadas
$ cat /sys/fs/cgroup/laboratorio-cgroup/memory.max
52428800
```
*Valores gravados nesses arquivos são imediatamente assumidos pelo subsistema de alocação de memória do kernel.*

Para colocar um processo sob a tutela desse cgroup, basta escrever o número do seu PID dentro do arquivo `cgroup.procs`. Vamos anexar a sessão atual do nosso terminal (representada pela variável especial `$$`):

```bash
# Mover o shell atual para dentro do cgroup criado
$ echo $$ | sudo tee /sys/fs/cgroup/laboratorio-cgroup/cgroup.procs

# Consultar o consumo atual de memória da nossa sessão em bytes
$ cat /sys/fs/cgroup/laboratorio-cgroup/memory.current
1925120
```
*O shell consome aproximadamente 1.8 MB de memória RAM; o kernel rastreia a contabilidade em tempo real com precisão de bytes.*

### O Guarda em Ação: O Assassino OOM (Out of Memory Killer)

O que acontece se uma aplicação que vive dentro de um cgroup tentar ultrapassar o teto estipulado no arquivo `memory.max`?

O kernel Linux entra em ação através do mecanismo **OOM Killer** (*Out of Memory Killer*). Ele avalia os processos pertencentes àquele grupo específico e envia um sinal fatal `SIGKILL` para eliminar a aplicação gulosa, protegendo a estabilidade de todo o restante do servidor hospedeiro.

Vamos forçar essa situação usando o Docker com limites declarados:

{% raw %}
```bash
# Subir um contêiner limitado a meros 30 MB de RAM e tentar forçar o consumo de 60 MB
$ docker run --name teste-estouro --memory=30m alpine sh -c \
    "head -c 60M /dev/zero | tail -c +1 > /dev/null"

# Inspecionar o motivo do encerramento do contêiner
$ docker inspect teste-estouro --format='Status: {{.State.Status}} | OOMKilled: {{.State.OOMKilled}} | ExitCode: {{.State.ExitCode}}'
Status: exited | OOMKilled: true | ExitCode: 137
```
{% endraw %}
*O código de saída 137 indica terminação por sinal fatal (128 + 9 para SIGKILL), acompanhado pelo marcador OOMKilled configurado como verdadeiro.*

Se você consultar as mensagens de diagnóstico do kernel no mesmo instante com o comando `dmesg`, verá o registro oficial do evento:

```bash
$ sudo dmesg -T | tail -n 6
[...] oom-kill:constraint=CONSTRAINT_MEMCG,nodemask=(null),cpuset=docker-...
[...] memory: usage 30720kB, limit 30720kB, failcnt 1
[...] Memory cgroup out of memory: Killed process 31405 (sh) total-vm:63280kB, anon-rss:29840kB
```
*O kernel deixa registrado explicitamente que o encerramento ocorreu por restrição do grupo de controle de memória (CONSTRAINT_MEMCG).*

> [!WARNING] Alerta de Produção
> Em ambientes de produção, contêineres morrendo misteriosamente com código 137 são quase sempre vítimas do OOM Killer. Monitore a métrica `memory.current` ou configure alertas em ferramentas de observabilidade antes que ela alcance a marca do `memory.max`.

> [!TIP] Ferramentas de Inspeção de Cgroups
> Você pode conferir os limites de qualquer contêiner Docker em tempo real diretamente no hospedeiro. O comando `docker stats --no-stream` exibe uma tabela resumida de consumo (CPU, memória, rede, PIDs) que é uma leitura formatada dos arquivos do cgroup de cada contêiner. Para uma investigação mais granular, descubra o PID real com `docker inspect -f '{% raw %}{{.State.Pid}}{% endraw %}' <nome>`, consulte `/proc/<PID>/cgroup` para localizar o caminho do grupo de controle e leia diretamente os arquivos `memory.max`, `cpu.max` e `pids.current` sob `/sys/fs/cgroup/`.

## Union Filesystems: Imagens em Camadas

Chegamos à terceira perna do nosso tripé fundamental. Até aqui, vimos como os *namespaces* isolam a visão dos processos e como os *cgroups* limitam o consumo de memória e processamento. Mas resta um problema crucial: de onde vem o sistema de arquivos que o contêiner enxerga?

Se você baixar uma imagem oficial do Ubuntu, ela tem cerca de 80 megabytes. Se você precisar rodar cem contêineres idênticos desse mesmo Ubuntu no mesmo servidor, copiar 80 MB cem vezes gastaria 8 gigabytes de espaço em disco e demoraria vários segundos durante a clonagem.

A solução elegante encontrada pelo ecossistema de contêineres é o uso de **Sistemas de Arquivos de União** (*Union Filesystems*), materializados no Linux moderno pelo driver de kernel **OverlayFS** [^6].

### A Mecânica do Copy-on-Write (CoW)

A ideia central de um sistema de arquivos de união é sobrepor múltiplos diretórios de forma transparente, apresentando para quem consome o ponto de montagem a ilusão de um único diretório unificado.

As imagens de contêiner são compostas por uma pilha de camadas estáticas somente leitura (*read-only*). Cada comando executado no processo de construção de uma imagem gera uma nova fatia fina gravada em disco. Quando você inicia um contêiner baseado nessa imagem, o runtime não duplica esses dados: ele simplesmente adiciona uma camada finíssima e efêmera de leitura e escrita (*read-write*) no topo de toda a pilha.

A regra de ouro desse modelo chama-se **Copy-on-Write (CoW)**:
1. **Operação de Leitura**: Se a sua aplicação ler um arquivo que pertence à imagem base, o sistema acessa diretamente o arquivo na camada inferior somente leitura.
2. **Operação de Modificação**: No milissegundo em que sua aplicação tenta alterar um arquivo existente da imagem base, o OverlayFS intercepta a chamada, faz uma cópia idêntica daquele arquivo para a camada superior de escrita e aplica a alteração exclusivamente na cópia. O arquivo original na camada inferior permanece 100% intocado.
3. **Operação de Criação**: Qualquer novo arquivo criado vai direto para a camada superior de escrita.
4. **Operação de Remoção**: Se um arquivo da camada base for apagado, o OverlayFS cria um arquivo especial de bloqueio (*whiteout file*) na camada de escrita, ocultando o arquivo original da visão unificada.

```
┌─────────────────────────────────────────────────────────┐
│              VISÃO UNIFICADA DO CONTÊINER               │  <- Diretório "merged"
│            /app  /etc  /usr  /bin  /tmp                 │     (o processo enxerga isto)
├─────────────────────────────────────────────────────────┤
│          CAMADA DE ESCRITA EFÊMERA (R/W)                │  <- Diretório "upperdir"
│     Arquivos criados ou modificados pelo contêiner      │     (morre com o contêiner)
├─────────────────────────────────────────────────────────┤
│          CAMADA DA IMAGEM: COPY app.jar (R/O)           │  <- Diretório "lowerdir[0]"
├─────────────────────────────────────────────────────────┤
│          CAMADA DA IMAGEM: RUN apt-get install (R/O)    │  <- Diretório "lowerdir[1]"
├─────────────────────────────────────────────────────────┤
│          CAMADA BASE: FROM debian:bookworm (R/O)        │  <- Diretório "lowerdir[2]"
└─────────────────────────────────────────────────────────┘
```

O OverlayFS estrutura essa mágica dividindo a operação em quatro diretórios fundamentais:
- **`lowerdir`**: Os diretórios base somente leitura (as camadas da imagem). Múltiplos caminhos podem ser encadeados separando-os por dois-pontos.
- **`upperdir`**: O diretório de leitura e escrita onde ficam as modificações efetuadas pelo contêiner.
- **`workdir`**: Uma pasta de serviço interna necessária para o kernel preparar operações atômicas antes de exibi-las.
- **`merged`**: O diretório final onde o sistema de arquivos unificado é montado e disponibilizado para consumo.

### Montando um OverlayFS na Mão

Para entender isso em definitivo, nada melhor do que criar as camadas e montá-las manualmente sem usar nenhum comando do Docker:

```bash
# Criar a estrutura física dos diretórios no /tmp
$ mkdir -p /tmp/experimento-overlay/{base,escrita,trabalho,unificado}

# Criar arquivos simulando uma camada base de sistema operacional
$ echo "Configuracao padrao v1.0" > /tmp/experimento-overlay/base/sistema.conf
$ echo "Binario utilitario" > /tmp/experimento-overlay/base/ferramenta.sh
$ chmod +x /tmp/experimento-overlay/base/ferramenta.sh

# Montar o OverlayFS usando o utilitário padrão de montagem do Linux
$ sudo mount -t overlay overlay \
    -o lowerdir=/tmp/experimento-overlay/base,upperdir=/tmp/experimento-overlay/escrita,workdir=/tmp/experimento-overlay/trabalho \
    /tmp/experimento-overlay/unificado

# Listar o conteúdo da visão unificada
$ ls /tmp/experimento-overlay/unificado/
ferramenta.sh  sistema.conf

# Conferir o conteúdo do arquivo lido da camada base
$ cat /tmp/experimento-overlay/unificado/sistema.conf
Configuracao padrao v1.0
```
*A pasta unificada expõe perfeitamente os arquivos que fisicamente residem dentro da pasta base.*

Agora, vamos observar o comportamento do *Copy-on-Write* alterando um arquivo e criando um item inédito:

```bash
# Modificar o arquivo existente através do diretório unificado
$ echo "Configuracao customizada pelo usuario" > /tmp/experimento-overlay/unificado/sistema.conf

# Criar um arquivo novo dentro da visão unificada
$ echo "Arquivo gerado em execucao" > /tmp/experimento-overlay/unificado/novo.log

# O arquivo original na camada base PERMANECE INTACTO
$ cat /tmp/experimento-overlay/base/sistema.conf
Configuracao padrao v1.0

# O arquivo modificado e o arquivo novo foram parar no diretório de escrita (upperdir)
$ ls /tmp/experimento-overlay/escrita/
novo.log  sistema.conf

$ cat /tmp/experimento-overlay/escrita/sistema.conf
Configuracao customizada pelo usuario

# Desmontar o sistema de arquivos de teste
$ sudo umount /tmp/experimento-overlay/unificado
```
*A camada base permaneceu imutável; toda e qualquer alteração foi gravada exclusivamente dentro do diretório de escrita.*

Quando você roda `docker rm meu-container`, tudo o que o Docker precisa fazer em disco é deletar o diretório `upperdir` correspondente. As camadas da imagem base nunca foram alteradas, e por isso podem ser compartilhadas concorrentemente por centenas de contêineres sem risco de corrupção cruzada.

> [!TIP] Inspecionando Camadas pelo Docker
> Se quiser visualizar a pilha de camadas de qualquer imagem sem montá-las manualmente, use `docker image inspect <imagem> --format='{% raw %}{{json .RootFS.Layers}}{% endraw %}'`. A saída é uma lista de hashes SHA256 representando cada camada em ordem de empilhamento. Para um contêiner em execução, `docker inspect <contêiner> --format='{% raw %}{{json .GraphDriver.Data}}{% endraw %}'` revela os caminhos físicos exatos do `LowerDir`, `UpperDir`, `WorkDir` e `MergedDir` no sistema de arquivos do hospedeiro.

## A Especificação OCI e o Ecossistema de Runtimes

Nos primeiros anos de vida do Docker, toda essa orquestração de chamadas de sistema era centralizada em um daemon monolítico e proprietário. À medida que grandes empresas começaram a adotar contêineres para cargas de trabalho críticas, surgiu o receio de que o formato ficasse refém dos rumos comerciais de uma única empresa.

Para sanar essa preocupação, a indústria se uniu sob a tutela da Linux Foundation e instituiu a **Open Container Initiative (OCI)**. O trabalho da OCI gerou três padrões fundamentais abertos que regem o universo de contêineres até hoje:

1. **OCI Image Specification**: Define como uma imagem deve ser empacotada em disco. Uma imagem OCI nada mais é do que um conjunto de arquivos compactados (*tarballs*) contendo as camadas de arquivos do sistema, acompanhados de um manifesto em formato JSON descrevendo arquitetura de hardware, variáveis de ambiente, portas e comandos de entrada.
2. **OCI Runtime Specification**: Define como pegar aquele sistema de arquivos descompactado e executá-lo no sistema operacional. Ela descreve a estrutura de um arquivo padronizado chamado `config.json`, que lista os namespaces que devem ser criados, os limites de cgroups e os privilégios do processo.
3. **OCI Distribution Specification**: Padroniza a API HTTP para publicação, busca e transferência de imagens entre registros de contêineres (como Docker Hub, Quay.io, GitHub Container Registry e Amazon ECR).

### A Cadeia de Execução Moderna

Graças à padronização OCI, o ecossistema de execução foi modularizado em camadas independentes de responsabilidade:

```
┌──────────────┐
│  docker CLI  │  Interface com o usuário (interpreta comandos e flags)
└──────┬───────┘
       │  API REST (via socket unix /var/run/docker.sock)
       ▼
┌──────────────┐
│   dockerd    │  Daemon de gerenciamento (imagens, volumes, redes e API)
└──────┬───────┘
       │  gRPC
       ▼
┌──────────────┐
│  containerd  │  Runtime de Alto Nível (baixa imagens, gerencia ciclo de vida)
└──────┬───────┘
       │  Execução OCI
       ▼
┌──────────────┐
│     runc     │  Runtime de Baixo Nível (chama clone, unshare, cgroups e morre)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Processo   │  Sua aplicação rodando isolada dentro do kernel
└──────────────┘
```

Repare na separação nítida:
- O **Runtime de Alto Nível** (como `containerd` ou `CRI-O`) é responsável por baixar imagens pela rede, validar assinaturas criptográficas, descompactar camadas em disco e preparar o sistema de arquivos montado.
- O **Runtime de Baixo Nível** (como `runc` ou `crun`) tem um papel estritamente pontual: ele recebe uma pasta já montada com um arquivo `config.json`, invoca as chamadas de sistema do kernel (`unshare`, `mount`, configuração de cgroup), executa o binário da sua aplicação e em seguida se encerra, deixando o processo isolado rodando supervisionado pelo kernel.

### O Raio-X do config.json da OCI

Você pode comprovar que um contêiner não passa de uma pasta com um arquivo JSON utilizando o próprio `runc` [^7] instalado no sistema.

Vamos gerar uma especificação padrão de contêiner OCI:

```bash
# Criar uma pasta temporária para o nosso pacote OCI
$ mkdir -p /tmp/bundle-oci && cd /tmp/bundle-oci

# Gerar o arquivo de configuração de referência da OCI
$ runc spec

# Inspecionar as primeiras linhas do arquivo gerado
$ head -n 35 config.json
{
	"ociVersion": "1.0.2-dev",
	"process": {
		"terminal": true,
		"user": {
			"uid": 0,
			"gid": 0
		},
		"args": [
			"sh"
		],
		"env": [
			"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
			"TERM=xterm"
		],
		"cwd": "/"
	},
	"root": {
		"path": "rootfs",
		"readonly": true
	},
	"hostname": "runc",
	"mounts": [
		{
			"destination": "/proc",
			"type": "proc",
			"source": "proc"
		}
```
*O arquivo config.json padroniza universalmente cada parâmetro de execução do processo.*

Se você rolar o arquivo até a seção `linux`, encontrará exatamente as estruturas de dados que estudamos nas seções anteriores deste post:

```json
"namespaces": [
	{ "type": "pid" },
	{ "type": "network" },
	{ "type": "ipc" },
	{ "type": "uts" },
	{ "type": "mount" }
]
```

Qualquer ferramenta que gere essa pasta com essa estrutura consegue rodar um contêiner em qualquer distribuição Linux do planeta. É a interoperabilidade levada ao estado da arte.

| Runtime de Baixo Nível | Linguagem | Mantenedor | Características Principais |
| :--- | :--- | :--- | :--- |
| **runc** | Go | OCI / Comunidade | A implementação de referência padrão utilizada pelo Docker e containerd |
| **crun** | C puro | Red Hat | Extremamente veloz, menor pegada de memória, padrão no Podman |
| **youki** | Rust | Comunidade | Implementação segura em memória aproveitando o ecossistema Rust |
| **gVisor (runsc)** | Go | Google | Intercepta chamadas de sistema em espaço de usuário para isolamento extremo |
| **Kata Containers** | Go / C | OpenInfra | Executa o contêiner dentro de uma micro-máquina virtual QEMU/Cloud-Hypervisor |

## Grand Finale: Construindo um Mini-Contêiner do Zero

Chegou a hora de juntar todas as peças. Nós vimos a história, entendemos por que contêineres não são máquinas virtuais, exploramos os *namespaces*, configuramos *cgroups* na mão e montamos camadas com *OverlayFS*.

Agora, vamos provar a tese inicial: **um contêiner é apenas um processo com a coleira do kernel**.

Abaixo está o código de um script em Bash funcional com cerca de 50 linhas úteis. Ele faz absolutamente tudo o que o Docker faz por baixo do capô quando você roda `docker run`: baixa uma distribuição Linux mínima oficial (Alpine Linux), monta as camadas com OverlayFS preservando a imagem intacta, cria um cgroup v2 com limites estritos de memória e quantidade de processos, isola todos os namespaces necessários e entrega um terminal interativo com o processo assumindo o PID 1.

```bash
#!/bin/bash
# mini-container.sh: Um motor de contêineres funcional em ~50 linhas de shell script
# Uso: sudo ./mini-container.sh
set -euo pipefail

CONTAINER_DIR="/tmp/mini-container-lab"
ALPINE_VERSION="3.20"
ALPINE_ARCH="x86_64"
ALPINE_URL="https://dl-cdn.alpinelinux.org/alpine/v${ALPINE_VERSION}/releases/${ALPINE_ARCH}/alpine-minirootfs-${ALPINE_VERSION}.0-${ALPINE_ARCH}.tar.gz"
CGROUP_NAME="mini-conteiner-$$"
MEMORY_LIMIT="104857600"  # Limite estrito de 100 MB em bytes
PIDS_LIMIT="50"           # Limite máximo de 50 processos

echo "==> [1/6] Preparando estrutura de diretórios do OverlayFS..."
mkdir -p "${CONTAINER_DIR}"/{rootfs,upper,work,merged}

echo "==> [2/6] Obtendo imagem base oficial do Alpine Linux ${ALPINE_VERSION}..."
if [ ! -f "${CONTAINER_DIR}/alpine.tar.gz" ]; then
    curl -fsSL "${ALPINE_URL}" -o "${CONTAINER_DIR}/alpine.tar.gz"
    tar xzf "${CONTAINER_DIR}/alpine.tar.gz" -C "${CONTAINER_DIR}/rootfs"
fi

echo "==> [3/6] Montando sistema de arquivos OverlayFS (camadas CoW)..."
mount -t overlay overlay \
    -o "lowerdir=${CONTAINER_DIR}/rootfs,upperdir=${CONTAINER_DIR}/upper,workdir=${CONTAINER_DIR}/work" \
    "${CONTAINER_DIR}/merged"

echo "==> [4/6] Configurando limites de recursos via Cgroup v2 (${CGROUP_NAME})..."
CGROUP_PATH="/sys/fs/cgroup/${CGROUP_NAME}"
mkdir -p "${CGROUP_PATH}"
echo "${MEMORY_LIMIT}" > "${CGROUP_PATH}/memory.max"
echo "${PIDS_LIMIT}" > "${CGROUP_PATH}/pids.max"

echo "==> [5/6] Preparando arquivos de configuração (DNS)..."
cp /etc/resolv.conf "${CONTAINER_DIR}/merged/etc/resolv.conf" 2>/dev/null || true

echo "==> [6/6] Inicializando processo isolado em novos Namespaces..."
echo "     Ambiente pronto! Digite 'exit' para sair e liberar os recursos."
echo ""

# unshare isola PID, rede, hostname, IPC, pontos de montagem e cgroups
# Pseudo-sistemas (/proc, /sys, /dev) são montados no namespace privado do contêiner
unshare --pid --fork --net --uts --ipc --mount --cgroup \
    sh -c "
        echo \$\$ > '${CGROUP_PATH}/cgroup.procs' 2>/dev/null || true
        mount -t proc proc '${CONTAINER_DIR}/merged/proc'
        mount -t sysfs sysfs '${CONTAINER_DIR}/merged/sys'
        mount --bind /dev '${CONTAINER_DIR}/merged/dev'
        exec chroot '${CONTAINER_DIR}/merged' /bin/sh -c '
            hostname mini-conteiner
            export PATH=/bin:/sbin:/usr/bin:/usr/sbin
            echo \"==================================================\"
            echo \"  BEM-VINDO AO SEU CONTÊINER ARTESANAL!\"
            echo \"  Hostname: \$(hostname)\"
            echo \"  PID local: \$\$\"
            echo \"  Memória limitada a: 100 MB\"
            echo \"==================================================\"
            exec /bin/sh
        '
    "

echo ""
echo "==> Finalizando e desmontando camadas com segurança..."
sleep 1
umount -l "${CONTAINER_DIR}/merged" 2>/dev/null || true
rmdir "${CGROUP_PATH}" 2>/dev/null || true
echo "==> Limpeza concluída com sucesso."
```
*Script autossuficiente demonstrando a convergência prática de namespaces, cgroups v2 e OverlayFS.*

### Entendendo a Mecânica Passo a Passo

A elegância desse script reside no fato de que cada bloco de código espelha diretamente os conceitos que dissecamos ao longo de todo o texto:

O primeiro bloco prepara as quatro pastas exigidas pelo driver OverlayFS. O segundo passo faz o papel do comando `docker pull`: ele baixa um arquivo comprimido de apenas três megabytes contendo os binários do Alpine Linux e descompacta o conteúdo na pasta `rootfs`. Essa pasta atua como a nossa camada inferior imutável (`lowerdir`).

No terceiro passo, o script realiza a montagem do OverlayFS. O diretório `merged` passa a ser a nossa visão consolidada, enquanto a pasta `upper` acolherá qualquer arquivo modificado pelo usuário durante o teste.

No quarto passo, o script fala diretamente com o subsistema cgroups v2 do kernel: cria uma pasta correspondente ao grupo de controle do contêiner e grava os limites de cem megabytes de RAM e cinquenta identificadores de processo.

O quinto passo cuida da configuração básica de rede, copiando as definições de servidores DNS de `/etc/resolv.conf` para dentro do ambiente montado.

No sexto passo, a grande mágica se concretiza: o utilitário `unshare` dispara novas instâncias de todos os seis namespaces essenciais. No namespace privado de montagem recém-criado, o script monta os pseudo-sistemas de arquivos `/proc`, `/sys` e `/dev` (garantindo que o `/proc` reflita exclusivamente a tabela de processos do novo contêiner e que essas montagens desapareçam do hospedeiro assim que o namespace for encerrado). Antes de entregar o terminal ao usuário, o shell grava o seu próprio identificador de processo dentro do arquivo `cgroup.procs` daquele cgroup, garantindo que os limites de hardware passem a valer imediatamente. Em seguida, a chamada `exec chroot` substitui o processo atual pelo `/bin/sh` assumindo rigorosamente o PID 1.

Ao digitar `exit`, a rotina de encerramento entra em ação: desmonta o ponto OverlayFS e remove o diretório do cgroup, devolvendo o sistema operacional hospedeiro exatamente ao estado em que se encontrava.

> [!NOTE] Nota Operacional
> Para executar o script em sua plenitude, rode-o com `sudo` para permitir a execução de `mount` e a configuração de cgroups no sistema. Se você preferir uma abordagem sem privilégios administrativos no seu usuário diário, utilize ferramentas como o Podman, que orquestram esses mesmos passos combinando *User Namespaces* com ferramentas auxiliares como o `crun`.

## Exercícios

Para fixar a dinâmica de isolamento do kernel, namespaces, cgroups e OverlayFS, execute os desafios práticos abaixo no seu terminal Linux.

**1. Criando Rootless com User Namespaces**

Crie um namespace de usuário (*User Namespace*) sem utilizar privilégios de `sudo`, mapeando o seu usuário atual para o usuário `root` dentro da sessão isolada através do comando:

```bash
$ unshare --user --map-root-user bash
```

Dentro dessa nova sessão, execute os comandos `whoami` e `id`. Em seguida, abra outro terminal no seu hospedeiro, descubra o PID desse novo shell bash e verifique com qual usuário ele está registrado no sistema executando `ps -o user,pid,comm -p <PID>`. O que você observa e por que esse mecanismo é crucial para a segurança de contêineres modernos?

<details markdown="1">
<summary>Ver resposta</summary>

Ao rodar `whoami` e `id` dentro da sessão isolada, a saída exibirá `root` e `uid=0(root) gid=0(root)`. Para o ambiente interno, você tem poderes administrativos totais. Porém, ao consultar o mesmo processo no segundo terminal do hospedeiro através do `ps`, você verá que o processo continua pertencendo estritamente ao seu usuário normal sem privilégios.

Esse mecanismo é a base fundamental dos **contêineres sem root** (*rootless containers*). Se um invasor conseguir explorar uma falha de segurança na sua aplicação web e quebrar a execução dentro do contêiner, para o kernel do hospedeiro ele continua sendo apenas um usuário comum sem privilégio algum. Ele não consegue alterar arquivos de sistema, instalar módulos no kernel ou comprometer o servidor físico.

</details>

**2. O Bloqueio de Fork Bombs com o Controller de PIDs**

Suba um contêiner em segundo plano restringindo o número total de processos simultâneos com um teto de segurança (por exemplo, `--pids-limit=20`):

```bash
$ docker run -d --name teste-pids --pids-limit=20 alpine sleep 3600
```

Em seguida, conecte-se a ele via terminal interativo (`docker exec -it teste-pids sh`) e dispare a clássica *fork bomb* de shell do ecossistema Unix:

```bash
/ # :(){ :|:& };:
```

O que acontece a partir do momento em que a função recursiva atinge o limite? Como o hospedeiro se comporta e qual métrica no cgroup confirma a contenção?

<details markdown="1">
<summary>Ver resposta</summary>

A função recursiva `:` define uma rotina que se auto-invoca enviando instâncias para segundo plano através de um pipe (`:|:&`), gerando uma duplicação exponencial de tarefas ($2^n$).

Assim que o número total de processos atinge a cota de 20 (somando o shell `sh`, o processo inicial `sleep 3600` e as ramificações filhas), qualquer nova chamada de sistema `fork()` é sumariamente rejeitada pelo kernel Linux:

```text
sh: can't fork: Resource temporarily unavailable
```

Ao inspecionar o cgroup correspondente no hospedeiro (em `/sys/fs/cgroup/system.slice/docker-<ID>.scope/pids.current`), o contador crava no valor máximo configurado (`20`). Enquanto um *fork bomb* tradicional fora de controle congelaria a máquina hospedeira ao esgotar a tabela global de PIDs do sistema operacional, o controlador de PIDs do cgroup v2 enjaula a tempestade estritamente dentro daquele contêiner, mantendo o servidor 100% responsivo e estável.

</details>

**3. Múltiplas Camadas e Resolução de Conflitos no OverlayFS**

Crie duas pastas de base diferentes: `/tmp/overlay-multi/camada1` contendo um arquivo `app.env` com o texto `AMB=producao` e `/tmp/overlay-multi/camada2` contendo um arquivo `app.env` com o texto `AMB=desenvolvimento`. Monte um OverlayFS passando ambas no parâmetro `lowerdir` com a sintaxe `lowerdir=/tmp/overlay-multi/camada2:/tmp/overlay-multi/camada1`. Qual conteúdo é exibido ao ler `app.env` no diretório montado e qual é a regra de precedência do kernel?

<details markdown="1">
<summary>Ver resposta</summary>

Ao inspecionar o arquivo montado, o valor retornado será `AMB=desenvolvimento`.

A regra do OverlayFS estabelece que as camadas passadas no parâmetro `lowerdir` são avaliadas rigorosamente da esquerda para a direita. O primeiro caminho listado tem precedência máxima sobre os subsequentes. É exatamente através dessa mecânica que uma instrução `COPY` ou `RUN` em um Dockerfile consegue substituir arquivos introduzidos por camadas anteriores da imagem.

</details>

**4. Investigando o Mini-Contêiner a Partir do Hospedeiro**

Execute o script `mini-container.sh`. Enquanto o terminal interno estiver ativo aguardando comandos, abra outro terminal comum no seu hospedeiro e execute os seguintes passos de investigação:

1. Localize o processo do contêiner com `ps aux | grep mini-conteiner`.
2. Compare a lista de namespaces de `/proc/<PID>/ns/` do processo localizado com os namespaces do processo 1 do host.
3. Consulte o arquivo `/sys/fs/cgroup/mini-conteiner-<PID>/memory.current` para averiguar o consumo de RAM em bytes.
4. Volte ao terminal do contêiner e execute `ps aux`. Quantos processos aparecem? Como você explica essa diferença gritante entre a visão do hospedeiro e a visão interna?

<details markdown="1">
<summary>Ver resposta</summary>

No hospedeiro, o processo do contêiner aparece listado como um processo comum qualquer, possuindo um identificador de PID regular e elevado (por exemplo, PID 41208). Seus inodes de namespace diferem totalmente dos inodes do hospedeiro, e o cgroup registra o consumo exato daquele processo.

Já dentro do contêiner, o comando `ps aux` exibe apenas dois processos: o `/bin/sh` assumindo com orgulho o posto de PID 1 e o próprio executável `ps` como PID 2. Essa divergência demonstra na prática o poder do isolamento do kernel: para quem está dentro, o universo se resume àquele ambiente; para quem está fora no sistema hospedeiro, é apenas mais um processo comum consumindo fatias de tempo da CPU.

</details>

## O Que Vem na Parte 2

Chegamos ao fim da primeira metade da nossa jornada.

Neste post, despimos o contêiner de todos os seus mitos de marketing. Você viu que não há mágica nem virtualização pesada: existem *namespaces* estabelecendo o que os processos conseguem ver, *cgroups* limitando o que eles conseguem gastar de hardware, e *sistemas de arquivos de união* entregando imagens em camadas sem desperdício de disco. Vimos também como a especificação da OCI padronizou essa fundação em componentes modulares como o `runc` e o `containerd`.

Mas vamos ser francos: ninguém em sã consciência vai ficar escrevendo scripts manuais em shell script e calculando offsets de montagem de OverlayFS toda vez que precisar colocar uma API em produção às três horas da tarde de uma sexta-feira.

É exatamente aqui que entram as ferramentas modernas de engenharia.

Na {% include post-ref.html slug="conteineres-pratica" text="Parte 2 da nossa série" %}, vamos subir para a camada de ferramentas e práticas do mundo real:
- **Anatomia avançada de Dockerfiles**: como estruturar construções em múltiplos estágios (*multi-stage builds*) eficientes para compilar aplicações pesadas gerando imagens de produção com menos de cem megabytes;
- **O ciclo de vida do contêiner**: as diferenças operacionais críticas entre estados de pausa, parada graciosa com tratamento de sinais `SIGTERM` e extermínio abrupto com `SIGKILL`;
- **Redes no Docker**: a arquitetura de pontes virtuais (*bridge*), tabelas de roteamento e resolução interna de nomes via DNS integrado;
- **Docker Compose**: como orquestrar múltiplos serviços interligados com bancos de dados, filas e caches em uma stack completa;
- **A revolução do Podman**: a arquitetura sem daemons centralizados (*daemonless*), contêineres sem privilégios (*rootless*) por padrão e a criação nativa de *Pods* no modelo do Kubernetes;
- **Segurança de contêineres**: análise de vulnerabilidades em imagens, restrição de capacidades administrativas do Linux (*capabilities*) e os perigos fatais de montar o socket do Docker em ambientes compartilhados.

Nos vemos na Parte 2 para colocar toda essa fundação em prática no mundo real.

## Referências

[^1]: **namespaces(7) - Overview of Linux Namespaces** {*Linux Programmer's Manual, man7.org*} ([Link](https://man7.org/linux/man-pages/man7/namespaces.7.html))

[^2]: **unshare(1) - Run Program with Some Namespaces Unshared from Parent** {*util-linux, man7.org*} ([Link](https://man7.org/linux/man-pages/man1/unshare.1.html))

[^3]: **nsenter(1) - Run Program in the Namespaces of Another Process** {*util-linux, man7.org*} ([Link](https://man7.org/linux/man-pages/man1/nsenter.1.html))

[^4]: **cgroups(7) - Linux Control Groups Overview** {*Linux Programmer's Manual, man7.org*} ([Link](https://man7.org/linux/man-pages/man7/cgroups.7.html))

[^5]: **Control Group v2 Official Kernel Documentation** {*Tejun Heo et al., The Linux Kernel Archives*} ([Link](https://docs.kernel.org/admin-guide/cgroup-v2.html))

[^6]: **Overlay Filesystem Documentation** {*Miklos Szeredi, The Linux Kernel Archives*} ([Link](https://docs.kernel.org/filesystems/overlayfs.html))

[^7]: **Open Container Initiative Runtime Specification (runc)** {*Open Container Initiative, GitHub*} ([Link](https://github.com/opencontainers/runtime-spec))

[^8]: **Namespaces in Operation: A Seven-Part Series** {*Michael Kerrisk, LWN.net, 2013*} ([Link](https://lwn.net/Articles/531114/))

[^9]: **What even is a container: namespaces and cgroups** {*Julia Evans, jvns.ca, 2016*} ([Link](https://jvns.ca/blog/2016/10/10/what-even-is-a-container/))

[^10]: **crun: A Fast and Low-Memory Footprint OCI Container Runtime** {*Giuseppe Scrivano et al., Red Hat / GitHub*} ([Link](https://github.com/containers/crun))

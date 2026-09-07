---
layout: post
title: "Kubernetes in a Box, Parte 2 - Ferramentas e Ambiente de Laboratório"
subtitle: "Do terminal vazio ao cluster virtual em duas placas de rede"
author:
  - "Eduardo N. S. R."
date: 2026-09-07 11:33:00 GMT-3
permalink: /posts/k8sbox-ferramentas-ambiente/
tags: [Kubernetes, Ansible, DevOps, Infraestrutura]
series: Kubernetes in a Box
---

Na Parte 1 desta série, gastamos o post inteiro falando sobre *por que* construir um cluster Kubernetes na mão e *o que* pretendemos montar. Conceitos, diagramas, motivação. Agora é hora de sujar as mãos de verdade: vamos configurar o computador hospedeiro, dissecar linha por linha como o Vagrant lê nosso inventário Ansible para criar máquinas virtuais e resolver o problema mais traiçoeiro de qualquer laboratório local de Kubernetes: fazer a rede funcionar direito.

> [!NOTE] Nota da Série
> Este post faz parte da série **"Kubernetes in a Box"**. Todo o código-fonte está disponível no repositório parceiro [vndmtrx/k8s-in-a-box](https://github.com/vndmtrx/k8s-in-a-box). Nesta parte, não usamos nenhuma *role* do Ansible ainda. Tudo gira em torno da infraestrutura do hospedeiro: `Vagrantfile`, `Makefile` e `config.mk`.

Se você já perdeu horas tentando entender por que as VMs do Vagrant conseguiam pingar a internet mas não se enxergavam entre si, ou por que um `vagrant up` subia seis máquinas idênticas com a mesma rota padrão apontando pro lugar errado, esse post é pra você. Vamos resolver cada um desses problemas, explicar as decisões por trás de cada linha de configuração e, no final, ter um ambiente local completamente funcional com VMs prontas para receber o cluster nas próximas partes.

## O que você precisa ter instalado

Antes de qualquer coisa, seu hospedeiro Linux precisa de cinco ferramentas. Essas são as únicas instalações manuais que você vai fazer em todo o processo: tudo o que acontece *dentro* das VMs (chaves SSH, configuração de rede, pacotes, provisionamento) é gerenciado automaticamente pelo Vagrantfile e pelo Ansible quando você roda `make up`.

| Ferramenta | Função no Projeto |
|:---|:---|
| **KVM** | Hipervisor nativo do kernel Linux |
| **libvirt** | API de gerenciamento de VMs (daemon `libvirtd`) |
| **Vagrant** | Orquestrador de máquinas virtuais via CLI |
| **vagrant-libvirt** | Plugin que conecta o Vagrant ao KVM/libvirt |
| **Ansible** | Motor de automação declarativa |

A forma de instalar cada uma varia conforme a sua distribuição, então não vou prescrever comandos aqui. O importante é que todas estejam disponíveis no `PATH` do seu usuário. Uma coisa que pode pegar desprevenido: o KVM precisa de permissões de grupo. Sem elas, o Vagrant vai pedir senha de `root` a cada operação ou simplesmente falhar silenciosamente. Garanta que o seu usuário pertence aos grupos `libvirt` e `kvm` (e faça logout/login depois de adicioná-los).

> [!TIP] Dica
> O projeto inclui o comando `make check-deps` que verifica todas essas dependências de uma vez. Ele testa se o Ansible, Vagrant, KVM, libvirt e o plugin vagrant-libvirt estão instalados e com as permissões corretas. É o primeiro comando que você deveria rodar depois de clonar o repositório.

A saída do `check-deps` é direta ao ponto:

```bash
$ make check-deps
Verificando dependências do host...
  - Ansible: OK
  - Vagrant: OK
  - KVM (/dev/kvm): OK
  - Conexão Libvirt (virsh): OK
  - Vagrant Libvirt Plugin: OK
Tudo OK! Pronto para iniciar o provisionamento.
```

Se alguma linha aparecer como `NÃO ENCONTRADO` ou `SEM PERMISSÃO`, o comando aborta a execução e te diz exatamente o que falta. Sem surpresas no meio do provisionamento.

## Por que KVM e não VirtualBox

A decisão de usar LibVirt [^5] com KVM [^3] em vez do VirtualBox foi, antes de tudo, uma questão de manter a stack o mais *open source* possível. O KVM é um módulo nativo do kernel Linux, mantido no *mainline* pela própria comunidade do kernel. O libvirt é LGPL. Tudo roda com ferramentas que vêm nos repositórios da sua distribuição, sem precisar baixar pacotes proprietários ou aceitar licenças de uso restritivo.

Sim, o VirtualBox também usa um módulo de kernel (`vboxdrv`) para acessar as extensões de virtualização do processador, então não é uma questão de "um usa hardware e o outro não". Ambos fazem virtualização assistida por hardware. Mas o módulo do VirtualBox é mantido fora da árvore do kernel, distribuído pela Oracle sob uma licença que mistura GPLv3 com componentes proprietários no *Extension Pack*, e precisa ser recompilado a cada atualização de kernel. Com KVM, esse atrito simplesmente não existe.

Na prática, pra um cluster Kubernetes com cinco a nove VMs rodando simultaneamente e disputando CPU, memória e disco, tanto KVM quanto VirtualBox vão entregar performance razoável. A diferença real é filosófica e operacional: com KVM você está usando a infraestrutura nativa do seu sistema operacional, sem dependências externas.

O Vagrant [^4] funciona como uma camada de abstração sobre o hipervisor. Ele não cria VMs sozinho: ele precisa de um *provider* que saiba efetivamente gerenciar o ciclo de vida das máquinas. O plugin `vagrant-libvirt` [^6] faz essa ponte, traduzindo as instruções do `Vagrantfile` para chamadas à API do libvirt, que por sua vez comanda o KVM.

## AlmaLinux 10: a distro das VMs

Para as máquinas virtuais do laboratório, escolhemos o **AlmaLinux 10** [^2] como sistema operacional base. Essa escolha não é um capricho estético.

O AlmaLinux é uma distribuição binariamente compatível com o Red Hat Enterprise Linux (RHEL), o que significa que tudo o que funciona no RHEL funciona aqui sem adaptação. Isso é relevante porque a maior parte da documentação corporativa de Kubernetes e os guias de hardening de segurança assumem um ecossistema RHEL-*like* (CentOS, Rocky, AlmaLinux). Do ponto de vista prático, a versão 10 traz o NetworkManager como gerenciador de rede padrão com o `nmcli` já integrado, `systemd` atualizado, e *boxes* oficiais para Vagrant publicados e mantidos ativamente no Vagrant Cloud.

> [!WARNING] Atenção
> A série e o projeto estão atualmente travados na versão **AlmaLinux 10**. Mudanças futuras de versão do sistema operacional podem exigir ajustes no Vagrantfile e nas *roles* do Ansible, especialmente na configuração de rede e nos pacotes disponíveis nos repositórios. Se você estiver acompanhando a série em um momento posterior, verifique o repositório do projeto para a versão atual suportada.

Se você preferir usar outra distribuição (Ubuntu, Debian, openSUSE), o conceito por trás de cada etapa será idêntico, mas os comandos de pacote, os caminhos de configuração e o gerenciador de rede podem ser diferentes. No nosso caso, o `nmcli` é protagonista absoluto na configuração de rede das VMs, e ele é cidadão de primeira classe no ecossistema RHEL.

## O Vagrantfile dissecado

Agora vamos ao arquivo que orquestra toda a criação das máquinas virtuais. O `Vagrantfile` do k8s-in-a-box não é um arquivo estático com meia dúzia de VMs *hardcoded*. Ele é um programa Ruby que lê dinamicamente o inventário do Ansible e constrói as VMs a partir das definições que encontra ali.

### Leitura dinâmica do inventário

A mágica começa logo nas primeiras linhas:

```ruby
require 'yaml'

inventario = YAML.load_file("inventario/hosts.yml")
grupos = inventario["all"]["children"]

nodes = {}

grupos.each do |grupo, dados|
  next unless dados["hosts"]

  dados["hosts"].each do |nome, props|
    nodes[nome] = {
      "ip"        => props["ansible_host"],
      "memory"    => props["memory"],
      "cpus"      => props["cpus"],
      "autostart" => props.fetch("autostart", true)
    }
  end
end
```

*O Vagrant carrega o arquivo `inventario/hosts.yml` (que é um symlink para a topologia ativa), percorre todos os grupos do inventário e extrai IP, memória, CPUs e a flag de autostart de cada host.*

A beleza desse mecanismo é que o Vagrantfile nunca precisa ser editado. Quer adicionar um worker? Bota no inventário YAML. Quer trocar a topologia inteira? Muda o symlink. A mesma lógica em Ruby vai gerar as VMs corretas independente de quantas máquinas estejam definidas no inventário.

O hash `nodes` resultante é um dicionário simples onde a chave é o nome da VM e o valor contém as especificações de hardware. Pra topologia `mini`, por exemplo, ele vai conter seis entradas: `loadbalancer1`, `nfs1`, `manager1`, `worker1`, `worker2` e `kubox`.

### Geração automática de chaves SSH

Um dos objetivos do projeto é que você não precise configurar nada manualmente dentro das VMs. Isso inclui o acesso SSH: antes de criar qualquer máquina, o Vagrantfile gera um par de chaves ed25519 caso elas ainda não existam:

```ruby
unless ARGV.include?("destroy")
  unless File.exist?('id_ed25519') && File.exist?('id_ed25519.pub')
    system('ssh-keygen -t ed25519 -f id_ed25519 -N "" >/dev/null 2>&1')
    puts "Nova chave SSH gerada."
  end
end
```

*Gera uma chave ed25519 sem passphrase, apenas se ela não existir e se o comando não for `vagrant destroy`.*

Durante a criação de cada VM, essa chave pública é automaticamente injetada no `authorized_keys` do usuário `vagrant`. É com ela que o Ansible vai se conectar às máquinas depois, sem que você precise copiar chaves manualmente, editar `authorized_keys` ou configurar qualquer coisa. O `config.ssh.insert_key = false` logo adiante desativa a inserção da chave padrão do Vagrant, garantindo que a única chave de acesso seja a do projeto. O arquivo `ssh_config` na raiz do repositório já aponta para essa chave e desabilita a verificação de *host keys*, fechando o ciclo: Vagrant gera, injeta e o Ansible usa.

E quando o cluster é destruído? Um *trigger* pós-destruição cuida da limpeza:

```ruby
config.trigger.after :destroy do |trigger|
  trigger.ruby do |env, machine|
    arquivos = ['id_ed25519', 'id_ed25519.pub']
    if arquivos.any? { |f| File.exist?(f) }
      arquivos.each { |f| File.delete(f) if File.exist?(f) }
      puts "Chaves SSH removidas."
    end
  end
end
```

*Remove as chaves SSH quando todas as VMs são destruídas. Ciclo de vida limpo.*

### Configuração global do provider LibVirt

A configuração do provider KVM é definida uma única vez e aplicada a todas as VMs:

```ruby
config.vm.provider :libvirt do |libvirt|
  libvirt.driver = "kvm"
  libvirt.memorybacking :source, :type => "memfd"
  libvirt.memorybacking :access, :mode => "shared"

  libvirt.cpu_mode = "host-model"
  libvirt.nested = true

  libvirt.nic_model_type = "virtio"
  libvirt.management_network_name = "vagrant"
  libvirt.management_network_address = "192.168.250.0/24"
  libvirt.management_network_mode = "none"
  libvirt.management_network_autostart = true
end
```

*Configuração do hipervisor: KVM com virtio, CPU passthrough em modo host-model, e rede de gerenciamento do Vagrant em `192.168.250.0/24` sem NAT.*

Duas decisões chamam atenção aqui. Primeiro, o `cpu_mode = "host-model"` expõe os *flags* da CPU do hospedeiro diretamente para as VMs, o que é essencial para o eBPF do Cilium funcionar corretamente. Segundo, a rede de gerenciamento do Vagrant (`192.168.250.0/24`) é configurada com `mode = "none"`, sem NAT e sem DHCP. Essa é a rede `eth0` que o Vagrant usa internamente pra comunicação via SSH. O cluster não usa essa rede pra nada.

> [!NOTE] Pastas Compartilhadas Desativadas
> Por padrão, o Vagrant tenta montar o diretório do projeto dentro de cada VM em `/vagrant` usando 9p, virtiofs ou NFS. No ecossistema KVM/libvirt, isso costuma ser uma fonte clássica de lentidão e erros de montagem caso o host não tenha os módulos correspondentes configurados. Como o nosso laboratório é 100% provisionado remotamente pelo Ansible via SSH, desativamos essa sincronização explicitamente com `config.vm.synced_folder "./", "/vagrant", disabled: true`. Menos atrito, boot mais veloz e zero dependências de filesystem compartilhado.

### Criação das VMs e a rede privada

O loop principal itera sobre cada nó do hash `nodes` e cria uma VM correspondente:

```ruby
nodes.each do |nome_no, specs|
  config.vm.define nome_no, autostart: specs["autostart"] do |node|
    node.vm.hostname = nome_no
    node.vm.network "private_network", ip: specs["ip"],
      libvirt__network_name: "k8sbox_mgmt",
      libvirt__forward_mode: "nat",
      libvirt__dhcp_enabled: false

    node.vm.provider :libvirt do |libvirt_host|
      libvirt_host.default_prefix = "k8sbox_"
      libvirt_host.memory = specs["memory"]
      libvirt_host.cpus = specs["cpus"]
    end
    # ... provisionamento de rede (próxima seção)
  end
end
```

*Para cada host no inventário, cria uma VM com o IP fixo definido, conecta à rede `k8sbox_mgmt` em modo NAT sem DHCP, e aplica as configurações de memória e CPU.*

Aqui o detalhe crucial: a rede `k8sbox_mgmt` é criada com `forward_mode: "nat"` e `dhcp_enabled: false`. Isso significa que as VMs terão acesso à internet (via NAT do host) mas sem servidor DHCP atribuindo IPs automaticamente. Os IPs são estáticos e definidos pelo inventário. Essa rede será a `eth1` dentro das VMs e é por onde todo o tráfego do cluster vai transitar.

Note também o `autostart: specs["autostart"]`. No inventário, o `kubox` é definido com `autostart: false`. Ele não sobe junto com as demais VMs quando você roda `vagrant up`, porque durante a construção do cluster ele ainda não é necessário. O Makefile cuida de subi-lo separadamente no momento certo.

## As duas placas de rede (e a armadilha do eth0)

Toda VM criada pelo nosso Vagrantfile recebe duas interfaces de rede. Isso é proposital, mas causa um problema que se você não tratar, vai quebrar todo o funcionamento do cluster.

| Configuração | `eth0` (`net_vagrant`) | `eth1` (`net_mgmt`) |
| :--- | :--- | :--- |
| **Finalidade** | Gerenciamento do Vagrant (SSH, provisionamento) | Rede interna do cluster Kubernetes |
| **IP (ex: `manager1`)** | `192.168.250.x` (DHCP) | `172.24.0.31` (Estático) |
| **Métrica de Rota** | `500` (Baixa prioridade) | `50` (Alta prioridade) |
| **Gateway / Rota Padrão** | `never-default: yes` (Não assume rota default) | `172.24.0.1` (Gateway principal) |

A `eth0` é a rede de gerenciamento do Vagrant. Ela existe porque o Vagrant precisa de uma forma de se comunicar com a VM via SSH para provisionamento e comandos como `vagrant ssh`. Mas essa rede é completamente inútil para o cluster Kubernetes. Pior: se deixada sem tratamento, ela se torna a rota padrão da VM, e todo o tráfego de saída vai por ela em vez de ir pela `eth1` onde o cluster mora.

A `eth1` é a rede privada `172.24.0.0/24`, que é o verdadeiro sistema circulatório do laboratório. Todo tráfego do `etcd`, do `kube-apiserver`, dos pods e dos serviços transita por essa interface.

### A guerra dos gateways via nmcli

Aqui entra o trecho mais importante do Vagrantfile: o provisionamento de rede via shell que resolve a prioridade entre as interfaces. Esse script foi resultado de bastante experimentação, especialmente na migração do AlmaLinux 9 para o 10, onde o comportamento do NetworkManager [^7] mudou significativamente.

No AlmaLinux 9, os nomes das conexões eram previsíveis (`eth0`, `System eth1`). Na versão 10, o NetworkManager passou a nomear as conexões de forma genérica (`Wired connection 1`, `Wired connection 2`), o que quebrou todas as referências estáticas que eu tinha no Vagrantfile. A solução foi implementar uma detecção dinâmica dos nomes das conexões por dispositivo:

```bash
# --- Ajustes de nomenclatura dinâmicos ---
CON_VAGRANT=$(nmcli -t -f NAME,DEVICE connection show \
  | grep ':eth0$' | cut -d: -f1 | head -n1)
CON_MGMT=$(nmcli -t -f NAME,DEVICE connection show \
  | grep ':eth1$' | cut -d: -f1 | head -n1)

if [ -n "$CON_VAGRANT" ]; then
  nmcli con mod "$CON_VAGRANT" connection.id net_vagrant ifname eth0
fi
if [ -n "$CON_MGMT" ]; then
  nmcli con mod "$CON_MGMT" connection.id net_mgmt ifname eth1
fi
nmcli con reload
```

*Descobre dinamicamente qual conexão está associada a cada dispositivo físico (`eth0`, `eth1`) e renomeia para nomes previsíveis (`net_vagrant`, `net_mgmt`).*

Depois de renomear, o script trata cada interface individualmente:

```bash
# --- Configurações net_vagrant ---
nmcli con mod net_vagrant \
  connection.autoconnect yes \
  connection.autoconnect-priority -999  \
  ipv4.route-metric 500 \
  ipv4.ignore-auto-dns yes \
  ipv4.never-default yes \
  ipv6.method ignore

nmcli con reload && nmcli con up net_vagrant
```

*Rebaixa a eth0: métrica 500 (baixa prioridade), ignora DNS do DHCP, `never-default` impede que ela se torne gateway. IPv6 desabilitado.*

```bash
# --- Configurações net_mgmt ---
nmcli con mod net_mgmt \
  ipv4.method manual \
  ipv4.addresses "172.24.0.31/24" \
  ipv4.gateway "172.24.0.1" \
  ipv4.route-metric "50" \
  ipv4.dns "1.1.1.1,8.8.8.8" \
  ipv6.method ignore \
  ipv4.dns-search "k8sbox.local"

nmcli con reload && nmcli con up net_mgmt
```

*Configura a eth1 como interface principal: IP manual, gateway apontando para o NAT do libvirt, métrica 50 (alta prioridade), DNS públicos e domínio de busca do cluster.*

> [!WARNING] Variáveis Dinâmicas no Repositório
> No `Vagrantfile` do repositório parceiro, esses comandos utilizam interpolações dinâmicas do Ruby, como `#{specs["ip"]}` e `#{PROJETO}.local`. Aqui no artigo, colocamos os valores já resolvidos para a máquina `manager1` (`172.24.0.31/24` e `k8sbox.local`) como referência fixa para facilitar a visualização e a leitura dos comandos.

A jogada é a combinação de `never-default yes` na eth0 com `route-metric 50` na eth1. O `never-default` diz ao NetworkManager que a eth0 nunca deve ser usada como gateway padrão, independente do que o DHCP sugira. E a métrica 50 na eth1 garante que, se por qualquer motivo ambas as rotas existirem na tabela, a eth1 vence.

Antes da migração para o AlmaLinux 10, o provisionamento de rede usava referências estáticas como `nmcli con mod eth0` e criava conexões novas do zero com `nmcli con add`. A versão 10.1 mudou o esquema de nomenclatura das conexões e exigiu a abordagem dinâmica com detecção por dispositivo. Se você estiver portando o projeto para outra distro, esse é um dos trechos que pode precisar de ajustes.

E pra fechar o script de provisionamento: tem um trecho crucial que lida com o xerife do sistema operacional:

```bash
# --- Configura o SELinux como Permissive ---
setenforce 0
sed -i 's/^SELINUX=enforcing/SELINUX=permissive/' /etc/selinux/config

# --- Corrige rotulos de SELinux dos arquivos criados pelo Vagrant ---
restorecon -R /etc/NetworkManager/system-connections/
```

*Coloca o SELinux em modo permissivo e restaura os rótulos dos arquivos de conexão do NetworkManager criados pelo Vagrant.*

O Vagrant cria arquivos de configuração de rede dentro da VM durante o processo de boot, mas esses arquivos nascem sem os rótulos de SELinux corretos. O NetworkManager simplesmente recusa processar conexões com rótulos inválidos quando o SELinux está ativo. Esse `restorecon` corrige o problema silenciosamente.

> [!NOTE] Mas Dudu, você não disse que não desabilitava o SELinux?!
> Calma, jovem padawan, respira. A gente **não** desabilitou o SELinux. Desabilitar (`SELINUX=disabled`) é o que tutorial preguiçoso de internet faz para varrer sujeira pra baixo do tapete e fingir que segurança não existe. O que fizemos aqui foi colocar em modo permissivo (`permissive`). A diferença não é sutil: no modo permissivo o kernel não bloqueia as ações, mas continua de olhos bem abertos, auditando rigorosamente cada chamada no `audit.log` e dedurando exatamente o que o Kubernetes, o Kubelet ou o CNI fizerem que não está nas regras implementadas. O importante na engenharia de verdade não é desligar cegamente, mas botar no permissivo, ver o que está disparando de alertas, acomodar tudo nas regras e aí então fechar as portas virando a chave para *enforcing*. Teremos um post dedicado exclusivamente a compilar essa política customizada (`k8s-custom-selinux.te`) quando instalarmos o Kubelet.

## O sistema de topologias: três clusters, um repositório

Na Parte 1, apresentamos as três configurações de cluster disponíveis: `nano`, `mini` e `completo`. Agora vamos ver como esse sistema funciona por dentro.

A engrenagem é simples e elegante: um arquivo de configuração (`config.mk`), um diretório com os inventários pré-definidos (`configs/`) e um symlink que conecta os dois.

```
k8s-in-a-box/
├── config.mk                        <-- Escolha da topologia
├── configs/
│   ├── hosts-nano.yml               <-- 5 VMs (~6GB RAM)
│   ├── hosts-mini.yml               <-- 6 VMs (~10GB RAM)
│   └── hosts-completo.yml           <-- 9 VMs (~19GB RAM)
└── inventario/
    └── hosts.yml -> ../configs/hosts-mini.yml  <-- Symlink ativo
```

O `config.mk` é um fragmento de Makefile que define uma única variável:

```makefile
CLUSTER = mini
```

*O arquivo inteiro. Uma linha. Altera esse valor para `nano` ou `completo` e rode `make init`.*

Quando você executa `make init`, o Makefile verifica se o arquivo de inventário correspondente existe e cria o symlink:

```bash
$ make init
Configuração mini ativada
```

O `make status` mostra qual configuração está ativa em qualquer momento:

```bash
$ make status
Configuração ativa: mini
```

### Anatomia de um inventário

Cada arquivo de topologia é um inventário YAML do Ansible padrão. Vamos olhar o `hosts-mini.yml` como exemplo:

```yaml
all:
  vars:
    ansible_user: vagrant

  children:
    loadbalancers:
      hosts:
        loadbalancer1:
          ansible_host: 172.24.0.21
          fqdn: loadbalancer1.k8sbox.local
          memory: 384
          cpus: 1

    managers:
      hosts:
        manager1:
          ansible_host: 172.24.0.31
          fqdn: manager1.k8sbox.local
          memory: 3072
          cpus: 2

    workers:
      hosts:
        worker1:
          ansible_host: 172.24.0.41
          fqdn: worker1.k8sbox.local
          memory: 3072
          cpus: 2
        worker2:
          ansible_host: 172.24.0.42
          fqdn: worker2.k8sbox.local
          memory: 3072
          cpus: 2

    clientes:
      hosts:
        kubox:
          ansible_host: 172.24.0.254
          fqdn: kubox.k8sbox.local
          memory: 384
          cpus: 1
          autostart: false
```

*Topologia `mini`: 1 LB, 1 NFS, 1 manager, 2 workers e o bastion host. Total de 6 VMs.*

Cada host carrega quatro campos obrigatórios: `ansible_host` (o IP na rede `172.24.0.0/24`), `fqdn` (o nome completo no domínio `k8sbox.local`), `memory` (RAM em MB) e `cpus` (número de vCPUs). Esses são os mesmos campos que o Vagrantfile lê para criar as VMs.

A estrutura de grupos (`loadbalancers`, `managers`, `workers`, `clientes`) não é cosmética. O Ansible usa esses grupos para decidir quais *roles* aplicar em quais máquinas. Os managers recebem `etcd` e *control plane*. Os workers recebem apenas o `kubelet`. Os load balancers recebem HAProxy e Keepalived. E o `kubox` recebe as ferramentas de operação.

Comparando as três topologias em números:

| Configuração | LBs | Managers | Workers | NFS | kubox | Total VMs | RAM Estimada |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `nano` | 1 | 1 | 1 | 1 | 1 | 5 | ~6 GB |
| `mini` | 1 | 1 | 2 | 1 | 1 | 6 | ~10 GB |
| `completo` | 2 | 3 | 2 | 1 | 1 | 9 | ~19 GB |

A configuração `completo` é a única que viabiliza testes reais de alta disponibilidade: com três managers, o `etcd` forma *quorum* e tolera a perda de um nó. Com dois load balancers, o Keepalived faz failover do VIP. Mas ela exige quase 20 GB de RAM livre no host, o que nem todo mundo tem à disposição.

## O Makefile como interface de comandos

Rodar o Ansible manualmente para testar uma única *role* envolve montar um comando com variáveis de ambiente, caminho do arquivo de configuração, caminho do *playbook*, *flags* de *tags* e eventuais opções de verbosidade. É o tipo de coisa que você digita uma vez, erra um caractere no meio e perde cinco minutos descobrindo por quê. O Makefile [^8] do projeto encapsula toda essa complexidade em *targets* legíveis:

```
════════════════════════════════════════════════════════════
  K8s in a Box - Makefile
════════════════════════════════════════════════════════════

Uso:
  make init                 # Ativa a configuração definida no config.mk
  make k8s-in-a-box         # Executa a esteira completa (ou 'make build')
  make status               # Mostra o tamanho de cluster ativo

Lista de targets:
  make init                  Ativa uma configuração de cluster
  make status                Mostra a configuração de cluster ativa
  make check-deps            Verifica se todas as dependências locais estão instaladas
  make up                    Sobe todas as VMs do cluster
  make down                  Interrompe todas as VMs do cluster
  make destroy               Exclui permanentemente todas as VMs
  make clean                 Deleta as VMs e limpa todos os artefatos
  make infra                 Prepara infraestrutura pré-k8s (PKI, SO, Balanceador, NFS)
  make control-plane         Instala o Kubernetes core (Kubelet, Etcd, Static Pods)
  make cluster               Executa o provisionamento do cluster completo
  make ops                   Provisiona completamente a VM de operações
  make addons                Instala ferramentas operacionais adicionais
  make exemplos              Faz deploy das aplicações de demonstração
  make snapshot              Cria uma snapshot única de todas as VMs
  make restore               Restaura o cluster para a última snapshot criada
```

Os targets são organizados em camadas que refletem a ordem de dependência do cluster:

1. **Configuração**: `init`, `status`, `check-deps`
2. **Ciclo de vida das VMs**: `up`, `down`, `destroy`, `clean`
3. **Provisionamento do Kubernetes**: `infra`, `control-plane`, `cluster`
4. **Operações e rede**: `ops`, `cni`
5. **Aplicações**: `addons`, `exemplos`
6. **Snapshots**: `snapshot`, `restore`

O target `k8s-in-a-box` (aliás de `build`) é o comando de esteira completa. Ele executa toda a cadeia na ordem correta:

```makefile
build: up cluster ops addons exemplos
```

*Um target, cinco etapas em sequência: sobe VMs, provisiona cluster, configura operações e rede, instala addons e deploya exemplos.*

### O mecanismo garante-config

Todo target que interage com o Vagrant ou o Ansible depende do target interno `garante-config`:

```makefile
garante-config:
	@CURRENT_LINK=$$(readlink "$(CLUSTER_LINK)" 2>/dev/null || echo ""); \
	EXPECTED_LINK="../$(CLUSTER_SOURCE)"; \
	if [ "$$CURRENT_LINK" != "$$EXPECTED_LINK" ]; then \
		echo "Sincronizando configuração do inventário para $(CLUSTER)..."; \
		$(MAKE) init; \
	fi
```

*Verifica se o symlink atual corresponde à topologia definida no `config.mk`. Se estiver dessincronizado, re-executa o `make init` automaticamente.*

Esse mecanismo evita um cenário traiçoeiro: você edita o `config.mk` para mudar de `mini` para `completo`, esquece de rodar `make init`, e acaba provisionando o cluster com a topologia errada. Com o `garante-config`, esse desalinhamento é corrigido automaticamente antes de qualquer operação.

### Snapshots: seu seguro contra desastres

Quando o cluster está funcionando e você quer experimentar uma mudança arriscada (trocar o CNI, rotacionar certificados, testar uma versão diferente do Kubernetes), as *snapshots* salvam a sua vida:

```bash
make snapshot    # Salva o estado atual de todas as VMs
make restore     # Restaura todas as VMs para o último snapshot
```

Cada `make snapshot` sobrescreve o snapshot anterior (não é um sistema de múltiplos pontos de restauração). A ideia é simples: antes de uma operação potencialmente destrutiva, salva. Se deu errado, restaura. Sem precisar reconstruir o cluster inteiro do zero, que dependendo da topologia leva de dez a trinta minutos.

## Do zero ao ambiente funcional: o fluxo completo

Pra quem quer ver tudo funcionando de uma vez, o caminho mínimo é:

```bash
git clone https://github.com/vndmtrx/k8s-in-a-box.git
cd k8s-in-a-box
make check-deps
make init
make up
```

O `make up` é onde a mágica visível acontece. Ele cria o diretório de artefatos, executa `vagrant up`, e o Vagrant cuida de absolutamente tudo sozinho: lê o inventário, cria as VMs no KVM, gera as chaves SSH, injeta a chave pública em cada máquina, configura as duas interfaces de rede via `nmcli` e corrige os rótulos de SELinux. Você não precisa entrar em nenhuma VM pra configurar nada. Quando o comando termina, as máquinas já estão acessíveis pelo Ansible.

O resultado final são VMs AlmaLinux 10 com:

- Rede `eth0` (`net_vagrant`) rebaixada e sem rota padrão
- Rede `eth1` (`net_mgmt`) como interface principal com IP estático e gateway
- SELinux em modo permissivo (estágio transitório de auditoria para compilar as regras antes do *enforcing*)
- Chave SSH do projeto no `authorized_keys` (gerada e injetada automaticamente)
- Conectividade plena entre todas as VMs na faixa `172.24.0.0/24`
- Ansible pronto para se conectar via o `ssh_config` do projeto

Nenhum componente Kubernetes instalado. Nenhuma *role* Ansible executada. Apenas máquinas virtuais com o sistema operacional base, rede configurada e prontas para receber o cluster.

## Diagnóstico e Troubleshooting

Se algo der errado no processo de subida das VMs, aqui estão os comandos de diagnóstico essenciais:

### Status das VMs

```bash
vagrant status
```

*Mostra o estado atual de cada VM (running, shutoff, not created).*

```bash
virsh list --all
```

*Lista todas as VMs no hipervisor KVM, incluindo as que estão desligadas. Útil quando o Vagrant perde a referência para uma VM.*

### Verificação de rede dentro das VMs

Conecte-se a uma VM e inspecione a configuração de rede:

```bash
vagrant ssh manager1
```

Dentro da VM:

```bash
nmcli con show
```

*Lista todas as conexões do NetworkManager. Você deve ver `net_vagrant` (eth0) e `net_mgmt` (eth1) com os nomes que definimos.*

```bash
nmcli con show net_mgmt | grep -E "ipv4\.(addresses|gateway|route-metric|dns)"
```

*Verifica se a eth1 está configurada corretamente com o IP, gateway, métrica e DNS.*

### Teste de conectividade entre VMs

De qualquer VM, teste o acesso a outra:

```bash
ping -c 3 172.24.0.31    # manager1
ping -c 3 172.24.0.41    # worker1
ping -c 3 172.24.0.21    # loadbalancer1
```

*Se algum ping falhar, verifique se a rede `k8sbox_mgmt` existe no libvirt com `virsh net-list --all`.*

### Problemas comuns

| Sintoma | Causa Provável | Solução |
|:---|:---|:---|
| `vagrant up` pede senha de root | Usuário não está nos grupos `libvirt`/`kvm` | `sudo usermod -a -G libvirt,kvm $(whoami)` + logout/login |
| VM sobe mas não pinga outra VM | Rede `k8sbox_mgmt` não foi criada | `virsh net-list --all` e `vagrant destroy -f && vagrant up` |
| `nmcli con show` mostra nomes genéricos | Script de provisionamento falhou | `vagrant provision <nome-vm>` para re-executar |
| Acesso à internet funciona via eth0 mas não via eth1 | Gateway da eth1 não configurado | Verificar se `172.24.0.1` responde com `ping 172.24.0.1` |

## Conclusão

Se tudo correu bem, neste momento você tem um ambiente de laboratório completo rodando na sua máquina: cinco a nove VMs AlmaLinux 10 interconectadas numa rede privada isolada, com IPs estáticos previsíveis, chaves SSH distribuídas e uma interface de Makefile que simplifica tudo.

Não tem Kubernetes instalado ainda. Não tem certificado gerado. Não tem nenhum serviço rodando. E isso é proposital. A ideia de separar a infraestrutura do hospedeiro do provisionamento do cluster permite que você destrua e recrie as VMs quantas vezes precisar sem perder tempo reinstalando ferramentas no seu sistema operacional.

No próximo post (**Parte 3: O Inventário Ansible e as Variáveis do Cluster**), vamos mergulhar na outra metade do cérebro do projeto: o arquivo `all.yml` onde todas as variáveis do cluster moram, o `.ansible.cfg` com suas decisões de configuração, e como uma única mudança de variável propaga por todo o ecossistema de *roles* e *playbooks*. É onde o Ansible deixa de ser apenas uma ferramenta de automação e vira o mapa completo do cluster que estamos construindo.

## Referências

[^1]: **Repositório k8s-in-a-box** {*GitHub*} ([Link](https://github.com/vndmtrx/k8s-in-a-box))

[^2]: **AlmaLinux OS** {*AlmaLinux*} ([Link](https://almalinux.org/))

[^3]: **KVM - Kernel-based Virtual Machine** {*Linux Kernel Documentation*} ([Link](https://www.linux-kvm.org/))

[^4]: **Vagrant by HashiCorp** {*HashiCorp*} ([Link](https://www.vagrantup.com/))

[^5]: **LibVirt - The virtualization API** {*libvirt.org*} ([Link](https://libvirt.org/))

[^6]: **vagrant-libvirt** {*GitHub*} ([Link](https://github.com/vagrant-libvirt/vagrant-libvirt))

[^7]: **NetworkManager Reference Manual** {*freedesktop.org*} ([Link](https://networkmanager.dev/docs/api/latest/nmcli.html))

[^8]: **GNU Make Manual** {*Free Software Foundation*} ([Link](https://www.gnu.org/software/make/manual/))

[^9]: **Ansible Documentation** {*Red Hat*} ([Link](https://docs.ansible.com/))

[^10]: **Kubernetes in a Box, Parte 1 - Visão Geral** {*vndmtrx.github.io*} ([Link](/posts/k8sbox-visao-geral/))

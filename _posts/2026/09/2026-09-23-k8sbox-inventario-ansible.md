---
layout: post
title: "Kubernetes in a Box, Parte 3 - O Inventário Ansible e as Variáveis do Cluster"
subtitle: "O cérebro declarativo que orquestra a infraestrutura e viabiliza upgrades com uma única linha"
author:
  - "Eduardo N. S. R."
date: 2026-09-23 21:48:00 GMT-3
permalink: /posts/k8sbox-inventario-ansible/
tags: [Kubernetes, Ansible, DevOps, Infraestrutura, Linux]
series: Kubernetes in a Box
category: Tutoriais
---

No post anterior, deixamos nossas máquinas virtuais ligadas e conversando em uma rede privada isolada no KVM. Temos load balancers, managers, workers e um servidor NFS com endereços estáticos e resolução de nomes básica. Se tentarmos rodar qualquer comando do Kubernetes nelas agora, nada vai acontecer: não há binários instalados, não há certificados emitidos e nenhum processo do *control plane* existe. Antes de enviar a primeira instrução para as máquinas, precisamos responder a uma pergunta de arquitetura: onde vive a verdade sobre as versões, as faixas de rede e os papéis de cada nó?

> [!NOTE] Nota da Série e Contexto de Laboratório
> Este post faz parte da série **"Kubernetes in a Box"**, onde dissecamos e construímos, do zero e de forma totalmente reproduzível via Ansible, um cluster Kubernetes completo, com alta disponibilidade, armazenamento persistente, rede moderna e observabilidade. Todo o código do projeto está disponível no repositório parceiro [vndmtrx/k8s-in-a-box](https://github.com/vndmtrx/k8s-in-a-box).
>
> **Aviso de escopo:** as decisões de arquitetura e parâmetros deste projeto foram pensadas sob medida para a nossa realidade de laboratório local em estações Linux com Vagrant e KVM/Libvirt. Elas priorizam aprendizado profundo e reprodutibilidade rápida sobre convenções corporativas de produção. O cluster foi originalmente projetado em versões anteriores e recentemente atualizado para o **Kubernetes v1.37.0**.

A tentação em tutoriais de automação é pular direto para a execução dos playbooks. Alguém escreve meia dúzia de tarefas com comandos shell soltos, define caminhos hardcoded nos scripts e torce para que nada mude no futuro. Quem já precisou atualizar a versão do Kubernetes em um ambiente desses sabe o pesadelo que isso representa: você precisa vasculhar cinquenta arquivos procurando por `1.36.2`, torcendo para não esquecer um manifesto estático ou uma URL de download escondida em uma role secundária.

No **k8s-in-a-box**, tomamos uma direção oposta. Toda a inteligência da infraestrutura está desacoplada da execução. O arquivo `inventario/group_vars/all.yml` funciona como o mapa genético do laboratório, enquanto a estrutura de inventário dita quem é quem na topologia. Para provar o valor dessa separação, fizemos hoje uma atualização real no repositório do projeto: saltamos a versão base do Kubernetes de `v1.36.2` para o **Kubernetes v1.37.0** [^1], acompanhado do etcd 3.7.1, crictl v1.37.0, helm v3.22.0 e cilium v1.20.2.

Sabe quantos arquivos de automação ou manifestos de pods estáticos precisaram ser reescritos para suportar essa nova versão em todo o cluster? Apenas um.

## O arquivo de configuração do Ansible e suas decisões

> [!NOTE] Mas Dudu, a gente não ia falar de Kubernetes?!
> Eu sei o que você está pensando: "vim aqui pra aprender Kubernetes Hardcore e o cara tá me explicando flag de SSH e arquivo de configuração do Ansible". Segura a ansiedade! O Vagrant e o Ansible são os alicerces que sustentam todo esse laboratório em pé. Precisamos dissecar e deixar essa fundação de automação totalmente resolvida agora exatamente para tirá-la do caminho. Nas próximas partes da série, quase não vamos mais falar de Vagrant ou Ansible: o foco será total e exclusivo nas entranhas do Kubernetes (PKI, etcd, Static Pods, CNI e observabilidade). Gastar esse tempo no assunto mais burocrático hoje é o que vai nos dar liberdade para mergulhar direto nos tópicos mais empolgantes depois, sem interrupções.
>
> Mas olha: se você não aguenta de curiosidade e prefere ver o bicho funcionando na prática antes de ler todo o manual, sem problemas! Vai lá no terminal, clona o repositório, roda a esteira com `make k8s-in-a-box` e vê o cluster se materializar. Depois volta aqui pra continuarmos a dissecar o inventário com calma. Eu te espero!

O ponto de entrada de qualquer automação com a ferramenta é o arquivo de configuração [.ansible.cfg](https://github.com/vndmtrx/k8s-in-a-box/blob/main/ansible/.ansible.cfg). No nosso repositório, ele fica dentro do diretório `ansible/` e estabelece parâmetros cruciais para que a automação rode de forma estável, performática e previsível:

```ini
[defaults]
interpreter_python=auto_silent
deprecation_warnings=False
nocows=True
forks = 5
inventory=../inventario/
host_key_checking=False
become=false
gather_facts=false
log_path=../artefatos/ansible_logs/ansible.log
fact_caching = jsonfile
fact_caching_connection = ../artefatos/ansible_cache/ansible_facts
fact_caching_timeout = 3600
callbacks_enabled = profile_tasks, timer

[inventory]
enable_plugins = host_list, script, auto, yaml, ini, toml
cache = yes
cache_connection = ../artefatos/ansible_cache/ansible_inventory

[ssh_connection]
ssh_args=-F ./ssh_config -o ControlMaster=auto -o ControlPersist=180s
control_path_dir = ../artefatos/ansible_cache/cp
```

Cada uma dessas linhas resolve um problema prático recorrente de automação local.

A diretiva `inventory=../inventario/` aponta para um diretório inteiro em vez de um arquivo estático. Isso permite que o Ansible combine o arquivo de máquinas (`hosts.yml`) com o subdiretório de variáveis de grupo (`group_vars/`) de maneira orgânica.

A opção `host_key_checking=False` é uma concessão consciente para o fluxo de desenvolvimento. Como estamos destruindo e recriando máquinas virtuais frequentemente com Vagrant, o hash de chave pública de cada VM mudaria a cada recriação, causando erros de *host key mismatch* no SSH.

> [!CAUTION] Alerta de Segurança
> A desativação de `host_key_checking` é aceitável exclusivamente em laboratórios locais descartáveis com redes privadas isoladas. Em ambientes de homologação ou produção, desativar essa checagem abre as portas para ataques de Man-in-the-Middle (MitM) em conexões SSH corporativas.

Outro ganho significativo de velocidade vem da trinca `gather_facts=false`, `forks = 5` e as opções de `[ssh_connection]`. Por padrão, o Ansible tenta coletar centenas de fatos do sistema operacional (interfaces, discos, variáveis de ambiente) logo no início de cada *play*. Para um cluster com várias máquinas virtuais, essa checagem pode adicionar vários segundos a cada execução. Desativamos a coleta global e deixamos a coleta pontual apenas para as tarefas que realmente precisam dela.

Com o `ssh_args` configurado com `ControlMaster=auto` e `ControlPersist=180s`, o cliente SSH reaproveita os sockets de conexão abertos com as VMs durante três minutos. Tarefas subsequentes na mesma máquina acontecem de forma quase instantânea, sem a latência de um novo *handshake* criptográfico a cada task.

## Anatomia do inventário e topologias com symlinks

O diretório `configs/` na raiz do projeto abriga três modelos de cluster distintos: `hosts-nano.yml`, `hosts-mini.yml` e `hosts-completo.yml`. Como discutimos na Parte 1, nem todo desenvolvedor tem uma máquina com recursos de sobra para rodar várias máquinas virtuais e manter um cluster etcd com quórum completo.

Quando executamos `make init` (ou definimos `CLUSTER=mini` no arquivo `config.mk`), o Makefile cria um link simbólico transparente:

```bash
inventario/hosts.yml -> ../configs/hosts-mini.yml
```

Essa abordagem garante que todo o restante do ferramental (Ansible, scripts de verificação e Vagrant) consuma sempre o mesmo caminho (`inventario/hosts.yml`), sem precisar reescrever parâmetros de linha de comando.

Em vez de listar todas as máquinas, basta olhar como declaramos um único nó e como ele se encaixa em um grupo (a listagem completa com todas as VMs está no [configs/hosts-mini.yml](https://github.com/vndmtrx/k8s-in-a-box/blob/main/configs/hosts-mini.yml)):

```yaml
all:
  children:
    managers:
      hosts:
        manager1:
          ansible_host: 172.24.0.31
          fqdn: manager1.k8sbox.local
          memory: 3072
          cpus: 2

    # Agrupamento composto para orquestração
    cluster:
      children:
        managers: {}
        workers: {}
```

A composição de grupos simplifica a execução dos playbooks:

1. **Grupos específicos**: `loadbalancers`, `nfs`, `managers`, `workers` e `clientes` (`kubox`, nosso *bastion host*).
2. **Grupo cluster**: une `managers` e `workers` para tudo o que é comum aos nós Kubernetes (CRI-O, kubelet, CNI).
3. **Grupo suporte**: une `loadbalancers` (HAProxy e Keepalived) e `nfs` (armazenamento persistente).
4. **Grupo todos**: encapsula todo o ambiente para a preparação base do sistema operacional.

### A simbiose entre Vagrant, Libvirt e o inventário

O inventário não serve apenas para o Ansible rodar tarefas. Ele funciona como a **fonte única da verdade** de toda a infraestrutura virtual:

* **Leitura dinâmica via Ruby**: em vez de manter um `Vagrantfile` estático gigante repetindo nomes, vCPUs e limites de RAM para cada máquina, o script Ruby do Vagrant usa a biblioteca nativa `YAML` para abrir e interpretar diretamente o arquivo ativo em `inventario/hosts.yml`. Ele itera pelos grupos do YAML e dimensiona cada máquina no hipervisor usando as variáveis `memory` e `cpus` declaradas no inventário. Uma única linha modificada no arquivo de configuração atualiza tanto o hardware da VM quanto a automação de software.
* **Provider Libvirt nativo (KVM) em vez de VirtualBox**: optamos deliberadamente pelo Libvirt comunicando direto com a virtualização KVM do kernel Linux. A eliminação da emulação de terceiros proporciona performance quase de máquina física (*bare-metal*), menor overhead de CPU e consumo de memória muito mais enxuto, viabilizando a execução de várias máquinas virtuais no mesmo computador sem travar o sistema hospedeiro.
* **Isolamento de redes com duas placas (Dual-NIC)**:
  * `eth0` (Rede NAT padrão do Libvirt): usada exclusivamente para acesso externo à internet (download de pacotes do sistema operacional via gerenciador de pacotes quando necessário). A rota padrão dessa interface é propositalmente contida para não interferir nas rotas do cluster.
  * `eth1` (Rede Privada 172.24.0.0/24): o coração da infraestrutura. O Vagrant atribui os IPs estáticos descritos no inventário a essas interfaces. Todo o tráfego do cluster (`etcd`, `kube-apiserver`, Pods, CNI e NFS) transita exclusivamente por aqui.

Essa arquitetura Dual-NIC blinda o laboratório contra peculiaridades da sua rede física: você pode trocar de rede Wi-Fi, ir para o escritório, conectar ou desconectar cabos de rede e até usar VPNs no seu computador hospedeiro, que a comunicação interna e o roteamento entre as máquinas do cluster continuam 100% íntegros e intocados.

## O arquivo all.yml como mapa genético da stack

Se a topologia define onde as coisas rodam, o arquivo [inventario/group_vars/all.yml](https://github.com/vndmtrx/k8s-in-a-box/blob/main/inventario/group_vars/all.yml) define o que roda e em qual versão. No Ansible, variáveis colocadas dentro de `group_vars/all.yml` tornam-se visíveis automaticamente para todos os hosts do inventário.

Vamos dissecar os principais blocos do `all.yml` e examinar as decisões por trás de cada um.

### Definição de redes e cálculo de IPs derivados

Um cluster Kubernetes possui pelo menos três domínios de rede distintos que nunca devem se sobrepor: a rede física ou dos hosts, a rede interna dos Pods e a rede virtual de Services (ClusterIPs).

Em vez de preencher manualmente endereços IP em dezenas de lugares, definimos as faixas CIDR principais e calculamos os endereços derivados utilizando o plugin `ansible.utils.ipaddr`:

```yaml
# Trecho de inventario/group_vars/all.yml
rede_cidr_services: "172.25.128.0/17"
primeiro_ip_services: "{% raw %}{{ rede_cidr_services | ansible.utils.ipaddr('1') | ansible.utils.ipaddr('address') }}{% endraw %}"
coredns_ip: "{% raw %}{{ rede_cidr_services | ansible.utils.ipaddr('10') | ansible.utils.ipaddr('address') }}{% endraw %}"
```

O filtro `ansible.utils.ipaddr('10')` pega o décimo endereço utilizável dentro da sub-rede `172.25.128.0/17`, resultando em `172.25.128.10`. Esse endereço é repassado tanto para a configuração do *service* do CoreDNS quanto para o parâmetro `--cluster-dns` na inicialização de cada `kubelet`. Se você precisar mudar toda a faixa de Services do cluster para `10.96.0.0/12`, altera apenas `rede_cidr_services` e todos os componentes convergem sem inconsistências.

> [!NOTE] Por que o décimo IP para o CoreDNS?
> Para as outras redes derivadas no projeto (hosts, pods e o primeiro IP de services), pegamos sistematicamente o primeiro IP disponível usando o filtro com argumento `'1'`. Mas o CoreDNS é um caso à parte: o Kubernetes precisa de um endereço de ClusterIP fixo e previsível para que os nós e os pods saibam exatamente para onde mandar consultas de DNS. Em vez de disputar o primeiro IP da rede (que tradicionalmente fica reservado para o próprio serviço interno da API do Kubernetes), escolhemos um endereço aleatório dentro da faixa que calhou de ser o décimo IP do range (`.10`). O segredo não é nenhuma mística no número dez, e sim ter essa decisão declarada de ponta a ponta no inventário. O mapeamento completo das redes pode ser conferido em [inventario/group_vars/all.yml](https://github.com/vndmtrx/k8s-in-a-box/blob/main/inventario/group_vars/all.yml).

### Alternância de runtimes e plugins de rede

O projeto foi desenhado para permitir experimentação controlada. Queremos poder alternar o runtime de contêiner ou o plugin de rede CNI com uma flag no inventário:

```yaml
# Trecho de inventario/group_vars/all.yml
container_runtime: "crio"  # crio ou containerd
plugin_cni: "cilium"       # cilium ou canal
```

A variável `container_runtime` é consumida pelas roles para definir quais repositórios habilitar, quais pacotes instalar e qual socket registrar na inicialização do kubelet (`--container-runtime-endpoint`).

Na rede, a variável `plugin_cni: "cilium"` seleciona a stack padrão moderna com eBPF nativo e suporte a Gateway API. Caso o leitor queira testar a stack tradicional com `canal` (Flannel + Calico) e kube-vip, basta alterar essa variável para `canal`.

### O caso prático do upgrade para Kubernetes v1.37.0

Aqui chegamos ao coração da atualização que realizamos hoje no repositório. Em vez de espalhar versões em múltiplos manifestos, concentramos a versão base em uma única linha e deixamos o Ansible propagar o valor:

```yaml
# Trecho de inventario/group_vars/all.yml
versao_kubernetes: "v1.37.0"

# O valor propaga automaticamente para imagens dos Static Pods:
control_plane_images:
  apiserver: "{% raw %}registry.k8s.io/kube-apiserver:{{ versao_kubernetes }}{% endraw %}"

# E para os downloads oficiais com checagem de integridade:
download_artefatos:
  kubelet-bin:
    url: "{% raw %}https://dl.k8s.io/release/{{ versao_kubernetes }}/bin/linux/amd64/kubelet{% endraw %}"
    arquivo: "kubelet"
    checksum: "{% raw %}sha256:https://dl.k8s.io/release/{{ versao_kubernetes }}/bin/linux/amd64/kubelet.sha256{% endraw %}"
```

Ao alterar a linha `versao_kubernetes: "v1.37.0"`, o Ansible automaticamente:

1. Calcula a nova URL oficial de download do binário do `kubelet` e seu hash SHA256 correspondente.
2. Faz o download do binário compilado do `kubectl v1.37.0`.
3. Atualiza os manifestos dos *Static Pods* em cada manager para apontar para as tags `registry.k8s.io/kube-apiserver:v1.37.0`, `kube-controller-manager:v1.37.0` e `kube-scheduler:v1.37.0`.
4. Garante que os nós baixem a imagem correspondente do `kube-proxy:v1.37.0`.

A lista com todas as versões vinculadas da stack (como etcd 3.7.1, crictl v1.37.0, helm v3.22.0 e cilium v1.20.2) está documentada na íntegra no [inventario/group_vars/all.yml](https://github.com/vndmtrx/k8s-in-a-box/blob/main/inventario/group_vars/all.yml). A versão do cluster torna-se um parâmetro puramente declarativo.

## A tríade de playbooks e o sistema semântico de tags

A execução do Ansible no projeto está dividida em três playbooks complementares, com separação estrita de contexto:

```
ansible/
├── cluster.yml   # Orquestra infraestrutura base, PKI, nós e control plane
├── ops.yml       # Provisiona o bastion host (kubox), rede CNI e exemplos
└── addons.yml    # Instala aplicações de monitoramento e dashboards
```

### O playbook principal: cluster.yml

O arquivo [ansible/cluster.yml](https://github.com/vndmtrx/k8s-in-a-box/blob/main/ansible/cluster.yml) orquestra a subida do cluster desde a máquina física até os pods do *control plane*. Em vez de um script monolítico, ele organiza as etapas por grupos de nós:

```yaml
# Trecho de ansible/cluster.yml
- name: Tarefas a serem executadas no host
  hosts: localhost
  connection: local
  become: false
  roles:
    - role: infra-artefatos
      tags: [cluster-artefatos, cluster]

- name: Configuração do kubelet
  hosts: cluster
  become: true
  serial: 1
  roles:
    - role: k8s-kubelet
      tags: [cluster-kubelet, cluster]
```

Note o uso da diretiva `serial: 1` na role `k8s-kubelet`. Quando atualizamos ou configuramos os agentes dos nós, queremos que o Ansible processe uma máquina por vez, minimizando o impacto no cluster em execuções de manutenção.

A sequência completa, incluindo as plays para balanceadores de carga, servidor NFS e os *Static Pods* do *control plane* (etcd, apiserver, controller-manager e scheduler), pode ser conferida diretamente em [ansible/cluster.yml](https://github.com/vndmtrx/k8s-in-a-box/blob/main/ansible/cluster.yml).

### O playbook operacional: ops.yml

O arquivo [ansible/ops.yml](https://github.com/vndmtrx/k8s-in-a-box/blob/main/ansible/ops.yml) opera em um plano diferente. Ele não roda contra os nós do cluster, mas sim contra a máquina `kubox` (grupo `clientes`), gerenciando a instalação da rede CNI por meio de condições dinâmicas:

```yaml
# Trecho de ansible/ops.yml
- name: Instalação da Rede CNI e dependências
  hosts: clientes
  become: false
  roles:
    - role: cni-cilium
      when: plugin_cni == 'cilium'
      tags: [ops-cni-cilium, ops-cni, ops]
    - role: cni-canal
      when: plugin_cni == 'canal'
      tags: [ops-cni-canal, ops-cni, ops]
```

É o `ops.yml` que aplica os manifestos de CNI no cluster. Em vez de rodar o comando `helm install` ou `kubectl apply` na sua máquina de desenvolvimento local (o que exigiria instalar o Helm, o CLI do Cilium e o kubectl no seu próprio Linux), essas ferramentas são instaladas e executadas de dentro da VM `kubox`. Seu hospedeiro permanece limpo.

O playbook completo com a instalação das ferramentas operacionais (`k9s`, `popeye`, `tailspin`) e deploys de exemplo está em [ansible/ops.yml](https://github.com/vndmtrx/k8s-in-a-box/blob/main/ansible/ops.yml).

### O playbook de addons: addons.yml

Por fim, o arquivo [ansible/addons.yml](https://github.com/vndmtrx/k8s-in-a-box/blob/main/ansible/addons.yml) isola a implantação de serviços opcionais que não afetam o ciclo de vida do Kubernetes básico:

```yaml
# Trecho de ansible/addons.yml
- name: Aplicação de addons independentes de CNI no cluster
  hosts: clientes
  become: false
  roles:
    - role: addon-apps-cluster
      tags: [addons]
```

Ele gerencia painéis e telemetria (Headlamp, Prometheus, Grafana) através da role `addon-apps-cluster`, permitindo ligar ou desligar essa camada a qualquer momento sem interferir no core do cluster.

### Como o Makefile encapsula as tags

Ninguém quer memorizar comandos longos do Ansible com argumentos de configuração e dezenas de tags separadas por vírgula. O [Makefile](https://github.com/vndmtrx/k8s-in-a-box/blob/main/Makefile) do repositório funciona como uma camada de abstração ergonômica:

```makefile
# Trecho do Makefile
infra: garante-config
	ANSIBLE_CONFIG="$(CFG)" ansible-playbook "$(PLAYBOOK)" --tags cluster-artefatos,cluster-pki,cluster-sistema,cluster-balanceador,cluster-nfs

control-plane: garante-config
	ANSIBLE_CONFIG="$(CFG)" ansible-playbook "$(PLAYBOOK)" --tags cluster-kubernetes-base,cluster-kubelet,cluster-etcd,cluster-kube-apiserver,cluster-kube-controller-manager,cluster-kube-scheduler
```

Quando você digita `make infra`, o Makefile valida se a configuração ativa no `config.mk` corresponde ao symlink atual, define a variável de ambiente `ANSIBLE_CONFIG` e dispara exatamente as tags necessárias para preparar o terreno antes do Kubernetes. 

Além disso, o Makefile traz utilitários essenciais de confiabilidade:

* **Validação prévia de dependências (`make check-deps`)**: antes de subir qualquer máquina ou playbook, o script verifica se o processador tem suporte a KVM habilitado, se o seu usuário faz parte do grupo `libvirt`, e se o Ansible, o Vagrant e o plugin `vagrant-libvirt` estão presentes. Isso impede falhas frustrantes no meio do provisionamento por falta de permissão ou pacote esquecido.
* **Ciclos rápidos de estudo (`make cluster-etcd`, `make cluster-kubelet`)**: durante o desenvolvimento ou depuração de um subsistema específico, essas tags executam apenas as tarefas da role designada. Você testa alterações em segundos sem ter que esperar a execução completa de todo o cluster.
* **Limpeza e purga de estado (`make clean`)**: além de destruir as VMs no Vagrant, esse comando apaga completamente a pasta `artefatos/`, garantindo que certificados antigos e caches locais do Ansible (`fact_caching` e inventário) sejam purgados sem deixar resíduos.

A lista completa de alvos está disponível no [Makefile](https://github.com/vndmtrx/k8s-in-a-box/blob/main/Makefile).

## Decisões de design no Ansible do projeto

Antes de avançarmos para os comandos práticos, vale a pena abrir o capô e entender por que a estrutura do Ansible neste projeto é organizada dessa maneira. Não se trata de convenção estética: tomamos decisões muito conscientes para garantir que o laboratório seja rápido, reproduzível e seguro.

### Construção centralizada de certificados no host

Em muitas instalações manuais, a geração de certificados TLS é uma bagunça espalhada: comandos `openssl` ou `cfssl` rodam dentro de cada VM, autoridades certificadoras são copiadas de um lado para o outro e qualquer erro exige caçar chaves perdidas no sistema de arquivos.

No nosso projeto, a role [ansible/infra-pki](https://github.com/vndmtrx/k8s-in-a-box/blob/main/ansible/infra-pki) roda inteiramente em `localhost`. Todos os certificados (Root CA, intermediárias de etcd, kubernetes e front-proxy, além de certificados de nós, clientes e service accounts) são forjados uma única vez na máquina hospedeira e armazenados em `artefatos/pki/`.

As máquinas virtuais nunca chegam a ver a chave privada da Root CA: elas recebem por cópia SSH estritamente o par exato de chave e certificado que precisam para funcionar. Além disso, controlamos a regeração com a variável `pki_regerar_certs: false`. Se você destruir e recriar as VMs, não precisa regerar toda a infraestrutura criptográfica do zero.

> [!NOTE] E as listas de revogação de certificados (CRLs)?
> Em ambientes de produção corporativos, é indispensável manter listas de revogação de certificados (CRLs) ou validação OCSP para revogar imediatamente o acesso caso uma máquina seja comprometida. Em um laboratório local e descartável como o nosso, onde os nós são destruídos e recriados em minutos e o acesso é estritamente isolado no host, implementar CRLs adicionaria burocracia sem benefício prático imediato. Contudo, a nossa arquitetura de CA centralizada no host permite plugar mecanismos de revogação no futuro sem retrabalho.

### Downloads atômicos e reaproveitamento de binários

A role [ansible/infra-artefatos](https://github.com/vndmtrx/k8s-in-a-box/blob/main/ansible/infra-artefatos) segue o mesmo princípio de eficiência. Em vez de várias máquinas virtuais baixarem os binários do `kubelet`, `kubectl` e plugins CNI simultaneamente da internet (disputando banda e correndo risco de throttling ou timeout), o Ansible baixa cada pacote uma única vez na máquina física, confere o hash SHA256 e guarda em `artefatos/bin/`. A partir dali, os binários são distribuídos localmente via SSH em segundos.

### Cache local de imagens OCI com Skopeo e importação direta

O mesmo raciocínio dos binários aplica-se às pesadas imagens de contêiner da infraestrutura (`pause`, `etcd`, `kube-apiserver`, etc.). Baixar essas imagens repetidamente a cada nova criação de cluster desperdiça banda e tempo.

A role `k8s-kubelet` (`tasks/07-download-imagens-sistema.yml`) implementa um mecanismo de cache local no host:

1. **Detecção**: o Ansible verifica se os tarballs das imagens necessárias já existem na pasta `imagens/` no host físico.
2. **Download centralizado**: se ausente, o primeiro nó manager (`manager1`) faz o download da imagem via `skopeo copy` direto do registro de contêineres para um tarball local e o transfere de volta para o host de desenvolvimento via `ansible.builtin.fetch`.
3. **Distribuição e carga direta no runtime**: para cada nó do cluster, o Ansible copia o tarball do host para a VM e o importa diretamente na camada de armazenamento do runtime configurado:
   * No **CRI-O**: a importação ocorre via `skopeo copy` diretamente para o `containers-storage`.
   * No **Containerd**: a importação ocorre via `ctr -n k8s.io images import`.

Esse fluxo viabiliza um ambiente "offline-ready": após o primeiro provisionamento, você pode destruir todas as VMs e recriar o laboratório completo sem depender de conexão externa com registries.

> [!NOTE] Cuidado com o espaço temporário no manager1
> Como o download da imagem do contêiner é feito inicialmente dentro do nó `manager1` antes de ser transferido de volta para o host físico, certifique-se de que o disco virtual do `manager1` tenha espaço livre suficiente para manipular esses tarballs temporários durante o primeiro ciclo de provisionamento.

### Extração dinâmica de ferramentas via OverlayFS

Outra solução prática do projeto está na forma como instalamos o utilitário `etcdctl` no bastion `kubox`. No passado, baixávamos da internet o arquivo compactado completo de lançamento do etcd (um tarball pesado para extrair um único binário).

Adiciona complexidade fazer isso direto do contêiner? Sim, admito que foi uma escolha arquitetural deliberada da minha parte: é um download pesado a menos da internet e uma garantia de paridade exata de versão entre o binário administrativo e o etcd que está rodando no cluster.

Aproveitamos o fato de que a imagem oficial do etcd já está rodando no cluster como Static Pod no `manager1`. O Ansible inspeciona o contêiner ativo com `crictl inspect`, localiza o caminho exato da camada mesclada no OverlayFS (`merged layer`) no disco do nó e copia o executável `/usr/local/bin/etcdctl` diretamente dessa montagem do Linux para o bastion. É economia de banda, eliminação de dependência externa e uso inteligente da infraestrutura que já está no ar.

### Padronização semântica de roles e tasklists

No passado do projeto, as roles usavam prefixos numéricos herdados (`00-artefatos`, `01-pki`, `02-sistema`, etc.). Conforme o cluster cresceu e incorporou novos CNIs e opções de runtime, essa numeração rígida virou uma armadilha de manutenção: para inserir um componente intermediário, era preciso renomear pastas inteiras.

Fizemos uma transição para uma taxonomia puramente semântica:

1. **infra-***: roles de fundação que preparam o terreno antes do Kubernetes existir (artefatos, PKI, balanceadores HAProxy e Keepalived, NFS e sistema operacional base).
2. **k8s-***: componentes centrais do Kubernetes (nós base, agente kubelet e os manifests dos pods estáticos do control plane).
3. **ops-***: ferramental administrativo e automações executadas a partir do bastion host `kubox`.
4. **cni-*** e **addon-***: redes de sobreposição intercambiáveis e serviços auxiliares de valor agregado.

Cada role possui tasklists enxutas e focadas em uma única responsabilidade. As tarefas são agrupadas logicamente (instalação de pacotes, renderização de templates Jinja2 e ativação de serviços systemd), permitindo que qualquer pessoa leia a pasta `tasks/` de uma role e entenda exatamente o que está acontecendo sem adivinhações.

## Diagnóstico e validação rápida

Para validar se o seu inventário e suas variáveis estão configurados corretamente antes de rodar qualquer playbook, o Ansible oferece comandos de introspecção nativos.

### Inspecionando a árvore de grupos

Para verificar como o Ansible enxerga a hierarquia de nós do cluster, execute a partir do diretório raiz:

```bash
$ ansible-inventory -i inventario/hosts.yml --graph
```

Esse comando renderiza a árvore completa de relações entre todos os grupos e nós. O ponto principal de atenção nessa inspeção é validar se os agrupamentos compostos (como `@cluster` unindo managers e workers, ou `@suporte` unindo balanceadores e NFS) estão aninhados corretamente. Se alguma máquina aparecer solta dentro de `@ungrouped` ou um grupo intermediário não for listado, significa que há um erro de indentação no seu arquivo `hosts-*.yml`.

### Verificando variáveis resolvidas por nó

Para confirmar quais variáveis e valores chegam a uma máquina específica, use a flag `--host`:

```bash
$ ansible-inventory -i inventario/hosts.yml --host manager1 | grep -E 'versao_kubernetes|plugin_cni|memory'
```

A saída confirma a consolidação das variáveis de host com as variáveis de grupo:

```json
    "memory": 3072,
    "plugin_cni": "cilium",
    "versao_kubernetes": "v1.37.0",
```

### Testando variáveis ativas com o módulo debug

Caso você queira inspecionar o valor de uma variável em todos os nós simultaneamente sem rodar nenhum playbook longo, o módulo `debug` em modo ad-hoc é a ferramenta ideal. Lembre-se apenas de que essa checagem ad-hoc exige que as máquinas virtuais estejam ligadas e acessíveis na rede privada (`make cluster-up`):

```bash
$ ANSIBLE_CONFIG=./ansible/.ansible.cfg ansible -m debug -a "var=versao_kubernetes" cluster
```

Saída esperada:

```
manager1 | SUCCESS => {
    "versao_kubernetes": "v1.37.0"
}
worker1 | SUCCESS => {
    "versao_kubernetes": "v1.37.0"
}
worker2 | SUCCESS => {
    "versao_kubernetes": "v1.37.0"
}
```

## Conclusão

Compreender o inventário e a estrutura de variáveis é a diferença entre operar automação como quem copia comandos cegamente e operar com controle total da arquitetura. No **k8s-in-a-box**, cada arquivo tem um propósito bem delimitado: o `hosts-*.yml` dimensiona e posiciona as peças, o `all.yml` dita as regras e versões da stack, e a tríade de playbooks executa as tarefas na ordem estrita de dependências.

Com o inventário compreendido e o nosso cluster configurado com o **Kubernetes v1.37.0**, estamos prontos para a próxima etapa: no próximo post ({% include post-ref.html slug="k8sbox-preparacao-sistema-base" text="Parte 4: Preparação do Sistema Base" %}), vamos entrar dentro das VMs e aplicar a role `infra-sistema`, configurando pacotes essenciais, módulos de kernel (`br_netfilter`, `overlay`), parâmetros de `sysctl`, desativação de swap e a política de SELinux para receber os binários do Kubernetes.

## Referências

[^1]: **Kubernetes v1.37: Garhwal Release Notes** {*Kubernetes Blog*} ([Link](https://kubernetes.io/blog/2026/08/26/kubernetes-v1-37-release/))

[^2]: **Ansible Documentation: How to build your inventory** {*Red Hat*} ([Link](https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html))

[^3]: **Ansible Documentation: Variables and group_vars** {*Red Hat*} ([Link](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html))

[^4]: **Ansible netaddr Filter Documentation** {*Ansible Community*} ([Link](https://docs.ansible.com/ansible/latest/collections/ansible/utils/docsite/filters_ipaddr.html))

[^5]: **Repositório k8s-in-a-box** {*GitHub*} ([Link](https://github.com/vndmtrx/k8s-in-a-box))

[^6]: **Kubernetes in a Box, Parte 2 - Ferramentas e Ambiente de Laboratório** {*vndmtrx.github.io*} ({% include post-ref.html slug="k8sbox-ferramentas-ambiente" text="Link" %})

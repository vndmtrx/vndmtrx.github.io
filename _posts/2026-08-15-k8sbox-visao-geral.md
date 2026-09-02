---
layout: post
title: "Kubernetes in a Box, Parte 1 - Visão Geral"
subtitle: "Por que construir um cluster Kubernetes na mão?"
author:
  - "Eduardo N. S. R."
date: 2026-08-15 14:30:00 GMT-3
modified_date: 2026-09-02 13:57:00 GMT-3
permalink: /posts/k8sbox-visao-geral/
tags: [Kubernetes, Ansible, DevOps, Infraestrutura]
series: Kubernetes in a Box
---

Se você trabalha com infraestrutura, nuvem ou DevOps, as chances de você já ter digitado `kubeadm init` ou subido um cluster em nuvem gerenciada (EKS, GKE, AKS) com dois cliques são de praticamente cem por cento. Essas ferramentas são incríveis para o dia a dia de trabalho porque ninguém em sã consciência quer passar quatro horas configurando certificados e manifestos na mão para subir um ambiente de homologação. O problema começa quando algo quebra nos bastidores e você não faz a menor ideia do que está acontecendo por baixo do capô.

> [!NOTE] Nota da Série
> Este post inaugura a série **"Kubernetes in a Box"**, onde vamos dissecar e construir, do zero e de forma totalmente reproduzível via Ansible, um cluster Kubernetes completo, com alta disponibilidade, armazenamento persistente, rede moderna e observabilidade. Todo o código do projeto está disponível no repositório parceiro [vndmtrx/k8s-in-a-box](https://github.com/vndmtrx/k8s-in-a-box).

Há algum tempo, eu mantinha um projeto de estudos chamado `vagrant-k8s-cluster` [^2], onde eu subia máquinas virtuais locais e deixava o `kubeadm` fazer a mágica dele. Funcionava perfeitamente, mas aquilo sempre me deixava com uma pulga atrás da orelha. O `kubeadm` gerava dezenas de certificados, subia um `etcd`, configurava o *control plane*, gerava *kubeconfigs*, e no final me entregava um comando de *join*. Mas o que exatamente estava acontecendo ali dentro? Como os certificados se conversavam? Como o *control plane* encontrava o `etcd`? Como o nó decidia quem tinha autoridade para fazer o quê?

A resposta para essas perguntas não está nos instaladores automáticos. Ela está em abrir a caixa preta e montar o quebra-cabeça peça por peça. Foi assim que nasceu o projeto **k8s-in-a-box** [^1]: um laboratório estruturado para construir um cluster Kubernetes seguindo a cartilha do *Kubernetes The Hard Way* [^3], mas com uma diferença crucial. Em vez de colar comandos gigantescos no terminal até os dedos doerem e nunca mais conseguir reproduzir o ambiente, automatizamos cada milímetro do processo com **Ansible** e **Vagrant**.

A proposta aqui é construir o conhecimento de forma estritamente progressiva. Vamos começar do hardware virtual até chegar num cluster completo, seguro e validado pelo teste de conformidade oficial da CNCF [^6].

## A ilusão da conveniência e o valor do Hard Way

Ferramentas como `kubeadm`, `k3s`, `k0s`, `minikube` ou `kind` são fantásticas para o que se propõem. Eu mesmo uso no meu cotidiano. Mas quando o seu objetivo é o **estudo profundo**, a conveniência excessiva vira um obstáculo pedagógico.

Quando o `kubeadm` roda, ele abstrai decisões de arquitetura fundamentais:

1. **A cadeia de confiança de PKI**: ele gera autoridades certificadoras temporárias, chaves de serviço e certificados com SANs pré-calculados, sem que você precise entender a diferença de papéis entre cliente e servidor em cada componente.
2. **O ciclo de vida do etcd**: ele coloca o banco de dados do cluster para rodar sem que você veja como o protocolo Raft negocia *quórum*, como os pares (*peers*) se autenticam via mTLS ou como fazer um *troubleshooting* direto na base.
3. **O ecossistema de rede e CNI**: ele apenas espera passivamente que você aplique um manifesto de rede para os nós finalmente saírem do estado `NotReady`.

Construir o cluster na mão, etapa por etapa, retira esse véu mágico. Quando um certificado expira, você sabe exatamente qual CA intermediária emitiu aquele arquivo e qual componente parou de falar com quem. Quando o *scheduler* não consegue posicionar um pod, você sabe onde olhar porque foi você quem escreveu o manifesto do *Static Pod* e configurou os parâmetros do binário.

E por que colocar Ansible no meio? Porque o *Kubernetes The Hard Way* clássico tem uma fraqueza: ele é manual demais. Se você errar um caractere no meio de um comando de vinte linhas na vigésima etapa, você muitas vezes precisa destruir tudo e começar do zero. Com Ansible, temos a clareza didática de cada tarefa expressa em YAML combinada com a capacidade de destruir e reconstruir o cluster inteiro em minutos com um único comando.

## Topologia e arquitetura do laboratório

Para simular um ambiente de produção realista dentro da nossa máquina local, desenhamos uma topologia com separação clara de responsabilidades. Nada roda na máquina física do hospedeiro, todo o laboratório vive dentro de uma rede privada isolada gerenciada pelo Vagrant e LibVirt (KVM).

A arquitetura geral do ambiente segue o diagrama abaixo:

```
[ MÁQUINA HOSPEDEIRA (HOST) ]
      │
      └──> [ REDE PRIVADA DO CLUSTER: 172.24.0.0/24 ]
            │
            ├──> VIP do Control Plane (Keepalived): 172.24.0.10
            │     │
            │     └──> [ LOAD BALANCERS: HAProxy + Keepalived ]
            │           ├──> loadbalancer1 (172.24.0.21)
            │           └──> loadbalancer2 (172.24.0.22) [Modo Completo]
            │
            ├──> [ MANAGERS / CONTROL PLANE: etcd + apiserver + controller + scheduler ]
            │     ├──> manager1 (172.24.0.31)
            │     ├──> manager2 (172.24.0.32) [Modo Completo]
            │     └──> manager3 (172.24.0.33) [Modo Completo]
            │
            ├──> [ WORKERS: kubelet + runtime de container ]
            │     ├──> worker1 (172.24.0.41)
            │     └──> worker2 (172.24.0.42)
            │
            ├──> [ SERVIÇOS AUXILIARES ]
            │     ├──> nfs (172.24.0.25) ──> Armazenamento Persistente
            │     └──> kubox (172.24.0.254) ──> Bastion Host de Operação
            │
            └──> [ FAIXAS DE IP DE APLICAÇÃO E LOAD BALANCER ]
                  ├──> 172.24.0.101 ──> Headlamp Dashboard
                  ├──> 172.24.0.102 ──> Traefik Dashboard (Canal)
                  ├──> 172.24.0.103 ──> Grafana (Observabilidade)
                  └──> 172.24.0.104 ──> Hubble UI (Cilium)
```

Cada grupo de máquinas possui uma função estrita no ecossistema:

* **Load Balancers (`loadbalancer1`, `loadbalancer2`)**: nós leves rodando HAProxy e Keepalived. Eles expõem o IP flutuante (VIP `172.24.0.10`), balanceando o tráfego do `kube-apiserver` (porta `6443`) e do `etcd` (porta `2379`) entre os nós de controle, garantindo que a queda de um manager não derrube a comunicação do cluster.
* **Managers (`manager1` a `manager3`)**: o cérebro do cluster. Cada nó manager roda uma instância do `etcd` (formando *quórum* distribuído) e os três componentes vitais do *control plane* [^4]: `kube-apiserver`, `kube-controller-manager` e `kube-scheduler`.
* **Workers (`worker1`, `worker2`)**: os nós de trabalho que efetivamente executam os contêineres e aplicações dos usuários, gerenciados pelo `kubelet` em conjunto com o *runtime* de contêiner.
* **Servidor NFS (`nfs`)**: fornece armazenamento em rede (`/srv/nfs/k8s`) para que o cluster consiga provisionar volumes persistentes dinâmicos via *StorageClass*.
* **Bastion Host (`kubox`)**: uma estação de trabalho dedicada à administração do cluster. Ela centraliza ferramentas como `kubectl`, `helm`, `etcdctl`, `k9s` e `popeye`. Isso evita a má prática clássica de acessar nós de produção por SSH para rodar comandos administrativos.

> [!NOTE] Workloads no Control Plane
> Por padrão no Kubernetes, os nós de *control plane* recebem uma marcação de restrição (*taint*) chamada `node-role.kubernetes.io/control-plane:NoSchedule`, impedindo que pods de aplicação sejam agendados neles para não competir por CPU e memória com os serviços vitais do cluster. No nosso laboratório, como estamos rodando em ambiente local com recursos de hardware finitos, o Ansible remove deliberadamente esse *taint*, permitindo que os managers também executem *workloads* de usuário para otimizar o aproveitamento das VMs. Em ambientes reais de produção, misturar plano de controle com aplicações comuns é uma péssima ideia. Vamos dissecar essa mecânica de *labels* e *taints*, e as boas práticas de isolamento, em detalhes na **Parte 18**.

### Segmentação das faixas de rede

Para evitar qualquer interferência com redes domésticas ou corporativas, o projeto divide a infraestrutura em três blocos de rede independentes e sem sobreposição:

| Finalidade | Bloco CIDR | Descrição |
|------------|------------|-----------|
| **Hosts / VMs** | `172.24.0.0/24` | Rede privada das máquinas virtuais e IPs virtuais |
| **Pods** | `172.25.0.0/17` | Rede interna atribuída aos contêineres pelo CNI |
| **Services** | `172.25.128.0/17` | Rede virtual para serviços internos (*ClusterIP*) |

> [!NOTE] Faixas de IP do Laboratório
> A imensa maioria dos roteadores residenciais utiliza a faixa `192.168.0.0/16` (geralmente `192.168.0.0/24` ou `192.168.1.0/24`), enquanto redes corporativas e VPNs adotam extensivamente blocos derivados de `10.0.0.0/8`. Já o bloco privado `172.16.0.0/12` (RFC 1918) é raramente configurado nesses contextos. Ao alocar nosso laboratório em `172.24.0.0/24` e `172.25.0.0/16`, eliminamos qualquer risco de conflito de rotas (*overlapping*) com o seu Wi-Fi doméstico ou a conexão da sua empresa.

## As três configurações de cluster

Nem todo mundo tem uma máquina com 32 GB de memória RAM disponível para subir meia dúzia de máquinas virtuais pesadas. Pensando nisso, o projeto foi arquitetado com um sistema dinâmico de configurações baseado em *symlinks* gerenciados pelo Makefile.

Você escolhe o tamanho do cluster que cabe no seu hardware e o projeto se adapta automaticamente:

| Configuração | LBs | Managers | Workers | Total VMs | Recursos Estimados | Cenário Recomendado |
|--------------|-----|----------|---------|-----------|--------------------|---------------------|
| `nano` | 1 | 1 | 1 | 5 VMs | ~6 GB RAM, 6 vCPUs | Testes rápidos em laptops modestos |
| `mini` (Padrão) | 1 | 1 | 2 | 6 VMs | ~10 GB RAM, 9 vCPUs | Estudos gerais e multi-pod |
| `completo` | 2 | 3 | 2 | 9 VMs | ~19 GB RAM, 18 vCPUs | Alta disponibilidade real e *failover* |

> [!NOTE] Nota
> O total de VMs inclui sempre o servidor NFS e a máquina de gestão `kubox`. No dia a dia da série, utilizaremos a configuração `mini` como referência padrão, pois ela já permite validar o balanceamento de carga entre múltiplos nós de trabalho sem sobrecarregar a máquina hospedeira.

## As decisões arquiteturais do projeto

Ao longo do desenvolvimento do projeto, várias decisões técnicas foram tomadas para aproximar o laboratório das práticas modernas de engenharia, sem abrir mão do aprendizado artesanal:

* **Control Plane via Static Pods** [^5]: em versões anteriores, o projeto instalava cada componente do *control plane* como um serviço nativo do sistema operacional gerenciado pelo `systemd`. Migramos essa arquitetura para *Static Pods* gerenciados diretamente pelo `kubelet` local. Isso espelha a arquitetura de instaladores consolidados e traz resiliência automática ao ciclo de vida dos componentes.
* **SELinux ativo com política customizada**: a esmagadora maioria dos tutoriais de Kubernetes manda você desabilitar o SELinux no primeiro parágrafo. Aqui fizemos o oposto: mantivemos o SELinux ativo e construímos uma política customizada de *Type Enforcement* (`k8s-custom-selinux`) compilada no kernel, resolvendo os acessos legítimos sem desativar a proteção do sistema operacional.
* **Cilium e eBPF como CNI padrão**: adotamos o Cilium como provedor de rede primário, aproveitando programas eBPF no kernel Linux para substituir regras do `iptables`, com suporte nativo a Gateway API e anúncio L2 (sem depender de ferramentas externas). Para fins comparativos, a stack clássica com Canal (Calico + Flannel) e Kube-vip também foi mantida.
* **Execução 100% Rootless**: as aplicações de demonstração do cluster rodam sem privilégios de `root`, utilizando `securityContext`, portas acima de 1024 e diretiva `fsGroup` no NFS, alcançando nota máxima (Score A 100%) no analisador de segurança Popeye.
* **Cache local com Skopeo e extração via OverlayFS**: para não gastar sua banda baixando gigabytes de imagens a cada recriação de laboratório, o projeto faz cache centralizado das imagens via `skopeo copy`. Além disso, o utilitário `etcdctl` é extraído diretamente da camada *OverlayFS* do contêiner do `etcd` em execução, sem necessidade de baixar pacotes compactados extras da internet.

> [!NOTE] Conformidade CNCF
> Desde a versão anterior (baseada puramente em serviços `systemd`) até a atual (com *Static Pods*), o cluster foi testado e **aprovado** na [suíte oficial de testes de conformidade da CNCF via Sonobuoy](https://github.com/cncf/k8s-conformance). Isso garante que a nossa construção artesanal não é só um brinquedo de entusiasta: o cluster é 100% aderente aos padrões e às especificações oficiais do Kubernetes.

## Como a série está organizada

Para garantir que cada conceito seja absorvido com calma e na ordem certa de dependências, organizamos os posts em **quatro blocos complementares**:

```
[ BLOCO 1: CLUSTER BASE (Posts 1 ao 13) ]
  -> Infraestrutura, Vagrant, Ansible, PKI, HAProxy, Kubelet,
     Static Pods (etcd, apiserver, controller, scheduler) e Kubox.

[ BLOCO 2: INTEGRAÇÃO (Posts 14 ao 17) ]
  -> Onde os módulos se conectam: CNI (Cilium), CoreDNS, kube-proxy,
     armazenamento persistente NFS, Gateway API e Observabilidade.

[ BLOCO 3: OPERAÇÕES (Posts 18 ao 20) ]
  -> O cluster pronto em ação: aplicações não-root, escalabilidade
     automática (VPA + HPA) e validação final com Sonobuoy da CNCF.

[ BLOCO 4: EXTRAS E DEEP-DIVES (Posts E1 ao E4) ]
  -> Mergulhos aprofundados opcionais: política de SELinux, CNI Canal,
     runtime containerd e acesso remoto via túneis SSH.
```

Essa separação garante que quem deseja apenas o cluster base funcional pode seguir os dois primeiros blocos e ter um ambiente totalmente operacional. Quem quiser ir além e dominar a operação e segurança avançada terá os blocos subsequentes como guia.

## A filosofia de diagnóstico e troubleshooting

Um dos maiores problemas que vejo em tutoriais de tecnologia é que eles ensinam o "caminho feliz" onde nada dá errado. No mundo real de infraestrutura, as coisas quebram. Certificados expiram, sockets do *runtime* ficam inacessíveis, nós entram em *split-brain*, e pods travam em *CrashLoopBackOff*.

Por isso, estabelecemos uma regra para toda a série: **cada post prático trará uma seção dedicada de Diagnóstico e Troubleshooting**. 

Em vez de apenas mandar você rodar uma *role* e torcer pelo melhor, vamos exercitar comandos reais de inspeção no terminal:

* Verificar certificados e datas de validade com `openssl`
* Avaliar saúde de membros e consistência Raft com `etcdctl`
* Inspecionar o *runtime* de contêineres diretamente com `crictl`
* Analisar *logs* e eventos detalhados do plano de controle com `kubectl` e `journalctl`
* Rastrear violações de segurança no kernel com `ausearch`

Com isso, o objetivo não é apenas ensinar você a construir um cluster, mas formar a musculatura operacional necessária para diagnosticar qualquer problema em ambientes Kubernetes reais.

## Conclusão

Ok, eu admito: este primeiro post foi puramente conceitual e não digitamos uma única linha de automação ou comando de infraestrutura no terminal ainda. Pode até dar uma sensação de post meio "vazio" na prática, mas sem assentar essa fundação teórica e alinhar as expectativas sobre a arquitetura que estamos buscando, as próximas etapas virariam apenas um amontoado de parâmetros do Ansible sem contexto.

Montar um cluster Kubernetes manualmente não é sobre reinventar a roda para colocar em produção amanhã. É sobre adquirir o domínio técnico que diferencia quem apenas consome abstrações prontas de quem realmente entende a engenharia distribuída que faz a nuvem moderna funcionar.

Se você for do tipo curioso (ou impaciente, como eu) e quiser ver o laboratório inteiro funcionando de antemão antes dos próximos posts saírem, o repositório parceiro [vndmtrx/k8s-in-a-box](https://github.com/vndmtrx/k8s-in-a-box) já está totalmente pronto, funcional e com documentação aprofundada (no diretório `docs/`) cobrindo cada um dos elementos que vamos dissecar aqui. Sinta-se à vontade para clonar, explorar os playbooks e brincar no terminal por conta própria.

Nas próximas semanas, vamos desmontar e remontar cada engrenagem desse sistema. No próximo post (**Parte 2: Ferramentas e Ambiente de Laboratório**), começaremos pela fundação prática: vamos configurar os pré-requisitos do hospedeiro, dissecar como o Vagrant lê dinamicamente nosso inventário YAML e subir as primeiras máquinas virtuais com rede privada via LibVirt e Makefile.

Prepare o seu terminal e até a próxima!

## Referências

[^1]: **Repositório k8s-in-a-box** {*GitHub*} ([Link](https://github.com/vndmtrx/k8s-in-a-box))

[^2]: **Repositório vagrant-k8s-cluster** {*GitHub*} ([Link](https://github.com/vndmtrx/vagrant-k8s-cluster))

[^3]: **Kubernetes The Hard Way** {*Kelsey Hightower*} ([Link](https://github.com/kelseyhightower/kubernetes-the-hard-way))

[^4]: **Kubernetes Components** {*Kubernetes Documentation*} ([Link](https://kubernetes.io/docs/concepts/overview/components/))

[^5]: **Static Pods** {*Kubernetes Documentation*} ([Link](https://kubernetes.io/docs/tasks/configure-pod-container/static-pod/))

[^6]: **CNCF Kubernetes Conformance Program** {*Cloud Native Computing Foundation*} ([Link](https://github.com/cncf/k8s-conformance))


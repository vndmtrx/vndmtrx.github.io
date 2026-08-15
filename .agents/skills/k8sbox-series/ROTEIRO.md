# Roteiro Final - Série Kubernetes in a Box

Série de posts para o blog vndmtrx.github.io, baseada no repositório [k8s-in-a-box](https://github.com/vndmtrx/k8s-in-a-box). Construção progressiva de conhecimento do zero ao cluster funcional, onde cada post foca em um tema isolado, posts de integração conectam os módulos, e posts de operação usam o cluster pronto.

## Estrutura da Série

| Bloco | Posts | Analogia | Descrição |
|-------|-------|----------|-----------|
| **Cluster Base** | 1–13 | Testes unitários | Cada módulo construído e explicado isoladamente |
| **Integração** | 14–17 | Testes de integração | Módulos se conectam, cluster ganha vida |
| **Operações** | 18–20 | Testes de comportamento | Cluster pronto sendo usado para coisas reais |
| **Extras** | E1–E4 | Opcionais | Deep-dives e alternativas para quem quer ir além |

**Convenções da série:**
- `series: Kubernetes in a Box` no front matter de cada post
- Cada post referencia as roles/tasks Ansible correspondentes no repositório (sem tags, apontando para o código na branch principal)
- Cada post termina com uma seção **Diagnóstico e Troubleshooting** com comandos reais de operação e cenários de problemas
- Menções breves a SELinux nos posts onde ele aparece (kubelet, etcd, etc.) com referência futura ao Extra 1

---

## Bloco 1: Cluster Base (Construção dos Módulos)

### Parte 1: Abertura da Série e Visão Geral do Projeto
- **Roles Ansible**: nenhuma (post conceitual)
- **Conteúdo**:
  - A história: do `vagrant-k8s-cluster` (kubeadm) ao k8s-in-a-box (hard way)
  - O que o `kubeadm` esconde e por que abrir a caixa preta
  - Filosofia do projeto: Kubernetes The Hard Way + Ansible para reprodutibilidade
  - Visão panorâmica da arquitetura final (diagrama ASCII da topologia completa)
  - Grupos de máquinas e a decisão consciente de taints: remoção do `NoSchedule` nos managers para viabilizar lab local vs boas práticas de isolamento em produção
  - As três configurações de cluster (nano, mini, completo) e quando usar cada uma
  - Decisões arquiteturais e a validação de conformidade da CNCF via Sonobuoy (aprovado desde a versão legado com systemd até a atual com Static Pods)
  - Apresentação do repositório parceiro e como acompanhar a série
  - Roadmap da série e o que será construído
- **Diagnóstico**: Nenhum neste post (é conceitual). Apresentar a filosofia de diagnóstico que será usada na série.
- **Objetivo**: Situar o leitor na motivação, dar a visão do destino final e criar entusiasmo pelo caminho.
- **Entregável**: Leitor com contexto completo sobre o que é o projeto, por que existe e o que será construído.

### Parte 2: Ferramentas e Ambiente de Laboratório
- **Roles Ansible**: nenhuma (infraestrutura do host)
- **Arquivos**: `Vagrantfile`, `Makefile`, `config.mk`
- **Conteúdo**:
  - Pré-requisitos do host (KVM, libvirt, Ansible, Vagrant, plugin vagrant-libvirt)
  - `make check-deps` e verificação completa de dependências
  - O Vagrantfile dissecado: leitura dinâmica do inventário YAML, geração de chaves SSH ed25519, criação das VMs
  - Duas placas de rede: eth0 (NAT do Vagrant, ignorada) vs eth1 (rede privada `172.24.0.0/24`, o coração do cluster)
  - Configuração de rede via `nmcli`: por que forçar eth1 como gateway e ignorar eth0
  - AlmaLinux 10: por que essa escolha e o que muda em relação a outras distros
  - O sistema de topologias via symlinks (`config.mk`, `make init`, `make status`)
  - O Makefile como interface: `make k8s-in-a-box`, `make cluster-etcd`, `make snapshot`/`make restore`
- **Diagnóstico**: `vagrant status`, `virsh list --all`, `nmcli con show`, verificar conectividade entre VMs via ping.
- **Objetivo**: Ambiente local funcional com VMs prontas para receber o cluster.
- **Entregável**: Host de desenvolvimento configurado, VMs subindo via `make up` com rede privada operacional.

### Parte 3: O Inventário Ansible e as Variáveis do Cluster
- **Roles Ansible**: nenhuma (configuração)
- **Arquivos**: `ansible/.ansible.cfg`, `inventario/group_vars/all.yml`, `configs/hosts-*.yml`, `ansible/cluster.yml`, `ansible/ops.yml`, `ansible/addons.yml`
- **Conteúdo**:
  - O `.ansible.cfg` do projeto e suas decisões (host_key_checking, SSH pipelining)
  - Estrutura do inventário: grupos (`loadbalancers`, `managers`, `workers`, `nfs`, `clientes`)
  - Anatomia do `hosts-*.yml`: IP, FQDN, memória, CPUs por VM
  - O `all.yml` dissecado: versões, redes, portas, plugins, certificados
  - Como trocar runtime (`crio`/`containerd`), CNI (`cilium`/`canal`), versão do K8s
  - Papel das variáveis derivadas (`primeiro_ip_hosts`, `coredns_ip`, etc.)
  - O conceito de roles no Ansible e a tag system do projeto (`cluster-*`, `ops-*`, `addons`)
  - A relação entre os três playbooks: `cluster.yml`, `ops.yml` e `addons.yml`
- **Diagnóstico**: `ansible-inventory --graph`, `ansible-inventory --host manager1`, validar variáveis com `ansible -m debug -a "var=versao_kubernetes" all`.
- **Objetivo**: Entender como uma única variável no `all.yml` propaga para todo o cluster.
- **Entregável**: Leitor capaz de personalizar versões, redes e plugins apenas editando variáveis.

### Parte 4: Preparação do Sistema Base
- **Roles Ansible**: `infra-sistema`, `k8s-cluster-base`
- **Tags**: `cluster-sistema`, `cluster-kubernetes-base`
- **Conteúdo**:
  - O que é feito em todas as VMs antes de qualquer componente Kubernetes
  - Pacotes essenciais: `curl`, `wget`, `conntrack`, `socat` e por que cada um
  - `/etc/hosts` gerado dinamicamente a partir do inventário Ansible
  - SELinux configurado como permissivo: menção breve, decisão consciente de não desabilitar (detalhes no Extra 1)
  - Tunáveis de kernel (`sysctl`): `net.ipv4.ip_forward`, `bridge-nf-call-iptables`
  - Módulos do kernel: `br_netfilter`, `overlay` e por que o Kubernetes precisa deles
  - Configuração do firewall e desabilitação do swap
- **Diagnóstico**: `sysctl net.ipv4.ip_forward`, `lsmod | grep br_netfilter`, `getenforce`, `cat /etc/hosts`, `swapon --show`.
- **Objetivo**: Toda VM com o sistema operacional preparado para receber componentes Kubernetes.
- **Entregável**: Cluster de VMs com sistema base uniforme, pronto para as próximas etapas.

### Parte 5: Certificados e a Infraestrutura de PKI (Teoria)
- **Roles Ansible**: nenhuma (post conceitual)
- **Conteúdo**:
  - O problema: como componentes distribuídos provam identidade entre si?
  - Conceitos fundamentais: chave privada, chave pública, CSR, certificado, CA
  - A cadeia de confiança: Root CA -> Intermediate CA -> End-entity
  - mTLS: autenticação mútua (servidor prova quem é, cliente também)
  - SANs (Subject Alternative Names): por que um certificado precisa de múltiplos nomes
  - Key Usage e Extended Key Usage: `serverAuth`, `clientAuth` e o que cada um habilita
  - Algoritmos: por que ECDSA secp256r1 em vez de RSA (chaves menores, mesma segurança)
  - Validade e rotação: por que certificados expiram e o que acontece quando expiram
  - Certificados de curta duração como ferramenta de aprendizado (30 dias no projeto vs 1–2 anos em produção)
  - Analogia: a PKI como o sistema de cartórios e registros civis do cluster
- **Diagnóstico**: Comandos OpenSSL para inspecionar certificados existentes (do próprio sistema): `openssl x509 -in /etc/pki/tls/certs/ca-bundle.crt -text -noout | head -30`.
- **Objetivo**: Leitor compreende por que certificados existem e o que cada campo significa.
- **Entregável**: Base conceitual sólida para entender a implementação prática no post seguinte.

### Parte 6: Certificados e PKI (Implementação)
- **Role Ansible**: `infra-pki`
- **Tag**: `cluster-pki`
- **Conteúdo**:
  - A hierarquia do k8s-in-a-box: Root CA + 3 CAs intermediários (etcd, kubernetes, front-proxy)
  - Segmentação: por que separar o CA do etcd do CA do Kubernetes (isolamento, revogação seletiva)
  - O fluxo automatizado: geração da chave -> CSR -> assinatura pelo CA -> distribuição
  - Certificados individualizados por nó (etcd-server, kubelet) vs certificados compartilhados (admin)
  - Mapeamento completo: quem assina quem, onde é usado, quais SANs tem
  - O `system:node:<hostname>` do kubelet e o Node Authorization do K8s (CN + Organization -> RBAC)
  - Par de chaves de Service Account (RSA, não x509) e sua função em tokens JWT
  - Validades curtas propositais: 30 dias end-entity, 1 ano CAs intermediários, 5 anos Root CA
  - O cenário de renovação: como os 30 dias criam um ciclo acelerado de aprendizado sobre rotação
  - Distribuição seletiva: chaves privadas geradas localmente, nunca transitam pela rede
  - Validação com OpenSSL: verificar cadeia, inspecionar SANs, testar mTLS
- **Diagnóstico**: `openssl x509 -in cert.pem -text -noout`, `openssl verify -CAfile ca-chain.pem cert.pem`, `openssl x509 -in cert.pem -enddate -noout` (verificar expiração), `openssl s_client -connect 172.24.0.31:2379 -cert client.pem -key client-key.pem -CAfile ca-chain.pem`.
- **Objetivo**: PKI completa gerada e validada.
- **Entregável**: Toda a cadeia de certificados gerada localmente pelo Ansible, com testes de verificação passando.

### Parte 7: O Balanceador de Carga (HAProxy e Keepalived)
- **Role Ansible**: `infra-balanceador`
- **Tag**: `cluster-balanceador`
- **Conteúdo**:
  - O problema: se o kube-apiserver roda em múltiplos nós, quem decide pra onde vai a requisição?
  - HAProxy como proxy reverso TCP: frontends (6443, 2379) e backends (managers)
  - Template `haproxy.cfg.j2` e a geração dinâmica a partir dos managers do inventário
  - Check de sintaxe antes de aplicar (`haproxy -c`)
  - Health checks: como o HAProxy detecta que um manager caiu e redireciona
  - Página de status em porta 9000 e o que ela mostra
  - Keepalived e VRRP: o VIP `172.24.0.10` que flutua entre load balancers
  - Ativo-passivo: MASTER vs BACKUP e failover automático
  - Por que instalar Keepalived mesmo em configuração nano (1 LB): uniformidade arquitetural
  - O fluxo completo: kubectl -> VIP -> HAProxy -> manager saudável
- **Diagnóstico**: `curl http://172.24.0.21:9000/stats`, `ip addr show | grep 172.24.0.10` (verificar quem tem o VIP), `systemctl status haproxy`, `systemctl status keepalived`, simular queda de um manager e observar o failover.
- **Objetivo**: Ponto de entrada único e resiliente para o cluster.
- **Entregável**: Load balancer operacional com VIP ativo, pronto para receber tráfego do API Server e etcd.

### Parte 8: O Container Runtime e o kubelet
- **Roles Ansible**: `k8s-kubelet`, `infra-artefatos`
- **Tags**: `cluster-kubelet`, `cluster-artefatos`
- **Conteúdo**:
  - O que é um Container Runtime e por que o Kubernetes não roda containers sozinho
  - CRI (Container Runtime Interface): o contrato entre kubelet e runtime
  - CRI-O vs containerd: as duas opções do projeto e por que CRI-O é o padrão (alternativa no Extra 3)
  - Instalação e configuração do runtime escolhido
  - Plugins CNI base: download e instalação em `/opt/cni/bin` (+ `restorecon` para SELinux, menção breve ao Extra 1)
  - Cache local de imagens com Skopeo: evitando downloads repetitivos
    - Detecção, download centralizado via `skopeo copy`, fetch para host, distribuição e carga
    - CRI-O (`skopeo copy -> containers-storage`) vs containerd (`ctr images import`)
  - Instalação do kubelet: download do binário, `setype: bin_t`, unit file systemd
  - Contexto SELinux do kubelet: `unconfined_service_t` (menção breve, detalhes no Extra 1)
  - O diretório `/etc/kubernetes/manifests` e o conceito de Static Pods (introdução)
  - O kubelet sobe, mas os nós ficam `NotReady` até o CNI ser instalado
- **Diagnóstico**: `systemctl status kubelet`, `journalctl -u kubelet -f`, `crictl ps`, `crictl images`, `crictl pods`, detectar problemas de socket CRI (`crictl info`).
- **Objetivo**: Todos os nós do cluster com runtime de container e kubelet operacionais.
- **Entregável**: kubelet rodando em todos os nós, pronto para receber Static Pods e workloads.

### Parte 9: A Evolução Arquitetural: de Binários a Static Pods
- **Roles Ansible**: nenhuma (post narrativo/histórico)
- **Referência**: PR #76, commit `5b24874`
- **Conteúdo**:
  - Como era antes: cada componente como binário + unit file systemd (o "hard way" puro)
  - Os problemas: múltiplos unit files para manter, ciclo de vida manual, sem auto-recovery
  - O que são Static Pods: manifestos em `/etc/kubernetes/manifests` gerenciados pelo kubelet
  - Por que o kubeadm usa Static Pods (e o k8s-in-a-box decidiu seguir o mesmo caminho)
  - A migração no projeto: PR #76 e o que mudou
    - Remoção de roles antigas (`07-etcd`, `08-kube-apiserver`, `09-kube-controller-manager`, `10-kube-scheduler`)
    - Unificação de playbooks (`cluster-bin.yml` e `cluster-pod.yml` -> `cluster.yml`)
    - Remoção da variável `INSTALACAO` e simplificação do Makefile
    - 910 linhas removidas, 64 adicionadas
  - O que continuou "hard way": toda a PKI, configurações e parâmetros ainda são gerados manualmente
  - Benefícios práticos: kubelet reinicia componentes caídos, menos código no Ansible, arquitetura uniforme
  - O kube-proxy como caso especial: DaemonSet em vez de Static Pod (autenticação via ServiceAccount)
  - O papel de `hostNetwork: true` nos Static Pods do control plane
- **Diagnóstico**: Nenhum (post narrativo). Apresentar o conceito de como diagnosticar Static Pods que será usado nos próximos posts.
- **Objetivo**: Leitor entende por que o projeto evoluiu e as vantagens de cada abordagem.
- **Entregável**: Compreensão completa da decisão arquitetural que fundamenta os próximos posts.

### Parte 10: O Cluster etcd
- **Role Ansible**: `k8s-etcd-pod`
- **Tags**: `cluster-etcd-pod`, `cluster-etcd`
- **Conteúdo**:
  - O que é o etcd: banco chave-valor distribuído, algoritmo Raft, quorum
  - Por que o etcd é o componente mais crítico do cluster (todo o estado vive aqui)
  - Manifesto do Static Pod privilegiado: por que `privileged: true` (domínio SELinux `spc_t`, escrita em `/var/lib/etcd`, menção breve ao Extra 1)
  - Distribuição de certificados: server, peer, client (cada nó com seu próprio par)
  - A flag `--initial-cluster`: descoberta entre membros, gerada dinamicamente pelo Ansible
  - Montagem de volumes: certificados e dados persistentes (`/var/lib/etcd`)
  - Configurações de cluster: URLs de listen (client, peer, metrics)
  - O truque do `etcdctl` via OverlayFS: extrair o binário do container em execução sem baixar nada
    - `crictl ps` -> `crictl inspect` -> caminho do merged layer -> cópia do binário
  - Validação: `etcdctl member list`, `endpoint health`, `endpoint status`
- **Diagnóstico**: `etcdctl member list -w json | yq -P`, `etcdctl endpoint health`, `etcdctl endpoint status -w json | yq -P`, `etcdctl endpoint hashkv` (verificar consistência Raft), `crictl logs <container-id-do-etcd>`, diagnosticar split-brain e problemas de quorum.
- **Objetivo**: Cluster etcd funcional e validado.
- **Entregável**: etcd rodando como Static Pod nos managers, com mTLS, quorum formado e `etcdctl` operacional no kubox.

### Parte 11: O kube-apiserver (Static Pod)
- **Role Ansible**: `k8s-apiserver-pod`
- **Tags**: `cluster-kube-apiserver-pod`, `cluster-kube-apiserver`
- **Conteúdo**:
  - O que o API Server faz: gateway REST para todo o estado do cluster
  - Por que ele é o único componente que fala com o etcd diretamente
  - O manifesto dissecado: flags de configuração
    - `--etcd-servers`: apontando para o VIP do HAProxy
    - Certificados de servidor, cliente-etcd, cliente-kubelet, front-proxy, service-account
    - `--service-cluster-ip-range`: a rede de serviços
    - `--authorization-mode`: Node, RBAC
  - kubeconfig files: admin, controller-manager, scheduler, kubelet (cada um com seu certificado)
  - Geração dos kubeconfig pelo Ansible: template, certificado embutido em base64, contexto
  - Como o API Server valida requests: cadeia de certificados + RBAC
  - Validação: `kubectl get nodes` (finalmente!) e `kubectl cluster-info`
- **Diagnóstico**: `kubectl get nodes`, `kubectl cluster-info`, `crictl logs <container-id-do-apiserver>`, `kubectl get --raw /healthz`, `curl -k https://172.24.0.10:6443/healthz`, diagnosticar certificados expirados (erro x509), CrashLoopBackOff no Static Pod do apiserver.
- **Objetivo**: API Server respondendo requisições autenticadas.
- **Entregável**: kube-apiserver como Static Pod, kubeconfig funcional, primeiro `kubectl get nodes` da série.

### Parte 12: Controller Manager e Scheduler (Static Pods)
- **Roles Ansible**: `k8s-controller-manager-pod`, `k8s-scheduler-pod`
- **Tags**: `cluster-kube-controller-manager-pod`, `cluster-kube-scheduler-pod`
- **Conteúdo**:
  - O kube-controller-manager: o "loop de reconciliação" do Kubernetes
    - Observa estado desejado vs atual e age para corrigir
    - Parâmetros críticos: `--cluster-signing-cert-file`, `--service-account-private-key-file`
    - Leader election em HA: apenas um controller ativo por vez
  - O kube-scheduler: o "alocador" de pods
    - Observa pods não agendados e escolhe o melhor nó
    - `KubeSchedulerConfiguration` (API moderna `kubescheduler.config.k8s.io/v1`)
    - Leader election em HA
  - Diferença entre ativo-ativo (etcd, apiserver) e ativo-passivo (controller, scheduler)
  - Kubeconfig de cada componente: certificado client, apontando pro VIP
  - Validação: pods em `kube-system`, logs dos componentes
- **Diagnóstico**: `kubectl get pods -n kube-system`, `crictl logs <container-id>`, `kubectl get leases -n kube-system` (verificar leader election), diagnosticar controller-manager em crash (certificados, conectividade com apiserver).
- **Objetivo**: Control plane completo e funcional.
- **Entregável**: Todos os componentes do control plane rodando como Static Pods nos managers.

### Parte 13: O Bastion Host (kubox) e as Ferramentas de Operação
- **Role Ansible**: `ops-ferramentas`
- **Tags**: `ops-sistema`, `ops-ferramentas`
- **Conteúdo**:
  - O problema: acessar managers diretamente para operar é anti-pattern
  - O kubox como bastion host: máquina dedicada para administração
  - Ferramentas instaladas: `kubectl`, `helm`, `etcdctl`, `k9s`, `popeye`, `yq`, `tailspin`
  - `etcdctl` via OverlayFS (recapitulação rápida do truque do post 10)
  - kubeconfig do admin no kubox: como ele se autentica no cluster
  - Primeiros comandos no cluster: `kubectl get nodes`, `kubectl get pods -A`, `kubectl get events`
  - `k9s`: interface interativa completa para o cluster
  - O cluster neste ponto: nós `NotReady`, sem CNI, sem DNS, sem nada rodando de verdade
  - Recapitulação: o que já temos e o que falta para o cluster ganhar vida
- **Diagnóstico**: `kubectl get nodes -o wide` (todos `NotReady`), `kubectl get pods -A -o wide`, `kubectl get events -A --sort-by=.metadata.creationTimestamp`, `k9s`, `popeye -A` (baseline antes dos addons).
- **Objetivo**: Estação de operação centralizada pronta.
- **Entregável**: kubox com todas as ferramentas configuradas, comunicação com o cluster validada, cluster "esqueleto" pronto para receber vida.

---

## Bloco 2: Integração (Conectando os Módulos)

> A partir daqui, os módulos construídos isoladamente nos posts unitários começam a se conectar. Cada post de integração mostra a interação entre componentes e o cluster vai ganhando funcionalidades reais.

### Parte 14: O Cluster Ganha Vida (CNI + CoreDNS + kube-proxy)
- **Roles Ansible**: `cni-cilium` (ou `cni-canal` + `addon-kube-proxy` + `addon-kubevip` + `addon-traefik`), `addon-apps-cluster` (CoreDNS e Metrics Server)
- **Tags**: `ops-cni`, `addons`
- **Conteúdo**:
  - O momento mágico: nós saem de `NotReady` para `Ready`
  - CNI (Container Network Interface): o que é e por que sem ele nada funciona
  - **Cilium (padrão)**: eBPF, substituição do iptables, performance nativa no kernel
    - Instalação via Helm, configuração no `all.yml`
    - Pools de IP e L2 Announcement nativos (substitui Kube-vip)
    - Hubble UI: visualização de fluxo de rede em tempo real
  - Stack alternativa Canal mencionada brevemente (detalhes no Extra 2)
  - CoreDNS via Helm: resolução interna (`svc.cluster.local`)
  - kube-proxy: DaemonSet no Canal ou eBPF replacement no Cilium
    - Por que DaemonSet e não systemd: ServiceAccount, sem certificados extras
    - Exposição de métricas na porta 10249
  - Metrics Server: `kubectl top nodes` e `kubectl top pods` funcionando
  - Validação: pods se comunicando, DNS resolvendo, `kubectl get nodes` mostra `Ready`
- **Diagnóstico**: `kubectl get nodes` (agora `Ready`!), `kubectl run test --image=busybox --rm -it -- nslookup kubernetes.default`, `kubectl top nodes`, `kubectl get pods -n kube-system`, `cilium status` (se Cilium), diagnosticar nó preso em `NotReady` (logs do kubelet, CNI não instalado).
- **Objetivo**: Cluster com rede funcional, DNS interno e métricas básicas.
- **Entregável**: Cluster operacional com nós `Ready`, pods se comunicando entre namespaces.

### Parte 15: Armazenamento: NFS, Volumes Persistentes e StorageClass
- **Roles Ansible**: `infra-nfs` (servidor), `addon-apps-cluster` (NFS Subdir Provisioner)
- **Tags**: `cluster-nfs`, `addons`
- **Conteúdo**:
  - O problema: pods são efêmeros, mas dados precisam sobreviver a reinícios
  - O conceito de PersistentVolume (PV), PersistentVolumeClaim (PVC) e StorageClass
  - O servidor NFS: `nfs-utils`, `/srv/nfs/k8s`, `/etc/exports` e suas opções (`rw`, `sync`, `no_root_squash`)
  - Exportação para a rede do cluster (`172.24.0.0/24`)
  - O NFS Subdir External Provisioner via Helm: ensinando o K8s a "fatiar" o NFS sob demanda
  - StorageClass `nfs-client` como classe padrão
  - Provisionamento dinâmico: PVC -> Provisioner -> subdiretório no NFS -> montado no pod
  - Interação NFS + rootless: o papel do `fsGroup` na permissão de escrita (introdução)
  - Comparação com cloud providers (EBS, GCE PD) para contextualizar

> [!NOTE]
> Embora o Ansible instale o servidor NFS no início da pipeline (para otimizar o fluxo de provisionamento), o NFS só é efetivamente útil após o cluster estar ativo e o Provisioner ser aplicado. Por isso o post está posicionado aqui na integração, quando o leitor pode ver o ciclo completo funcionando.

- **Diagnóstico**: `showmount -e 172.24.0.25` (do NFS server), `kubectl get sc` (StorageClass), `kubectl get pv,pvc -A`, criar um PVC de teste e verificar subdiretório criado no NFS, diagnosticar PVC preso em `Pending`.
- **Objetivo**: Armazenamento persistente operacional no cluster.
- **Entregável**: Servidor NFS configurado, Provisioner ativo, PVCs sendo atendidos dinamicamente.

### Parte 16: Gateway API e Exposição de Serviços
- **Roles Ansible**: `cni-cilium` (Gateway nativo) ou `addon-traefik` (Canal)
- **Conteúdo**:
  - O problema: como acessar aplicações rodando dentro do cluster a partir de fora?
  - A evolução: Ingress (legado) -> Gateway API (futuro)
  - Objetos Gateway API: `GatewayClass`, `Gateway`, `HTTPRoute`
  - **Com Cilium**: Envoy integrado como controller nativo do Gateway API
  - **Com Canal**: Traefik como Gateway API Controller (menção, detalhes no Extra 2)
  - CRDs do Gateway API: instalação e configuração
  - Pools de IP para LoadBalancer: `kubevip_ips_manuais` e `kubevip_ips_loadbalacing`
  - L2 Announcement: como IPs virtuais são anunciados na rede via ARP
  - Configuração prática: criar um Gateway e um HTTPRoute
  - O fluxo: request externo -> IP de LoadBalancer -> Gateway -> HTTPRoute -> Service -> Pod
- **Diagnóstico**: `kubectl get gateway -A`, `kubectl get httproute -A`, `kubectl describe gateway <nome>`, testar acesso via `curl http://172.24.0.1xx`, diagnosticar HTTPRoute sem backend.
- **Objetivo**: Cluster capaz de expor serviços para acesso externo via Gateway API.
- **Entregável**: Gateway operacional, leitor capaz de expor qualquer serviço via HTTPRoute.

### Parte 17: Observabilidade (Prometheus + Grafana + Headlamp)
- **Role Ansible**: `addon-apps-cluster` (Prometheus Stack, Headlamp)
- **Tags**: `addons`
- **Conteúdo**:
  - kube-prometheus-stack via Helm: Prometheus, Grafana e Alertmanager (desabilitado para economia)
  - Namespace `monitoramento` e configuração de recursos (requests/limits)
  - Monitoramento dos Static Pods do Control Plane (endpoints estáticos dos managers)
    - kubeControllerManager e kubeScheduler com `insecureSkipVerify`
    - kubeEtcd com esquema `http`
  - ServiceMonitor do CoreDNS com label para Prometheus
  - Métricas do kube-proxy via porta 10249
  - Dashboards pré-carregados no Grafana (global, api-server, coredns, namespaces, nodes, pods)
  - Exposição do Grafana via LoadBalancer (`172.24.0.103`)
  - Headlamp Dashboard: interface web administrativa (`172.24.0.101`)
    - Token de ServiceAccount para autenticação
  - Hubble UI (`172.24.0.104`): observabilidade de rede do Cilium
  - Obtendo a senha do Grafana via `kubectl get secret`
- **Diagnóstico**: `kubectl get pods -n monitoramento`, `kubectl get servicemonitor -A`, verificar targets no Prometheus (`/targets`), diagnosticar scrape falhando (certificados, portas), `kubectl -n headlamp create token headlamp-admin`.
- **Objetivo**: Cluster completamente observável.
- **Entregável**: Grafana com dashboards ricos, Headlamp operacional, Hubble UI mostrando fluxos de rede.

---

## Bloco 3: Operações (Cluster Pronto, Hora de Usar)

> O cluster está completo: rede, armazenamento, exposição externa e monitoramento. Agora é hora de usá-lo para coisas reais.

### Parte 18: Labels, Taints e Primeiras Aplicações (Rootless)
- **Roles Ansible**: `addon-apps-cluster` (labels/taints), `ops-exemplos`
- **Tags**: `addons`, `exemplos`
- **Conteúdo**:
  - Labels nos nós: `node-role.kubernetes.io/control-plane`, `node-role.kubernetes.io/worker`
  - Taints nos managers: o papel do `node-role.kubernetes.io/control-plane:NoSchedule` em produção vs decisão de remoção no lab local para viabilizar cargas com recursos finitos
  - Deploy da hello-app (Nginx rootless): dashboard do cluster com atalhos para serviços
    - Redirecionamento de portas (80 -> 8080 via ConfigMap)
    - `securityContext`: `runAsNonRoot`, `runAsUser: 101`, `runAsGroup: 101`
    - `emptyDir` para `/var/run` e `/var/cache/nginx` (pastas temporárias do root)
    - Preservação de logs em stdout/stderr (links simbólicos)
    - PodDisruptionBudget para disponibilidade
  - Deploy do contador (PHP/Apache rootless + CronJob)
    - Persistência em PVC via NFS (usando o StorageClass da Parte 15)
    - `fsGroup: 10001` para compartilhar escrita entre app e cronjob
    - Apache rootless: `ports.conf` e `000-default.conf` via ConfigMap
  - Exposição via Gateway API (HTTPRoute para cada app)
  - Por que rootless: o risco real de containers root (escape -> privilégios no host)
- **Diagnóstico**: `kubectl get pods -n exemplos`, `kubectl describe pod <pod> -n exemplos`, `kubectl logs <pod> -n exemplos`, testar acesso via LoadBalancer, `curl http://172.24.0.1xx/contador/`, verificar PVC montado (`kubectl exec -n exemplos <pod> -- ls /dados/`).
- **Objetivo**: Aplicações reais rodando no cluster com segurança e persistência.
- **Entregável**: Aplicações rootless acessíveis via LoadBalancer, dados persistidos no NFS.

### Parte 19: Autoscaling (VPA + HPA + Testes de Carga)
- **Role Ansible**: `addon-apps-cluster` (VPA), `ops-exemplos` (HPA, stress tests)
- **Tags**: `addons`, `exemplos`
- **Conteúdo**:
  - **Horizontal Pod Autoscaler (HPA)**: escala a quantidade de réplicas
    - Baseado em CPU via Metrics Server
    - `minReplicas: 2`, `maxReplicas: 5`, `targetCPUUtilizationPercentage: 50`
    - CronJob de teste de estresse: gerando carga artificial
    - PodDisruptionBudget: garantindo disponibilidade durante scaling
  - **Vertical Pod Autoscaler (VPA)**: ajusta recursos (CPU/RAM) dos pods
    - Chart Helm `autoscalers/vertical-pod-autoscaler`
    - Modos: `Off` (recomendação), `Initial` (na criação), `Auto` (recria pods)
    - Convivência VPA + HPA: por que usar `Off` quando HPA está ativo
    - `controlledValues: RequestsOnly` e `minAllowed/maxAllowed`
  - Cenários dedicados de teste:
    - CronJob com VPA `Initial` (ajusta recursos na criação)
    - Deployment com VPA `Auto` + PDB (evict alternado, respeitando PDB)
  - Observando scaling em ação: `kubectl get hpa --watch`, `kubectl describe vpa`
- **Diagnóstico**: `kubectl get hpa -n exemplos --watch`, `kubectl describe vpa -n exemplos`, `kubectl top pods -n exemplos`, observar réplicas subindo e descendo, `kubectl get events -n exemplos --sort-by=.metadata.creationTimestamp`.
- **Objetivo**: Cluster respondendo automaticamente a variações de carga.
- **Entregável**: HPA e VPA demonstrados com cenários reais de estresse.

### Parte 20: Conformidade e Validação Final
- **Conteúdo**:
  - Recapitulação: tudo o que foi construído em 19 posts
  - **Popeye**: varredura de boas práticas
    - `popeye -n exemplos`: Score A (100%) no namespace de exemplos
    - `popeye -A`: análise global do cluster
    - Critérios: sem root, probes configuradas, resources definidos
  - **Sonobuoy**: o teste oficial de conformidade da CNCF
    - O que ele valida (control plane, nodes, APIs, conformidade oficial)
    - Histórico e evolução: aprovação total desde a stack legado com systemd até a consolidação em Static Pods
    - Execução e resultados práticos (100% dos testes aplicáveis aprovados)
  - Topologia `completo` (3 managers, 2 workers, 2 LBs): teste de failover
    - Simular queda de um manager e observar o cluster se recuperar
    - Verificar leader election do controller-manager e scheduler
  - O cluster base está pronto: o que é possível fazer a partir daqui
  - Teaser dos extras disponíveis
- **Diagnóstico**: `popeye -A`, `popeye -n exemplos`, `sonobuoy run`, `sonobuoy status`, `sonobuoy results`, simular falhas e observar auto-recovery.
- **Objetivo**: Cluster validado com selo de conformidade CNCF.
- **Entregável**: Leitor com cluster base completo, validado e pronto para expandir.

---

## Bloco 4: Extras (Posts Independentes e Opcionais)

> Posts standalone que aprofundam temas específicos. Podem ser lidos em qualquer ordem após o cluster base estar completo.

### Extra 1: SELinux e Kubernetes
- **Role Ansible**: `k8s-kubelet` (task `08-selinux.yml`)
- **Conteúdo**:
  - O elefante na sala: "basta desabilitar o SELinux" (e por que isso é péssima ideia)
  - O que o SELinux faz: confinamento por contextos (domínios), mesmo se o container escapar do namespace
  - Camadas de domínio no cluster: `init_t`, `unconfined_service_t`, `container_t`, `spc_t`, `container_file_t`
  - O kubelet como `unconfined_service_t` e o binário com `setype: bin_t`
  - Containers normais como `container_t` vs containers privilegiados como `spc_t`
  - A política customizada `k8s-custom-selinux` dissecada:
    - Bloco `require`: tipos, atributos e classes do sistema
    - Regras `allow` por domínio: dispositivos, sysfs, cgroups, rede, NFS, procfs, capabilities, eBPF
  - Decisões de hardening:
    - Read-only a `cgroup_t` (runtimes Go/Java leem limites, mas não podem alterar)
    - Read-only a `var_lib_t` (race condition do overlayfs, proteção de `/var/lib/etcd`)
  - Pipeline de compilação: `checkmodule` -> `semodule_package` -> `semodule -i`
  - Modo permissivo vs enforcing: como migrar com segurança
  - Componentes do Control Plane: etcd como `spc_t`, apiserver/scheduler/controller como `container_t`
  - Plugins CNI e `restorecon`
- **Diagnóstico**: `getenforce`, `semodule -l | grep k8s-custom-selinux`, `ausearch -m avc -ts recent`, `ls -Z /usr/local/bin/kubelet`, `ps -eZ | grep kubelet`, interpretar logs AVC (scontext, tcontext, tclass).
- **Objetivo**: SELinux ativo e compreendido, sem desabilitar segurança por conveniência.
- **Entregável**: Leitor entende cada regra da política customizada e sabe diagnosticar AVCs.

### Extra 2: CNI Alternativo (Canal - Flannel + Calico)
- **Roles Ansible**: `cni-canal`, `addon-kube-proxy`, `addon-kubevip`, `addon-traefik`
- **Conteúdo**:
  - Quando escolher Canal em vez de Cilium
  - Flannel (overlay VXLAN) + Calico (network policies): a stack clássica
  - kube-proxy como DaemonSet com iptables/IPVS
    - Métricas na porta 10249
    - Rollout automático via Ansible quando ConfigMap muda
  - Kube-vip: LoadBalancer L2 + Cloud Provider + Egress Gateway
  - Traefik como Gateway API Controller
  - Traefik Dashboard (`172.24.0.102`)
  - Comparação prática: Cilium vs Canal em funcionalidade e performance
- **Diagnóstico**: `kubectl get pods -n kube-system | grep canal`, `kubectl get pods -n kube-system | grep kube-proxy`, `kubectl get pods -n kube-system | grep kube-vip`.
- **Objetivo**: Demonstrar a alternativa de CNI disponível no projeto.
- **Entregável**: Cluster funcional com stack Canal completa.

### Extra 3: Container Runtime Alternativo (containerd)
- **Role Ansible**: `k8s-kubelet` (condicional `container_runtime: containerd`)
- **Conteúdo**:
  - Diferenças práticas entre CRI-O e containerd
  - Instalação e configuração do containerd
  - Importação de imagens via `ctr -n k8s.io images import` em vez de `skopeo copy`
  - Quando preferir um ou outro
  - Como alternar: `container_runtime: "containerd"` no `all.yml`
- **Diagnóstico**: `ctr -n k8s.io images list`, `ctr -n k8s.io containers list`, `crictl info` (funciona com ambos via CRI).
- **Objetivo**: Demonstrar a segunda opção de runtime do projeto.
- **Entregável**: Cluster funcional com containerd.

### Extra 4: Acesso Remoto com Túneis SSH
- **Conteúdo**:
  - O cenário: laboratório rodando num servidor headless, browser no laptop
  - Local Port Forwarding com SSH: mapeando IPs privados para localhost
  - Configuração via CLI (Linux/macOS/Windows Terminal)
  - Configuração via PuTTY (Windows GUI)
  - Mapeamento: 8080->Headlamp, 8081->Traefik, 8082->Grafana, 8083->Hubble
  - Testando acesso a cada dashboard
- **Diagnóstico**: `ssh -L ... -N -f` (modo background), `ss -tlnp | grep 8080` (verificar túnel ativo).
- **Objetivo**: Acesso aos dashboards de qualquer lugar via SSH.
- **Entregável**: Dashboards acessíveis via localhost no browser do usuário.

---

## Resumo Visual da Progressão

```
CLUSTER BASE (unitários) ─────────────────────────────────────
 1. Visão Geral
 2. Ferramentas (Vagrant/LibVirt/Make)
 3. Inventário Ansible
 4. Sistema Base
 5. PKI - Teoria
 6. PKI - Implementação
 7. HAProxy + Keepalived
 8. Container Runtime + kubelet
 9. Evolução: Binários -> Static Pods         <- PR #76
10. etcd (Static Pod)
11. kube-apiserver (Static Pod)
12. controller-manager + scheduler
13. kubox (Bastion Host)
                                    kubectl get nodes -> NotReady

INTEGRAÇÃO (conectando módulos) ──────────────────────────────
14. CNI + CoreDNS + kube-proxy                <- nós Ready!
15. Armazenamento (NFS + PV/PVC)
16. Gateway API
17. Observabilidade (Prometheus + Grafana)

OPERAÇÕES (usando o cluster) ─────────────────────────────────
18. Labels, Taints + Apps Rootless
19. Autoscaling (VPA + HPA)
20. Conformidade (Sonobuoy + Popeye)          <- cluster validado!

EXTRAS (opcionais, qualquer ordem) ───────────────────────────
E1. SELinux e Kubernetes
E2. CNI Alternativo (Canal)
E3. Runtime Alternativo (containerd)
E4. Túneis SSH
```

## Metadados da Série

```yaml
series: Kubernetes in a Box
tags: [Kubernetes, Ansible, DevOps, Infraestrutura]
```

- **Total**: 24 posts (13 base + 4 integração + 3 operações + 4 extras)
- **Repositório parceiro**: [vndmtrx/k8s-in-a-box](https://github.com/vndmtrx/k8s-in-a-box) (referências às roles/tasks Ansible na branch principal)
- **Seção de diagnóstico** em cada post (comandos reais de troubleshooting)
- **Menções breves** a SELinux nos posts relevantes (8, 10, 11) com referência ao Extra 1

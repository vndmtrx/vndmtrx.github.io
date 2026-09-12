---
layout: post
title: "Do Zero ao Desktop Perfeito: Automatizando o Debian 13 Trixie com Ansible"
subtitle: "Como transformar a sofrência de formatar a máquina em algo idempotente"
author:
  - "Eduardo N. S. R."
date: 2026-09-14 14:45:00 GMT-3
permalink: /posts/ansible-debian-desktop/
tags: [Linux, Debian, Ansible, DevOps, Produtividade]
published: false
---

Formatar o computador sempre começa com uma sensação maravilhosa de tela limpa e termina, invariavelmente, num pesadelo de três dias. Você senta na cadeira jurando que em vinte minutos vai estar com o ambiente pronto para programar. Quatro horas depois, você ainda está caçando chaves GPG na internet, brigando com repositórios que mudaram de nome, tentando lembrar quais extensões do GNOME deixavam sua barra utilizável e instalando compiladores na mão porque o sistema operacional veio pelado.

> [!NOTE] Repositório Parceiro
> Todo o código, a estrutura modular de tasks, templates de dconf e o script de bootstrap deste projeto estão disponíveis no repositório parceiro [vndmtrx/ansible-debian-desktop](https://github.com/vndmtrx/ansible-debian-desktop). Fique à vontade para clonar, dissecar e adaptar para as suas próprias preferências.

Quase todo profissional de tecnologia já tentou resolver essa dor escrevendo o infame arquivo `setup.sh`. Aquele script de oitocentas linhas de Bash recheado de `sudo apt-get install`, comandos encadeados com pipe no `curl` e dezenas de `echo >> ~/.bashrc`. O problema do script improvisado é que ele funciona exatamente uma vez: na segunda execução, ele duplica variáveis no seu shell, quebra pacotes pela metade quando a internet oscila e te deixa com uma máquina em estado imprevisível.

Se nós exigimos infraestrutura como código, testes rigorosos e garantia matemática de idempotência para os servidores e clusters que gerenciamos no trabalho, por que raios tratamos o nosso computador pessoal como uma colcha de retalhos artesanal?

Depois da enésima vez em que me vi num domingo à noite caçando atalho do GNOME no DuckDuckGo, cansei dessa palhaçada (e de pagar esse pedágio voluntário de masoquismo). Uns anos atrás decidi que se o computador precisa de mim pra fazer funcionar a barra de tarefas, quem está errado sou eu. Peguei o **Debian 13 (Trixie)** e dei uma bela repaginada em um playbook antigo meu de instalação: você clona o repositório, roda um único comando no terminal e, poucos minutos depois, tem um desktop completo, seguro, afinado para desenvolvimento e com zero intervenção humana.

Pois bem. Cá estamos para contar os bastidores técnicos, as minhas escolhas, os meus tropeços e a filosofia por trás dessa automação.

## A virtude da preguiça e a blindagem do Debian

Antes de falar de código, preciso fazer uma confissão honesta sobre a minha escolha de sistema operacional: eu gosto do Debian porque eu atualmente sou preguiçoso.

Calma, não me olhe com cara de julgamento. Eu tenho lugar de fala nessa área e já paguei todos os meus pedágios de iniciação no mundo do software livre. Já usei Conectiva lá nos primórdios do Linux no Brasil, já passei pelo Mandrake, passei anos configurando `rc.local` e compilando o kernel na mão no Slackware, fui usuário ferrenho de Arch Linux (com aquele frio na espinha característico a cada `pacman -Syu` na segunda-feira de manhã) e cheguei a compilar o meu próprio Gentoo do zero, passando um fim de semana inteiro esperando o GCC compilar tudo com flags agressivas de otimização só para ver um aplicativo abrir dois milissegundos mais rápido.

Para ser bem sincero, já cometi até o masoquismo supremo de qualquer usuário de Linux: encarar o **Linux From Scratch (LFS)** e desbravar o **Beyond Linux From Scratch (BLFS)** na unha, compilando toolchain, glibc e bibliotecas direto do código-fonte. Inclusive pretendo escrever posts futuros dedicados a essa jornada e a todo esse sofrimento autoimposto, ainda mais agora que soube que saíram versões atualizadas de ambos recentemente.

Só que a gente envelhece.

Chega uma fase na vida em que você não quer mais provar nada para ninguém, muito menos para o seu computador. Você não quer passar o sábado à noite consertando o servidor gráfico que quebrou depois de uma atualização de drivers ou caçando dependência órfã de biblioteca C. Hoje eu quero apenas paz de espírito, estabilidade e atualizações previsíveis que não quebram o meu trabalho.

É por isso que estou no Debian. Mais especificamente, no **Debian 13 (Trixie)**, a versão *Stable* (quem quiser fortes emoções com a ramificação *Testing* que vá rodar o Sid). E digo mais sobre a minha preguiça: eu não habilitei nem mesmo o repositório de *backports* na minha instalação. Quero o Debian estável puro, algo previsível e testado à exaustão. Se o pacote está na versão estável do Trixie, é ele que vai rodar. Sem inventar moda.

Mas a minha preguiça vem acompanhada de uma política muito rígida que adotei nos últimos anos: **a raiz do meu sistema operacional é sagrada**.

Eu adotei uma regra pessoal estrita: eu não instalo coisas no sistema operacional raiz sempre que possível, a não ser que o pacote venha do repositório oficial da distribuição ou do catálogo curado do `extrepo`. Sei que nem sempre dá para viver exclusivamente dos repositórios oficiais, mas quando preciso de algo de fora, tento colocar tudo no meu próprio usuário, isolado dentro da pasta `~/.local/bin` ou `~/.local/share`.

Se é uma ferramenta de automação em Python? Entra via `pipx` com venv próprio.
Se são runtimes de desenvolvimento como Erlang, Elixir ou Java? Vivem no meu home via `asdf` e `sdkman`.
Se é uma biblioteca pesada de machine learning? Roda em contêiner descartável no Docker.
Se é um AppImage? Fica no espaço do usuário, sem invadir o `/usr`.

O sistema operacional cuida dos drivers, do kernel e dos serviços essenciais. O resto vive no meu usuário. Se algo der errado com uma ferramenta de trabalho, o Debian continua impecável.

> [!NOTE] Em Casa de Ferreiro, Espeto de Pau
> Tá bom, confesso: minha regra sagrada de purismo às vezes parece aquele clássico "faça o que eu digo, não faça o que eu faço". No papel, o discurso de manter a raiz intocada é lindo e austero. Na prática do dia a dia, meu `$HOME` tem Flatpaks do Flathub para utilitários gráficos, AppImages soltos rodando sem a menor cerimônia e binários compilados na mão no `~/.local/bin`. O segredo da minha paz de espírito não é o celibato digital absoluto, mas manter o estrago estritamente contido no espaço de usuário sem poluir o sistema operacional raiz.

E adivinha? O próprio Debian moderno agora concorda comigo e adotou essa mesma postura na marra.

Quando fui rodar o meu playbook antigo de automação, a primeira surpresa foi tomar uma porta na cara do interpretador Python: `externally-managed-environment` [^1].

Essa é a implementação rigorosa do **PEP 668** [^2]. O Debian agora bloqueia qualquer tentativa de rodar `pip install` diretamente no ambiente global do sistema operacional. E com toda razão: misturar bibliotecas Python globais do sistema com pacotes pip gerenciados pelo usuário era a receita perfeita para quebrar ferramentas nativas na próxima atualização de versão.

Em vez de brigar com o sistema operacional ou tentar forçar a barra com flags perigosas como `--break-system-packages`, eu abracei o padrão oficial: o `pipx`.

```bash
#!/usr/bin/env bash
# bootstrap.sh: preparação isolada do ambiente
set -euo pipefail

# Garante ~/.local/bin no PATH sem duplicar no .bashrc
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  export PATH="$HOME/.local/bin:$PATH"
fi

# Instalação do Ansible em venv dedicado gerenciado pelo pipx
if ! command -v pipx >/dev/null 2>&1; then
  sudo apt-get update && sudo apt-get install -y pipx
fi

if ! command -v ansible-playbook >/dev/null 2>&1; then
  pipx install --include-deps ansible
fi
```
*Trecho do script de bootstrap preparando o interpretador do Ansible de forma 100% isolada.*

O `pipx` cria um ambiente virtual isolado para o Ansible dentro de `~/.local/share/pipx/venvs/ansible` e expõe apenas os executáveis necessários na minha pasta `~/.local/bin`. A raiz do sistema operacional continua intocada, o Ansible ganha acesso total aos seus módulos modernos e eu não corro o menor risco de quebrar o Python do sistema.

Além disso, transformei o meu `bootstrap.sh` em um painel de diagnóstico da máquina antes de disparar o playbook: ele checa se deixei instaladores manuais esperando na pasta de Downloads, confere versões de runtimes instaladas no host e cronometra o tempo exato do provisionamento.

## O segredo mais bem guardado da distribuição: o extrepo

Com o Ansible pronto no meu espaço de usuário, a primeira necessidade prática em qualquer máquina recém-formatada é habilitar repositórios de softwares externos. Afinal, navegadores focados em privacidade, ferramentas de contêiner e utilitários de infraestrutura raramente estão nos repositórios *main* da distribuição.

A via-crúcis clássica do usuário de Linux aqui é deplorável. Você entra no site de cada software, copia um comando com `curl` que baixa uma chave GPG, descobre que o comando antigo usava o obsoleto `apt-key add`, quebra a cabeça tentando entender onde salvar o arquivo `.gpg`, e no fim das contas seu diretório `/etc/apt/sources.list.d/` vira uma lixeira de fontes não confiáveis e avisos de segurança a cada `apt update`.

Existe uma alternativa oficial criada pelos próprios desenvolvedores do Debian que quase ninguém conhece: o **extrepo** [^3].

O `extrepo` é um gerenciador de repositórios externos com curadoria oficial. A equipe do Debian mantém uma lista centralizada de repositórios confiáveis de terceiros, com suas respectivas chaves públicas de assinatura auditadas e políticas de licença declaradas. Para habilitar um repositório oficial de terceiro, você não precisa baixar chaves na mão nem escrever arquivos de sources. Você apenas diz ao sistema o que quer habilitar.

No meu playbook, a task `01-extrepo.yaml` parametriza o arquivo de políticas do extrepo de forma dinâmica para a versão corrente da distribuição e habilita os repositórios declarados em lote:

```yaml
- name: Habilita repositórios via extrepo
  ansible.builtin.command:
    cmd: "extrepo enable {{ item.item }}"
  loop: "{{ extrepo_files.results }}"
  loop_control:
    label: "{{ item.item }}"
  when:
    - extrepo_install is succeeded
    - not item.stat.exists
  register: extrepo_result
  changed_when: extrepo_result.rc == 0
```
*Ativação declarativa de repositórios upstream homologados sem intervenção manual de chaves.*

Com isso, o playbook provisiona com segurança e integridade criptográfica o **LibreWolf** (meu navegador padrão focado em privacidade estrita), o **VSCodium** (meu editor de código sem telemetria), o **Docker CE** oficial e o repositório da **HashiCorp** para ferramentas de infraestrutura. Tudo auditado e respeitando as políticas de licença `main`, `contrib` e `non-free` do Debian.

Mas o que acontece quando você precisa de um aplicativo que não está listado no catálogo do extrepo?

## Repositórios manuais com a arquitetura moderna deb822

A pergunta de um milhão de reais surgiu quando decidi incluir o navegador **Vivaldi** no meu setup diário de trabalho. Fui consultar o banco de dados do `extrepo-data` todo animado e constatei que o Vivaldi não faz parte do catálogo oficial mantido pelo Debian.

Nessas horas, a maioria dos tutoriais da internet manda você baixar a chave pública e jogar num arquivo `.list` de linha única em `/etc/apt/sources.list.d/vivaldi.list`. Por favor, não faça isso. O formato de linha única é herança legada dos anos noventa e está sendo gradativamente substituído no Debian pelo formato estruturado **deb822** [^4].

No Debian 13, a convenção moderna para fontes de pacotes utiliza arquivos `.sources` baseados em blocos declarativos RFC 822 (o mesmo padrão usado nos arquivos de controle de pacotes do Debian). Além disso, o gerenciador de pacotes moderno aceita diretamente chaves públicas de assinatura em formato ASCII puro (`.asc`), dispensando invocações desnecessárias de `gpg --dearmor`.

Para manter a minha política de isolamento e não misturar repositórios manuais com as ferramentas oficiais, criei a task dedicada `10-vivaldi.yaml`:

```yaml
- name: Baixa chave pública de assinatura do repositório Vivaldi
  ansible.builtin.get_url:
    url: https://repo.vivaldi.com/stable/linux_signing_key.pub
    dest: /etc/apt/keyrings/vivaldi-browser.asc
    mode: '0644'
    owner: root
    group: root

- name: Configura repositório APT oficial do Vivaldi
  ansible.builtin.copy:
    dest: /etc/apt/sources.list.d/vivaldi.sources
    content: |
      Types: deb
      URIs: https://repo.vivaldi.com/stable/deb/
      Suites: stable
      Components: main
      Architectures: amd64
      Signed-By: /etc/apt/keyrings/vivaldi-browser.asc
    mode: '0644'
    owner: root
    group: root
  register: vivaldi_repo

- name: Instala o navegador Vivaldi
  ansible.builtin.apt:
    name: vivaldi-stable
    state: present
    update_cache: "{{ vivaldi_repo.changed }}"
```
*Configuração do repositório oficial Vivaldi utilizando o padrão deb822 nativo do Debian moderno.*

Repare na sutileza do parâmetro `update_cache: "{{ vivaldi_repo.changed }}"`: se a definição do repositório não mudou desde a última execução, o Ansible não perde tempo fazendo requisições de rede para atualizar o cache do apt. Ele vai direto ao ponto.

## A saga dos AppImages e o fantasma do libfuse2t64

Outro componente indispensável no meu fluxo diário de trabalho é o **pCloud Drive**. Eu uso o pCloud porque ele monta uma unidade virtual no sistema de arquivos: tenho acesso aos meus arquivos na nuvem sem precisar torrar o espaço do meu SSD local.

No Linux, a pCloud distribui seu cliente oficial no formato **AppImage**. E aqui entra uma decisão arquitetural alinhada à minha regra de isolamento: vale a pena descompactar um AppImage, tentar extrair bibliotecas internas e empacotar um `.deb` no braço para colocar no sistema?

De jeito nenhum. Um AppImage foi desenhado especificamente para ser um executável auto-contido que vive no espaço do usuário. O próprio cliente pCloud possui rotinas internas de auto-atualização em segundo plano. Se você tentar empacotar o software de forma estática no sistema operacional, você quebra o mecanismo nativo de atualização dele.

Minha abordagem foi mantê-lo exatamente onde deve estar: baixado no meu usuário (`~/.local/share/pcloud/pcloud.AppImage`), com um atalho no meu `~/.local/bin` e um lançador `.desktop` no menu do GNOME.

Só que no Debian 13 (Trixie), essa tarefa simples me reservou uma surpresa desagradável.

Baixei o AppImage, dei permissão de execução, tentei rodar no terminal e tomei um erro seco na cara:

```
error while loading shared libraries: libfuse.so.2: cannot open shared object file: No such file or directory
```

Em qualquer distribuição antiga ou no Debian 12, a reação mecânica de qualquer usuário seria rodar `sudo apt install libfuse2`.
Fui todo confiante rodar o comando e o Debian 13 respondeu friamente:
`E: O pacote 'libfuse2' não tem candidato para instalação`.

Fiquei alguns segundos olhando para a tela pensando o que diabos tinha acontecido.

A explicação para isso é fascinante: o projeto Debian passou recentemente pela monumental transição do **ano 2038** (a famosa migração do tipo `time_t` de 32 bits para 64 bits em arquiteturas de hardware) [^5]. Para evitar quebra de compatibilidade binária entre bibliotecas compiladas antes e depois da transição, dezenas de pacotes receberam o sufixo `t64`. O pacote do FUSE clássico no Debian 13 chama-se oficialmente **`libfuse2t64`**.

Com essa dependência resolvida na base do sistema, a task `08-pcloud.yaml` opera com total previsibilidade:

```yaml
- name: Garante diretórios de suporte ao pCloud
  ansible.builtin.file:
    path: "{{ item }}"
    state: directory
    mode: '0755'
  loop:
    - "{{ pcloud_dir }}"
    - "{{ pcloud_bin_dir }}"
    - "{{ pcloud_desktop_dir }}"

- name: Verifica se o pCloud AppImage já está instalado
  ansible.builtin.stat:
    path: "{{ pcloud_dir }}/pcloud.AppImage"
  register: pcloud_installed_stat

- name: Copia pCloud AppImage de Downloads se disponível
  ansible.builtin.copy:
    src: "{{ ansible_env.HOME }}/Downloads/pCloud.AppImage"
    dest: "{{ pcloud_dir }}/pcloud.AppImage"
    mode: '0755'
  when:
    - not pcloud_installed_stat.stat.exists
    - pcloud_downloaded_stat.stat.exists | default(false)
```
*Módulo pCloud respeitando instalações prévias e evitando downloads redundantes.*

O playbook confere se o executável já existe no meu home. Se existir, não mexe em nada para não sobrescrever atualizações que o próprio aplicativo já tenha baixado sozinho. Se eu já tiver colocado o instalador na pasta de Downloads, ele reaproveita o arquivo local. Se não houver nada, ele consulta a API pública de distribuição da pCloud e baixa o binário oficial automaticamente. Em seguida, extrai o ícone embutido do próprio AppImage com `--appimage-extract pcloud.png` e gera o lançador `.desktop` no menu de aplicativos.

Zero atrito. Uma vez rodado, nunca mais precisei pensar nisso.

## Desabafos de bastidor: quando a arquitetura quebra na prática

Em artigos técnicos de internet, tudo parece sempre nascer pronto, límpido e funcionando na primeira tentativa. Você lê a documentação alheia e parece que o autor sentou na cadeira, datilografou duzentas linhas de código com a iluminação de um monge e tudo funcionou de primeira com zero erros.

Mentira deslavada. A vida real de quem mexe com automação é cheia de tropeços bobos, erros de julgamento e momentos em que você olha para o terminal com cara de tacho.

Vou contar exatamente o que aconteceu durante a construção dessa versão do playbook.

Eu decidi que queria adicionar dois novos aplicativos à minha máquina: o navegador Vivaldi e a VPN do Tailscale. Como o Tailscale é distribuído através de repositórios externos, pensei com a minha pressa habitual: "Ah, o Tailscale tem repositório no extrepo, então vou colocar a instalação dele, a chave do Vivaldi e o serviço do systemd tudo junto dentro de `01-extrepo.yaml`".

Fiz a alteração correndo, salvei o arquivo e mandei executar o playbook.

Resultado? Um erro vermelho gritante bem na minha cara logo no comecinho do processo, na task `00-base.yaml`:

```
TASK [sistema : Habilita serviços de sistema] *********************************
failed: [localhost] (item=tailscaled.service) => {
  "changed": false,
  "msg": "Could not find the requested service tailscaled.service: host"
}
```

O erro era ridículo de óbvio: a lista `servicos_sistema` do meu módulo base tentava habilitar o `tailscaled.service` antes mesmo de o playbook ter chegado na etapa de habilitar o repositório no extrepo e instalar o pacote do Tailscale. O arquivo de serviço do systemd simplesmente não existia no disco da máquina naquele instante.

Minha primeira tentação foi o remendo clássico: tirar o serviço da base e colar a ativação dele no final do arquivo de extrepo.

Mas quando olhei para aquilo, bateu uma vergonha imediata.
Por que diabos um arquivo chamado `01-extrepo.yaml`, cuja única responsabilidade deveria ser gerenciar a ferramenta de repositórios do Debian, estava configurando navegador com chave GPG manual e gerenciando ciclo de vida de daemons de VPN? Que gambiarra era essa na minha própria casa?

Parei, respirei fundo e decidi fazer a coisa certa: dar um passo atrás e aplicar o **Princípio da Responsabilidade Única** (falei bonito agora, obrigado de nada).

```
[ SISTEMA / TASKS / MAIN.YAML ]
      │
      ├──> 00-base.yaml           (Sistema base, timezone, UFW, Flatpak)
      ├──> 01-extrepo.yaml        (Apenas configuração e repositórios extrepo)
      ├──> 02-usuario.yaml        (Diretórios XDG, aliases, cron, PAM touch)
      ├──> 03-asdf.yaml           (Binário ASDF v0.20 em Go e shims)
      ├──> 04-asdf-shims.yaml     (Erlang/OTP 29 e Elixir 1.20)
      ├──> 05-sdkman.yaml         (Java Temurin 26 e Maven 3.9)
      ├──> 06-virtualizacao-containers.yaml (Docker CE, KVM/Libvirt, Vagrant e plugins)
      ├──> 07-antigravity.yaml    (Google Antigravity Standalone e IDE)
      ├──> 08-pcloud.yaml         (pCloud Drive AppImage e FUSE)
      ├──> 09-tailscale.yaml      (Habilitação, pacote e serviço do Tailscale)
      ├──> 10-vivaldi.yaml        (Chave GPG, deb822 e navegador Vivaldi)
      └──> 99-gnome-extensions.yaml (gext silencioso, dconf e wallpaper)
```

Cada ferramenta ganhou seu próprio módulo desacoplado:
* O `01-extrepo.yaml` voltou a ser puramente focado em habilitar os repositórios curados pelo Debian.
* O Tailscale ganhou o arquivo `09-tailscale.yaml`, cuidando de habilitar seu repositório no extrepo, instalar o pacote e iniciar o serviço na sequência temporal correta.
* O Vivaldi ganhou o arquivo `10-vivaldi.yaml`, isolado com suas próprias chaves e sources deb822.
* E para o Tailscale no desktop, adicionei a interface gráfica com o **Trayscale** (`dev.deedles.Trayscale`), instalado nativamente via Flathub com suporte a GTK4 e Libadwaita no GNOME.

Com isso, ganhei algo essencial para o meu dia a dia: isolamento de execução via tags do Ansible. Se amanhã eu quiser reconfigurar apenas a VPN, rodo `./bootstrap.sh --tags tailscale`. Se quiser atualizar os navegadores, rodo `./bootstrap.sh --tags vivaldi`. Sem precisar rodar o playbook inteiro e sem efeitos colaterais em outras partes da máquina.

## Runtimes sem drama: minha máquina não é lixeira de dependências

Se tem uma coisa que aprendi nas minhas décadas usando Linux é: **nunca instale runtimes de desenvolvimento pelo gerenciador de pacotes do sistema operacional**.

Instalar versões de Java, Node.js, Erlang ou Elixir através do `apt` é pedir para ter dor de cabeça no futuro. O empacotamento da distribuição costuma travar em versões específicas que raramente coincidem com os requisitos dos projetos em que você trabalha. Além disso, quando você precisa alternar entre duas versões de uma mesma linguagem em repositórios diferentes, o sistema operacional vira um emaranhado de links quebrados no `/usr/bin`.

Seguindo a minha filosofia de manter o Debian limpo, dividi os runtimes em ecossistemas isolados estritamente no meu espaço de usuário:

### ASDF em Go para Erlang e Elixir
Historicamente, o ASDF era um conjunto massivo de scripts em Bash que adicionava uma lentidão perceptível a cada abertura de terminal. A partir da versão `v0.20.0`, o projeto foi reescrito integralmente em **Go** [^6]. O executável agora é um binário único, compilado e muito rápido.

O playbook baixa o binário diretamente em `~/.local/bin/asdf`, configura os plugins necessários e compila o **Erlang/OTP 29** com suporte completo a bibliotecas gráficas (wxWidgets) e segurança (OpenSSL). Na sequência, instala o binário oficial pré-compilado do **Elixir 1.20** casado com o OTP 29 e ativa as versões globais via `~/.tool-versions`.

Para garantir que o Ansible não perca tempo tentando recompilar linguagens que já estão presentes no sistema, a task inspeciona o disco previamente com `ansible.builtin.stat`. Se a versão já existe dentro de `~/.asdf/installs/erlang/29.0.6`, a etapa de compilação é ignorada sem pestanejar.

### SDKMAN para o ecossistema Java
Embora o ASDF possua plugins para Java, o **SDKMAN!** [^7] continua sendo a minha escolha definitiva no ecossistema Java. Ele gerencia versões do OpenJDK de todos os fornecedores (Temurin, GraalVM, Corretto, Zulu) e utilitários de build de forma nativa e transparente.

A task `05-sdkman.yaml` instala o SDKMAN! no meu perfil de usuário e provisiona automaticamente:
* **Java:** Eclipse Temurin OpenJDK 26 (`26-tem`).
* **Maven:** Apache Maven estável (`3.9.16`).

Ambos ficam imediatamente disponíveis no PATH do shell e configurados como padrões do meu ambiente, sem encostar um único arquivo dentro de `/usr`.

### Ferramentas isoladas no Docker: TensorFlow e PlantUML
Instalar pacotes de aprendizado de máquina e bibliotecas de tensores diretamente no Python do sistema operacional é a receita perfeita para o desastre. Pilhas gigantescas de dependências, versões concorrentes de CUDA, drivers de compilação cruzada e gigabytes de dados que nunca mais saem do disco.

A mesma dor se repete quando preciso desenhar diagramas de arquitetura com o **PlantUML**. Para rodar o PlantUML de forma nativa, você precisa instalar Graphviz no sistema operacional, bibliotecas gráficas do Java, fontes e um punhado de pacotes auxiliares. Para que sujar o Debian com ferramentas que só uso pontualmente?

Em vez de instalar o TensorFlow ou servidores de diagramação na minha máquina física, criei atalhos simples no meu `~/.bash_aliases`:

```bash
# Ambiente interativo de Machine Learning
alias tensor="docker run -it --rm -p 8888:8888 -v $HOME/du/dev/tensor:/tf/notebooks tensorflow/tensorflow:latest-jupyter"

# Servidor local do PlantUML para diagramação
alias plantuml="docker run -it --rm -p 8080:8080 plantuml/plantuml-server:jetty"
```
*Execução isolada de Jupyter/TensorFlow e servidor PlantUML via Docker mantendo o host limpo.*

Repare em dois detalhes deliberados nesses comandos:
1. **Sem modo daemon (`-d`):** os comandos rodam com `-it` para manter o terminal ocupado com a execução ativa em primeiro plano. Nada de serviços fantasmas rodando em segundo plano sem eu perceber. Se a ferramenta está aberta, ela prende o terminal e eu acompanho os logs em tempo real.
2. **Limpeza atômica pós-execução (`--rm`):** nada de dezenas de contêineres parados acumulando lixo invisível no `docker ps -a`. Quando termino de trabalhar e mando um `Ctrl+C` (`^C`), o contêiner morre e é imediatamente destruído pelo Docker.

No caso do `tensor`, o contêiner expõe o Jupyter na porta 8888 e persiste os notebooks dentro de `~/du/dev/tensor`. No caso do `plantuml`, tenho um servidor oficial Jetty pronto na porta 8080 para gerar meus diagramas no navegador ou integrar com extensões do editor. Deu `^C`, o terminal fecha e a máquina continua 100% limpa.

> [!TIP] Aceleração por Hardware no Docker
> O alias padrão do TensorFlow roda com eficiência máxima na CPU. Caso você vá executar em uma máquina com placa de vídeo dedicada, não instale nada no Python do sistema: basta instalar o driver de vídeo do fabricante e repassar os dispositivos correspondentes para o Docker:
> * **NVIDIA:** instale o pacote `nvidia-container-toolkit` no host e adicione a flag `--gpus all` usando a imagem `tensorflow/tensorflow:latest-gpu-jupyter`.
> * **AMD Radeon:** garanta o driver `amdgpu` e adicione as flags `--device=/dev/kfd --device=/dev/dri --group-add video` usando a imagem `rocm/tensorflow:latest`.
> * **Intel Arc / Xe:** instale as bibliotecas de computação Level Zero e passe `--device=/dev/dri` com a imagem oficial da Intel.

## A domação do GNOME 48: extensões silenciosas e dconf atômico

Chegamos à parte que costuma consumir a maior quantidade de horas de qualquer um que tente automatizar um desktop Linux: a interface gráfica e o gerenciador de janelas.

O GNOME moderno é fantástico em termos de usabilidade, mas a instalação de extensões sempre foi um calcanhar de aquiles. Historicamente, você precisava abrir o navegador, instalar um conector de browser, entrar no site extensions.gnome.org e clicar em botões de ativar um por um. Scripts de automação antigos tentavam fazer scraping do site ou usar APIs instáveis que quebravam a cada lançamento semestral do GNOME Shell.

Para o Debian 13 rodando GNOME 48, adotei uma ferramenta fantástica chamada **`gnome-extensions-cli` (`gext`)** [^8], instalada via `pipx` no meu usuário.

O `gext` possui um backend de instalação direta chamado `--filesystem`. Em vez de tentar se comunicar com o barramento gráfico do GNOME na tela (o que quase sempre falha ou trava quando executado por ferramentas de automação como o Ansible), o utilitário baixa o pacote oficial da extensão, valida a compatibilidade com a versão do GNOME Shell, extrai os arquivos diretamente em `~/.local/share/gnome-shell/extensions/<UUID>` e compila os esquemas do GSettings com `glib-compile-schemas`.

```yaml
- name: Instala extensões GNOME via gext com backend de sistema de arquivos
  ansible.builtin.command:
    cmd: "gext --filesystem install {{ item.id }}"
  loop: "{{ extensoes_gnome }}"
  loop_control:
    label: "{{ item.nome }}"
  when: not gext_check.stat.exists
  changed_when: true
```
*Instalação silenciosa de extensões em lote sem janelas piscando na tela.*

Com esse comando, o playbook provisiona silenciosamente doze extensões essenciais para o meu fluxo de trabalho:
1. **Dash to Panel:** unifica a barra superior e o dock em uma única barra de tarefas inferior moderna.
2. **AppIndicator Support:** traz de volta os ícones de bandeja essenciais (como pCloud, Tailscale e mensageiros).
3. **Tiling Shell:** gerenciamento moderno de janelas em mosaico com zonas de encaixe magnéticas.
4. **Blur my Shell:** efeitos visuais translúcidos elegantes no shell e no painel.
5. **Burn my Windows:** transições suaves de abertura e fechamento de janelas.
6. **Caffeine:** botão rápido para impedir que o computador suspenda durante tarefas longas.
7. **Fly-Pie:** menu radial de atalhos acionado pelo mouse para máxima velocidade.
8. **Clipboard Indicator, Custom Hot Corners, No Overview, Wallpaper Switcher e Window Is Ready Remover.**

### O golpe de mestre: restauração atômica via dconf
Instalar a extensão é apenas cinquenta por cento do caminho. A outra metade, muito mais dolorosa, é configurar os parâmetros internos de cada uma delas, além dos atalhos de teclado do próprio GNOME.

Eu não quero ter que abrir o aplicativo de extensões para configurar a altura do Dash to Panel, definir que o `Alt+Tab` deve alternar apenas entre janelas do workspace atual ou reconfigurar atalhos de maximização (`Super+Up`).

A solução definitiva para isso é o **dconf**. Todas as configurações do GNOME e das extensões ficam armazenadas no banco de dados binário do GSettings. O que fiz foi exportar a árvore completa de configurações do meu ambiente ideal para um template Jinja2 parametrizado chamado `gnome-desktop.dconf.j2`.

{% raw %}
```yaml
- name: Aplica template com todas as configurações do GNOME e Extensões
  ansible.builtin.template:
    src: gnome-desktop.dconf.j2
    dest: "{{ ansible_env.HOME }}/.config/gnome-desktop.dconf"
    mode: '0644'
  register: dconf_template_res

- name: Carrega configurações atômicas no dconf
  ansible.builtin.command:
    cmd: dconf load /
    stdin: "{{ lookup('file', ansible_env.HOME ~ '/.config/gnome-desktop.dconf') }}"
  when: dconf_template_res.changed
```
{% endraw %}
*Restauração instantânea de centenas de preferências de janelas, atalhos e extensões.*

Em vez de disparar dezenas de comandos `gsettings set` que levam minutos para executar e deixam o terminal lento, o comando `dconf load /` lê o arquivo gerado pelo template e injeta o estado completo do desktop em menos de cem milissegundos.

E a cereja no topo do bolo: para garantir que qualquer ajuste fino feito no dia a dia não se perca, criei um utilitário em Bash chamado `salvar-extensoes` em `~/.local/bin/salvar-extensoes`. Se eu mexer nas cores do painel ou trocar um atalho de teclado no futuro, basta rodar esse comando no terminal: ele extrai o estado atual do `dconf` e salva cópias carimbadas com data e hora dentro de `~/du/conf/`.

Para finalizar a personalização visual com um toque nostálgico, o playbook armazena e aplica automaticamente o lendário papel de parede **Bliss** do Windows XP, renderizado a partir de uma digitalização em altíssima definição de 600 DPI, sincronizado simultaneamente para os modos claro e escuro do GNOME 48.

## A obsessão pela idempotência no dia a dia

Um dos maiores erros ao escrever automações no Ansible é achar que a ferramenta é magicamente idempotente por padrão só porque você usou módulos oficiais.

Idempotência real significa o seguinte: na primeira vez em que você executa o playbook numa máquina zerada, ele baixa pacotes, cria diretórios, configura serviços e leva quinze minutos para concluir. Na segunda vez consecutiva que você aperta Enter no mesmo comando, ele deve rodar em dez segundos, conferir que tudo já está no estado desejado e devolver um resumo com zero alterações (`changed=0`).

Para atingir esse nível de confiança operacional, passei por um processo minucioso de auditoria em cada arquivo de task:

* **Eliminação de loops no apt:** tarefas antigas costumavam iterar com `loop: "{{ pacotes }}"` chamando o módulo `ansible.builtin.apt` vinte vezes seguidas. Consolidei isso em chamadas únicas passando a lista completa de pacotes (`name: "{{ pacotes }}"`), reduzindo o tempo de verificação de pacotes em mais de oitenta por cento.
* **Checagem de comandos de sistema:** comandos como a sincronização de hora (`timedatectl set-ntp true`) só disparam se a consulta prévia de status indicar que o NTP não está ativo.
* **Tratamento de arquivos de configuração:** no arquivo `~/.bash_aliases`, a expressão regular do módulo `lineinfile` foi calibrada para casar com exatidão a chave do alias antes do sinal de igual (`^alias {% raw %}{{ item.split('=')[0] }}{% endraw %}=`). Se eu rodar o playbook cem vezes seguidas, ele jamais duplicará uma única linha no meu arquivo de aliases.
* **Separação estrita de precedência de variáveis:** todas as variáveis que tenho interesse em customizar (versões de linguagens, listas de pacotes extras, preferências de extensões) foram centralizadas em `sistema/defaults/main.yaml` (nível 2 de precedência no Ansible) [^9]. Já os caminhos internos de infraestrutura e diretórios imutáveis vivem protegidos em `sistema/vars/main.yaml` (nível 16).

O resultado prático é um playbook tão confiável que não o utilizo apenas quando formato a máquina: posso colocá-lo para rodar periodicamente ou após atualizações de sistema para garantir que nenhuma configuração saiu do lugar.

## O poder da máquina descartável

No final do dia, construir uma automação desse porte vai muito além de economizar cliques do mouse. Trata-se de uma mudança fundamental de postura: a tranquilidade psicológica de transformar o seu computador de trabalho em uma peça de infraestrutura descartável.

Se o meu laptop cair no chão hoje ou o SSD sofrer uma falha catastrófica, o impacto no meu trabalho é praticamente zero. Eu pego outra máquina, instalo um Debian básico com partição criptografada, clono o repositório, executo `./bootstrap.sh` e vou tomar um café.

Quando retorno, meu terminal está configurado com ferramentas modernas (`eza`, `btop`, `tailspin`, `fzf`), o firewall e o OpenSSH estão ativos com regras restritivas, os contêineres Docker e o ambiente de virtualização KVM estão operacionais, o Java 26 e o Elixir 1.20 estão prontos para compilar código, o pCloud e o Tailscale estão sincronizando e as minhas doze extensões do GNOME 48 estão exatamente nas mesmas posições de tela de sempre.

Se você também já passou pela fase de compilar distros no braço e hoje só quer paz de espírito e estabilidade, recomendo fortemente fazer o mesmo exercício. Dá trabalho construir a primeira vez? Dá um trabalhão tremendo. Mas a sensação de ver o terminal subir o seu ambiente de trabalho perfeito do zero com um único comando é uma das coisas mais gratificantes que a cultura DevOps pode proporcionar.

---

## Referências

[^1]: **PEP 668 – Marking Python base environments as "externally managed"** {*Python Software Foundation*} ([Link](https://peps.python.org/pep-0668/))
[^2]: **pipx - Install and Run Python Applications in Isolated Environments** {*Python Packaging Authority*} ([Link](https://pipx.pypa.io/))
[^3]: **extrepo - External repository manager for Debian** {*Debian Wiki*} ([Link](https://wiki.debian.org/ExtRepo))
[^4]: **Debian SourcesList Format: deb822 style** {*Debian Manpages*} ([Link](https://manpages.debian.org/sources.list.5))
[^5]: **Debian 64-bit time_t transition guide and release notes** {*Debian Wiki*} ([Link](https://wiki.debian.org/ReleaseGoals/64bit_time))
[^6]: **ASDF Version Manager: Modern Go Implementation** {*ASDF Community*} ([Link](https://asdf-vm.com/))
[^7]: **SDKMAN! The Software Development Kit Manager** {*SDKMAN! Team*} ([Link](https://sdkman.io/))
[^8]: **gnome-extensions-cli (gext)** {*GitHub Repository*} ([Link](https://github.com/essembeh/gnome-extensions-cli))
[^9]: **Ansible Variable Precedence: Where Should I Put A Variable?** {*Ansible Documentation*} ([Link](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html#understanding-variable-precedence))

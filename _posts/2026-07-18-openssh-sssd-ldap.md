---
layout: post
title: "OpenSSH + SSSD: Integrando autenticação LDAP ao SSH"
subtitle: "Centralizando usuários, grupos e chaves públicas com Debian Trixie sem gambiarras locais"
author:
  - "Eduardo N. S. R."
date: 2026-07-18 21:57:00 GMT-3
permalink: /posts/openssh-sssd-ldap/
tags: [SSH, SSSD, LDAP, Debian]
series: OpenSSH na Prática
---

No post anterior sobre Certificados SSH, encerramos com uma confissão honesta: certificados resolvem brilhantemente a **autenticação** e a **autorização** na camada do protocolo, mas não criam contas de usuário no sistema operacional por mágica. Você ainda precisava de "algo" para garantir que as role accounts (`deploy`, `db_admin`, `db_readonly`) existissem no `/etc/passwd` de cada servidor. Naquele momento, eu mencionei "LDAP/SSSD" quase como um feitiço sussurrado no final da frase, prometendo que o assunto renderia um post dedicado.

Pois bem. Cá estamos.

Hoje vamos resolver a outra metade do quebra-cabeça: como fazer o sistema operacional **reconhecer usuários e chaves públicas vindos de um diretório central (LDAP)**, sem precisar criar contas locais manualmente em cada servidor, sem manter arquivos `authorized_keys` espalhados como migalhas de pão pelo data center, e (o melhor de tudo) sem instalar gambiarras de scripts caseiros que ninguém entende seis meses depois.

A ferramenta que vai costurar tudo isso é o **SSSD (System Security Services Daemon)** [^1], o leão de chácara do Linux moderno para autenticação centralizada. E como cenário, vamos usar o **Debian 13 (Trixie)**, que traz o SSSD na versão **2.10.x** nos repositórios oficiais [^2].

Se o post anterior era sobre criar a "carteira de identidade criptográfica" (certificados) dos seus usuários, este é sobre colocar o "porteiro biométrico" na entrada de cada servidor: um porteiro que consulta a base central de identidades em tempo real e já sabe de antemão qual é a chave pública de cada pessoa.

## O cenário: onde paramos e para onde vamos

Recapitulando rapidamente o que já tínhamos configurado:

1. Uma **CA de Host** e uma **CA de Usuário** (ambas ED25519) assinando certificados.
2. Servidores configurados com `TrustedUserCAKeys` e `AuthorizedPrincipalsFile` no `sshd_config`.
3. **Role accounts** locais (`deploy`, `db_admin`, `db_readonly`) criadas manualmente via `useradd` em cada servidor.
4. Principals mapeados nos certificados dos usuários para controle de acesso RBAC.

O ponto 3 é onde dói. Aquela dor de quem tem 5 servidores e precisa garantir que a conta `deploy` exista em todos, com o mesmo UID, o mesmo shell, o mesmo GID. Agora multiplique por 50 servidores. Ou 500. O Ansible resolve até certo ponto, mas você acaba com centenas de linhas de playbook dedicadas a gerenciar algo que deveria ser um *lookup* trivial numa base centralizada.

E o ponto que nem tocamos no post anterior: **chaves públicas**. No modelo de certificados, a CA assina a chave do usuário e pronto. Mas em cenários híbridos (quando a empresa tem desenvolvedores que ainda usam chaves públicas nuas, ou quando você precisa de uma segunda camada de autenticação além do certificado), manter essas chaves espalhadas em arquivos `authorized_keys` é uma receita para o caos.

É aqui que o SSSD entra como a peça que faltava no tabuleiro.

## O que é o SSSD e por que ele existe?

O SSSD não é apenas "mais um cliente LDAP". Ele é um **daemon de sistema** [^1] que abstrai completamente a comunicação com provedores de identidade remotos (LDAP, Active Directory, FreeIPA, Kerberos) e expõe essas identidades para o sistema operacional através de duas interfaces fundamentais:

- **NSS (Name Service Switch):** Permite que comandos como `getent passwd`, `id`, `ls -la` resolvam nomes de usuários e grupos que não existem no `/etc/passwd` local. Para o kernel e os programas, é como se o usuário fosse local. Transparente. Invisível.
- **PAM (Pluggable Authentication Modules):** Permite que o processo de login (seja via SSH, console, `su`, ou qualquer outra porta de entrada) valide a senha do usuário contra o diretório remoto, sem precisar de senhas locais no `/etc/shadow`.

O SSSD faz tudo isso com **cache local** inteligente: se o servidor LDAP cair (porque servidores LDAP adoram cair na sexta-feira às 18h), os usuários que já logaram recentemente continuam acessando normalmente, graças a credenciais cacheadas localmente no banco de dados do SSSD (`/var/lib/sss/db/`).

> 💡 *Curiosidade*: O SSSD nasceu como um projeto da Red Hat/Fedora, mas hoje é mantido como projeto upstream independente [^3] e está presente nos repositórios de praticamente todas as distribuições Linux relevantes. No Debian 13 (Trixie), o metapacote `sssd` puxa automaticamente os módulos para NSS (`sssd-common`), PAM (`libpam-sss`) e o provedor LDAP (`sssd-ldap`).

Mas a cereja no topo do bolo para o nosso contexto é uma feature que pouca gente conhece: o SSSD pode **armazenar e servir chaves públicas SSH diretamente do LDAP** para o OpenSSH, usando um utilitário chamado `sss_ssh_authorizedkeys` [^4]. É isso que vamos explorar a fundo.

## Pré-requisito: O LDAP precisa conhecer chaves SSH

Antes de mexer em qualquer configuração do lado do servidor, precisamos garantir que o diretório LDAP saiba armazenar chaves públicas SSH nos registros dos usuários. Isso não é nativo do esquema padrão LDAP (RFC 4519) [^5], e você precisa de um esquema customizado.

O esquema mais usado pela comunidade é o **openssh-lpk (LDAP Public Key)**, que define:

- Um **objectClass auxiliar** chamado `ldapPublicKey`.
- Um **atributo** chamado `sshPublicKey`, que armazena a chave pública no formato OpenSSH (aquela string `ssh-ed25519 AAAAC3NzaC1...`).

Na prática, o LDIF para adicionar o esquema no OpenLDAP (o servidor LDAP de referência do Debian) é algo assim:

```ldif
dn: cn=openssh-lpk,cn=schema,cn=config
objectClass: olcSchemaConfig
cn: openssh-lpk
olcAttributeTypes: ( 1.3.6.1.4.1.24552.500.1.1.1.13
  NAME 'sshPublicKey'
  DESC 'OpenSSH Public Key'
  EQUALITY octetStringMatch
  SYNTAX 1.3.6.1.4.1.1466.115.121.1.40 )
olcObjectClasses: ( 1.3.6.1.4.1.24552.500.1.1.2.0
  NAME 'ldapPublicKey'
  DESC 'OpenSSH LPK objectclass'
  SUP top AUXILIARY
  MAY ( sshPublicKey ) )
```

*Esquema LDIF que define o atributo `sshPublicKey` e a classe auxiliar `ldapPublicKey` para o OpenLDAP.*

> 💡 *Nota*: Se você está usando FreeIPA ou 389 Directory Server em vez de OpenLDAP, o suporte a chaves SSH já vem embutido nativamente. O FreeIPA, na verdade, é tão gentil que até oferece uma interface web para colar a chave pública do usuário. Luxo.

Com o esquema carregado, uma entrada de usuário no LDAP ficaria assim:

```ldif
dn: uid=joao,ou=people,dc=example,dc=com
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: ldapPublicKey
uid: joao
cn: João da Silva
uidNumber: 10001
gidNumber: 10001
homeDirectory: /home/joao
loginShell: /bin/bash
sshPublicKey: ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... joao@example.com
```

*Registro LDIF de usuário contendo atributo de chave pública SSH para consultas.*

Repare que o campo `sshPublicKey` é **multi-valorado**: o João pode ter duas, três, dez chaves cadastradas no mesmo registro. Isso é importante para quem usa chaves diferentes em máquinas diferentes (notebook pessoal, estação de trabalho, YubiKey).

## Instalação no Debian 13 (Trixie)

Hora de sujar as mãos. No Debian 13, a instalação é deliciosamente simples:

```bash
$ sudo apt update
$ sudo apt install sssd sssd-ldap libpam-sss libnss-sss
```

*Instala o daemon do SSSD, seu módulo LDAP e os drivers de integração com PAM e NSS.*

Dissecando os pacotes:

- `sssd`: O metapacote principal, que arrasta o daemon e as dependências comuns.
- `sssd-ldap`: O módulo provedor de identidade via LDAP. Sem ele, o SSSD não sabe falar com o seu diretório.
- `libpam-sss`: O módulo PAM que conecta o subsistema de autenticação do Linux ao SSSD.
- `libnss-sss`: A biblioteca NSS que faz o `getent passwd` e amigos enxergarem os usuários do LDAP.

> ⚠️ *Importante*: Não confunda `libnss-sss` com o antigo `libnss-ldapd` (e seu daemon `nslcd`). O `libnss-ldapd` consulta o LDAP diretamente, sem cache inteligente, sem failover automático, sem integração com PAM. É a abordagem "à moda antiga". O SSSD substitui tudo isso com um daemon unificado, cache local, e gerenciamento de credenciais offline. Se você ainda está usando `nslcd` em 2026, eu respeitosamente sugiro que reconsidere suas escolhas de vida.

## Configurando o `/etc/sssd/sssd.conf`

Este é o coração da operação. O arquivo `/etc/sssd/sssd.conf` é onde você define quais serviços o SSSD vai prover, e como ele se conecta ao seu provedor de identidade. Ele **precisa** ter permissões `0600` (leitura/escrita apenas pelo `root`), caso contrário o SSSD se recusa a iniciar. E com razão, pois o arquivo pode conter credenciais de *bind* do LDAP.

```bash
$ sudo touch /etc/sssd/sssd.conf
$ sudo chmod 0600 /etc/sssd/sssd.conf
```

*Cria o arquivo de configuração do SSSD com permissões restritas exclusivas de root.*

E aqui vai a configuração completa para o nosso cenário. Leia cada seção com calma, porque cada linha tem uma razão de existir:

```ini
[sssd]
config_file_version = 2
services = nss, pam, ssh
domains = example.com

[nss]
filter_users = root,daemon,bin,sys,nobody
filter_groups = root,daemon,bin,sys,nogroup

[pam]

[ssh]

[domain/example.com]
# Provedor de identidade e autenticação
id_provider = ldap
auth_provider = ldap
access_provider = ldap

# Conexão com o servidor LDAP
ldap_uri = ldaps://ldap.example.com
ldap_search_base = dc=example,dc=com

# Credenciais de bind (conta de serviço para leitura)
ldap_default_bind_dn = cn=readonly,dc=example,dc=com
ldap_default_authtok_type = password
ldap_default_authtok = S3nh@MuitoSegura!

# Segurança TLS
ldap_tls_cacert = /etc/ssl/certs/ca-certificates.crt

# Cache de credenciais (sobrevivência offline)
cache_credentials = true
entry_cache_timeout = 300

# Mapeamento de chaves SSH via LDAP
ldap_user_ssh_public_key = sshPublicKey

# Home directory: a abordagem moderna (sem /home local)
override_homedir = /tmp/%u
default_shell = /bin/bash

# Controle de acesso: apenas usuários com shell válido
ldap_access_filter = (loginShell=/bin/bash)
```

*Configuração completa do SSSD cobrindo serviços NSS, PAM e SSH com cache e conexão TLS.*

Vamos dissecar as partes mais interessantes:

### A seção `[sssd]`

```ini
services = nss, pam, ssh
```

*Habilita os serviços NSS para nomes, PAM para autenticação e SSH para resolução de chaves públicas.*

Três serviços habilitados:
- **nss**: Resolução de nomes (faz o `getent passwd joao` funcionar).
- **pam**: Autenticação de senhas contra o LDAP.
- **ssh**: A feature que nos interessa. Habilita o responder de chaves SSH, permitindo que o utilitário `sss_ssh_authorizedkeys` consulte o atributo `sshPublicKey` do LDAP.

### A seção `[nss]` e o `filter_users`

```ini
filter_users = root,daemon,bin,sys,nobody
filter_groups = root,daemon,bin,sys,nogroup
```

*Garante que contas nativas do sistema nunca gerem requisições lentas ou timeouts ao LDAP.*

Isso diz ao SSSD: *"Nunca tente resolver esses usuários/grupos no LDAP"*. Parece inocente, mas é uma proteção crítica. Sem isso, toda vez que o sistema chamar `getent passwd root`, o SSSD vai perder tempo fazendo um round-trip inútil até o LDAP procurando um `root` que só existe localmente. No melhor caso, isso é lento. No pior caso (se o LDAP estiver fora), o login do `root` local pode travar por timeout. Ninguém quer ficar trancado para fora do próprio servidor esperando o LDAP responder.

### A seção `[domain/example.com]`

**`ldap_uri = ldaps://ldap.example.com`**: Note o protocolo `ldaps://` (LDAP sobre TLS implícito, porta 636). Se o seu LDAP usa StartTLS na porta 389, substitua por `ldap://` e adicione `ldap_id_use_start_tls = true`. Em 2026, se o seu LDAP não está criptografado, pare tudo o que está fazendo e vá corrigir isso agora.

**`ldap_user_ssh_public_key = sshPublicKey`**: Essa é a diretiva mágica [^6]. Ela diz ao SSSD: *"Quando alguém pedir a chave SSH de um usuário, procure no atributo LDAP chamado `sshPublicKey`"*. O valor padrão já é `sshPublicKey`, mas eu recomendo ser explícito. Configuração implícita é o paraíso dos bugs silenciosos.

**`cache_credentials = true`**: Com isso, o SSSD armazena o hash das senhas localmente em `/var/lib/sss/db/`. Se o servidor LDAP cair, os usuários que já logaram continuam entrando. O cache expira conforme o `entry_cache_timeout` (300 segundos no nosso exemplo, ou 5 minutos). Encontrar o equilíbrio certo aqui é uma arte: tempo curto demais causa muitas consultas ao LDAP; tempo longo demais significa que uma senha recém-alterada ou um usuário recém-desabilitado no LDAP vai demorar para refletir nos servidores.

> 🚨 *Aviso Crítico de Segurança*: A senha de bind (`ldap_default_authtok`) fica em *plain text* dentro do `sssd.conf`. É por isso que a permissão `0600` é inegociável. A conta de bind deve ser uma conta **read-only** no LDAP, com o mínimo de privilégios possível. Ela só precisa ler atributos de usuário (`uid`, `uidNumber`, `gidNumber`, `sshPublicKey`, etc.). Nunca use a conta `cn=admin` para bind do SSSD. Se alguém comprometer o servidor e ler esse arquivo, o estrago com uma conta read-only é infinitamente menor.

## O truque elegante: `override_homedir = /tmp/%u`

Essa diretiva merece uma seção própria, porque ela desafia a intuição de qualquer sysadmin criado na era clássica do Linux.

A abordagem tradicional diz: *"Todo usuário precisa de um `/home/usuario` local com `~/.ssh/authorized_keys`, `~/.bashrc`, `~/.profile` e toda aquela parafernália"*. E para garantir que esse diretório exista no primeiro login, você habilitava o módulo PAM `pam_mkhomedir`, que cria o diretório automagicamente.

Mas em infraestruturas modernas (servidores efêmeros, containers, VMs descartáveis), **criar diretórios home persistentes é uma responsabilidade que você não quer ter**. O servidor pode ser destruído e recriado a qualquer momento. Nenhum dado deveria viver localmente.

A solução elegante:

```ini
override_homedir = /tmp/%u
```

*Substitui dinamicamente o diretório home para um caminho temporário `/tmp/usuario`.*

Isso faz o SSSD **ignorar** o atributo `homeDirectory` do LDAP (que provavelmente está apontando para `/home/joao`) e substituir por `/tmp/joao` em todos os servidores. O diretório `/tmp` já existe, é limpo automaticamente pelo sistema, e ninguém deveria guardar nada importante lá.

> 💡 *Nota*: O `%u` é um token que o SSSD expande para o nome do usuário. Existem outros tokens úteis: `%d` (nome do domínio), `%f` (FQDN do usuário), `%U` (UID numérico). A documentação completa está no `sssd.conf(5)` [^7].

"Mas Dudu, se o home directory do usuário é `/tmp/joao`, o SSH não vai procurar o `authorized_keys` nesse diretório?"

Excelente pergunta. E é exatamente por isso que no nosso setup nós **não usamos** `authorized_keys` de jeito nenhum. As chaves vêm direto do LDAP via `sss_ssh_authorizedkeys`. O diretório home pode ser `/tmp`, `/dev/null` ou a superfície de Marte, tanto faz. O SSH nem olha para ele, porque vamos configurá-lo para usar o `AuthorizedKeysCommand` no lugar.

E para cenários onde o diretório precisa existir de fato (porque algum programa teimoso insiste em escrever no `$HOME`), o Systemd moderno do Debian 13 já cuida disso: o serviço `systemd-tmpfiles` pode criar diretórios temporários com permissões corretas via configuração em `/etc/tmpfiles.d/`.

## Ajustando o `/etc/nsswitch.conf`

O NSS (Name Service Switch) é o mecanismo do glibc que define **onde** o sistema procura por informações de usuários, grupos, hostnames, etc. Sem configurar o NSS, o SSSD pode estar rodando perfeitamente, mas o sistema operacional não vai enxergar os usuários do LDAP.

Abra o `/etc/nsswitch.conf` e ajuste as três linhas que nos interessam:

```text
passwd:         files sss
group:          files sss
shadow:         files sss
```

*Configura a ordem de resolução do sistema operacional, buscando nos arquivos locais antes do SSSD.*

A **ordem importa** [^8]. `files` vem primeiro: o sistema sempre consulta `/etc/passwd`, `/etc/group` e `/etc/shadow` antes de ir ao SSSD. Isso garante que contas locais de sistema (`root`, `www-data`, `postgres`, `nobody`) sejam resolvidas instantaneamente, sem depender do LDAP. O `sss` só é consultado se o `files` não encontrar o usuário.

> ⚠️ *Importante*: A linha `shadow: files sss` é um pouco enganosa. O SSSD **não** expõe hashes de senha via NSS por segurança. O `getent shadow joao` provavelmente retornará um asterisco (`*`) ou nada para usuários LDAP. A autenticação real é feita pelo módulo PAM (`pam_sss.so`), não pelo NSS. A presença do `sss` na linha `shadow` serve mais para consistência e para que utilitários como `chage` não reclamem de "usuário inexistente".

Vamos verificar se está funcionando:

```bash
$ sudo systemctl restart sssd
$ getent passwd joao
joao:*:10001:10001:João da Silva:/tmp/joao:/bin/bash
```

*Reinicia o SSSD e valida a resolução do usuário joao via NSS.*

Se você viu essa saída, comemore discretamente. O SSSD acabou de consultar o LDAP, aplicou o `override_homedir` (repare no `/tmp/joao` em vez do `/home/joao` do LDAP), e devolveu a informação exatamente como se o João fosse um usuário local. O `id joao` também deve funcionar perfeitamente:

```bash
$ id joao
uid=10001(joao) gid=10001(joao) groups=10001(joao)
```

*Confirma que UID e GID foram carregados com sucesso do diretório central.*

Para o kernel do Linux, o `getent` e o `id`, o João é indistinguível de um usuário criado via `useradd`. É essa transparência que faz do SSSD uma ferramenta tão poderosa.

## Habilitando o PAM

Para que o login via SSH (e outros serviços) consiga autenticar senhas contra o LDAP, o módulo PAM do SSSD precisa estar ativado. No Debian, a forma canônica de fazer isso é com o `pam-auth-update`:

```bash
$ sudo pam-auth-update --enable sss
```

*Habilita a pilha do SSSD em todas as configurações comuns do PAM do sistema.*

Esse comando atualiza os arquivos em `/etc/pam.d/common-*` (`common-auth`, `common-account`, `common-session`, `common-password`) para incluir o módulo `pam_sss.so` na cadeia de autenticação.

Note que **não** vamos habilitar o `mkhomedir`:

```bash
# NÃO faça isso no nosso cenário:
# sudo pam-auth-update --enable mkhomedir
```

*Evitamos criar diretórios persistentes mantendo os ambientes de servidores desacoplados e efêmeros.*

Lembra do `override_homedir = /tmp/%u`? Criar diretórios home persistentes é exatamente o que estamos evitando. O `/tmp/joao` será criado sob demanda se necessário, ou simplesmente não existirá. E está tudo bem.

## A peça final: `AuthorizedKeysCommand` e o `sss_ssh_authorizedkeys`

Aqui é onde o OpenSSH encontra o SSSD e os dois dançam uma valsa elegante. No post sobre certificados, mencionei brevemente a diretiva `AuthorizedPrincipalsCommand` como forma avançada de consultar "quais principals são válidos" num LDAP. Agora vamos usar a irmã dela: **`AuthorizedKeysCommand`** [^9].

Essa diretiva do `sshd_config` diz ao servidor SSH: *"Em vez de procurar chaves públicas no arquivo `~/.ssh/authorized_keys`, execute este programa e use o que ele cuspir no stdout"*.

O programa que o SSSD fornece para isso é o `sss_ssh_authorizedkeys` [^4]. Ele recebe o nome de usuário como argumento, consulta o SSSD (que por sua vez consulta o cache ou o LDAP), e imprime as chaves no formato padrão `authorized_keys`.

No `/etc/ssh/sshd_config` dos seus servidores, adicione:

```text
AuthorizedKeysCommand /usr/bin/sss_ssh_authorizedkeys
AuthorizedKeysCommandUser nobody
```

*Configura o sshd para consultar chaves públicas remotas invocando o comando do SSSD como nobody.*

Dissecando:

- **`AuthorizedKeysCommand /usr/bin/sss_ssh_authorizedkeys`**: O caminho absoluto para o binário. O OpenSSH exige caminho absoluto (sem `$PATH`, sem atalhos, sem desculpas). Além disso, o binário precisa ser de propriedade do `root` e **não pode ser gravável** por grupo ou outros (`chmod 755` no máximo). Se essas permissões estiverem erradas, o `sshd` silenciosamente ignora o comando, e você vai passar horas debugando "por que a chave não funciona" quando o problema é uma permissão.
- **`AuthorizedKeysCommandUser nobody`**: O `sshd` precisa rodar o comando como algum usuário. Usar `nobody` é a prática recomendada: um usuário sem privilégios, sem home, sem shell. O processo consulta o SSSD via socket Unix, então não precisa de nenhum privilégio especial.

Se qualquer uma dessas condições falhar, o `sshd` simplesmente ignora a diretiva sem nenhuma mensagem de erro visível no log padrão. Use `sshd -T` para validar a configuração ativa:

```bash
$ sudo sshd -T | grep -i authorizedkeys
authorizedkeyscommand /usr/bin/sss_ssh_authorizedkeys
authorizedkeyscommanduser nobody
authorizedkeysfile none
```

*Verifica a configuração ativa do sshd confirmando a delegação da busca de chaves para o SSSD.*

Se as linhas aparecerem, a configuração está sendo carregada corretamente.

## Limpando o cache do SSSD (quando tudo parece perdido)

O cache do SSSD é persistente em `/var/lib/sss/db/`. Quando você está debugando e fez alterações no LDAP que não estão refletindo, o cache pode ser o culpado. A forma nuclear de limpar tudo:

```bash
$ sudo systemctl stop sssd
$ sudo rm -rf /var/lib/sss/db/*
$ sudo rm -rf /var/lib/sss/mc/*
$ sudo systemctl start sssd
```

*Interrompe o serviço e remove completamente os arquivos de cache local do SSSD.*

Ou, de forma mais elegante, use o `sss_cache` para invalidar apenas o que precisa:

```bash
# Invalidar o cache de um usuário específico
$ sudo sss_cache -u joao

# Invalidar todos os usuários
$ sudo sss_cache -U

# Invalidar todos os grupos
$ sudo sss_cache -G
```

*Invalida entradas do cache seletivamente forçando nova consulta ao LDAP no próximo login.*

O `sss_cache` [^10] marca as entradas como "expiradas" sem apagar o banco. Na próxima consulta, o SSSD vai buscar dados frescos no LDAP. É menos brutal do que apagar o banco inteiro e evita que os usuários percam o acesso offline temporariamente durante o rebuild do cache.

## Conclusão

A combinação OpenSSH + SSSD + LDAP fecha o ciclo completo de gerenciamento de identidade em infraestrutura Linux de verdade. Onde antes você tinha uma constelação de gambiarras (scripts bash criando contas, chaves públicas copiadas via `scp` para dezenas de servidores, `authorized_keys` inchados e desatualizados), agora você tem um pipeline limpo e centralizado:

1. O usuário existe **uma vez** no LDAP, junto com seus UIDs, GIDs e grupos.
2. Os **Certificados SSH** cuidam da autenticação criptográfica dos humanos, com expiração e revogação nativas.
3. O SSSD distribui as identidades do LDAP para todos os servidores automaticamente, com cache inteligente e failover.
4. O OpenSSH valida os certificados contra a CA local e consulta o SSSD apenas para confirmar que a conta existe no sistema operacional.
5. Para contas de serviço e automação que não suportam certificados, o `AuthorizedKeysCommand` busca chaves públicas no LDAP via SSSD como fallback controlado.

É o tipo de setup que não impressiona em screenshots (não tem dashboard bonito, não tem interface web chamativa), mas que faz um engenheiro sênior de Ops dormir tranquilo sabendo que quando o estagiário for demitido na segunda-feira, basta desabilitar a conta no LDAP e ele instantaneamente perde acesso a todos os servidores da rede. Sem correria, sem Ansible, sem esquecimento.

No próximo post da série, vamos explorar o universo do `sudo` granular e a arte de criar políticas de elevação de privilégio que dão poder sem dar a chave do cofre. Porque, como todo bom engenheiro de infraestrutura sabe: dar `NOPASSWD: ALL` no `sudoers` é como dar a chave mestra do prédio para o entregador de pizza. Funciona? Funciona. É uma boa ideia? Definitivamente não.

Até a próxima!

## Referências

[^1]: **SSSD - System Security Services Daemon** {*sssd.io, Documentação oficial do projeto*} ([Link](https://sssd.io/docs/introduction.html))

[^2]: **Debian - Details of package sssd in trixie** {*packages.debian.org*} ([Link](https://packages.debian.org/trixie/sssd))

[^3]: **SSSD/sssd - Repositório oficial no GitHub** {*github.com/SSSD*} ([Link](https://github.com/SSSD/sssd))

[^4]: **sss_ssh_authorizedkeys(1) - Debian Manpages** {*manpages.debian.org*} ([Link](https://manpages.debian.org/testing/sssd-common/sss_ssh_authorizedkeys.1.en.html))

[^5]: **RFC 4519 - Lightweight Directory Access Protocol (LDAP): Schema for User Applications** {*IETF*} ([Link](https://datatracker.ietf.org/doc/html/rfc4519))

[^6]: **sssd-ldap(5) - SSSD LDAP Provider Man Page** {*manpages.debian.org*} ([Link](https://manpages.debian.org/testing/sssd-ldap/sssd-ldap.5.en.html))

[^7]: **sssd.conf(5) - SSSD Configuration File Man Page** {*manpages.debian.org*} ([Link](https://manpages.debian.org/testing/sssd-common/sssd.conf.5.en.html))

[^8]: **LDAP/NSS - Debian Wiki** {*wiki.debian.org*} ([Link](https://wiki.debian.org/LDAP/NSS))

[^9]: **OpenSSH Manual Pages: sshd_config(5) - AuthorizedKeysCommand** {*OpenBSD manual*} ([Link](https://man.openbsd.org/sshd_config#AuthorizedKeysCommand))

[^10]: **Authenticating Linux with Active Directory using SSSD** {*Debian Wiki*} ([Link](https://wiki.debian.org/AuthenticatingLinuxWithActiveDirectory))

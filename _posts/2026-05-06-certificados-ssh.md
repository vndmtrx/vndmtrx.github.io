---
layout: post
title: "OpenSSH - A mágica dos Certificados (e o fim do TOFU)"
author:
  - "Eduardo N. S. R."
date: 2026-05-09 19:24:00 GMT-3
modified_date: 2026-05-10 10:26:00 GMT-3
permalink: /posts/certificados-ssh/
tags: [SSH, Certificados]
series: OpenSSH na Prática
---

No último post sobre SSH, falei sobre o poder oculto dos túneis (`-L`, `-R`, `-D`) e como a maioria de nós usa apenas uma fração do que o OpenSSH oferece. Hoje, vamos dar mais um passo nessa jornada e falar sobre um recurso que resolve uma das maiores dores de cabeça de quem administra infraestrutura em escala: o gerenciamento de identidades e chaves públicas.

Se você trabalha com infraestrutura, com certeza conhece a rotina clássica: um novo desenvolvedor entra no time, gera um par de chaves, manda a chave pública pelo Slack para alguém de Ops, e essa pessoa adiciona a string gigante no final do arquivo `~/.ssh/authorized_keys` dos servidores. 

Ou pior, se você trabalha em uma daquelas equipes cabeça dura que juram de pés juntos que logar direto como `root` em tudo é "mais ágil", o desenvolvedor novo simplesmente recebe no WhatsApp a chave privada do `root` que a empresa inteira usa. Afinal, pra que auditoria e controle de acesso se a gente pode viver a "agilidade do caos", não é mesmo? (spoiler: não é mais ágil, é só mais perigoso e desorganizado).

E então, quando esse dev vai conectar pela primeira vez no servidor, a tela joga isso na cara dele:

```text
The authenticity of host '10.0.254.10 (10.0.254.10)' can't be established.
ED25519 key fingerprint is SHA256:+++++++++++++++++++++++++++++++++++++++++++.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

*O prompt clássico de aviso no primeiro acesso a um servidor desconhecido.*

Todo mundo digita `yes` no automático, não é? Isso se chama **TOFU (Trust On First Use)** [^1]. Nós confiamos cegamente que aquele servidor é realmente quem diz ser no primeiro acesso, e a partir daí a chave do host fica salva no arquivo `~/.ssh/known_hosts` da máquina do dev. 

O problema é múltiplo: 
1. **O TOFU cria fadiga de alerta.** Ninguém valida aquele SHA256. Se o tráfego estiver sendo interceptado (Man-In-The-Middle), o atacante ganha o `yes` de graça.
2. **Escalabilidade.** Imagina gerenciar arquivos `authorized_keys` de 500 servidores para 50 pessoas.
3. **Auditoria e Revogação.** Como você sabe quem é o dono da terceira chave no arquivo de 14 linhas do servidor de banco de dados? Quando alguém é demitido, a corrida contra o tempo pra garantir que o Ansible apagou a chave dessa pessoa de *todos* os cantos é desesperadora.

A solução elegante, nativa e absurdamente poderosa do OpenSSH para tudo isso se chama **Certificados SSH** [^2] [^3].

## O que são Certificados SSH?

Ao ouvir a palavra "Certificado", é normal ter calafrios lembrando do padrão X.509 usado em sites HTTPS (com toda aquela sopa de letrinhas: ASN.1, CSR, PEM, DER, Cadeias de Confiança). Mas respire fundo, pois como a própria documentação oficial deixa claro [^4], **Certificados SSH não são certificados X.509**. O OpenSSH usa um formato próprio, que é deliciosamente simples.

Em termos práticos, um certificado SSH é apenas uma chave pública normal que recebeu um "carimbo" (uma assinatura criptográfica) de uma outra chave. Essa chave carimbadora é a nossa Certificate Authority (CA).

A lógica do jogo vira de cabeça para baixo:
- Em vez de você dizer para cada servidor confiar na chave pública de cada desenvolvedor, você diz para os servidores confiarem apenas na CA. A CA, por sua vez, assina a chave dos desenvolvedores.
- Em vez dos desenvolvedores usarem TOFU para confiar em cada servidor, eles configuram suas máquinas para confiar apenas na CA. A CA assina a chave dos servidores.

Isso é feito através de duas vias independentes: **Host Certificates** e **User Certificates**. Vamos dissecá-los.

## Um parênteses importante: Qual tipo de chave usar para a CA?

Antes de criar a CA, precisamos decidir qual algoritmo criptográfico ela vai usar. Historicamente, nós criávamos CAs com RSA (`ssh-keygen -t rsa -b 4096`). Mas os tempos mudaram. 

O RSA com chaves menores (como 1024 e 2048 bits) já não oferece margem de segurança confortável contra a capacidade computacional moderna. Usar 4096 bits resolve, mas cria chaves lentas para assinar/verificar e arquivos gigantes. Já o ECDSA (Elliptic Curve Digital Signature Algorithm) sofre com a desconfiança da comunidade devido ao fato de usar as curvas padronizadas pelo NIST, que muitos criptógrafos encaram com suspeita por causa da influência histórica da NSA.

A recomendação padrão ouro hoje em dia, e o que eu pessoalmente uso para tudo, é o **ED25519** [^5]. Baseado na Curve25519 de Daniel J. Bernstein (o mesmo cara por trás do ChaCha20/Poly1305 usado no WireGuard). Chaves ED25519 são absurdamente menores (68 caracteres de chave pública), mais rápidas de verificar, resistentes a ataques de temporização (side-channel timing attacks) e não dependem das curvas do NIST.

> 🚨 **Aviso Crítico de Segurança**: A chave privada da sua CA é a "joia da coroa" de toda a operação. Se ela for vazada, um atacante poderá forjar certificados válidos para se passar por qualquer usuário ou servidor, tendo acesso irrestrito e silencioso à sua infraestrutura. Por design, essa chave **NUNCA** deve residir em um servidor acessível via internet ou na máquina de trabalho diário. O padrão ouro é mantê-la em uma máquina *air-gapped* (desconectada da rede), armazenada em dispositivos de hardware (como YubiKeys ou HSMs) ou delegar a custódia para soluções de cofre corporativo (como o HashiCorp Vault).

Para uma CA (que vai viver por anos e ser a raiz da confiança da sua infraestrutura) use `ed25519`.

## Host CA: O fim do "Are you sure you want to continue connecting?"

A primeira CA que vamos criar é a de Host. O objetivo dela é acabar com o prompt do TOFU, permitindo que a sua máquina local tenha certeza absoluta de que aquele IP/DNS pertence ao servidor correto.

Para começar, você gera o par de chaves ED25519 em uma máquina super segura (idealmente off-line ou em um cofre digital). Essa será a nossa CA de Host:

```bash
$ ssh-keygen -t ed25519 -f ca_host -C "CA de Hosts da Empresa"
Generating public/private ed25519 key pair.
Enter passphrase for "ca_host" (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in ca_host
Your public key has been saved in ca_host.pub
The key fingerprint is:
SHA256:=========================================== CA de Hosts da Empresa
The key's randomart image is:
+--[ED25519 256]--+
|... ..o. .       |
| + ..o .o .      |
|..=  .oo .       |
| oo=.. .o        |
|o.o=o. .So..     |
|o.o.o o.+.o..   .|
|. o. . . E.... o |
| o..    ......+  |
|.  .o.   .ooo+.  |
+----[SHA256]-----+
```

*Gera o par de chaves da CA de Host em ED25519 com fingerprint e representação gráfica de randomart.*

> 💡 **Curiosidade**: Aquele quadro `randomart image` gerado pelo comando não é só decoração de terminal. Ele é uma representação visual do fingerprint da chave. O cérebro humano é péssimo em memorizar strings SHA256 gigantes, mas é excelente em reconhecer formas e padrões visuais. A ideia do randomart é permitir que você perceba rapidamente, num "bater de olhos", se a chave foi alterada, pois o desenho será completamente diferente.

Como no nosso exemplo de equipe teremos dois servidores alvo (`php-01` e `db-01`), vamos provisionar os certificados de host para ambos. Primeiro, geramos o par de chaves interno de cada servidor. Muitas vezes isso é feito automaticamente na instalação do SO, mas vamos gerar explicitamente:

```bash
# No servidor php-01
$ ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N "" -C "Chave Host php-01"

# No servidor db-01
$ ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N "" -C "Chave Host db-01"
```

*Gera os pares de chaves de host em cada um dos servidores destino.*

Você pega apenas as chaves públicas que eles geraram, leva até a máquina segura onde está a sua `ca_host`, e assina, gerando finalmente os certificados de host para cada um:

```bash
# Na máquina segura da CA: gerando cert do php-01
$ mv ssh_host_ed25519_key.pub php-01_key.pub
$ ssh-keygen -s ca_host -I "servidor-php-01" -h \
  -n "php-01.example.com,10.0.254.5" -V +52w php-01_key.pub

# Na máquina segura da CA: gerando cert do db-01
$ mv ssh_host_ed25519_key.pub db-01_key.pub
$ ssh-keygen -s ca_host -I "servidor-db-01" -h \
  -n "db-01.example.com,10.0.254.10" -V +52w db-01_key.pub
```

*Assina as chaves públicas de cada servidor associando FQDNs e IPs aos Principals com validade de 52 semanas.*

Dissecando essa sopa de letrinhas do comando de assinatura:
- `-s ca_host`: Indica a chave privada da nossa CA que vai realizar a assinatura.
- `-I "servidor-..."`: É a identidade ("Key ID"). Serve para registrar nos logs da CA qual certificado foi emitido.
- `-h`: **Muito importante.** Indica que é um certificado de **Host** (e não de usuário). O SSH usa bits internos diferentes para os dois tipos.
- `-n`: Os **Principals**. Para servidores, os principals são os nomes de host (FQDN) ou IPs pelos quais esse servidor tem permissão para responder. É assim que evitamos que o `php-01` tente se passar pelo `db-01`.
- `-V +52w`: Validade. O certificado só vai valer por 52 semanas.

O comando cospe arquivos com o sufixo `-cert.pub`. Você devolve o certificado respectivo para cada servidor (salvando no caminho padrão `/etc/ssh/ssh_host_ed25519_key-cert.pub`) e adiciona uma linha no `sshd_config` de ambos:

```text
HostCertificate /etc/ssh/ssh_host_ed25519_key-cert.pub
```

*Declara no sshd_config qual certificado de host assinado o daemon deve apresentar nos handshakes.*

### Inspecionando os Certificados

Diferente de um certificado X.509 onde você precisa do `openssl x509 -text...`, no SSH você só precisa usar a flag `-L` no `ssh-keygen` para ler os metadados de um certificado em plain text. Vamos ver como ficaram nossos dois servidores:

```bash
$ ssh-keygen -L -f php-01_key-cert.pub
php-01_key-cert.pub:
        Type: ssh-ed25519-cert-v01@openssh.com host certificate
        Public key: ED25519-CERT SHA256::+++++++++++++++++++++++++
        Signing CA: ED25519 SHA256:========================== (using ssh-ed25519)
        Key ID: "servidor-php-01"
        Serial: 0
        Valid: from 2026-05-09T17:20:00 to 2027-05-08T17:21:18
        Principals:
                php-01.example.com
                10.0.254.5
        Critical Options: (none)
        Extensions: (none)

$ ssh-keygen -L -f db-01_key-cert.pub
db-01_key-cert.pub:
        ...
        Key ID: "servidor-db-01"
        Serial: 0
        Valid: from 2026-05-09T17:20:00 to 2027-05-08T17:21:26
        Principals:
                db-01.example.com
                10.0.254.10
        ...
```

*Inspeciona os metadados do certificado confirmando tipo host, validade e a lista de Principals autorizados.*

Olha que estrutura limpa. Ele mostra o formato `v01@openssh.com` (o padrão de certificado), quem assinou, a validade e, principalmente, os diferentes **Principals** de cada servidor. É essa lista de *principals* exclusiva em cada certificado que impede que o servidor PHP (mesmo possuindo um certificado de host válido assinado pela CA da empresa) responda por conexões destinadas ao banco de dados e intercepte o tráfego da Maria, por exemplo.

### O Lado do Cliente

O servidor agora apresenta um certificado no *handshake* SSH em vez da chave pública comum. Mas como o seu PC sabe que deve confiar nele? Você só precisa adicionar **uma única linha** no seu `~/.ssh/known_hosts` local:

```text
@cert-authority *.example.com ssh-ed25519 AAAAC3NzaC1... (conteúdo do ca_host.pub)
```

*Instrui o cliente SSH a confiar em qualquer máquina do domínio *.example.com autenticada pela CA de Host.*

Pronto. Você acabou de dizer: *"Confie cegamente em qualquer máquina que responda por `.example.com` SE ela apresentar um certificado assinado por esta CA"*. Adeus prompt do TOFU. Zero cliques. Total segurança contra MITM.

## User CA: O expurgo do arquivo authorized_keys

Se o Host CA facilita a vida de quem conecta, a User CA salva a alma de quem administra o servidor. Vamos criar uma segunda CA, exclusiva para assinar chaves de usuários:

```bash
$ ssh-keygen -t ed25519 -f ca_user -C "CA de Usuarios da Empresa"
Generating public/private ed25519 key pair.
Enter passphrase for "ca_user" (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in ca_user
Your public key has been saved in ca_user.pub
The key fingerprint is:
SHA256:=========================================== CA de Usuarios da Empresa
The key's randomart image is:
+--[ED25519 256]--+
|         .+o     |
|       ..o..     |
|    = o +.+      |
|   = + * + . .   |
|    + o S +   +  |
|   . & + o o = . |
|  o O B .   = +  |
|   = .     o * o |
|  . .       o.= E|
+----[SHA256]-----+
```

*Gera a CA exclusiva para emissão de certificados para desenvolvedores e operadores.*

No `sshd_config` de **todos os seus servidores**, você pode apagar ou simplesmente parar de manter arquivos `authorized_keys`. Basta colocar isso:

```text
TrustedUserCAKeys /etc/ssh/ca_user.pub
```

*Aponta a chave pública da CA de usuários como autoridade confiável para logins.*

Reinicie o `sshd`. Agora o servidor não confia mais na chave pública do João ou da Maria de forma isolada. Ele confia estritamente na assinatura da `ca_user`. 

Imagine que temos três colaboradores na nossa equipe de engenharia:
- O **João** é dev júnior e só precisa acessar os servidores de aplicação PHP.
- A **Maria** é a DBA da equipe e seu acesso é focado exclusivamente nos servidores de banco de dados, com privilégios administrativos.
- O **Antônio** é do time de QA e não deveria ter acesso via SSH a nenhum desses servidores (mas tentará).

O primeiro passo é que cada um deles gere sua própria chave ED25519 em suas máquinas locais:

```bash
# Na máquina do João
$ ssh-keygen -t ed25519 -f ~/.ssh/id_joao -C "joao@example.com"

# Na máquina da Maria
$ ssh-keygen -t ed25519 -f ~/.ssh/id_maria -C "maria@example.com"

# Na máquina do Antônio
$ ssh-keygen -t ed25519 -f ~/.ssh/id_antonio -C "antonio@example.com"
```

*Gera as chaves ED25519 locais de cada desenvolvedor nas suas respectivas estações de trabalho.*

Uma vez geradas as chaves, eles mandam apenas as chaves públicas (`id_joao.pub`, `id_maria.pub` e `id_antonio.pub`) para a equipe de Ops. A equipe assina essas chaves atribuindo as identidades (Principals) corretas para o perfil de cada um:

```bash
# Assinando a chave do João (acessa PHP e banco com restrições)
$ ssh-keygen -s ca_user -I "joao_dev" \
  -n "joao,dev_php,dev_db" -V +12w id_joao.pub

# Assinando a chave da Maria (DBA, acesso irrestrito ao banco)
$ ssh-keygen -s ca_user -I "maria_dba" \
  -n "maria,dba" -V +12w id_maria.pub

# Assinando a chave do Antônio (sem principals com acessos mapeados)
$ ssh-keygen -s ca_user -I "antonio_qa" \
  -n "antonio,qa_team" -V +12w id_antonio.pub
```

*Emite os certificados de usuário com os Principals de função e tempo de validade de 12 semanas.*

Isso gera os arquivos `-cert.pub`. Cada um baixa o seu respectivo certificado e o coloca na mesma pasta `~/.ssh/` onde está a chave privada. 

### A mágica no cliente (ssh-agent)

O mais legal é que o cliente SSH e o `ssh-agent` são incrivelmente inteligentes na hora de gerenciar essas chaves. O **ssh-agent** é um programa que roda em background na sua máquina e guarda suas chaves privadas na memória, evitando que você digite a passphrase toda vez que for conectar.

Para garantir que o agent está rodando e carregar a chave, o João executa no seu terminal:

```bash
# Inicia o ssh-agent em background (se já não estiver rodando)
$ eval "$(ssh-agent -s)"
Agent pid 59566

# Adiciona a chave do João no agent
$ ssh-add ~/.ssh/id_joao
Enter passphrase for /home/joao/.ssh/id_joao: 
Identity added: /home/joao/.ssh/id_joao (joao@example.com)
Certificate added: /home/joao/.ssh/id_joao-cert.pub (joao_dev)
```

*Carrega a chave privada no agente SSH, que detecta e vincula automaticamente o arquivo de certificado vizinho.*

Observe que o João apontou apenas para a chave privada (`id_joao`). O mais legal acontece aqui: o agent nota que existe um arquivo com o sufixo `-cert.pub` vizinho na mesma pasta e **automaticamente carrega o certificado na memória** junto com a chave! 

E como o cliente SSH sabe qual chave usar quando você tem várias? Ele é esperto: durante o *handshake* da conexão, o cliente negocia com o servidor quais métodos de autenticação são suportados. Se o servidor informar que aceita certificados, o agent prioriza apresentar o certificado antes de tentar usar chaves públicas nuas. O João só precisa digitar `ssh deploy@php-01` e **ele entra direto**. 

Esse mesmo ciclo de subir o agent e rodar o `ssh-add` é feito pela Maria, pelo Antônio e por qualquer outro usuário.

E a grande vantagem do campo de validade: se a empresa contratar o **Carlos** (um consultor terceirizado) para atuar na infraestrutura por apenas uma semana, a equipe de Ops pode emitir o certificado dele com `-V +1w` (válido por 1 semana) ou até mesmo `-V +1d` para um acesso de apenas um dia. Quando o prazo acabar, o acesso do Carlos some automaticamente de toda a rede. Ninguém precisa criar um ticket lembrando de entrar nos servidores para limpar chaves. O certificado simplesmente "vence" e o SSH recusa novas conexões.

### E se um notebook for roubado? A Lista de Revogação (KRL)

"Mas Dudu, o certificado do João vale por 12 semanas, e ele teve o notebook roubado hoje. Como eu bloqueio o acesso dele se não tem `authorized_keys` pra apagar?"

Excelente pergunta. É pra isso que serve a **KRL (Key Revocation List)**. O OpenSSH suporta revogação nativa. Você usa o mesmo `ssh-keygen` para criar e atualizar um arquivo binário listando quais chaves e certificados estão banidos:

```bash
# Passando a chave pública do João para a lista negra
ssh-keygen -k -f /etc/ssh/rev_keys.krl id_joao.pub
```

*Cria ou atualiza o arquivo binário de revogação inserindo a chave comprometida na lista negra.*

Você precisa distribuir esse arquivo `.krl` pelos servidores e adicionar a seguinte linha no `sshd_config`:

```text
RevokedKeys /etc/ssh/rev_keys.krl
```

*Configura o sshd para validar se a chave ou certificado apresentado consta na lista de revogações ativas.*

Agora, mesmo que o certificado esteja matematicamente válido, o servidor consulta o arquivo KRL na hora do handshake e derruba a conexão.

A parte chata aqui é manter esse arquivo sempre atualizado em todas as máquinas. Uma solução simples e elegante para isso é hospedar o arquivo `.krl` num servidor web interno e criar uma entrada no `/etc/crontab` de cada servidor para baixar a lista mais recente, por exemplo, duas vezes ao dia (tipo, à meia-noite e ao meio-dia):

```cron
0 0,12 * * * root curl -s https://pki.example.com/revs.krl -o /etc/ssh/rev_keys.krl
```

*Agenda a atualização periódica da lista KRL duas vezes ao dia via cron.*

## O Segredo do Sucesso: Principals e Identities

Você percebeu o parâmetro `-n` recebendo uma lista separada por vírgulas (como `joao,dev_php,dev_db`) quando assinamos as chaves? Isso define os **Principals** (identidades) [^6], e é a parte mais poderosa da autorização via certificado. É o que permite agrupar múltiplos acessos em um único certificado válido para a rede inteira.

> 💡 **Nota**: Como os *Principals* de usuário (`dev_php`, `dev_db`, `dba`) se mapeiam no certificado do Host? **A resposta é: eles não mapeiam!** Os certificados de Host e de Usuário não se misturam. O certificado do Host só carrega o seu FQDN/IP para provar quem ele é para o cliente. O mapeamento que define "quem tem o principal dev_php pode entrar no servidor php-01" acontece inteiramente na configuração local do Sistema Operacional de destino.

A autenticação de certificados no SSH não é um simples *"a assinatura bate com a CA que eu confio, então pode entrar"*. O OpenSSH executa uma camada adicional de autorização (uma espécie de RBAC nativo): ele verifica se os Principals que estão "carimbados" no seu certificado possuem permissão para acessar a conta destino no sistema operacional.

A boa prática diz que não devemos logar diretamente como `root` e que não devemos distribuir a mesma conta para pessoas de áreas diferentes. O normal é termos contas genéricas de função ("role accounts") no sistema operacional (ex: o usuário `deploy` na máquina PHP, e na máquina de banco podemos ter `db_admin` para os DBAs operarem a infra e `db_readonly` para os devs). Ninguém deveria acessar a conta do `root` diretamente via SSH.

Criar essas contas locais, garantir que não tenham senhas (`usermod -L`) e amarrar os privilégios exatos de cada uma no arquivo `/etc/sudoers` é uma arte à parte. Para dar um exemplo rápido de como isso ficaria no Linux, você adicionaria algo assim no `sudoers`:

```bash
# Permite que o usuário 'deploy' apenas reinicie o PHP, sem pedir senha
deploy ALL=(root) NOPASSWD: /usr/bin/systemctl restart php-fpm
```

*Regra granular no sudoers permitindo reinício controlado do serviço php-fpm sem necessidade de senha de root.*

> ⚠️ **Importante**: Essa gerência do ciclo de vida dos usuários e de suas permissões granulares de elevação de privilégio é um assunto tão extenso e vital que com certeza faremos um post dedicado só para isso no futuro.

Voltando ao SSH: se nós fôssemos amadores, colocaríamos diretamente o principal `db_admin` no certificado da Maria. O problema? A Maria conseguiria logar com o usuário `db_admin` em **qualquer** máquina da empresa! O movimento lateral ficaria livre.

A solução elegante é desacoplar o Principal do usuário local usando a diretiva do OpenSSH chamada `AuthorizedPrincipalsFile`. No `sshd_config` de ambos os servidores, configuramos:

```text
AuthorizedPrincipalsFile /etc/ssh/auth_principals/%u
```

*Define que os Principals válidos para cada conta residem no arquivo nomeado após o usuário em `/etc/ssh/auth_principals/`.*

> 💡 **Nota**: A variável `%u` é parseada como o nome do usuário de destino durante o login.

E então configuramos o que cada conta permite. No servidor **PHP** (`php-01`), criamos o arquivo `/etc/ssh/auth_principals/deploy` com o conteúdo:

```text
dev_php
```

*Exige o Principal dev_php para conceder acesso à conta deploy.*

No servidor de **Banco de Dados** (`db-01`), vamos ter **duas contas** diferentes. O arquivo `/etc/ssh/auth_principals/db_admin` exige o principal de DBA:

```text
dba
```

*Exige o Principal dba para autorizar o login administrativo no banco.*

> 💡 **Nota**: Esse usuário `db_admin` não é o dono do banco. Ele loga via SSH e depois usa privilégios no `/etc/sudoers` para rodar um `sudo -u postgres psql` ou `sudo systemctl restart postgresql`, mantendo a trilha de auditoria limpa.

Por último, o arquivo `/etc/ssh/auth_principals/db_readonly` exige apenas o principal de dev:

```text
dev_db
```

*Exige o Principal dev_db para autorizar o login de leitura.*

### O Desfecho dos Testes de Acesso

Vamos ver o que acontece na prática com o nosso time:

**1. O João tenta acessar o PHP:**
Ele digita `ssh deploy@php-01`. O servidor recebe o certificado e faz três validações:
1. "Assinado pela `ca_user`?" -> **Sim.**
2. "Dentro da validade?" -> **Sim.**
3. "O arquivo do usuário `deploy` exige o principal `dev_php`. O certificado do João possui isso?" -> **Sim.**
*Acesso concedido!*

**2. O João tenta acessar o Banco de Dados como DBA:**
Ele digita `ssh db_admin@db-01`. O servidor faz as mesmas validações. Na terceira etapa:
"O arquivo do usuário `db_admin` exige o principal `dba`. O certificado do João possui isso?" -> **NÃO.** (Ele tem `joao,dev_php,dev_db`).
*Acesso Negado.* A tentativa registra o bloqueio nos logs, impedindo que o dev derrube o banco acidentalmente.

**3. O João tenta acessar o Banco de Dados como Leitor:**
Ele digita `ssh db_readonly@db-01`. A validação checa e percebe que ele **possui** o principal `dev_db`. O acesso é concedido! Um único certificado validou dois usuários diferentes em servidores diferentes.

**4. A Maria (DBA) tenta acessar a web e o banco:**
Ela tenta `ssh deploy@php-01`. Como o seu certificado tem apenas `maria,dba` e o usuário `deploy` exige `dev_php`, o acesso é **negado**. Em seguida, ela tenta `ssh db_admin@db-01`. O certificado possui o principal `dba` exigido, e o acesso é **concedido**. A separação de privilégios funcionou perfeitamente.

**5. O Antônio (QA) tenta "dar uma espiada" no PHP:**
Ele tenta `ssh deploy@php-01`. O certificado do Antônio tem apenas o principal `qa_team`. O servidor checa e barra na hora. O QA fica de fora, exatamente como a política dita.

Para empresas muito grandes, o OpenSSH oferece até a diretiva `AuthorizedPrincipalsCommand`, que permite que o SSH execute um script ou binário (passando o certificado do usuário) que pode bater num LDAP ou API interna para retornar "quais principals são válidos para esse login", removendo totalmente a necessidade de distribuir arquivos de configuração de principals localmente em cada servidor.

## O perigo mora nos detalhes: A falha CVE-2026-35414

Claro que nem tudo é perfeito. Toda feature complexa carrega suas armadilhas, e o subsistema de Principals teve uma prova de fogo recente com a **CVE-2026-35414** [^7] (afetando OpenSSH em versões anteriores à 10.3).

Em cenários reais de transição (quando a empresa ainda não apagou todos os `authorized_keys`), usa-se um modo híbrido, instruindo o `authorized_keys` antigo a delegar a confiança a uma CA e exigir determinados principals na mesma linha:

```text
cert-authority,principals="bob,admin" ssh-rsa AAAAB3... (chave publica da CA)
```

*Sintaxe híbrida legada em authorized_keys restringindo o login por CA aos principals especificados.*

Essa linha diz ao servidor: *"Aceite o acesso SE a chave pública apresentada for um certificado assinado por esta CA e se esse certificado tiver o principal 'bob' OU o principal 'admin'"*.

A vulnerabilidade residia especificamente no *parser* de opções (a função interna do OpenSSH em C que faz o *split* da string). O OpenSSH antigo falhava miseravelmente em lidar com vírgulas usadas dentro da declaração `principals="..."` acoplada ao `cert-authority`. Em vez de quebrar a string em dois tokens (`bob` e `admin`), o parser engasgava, não separava nada, e registrava em memória que a linha exigia **um único principal longo** chamado literalmente `"bob,admin"`.

A implicação disso em produção causa tanto DoS quanto Bypass:

1. **Negação de Serviço:** O administrador Bob chega com seu certificado validado contendo apenas o principal `bob`. Ele tenta entrar. O servidor nega acesso, pois a memória do parser exige uma string idêntica a `"bob,admin"`.

2. **Exploitation (Bypass de Segurança):** Se a sua CA for controlada por um portal automatizado (tipo Vault) e tiver uma brecha no input, um atacante (ou um usuário insider mal intencionado) poderia solicitar propositalmente um certificado forjado contendo o caractere de vírgula na identidade:

   ```bash
   # Comando usado pelo atacante para forjar o certificado "bugado"
   ssh-keygen -s ca_user -I "hacker_id" -n "bob,admin" id_ed25519.pub
   ```

   *Gera um certificado propositalmente forjado contendo uma vírgula literal no campo do principal.*

   Quando o atacante usa esse certificado com o principal exato `"bob,admin"`, o parser quebrado do servidor examina a string, faz o `strcmp()`, e como as strings batem exatamente com a interpretação errônea dele, **o servidor concede acesso imediato**, contornando a intenção de controle de acesso de "apenas bob ou admin separadamente".

A correção definitiva requer atualizar para a versão 10.3+. Mas há uma regra de design universal para levar pra vida: **Nunca use vírgulas, espaços ou caracteres especiais nos nomes dos seus Principals**. Trate Principals como variáveis limpas e restritas (ex: `admin`, `db_read`, `squad_frontend`). Deixe as vírgulas apenas para separar os argumentos do `ssh-keygen`.

## Conclusão

Implementar Certificados SSH muda drasticamente a maturidade técnica de um time de operações. Você elimina de vez a dor de cabeça com gerenciamento de estado (as chaves espalhadas e esquecidas por dezenas de servidores), ganha controle por expiração automática, consegue revogar acesso de ex-funcionários de forma centralizada (com KRL) e garante a identidade criptográfica dos servidores sem treinar seus desenvolvedores a ignorarem alertas de segurança no terminal.

A configuração de CAs, ED25519, Principals e KRLs é exatamente o que separa uma infraestrutura *"feita de qualquer jeito no terminal"* de um ambiente com processos de escala *enterprise*. Parece muita sopa de letrinhas no início, mas quando os certificados de acessos temporários começarem a expirar sozinhos no final de semana sem deixar rastro no seu `authorized_keys`, você vai dormir muito mais tranquilo.

Vale lembrar, no entanto, que os certificados SSH resolvem brilhantemente o problema de **autenticação** e **autorização** na camada do protocolo, mas eles não criam as contas de usuário no sistema operacional de forma mágica. Você ainda precisará de ferramentas de automação (como Ansible) ou diretórios centrais (LDAP/SSSD) para garantir que as contas de serviço ("role accounts", como `deploy`, `db_admin` ou `db_readonly`) existam no `/etc/passwd`. Mais do que isso, como vimos ao proibir o acesso SSH direto ao dono do banco (`postgres`), a arte de amarrar essas contas com políticas rígidas de elevação de privilégios granulares via `sudo` é uma peça vital desse quebra-cabeça corporativo. E isso, com certeza, rende um ótimo assunto para um próximo post!

Até a próxima!

## Referências

[^1]: **SSH certificates: the better SSH experience** {*jpmens.net, Abril/2026*} ([Link](https://jpmens.net/2026/04/03/ssh-certificates-the-better-ssh-experience/))

[^2]: **Using OpenSSH Certificate Authentication** {*Red Hat Documentation, RHEL 6 Deployment Guide*} ([Link](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/deployment_guide/sec-using_openssh_certificate_authentication))

[^3]: **If you're not using SSH certificates you're doing SSH wrong** {*Smallstep Blog, Maio/2024*} ([Link](https://smallstep.com/blog/use-ssh-certificates/))

[^4]: **OpenSSH Manual Pages: ssh-keygen(1) - CERTIFICATES** {*OpenBSD manual*} ([Link](https://man.openbsd.org/ssh-keygen.1#CERTIFICATES))

[^5]: **SSH CA host and user certificates** {*liw.fi*} ([Link](https://liw.fi/sshca/))

[^6]: **Como configurar autenticação baseada em certificados SSH** {*Tempest SideChannel Blog*} ([Link](https://www.sidechannel.blog/como-configurar-autenticacao-baseada-em-certificados-ssh/))

[^7]: **CVE-2026-35414: Exploiting OpenSSH’s authorized_keys Principals Mishandling** {*CVE.news, Abril/2026*} ([Link](https://www.cve.news/cve-2026-35414/))

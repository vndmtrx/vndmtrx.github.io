---
title: "Túneis: O poder oculto do SSH (e que vc provavelmente não usa)"
date: 2026-03-14 21:16:00 
permalink: /posts/tuneis-ssh/
tags: SSH, DevOps, Infraestrutura, Segurança, Túneis
---

SSH é daquelas ferramentas que todo mundo na área de infra tem na ponta da língua: `ssh usuario@servidor`, entra, faz o que tem que fazer, sai. Simples, confiável, onipresente. O problema é que boa parte das pessoas pára exatamente por aí, e o pior é que o SSH possui alguns recursos que ficam completamente invisíveis pra quem nunca foi além do básico. Não porque sejam obscuros ou experimentais. Eles estão inclusive na man page, funcionam desde sempre, e aparecem toda vez que você digita `ssh --help`. Só que ninguém parou pra explicar direito como usar de forma intuitiva.

Um desses recursos são os **túneis SSH**. Três flags (`-L`, `-R` e `-D`) que permitem redirecionar tráfego de rede arbitrário por dentro de uma conexão SSH já estabelecida. Sem VPN, sem configuração extra no firewall, sem instalar nada. É o tipo de coisa que, quando você descobre, fica se perguntando por que ninguém nunca te contou antes, e que faz você olhar pro seu histórico de comandos e pensar _"mds, quanto tempo eu perdi sem isso"_.

E ainda vou deixar uma pulga atrás da orelha antes de continuar: essas mesmas técnicas que você vai aprender aqui para fazer o seu trabalho com mais eficiência são exatamente as que times de red team e atacantes reais costumam usar para se mover lateralmente dentro de redes comprometidas. O MITRE ATT&CK inclusive cataloga isso como técnica [T1021.004](https://attack.mitre.org/techniques/T1021/004/), e a Red Canary já descreveu o abuso de túneis SSH como um vetor de lateralização "incrivelmente difícil de detectar quando as ferramentas certas não estão no lugar". E em 2025, a Sygnia documentou grupos de ransomware usando exatamente o `-D` pra se mover por ambientes VMware ESXi sem levantar alertas ([ESXi Ransomware Attacks: Stealthy Persistence through SSH Tunneling](https://www.sygnia.co/blog/esxi-ransomware-ssh-tunneling-defense-strategies/)). Conhecer o recurso é a primeira linha de defesa (e também de uso legítimo).

Dito isso, nesse post vou explicar cada um dos três modos de uso de túneis que existem no SSH (e por tabela no PuTTY, ok?). A idéia é simular um cenário real, e sem pular etapas. No final ainda tem um bônus sobre o `ProxyJump` (`-J`), que muita gente confunde com túnel mas é outra coisa — vale ficar até lá.

## Mas antes: o que diabos é um túnel SSH, Dudu?

Ok, vamos do começo então. Imagina que você tem um cano de água entre dois pontos. Normalmente, esse cano carrega água, mas nada impede que você enfie um cabo elétrico dentro dele pra chegar no mesmo lugar (_por favor não faça isso_), só que usando a estrutura já existente.

Um túnel SSH funciona assim. Você já tem uma conexão SSH estabelecida entre dois pontos. O que o túnel faz é pegar outro tráfego de rede (banco de dados, HTTP, o que for) e mandar junto, empacotado dentro dessa conexão SSH. Criptografado, sem abrir novas portas no firewall, sem VPN.

A fonte de confusão que quase todo mundo tem quando vê túneis SSH pela primeira vez é: **de quem é o ponto de vista?**? Quando o comando diz `localhost`, a qual máquina ele está se referindo? Quando diz _"escutar uma porta"_, é no seu PC ou no servidor? Essa é exatamente a pergunta de um mihão de reais, e vamos respondê-la para cada cenário de tunelamento que temos no SSH.

## Configurando o cenário

Então, antes de ir para as flags, vamos montar um ambiente concreto — porque túnel SSH sem contexto real é difícil de visualizar.

Primeiramente temos:
- Uma **rede interna**: rede na qual estão os nossos recursos que queremos acessar;
- Um servidor **Bastion** (também chamado de **Jump Server**): é o único servidor acessível de fora da estrutura, via SSH;
- Um servidor qualquer, tipo um **Postgres**: não tem porta SSH exposta, você não consegue entrar nele diretamente;
- Um servidor do tipo **Dashboard**: esse só aceita conexões de IPs da rede interna.
- **Seu PC**: tem um cliente SSH e, para o caso do segundo cenário, um servidor SSH rodando na porta 22.

```
[SEU PC] ─> [BASTION: IP Público / IP local: 10.0.254.10] 
                └─> [REDE INTERNA: 10.0.254.0/24]
                        ├─> POSTGRES: 10.0.254.25 (PostgreSQL :5432)
                        └─> DASHBOARD: 10.0.254.50 (HTTPS :443)
```

É o tipo de topologia que aparece o tempo todo em ambientes corporativos, homelabs com um mínimo de segurança, e praticamente qualquer cloud bem configurada. E é exatamente nesses ambientes que os túneis SSH brilham.

## Primeiro Cenário - Túnel Local: `-L`

Vamos começar pelo caso mais comum: você precisa acessar um serviço que está **na rede interna**, mas que não tem acesso direto da internet. Pode ser um servidor web, um banco de dados, uma API interna, qualquer coisa que só responde para a rede interna.

É exatamente pra isso que serve o **túnel local** (`-L`).

### "Eu quero acessar algo que só o servidor enxerga"

```bash
ssh -L [porta_local]:[host_destino]:[porta_destino] usuario@bastion
```

É só isso. A flag `-L` cria uma **porta de escuta no seu PC**. Quando você conectar nessa porta local, o SSH pega esse tráfego, manda pelo túnel até o `bastion`, e o `bastion` faz a conexão final com `host_destino:porta_destino`.

O detalhe crucial (e fonte de 90% da confusão com o comando) é que o `host_destino` é resolvido do **ponto de vista do bastion**, não do seu PC. Então quando você escreve `localhost` ali, você tá falando do `localhost` do `bastion`. Quando você escreve `10.0.254.25`, você tá falando de um host que o `bastion` alcança diretamente, mas que o seu PC nem conhece.

Por que eu falei de `localhost`? Pq as vezes usamos isso diretamente em uma máquina que pode ter acesso SSH exposto mas outra porta filtrada (banco de dados é o melhor exemplo).

### Exemplo: acessar o PostgreSQL interno

O banco em `10.0.254.25:5432` só aceita conexões da rede interna. Do seu PC, direto, não tem como. Então, com o túnel local fazemos:

```bash
ssh -L 54322:10.0.254.25:5432 usuario@ip_publico_bastion
```

Isso abriu a porta 54322 na minha máquina local, e essa porta é ligada a um túnel via SSH que passa pelo `bastion` e o `bastion` então redireciona para a porta 5432 da máquina `10.0.254.25`, que no nosso diagrama lá em cima é o Postgres.

Agora, em outro terminal:

```bash
psql -h localhost -p 54322 -U meu_usuario -d meu_banco
```

Do ponto de vista do banco de dados, a conexão veio do `bastion` (`10.0.254.10`), que está dentro da rede interna. Sem VPN, sem abrir o PostgreSQL para a internet, sem config especial. O SSH fez o trabalho sujo.

```
SEU_PC:54322 ─[túnel SSH]─> BASTION ─> POSTGRES:10.0.254.25:5432
```

## Segundo Cenário - Túnel Reverso: `-R`

Agora vamos inverter completamente a lógica. E se você quiser que o **servidor te acesse** em vez de você acessar o servidor? Pode ser pra receber um arquivo grande do `bastion`, expor uma ferramenta local que o time precisa usar, ou qualquer situação onde a conexão precisa vir do servidor pra você.

É exatamente pra isso que serve o **túnel reverso** (`-R`).

### "Eu quero que o servidor acesse algo que só eu enxergo"

```
ssh -R [porta_remota]:[host_destino]:[porta_local] usuario@bastion
```

Da mesma forma que o outro comando, é só isso também. A flag `-R` inverte completamente a lógica. Agora quem **escuta a porta é o bastion**. Quando alguém se conectar nessa porta no `bastion`, o tráfego vem pelo túnel SSH de volta até você, e aí o seu PC faz a conexão final com `host_destino:porta_local`.

E agora vêm o real pulo do gato (e a maior fonte de confusões com a sintaxe do comando): com a flag `-R` o host destino é resolvido a partir do ponto de vista do **seu PC**, não do `bastion`. Então, quando vc escreve `localhost` ali, você está dizendo que a porta é no **seu PC**.

Por que isso importa? Porque é comum usar `-R xx:localhost:22` (sendo `xx` um valor aleatório) pra expor o SSH do seu PC pro `bastion` (ou rede interna toda).

### Exemplo: receber um arquivo pelo bastion no seu PC

Um dump de banco de dados foi gerado no **Postgres** (`10.0.254.25`) e você precisa trazer pra sua máquina. Transferir diretamente não é possível porque o **Postgres** não sabe chegar no seu PC.

No **seu PC**, execute primeiro:

```bash
ssh -R 2222:localhost:22 usuario@ip_publico_bastion
```

Isso abre a porta **2222 no bastion**, que aponta pro SSH do **seu PC** via túnel reverso.

Agora, **no terminal do Postgres** (`10.0.254.25`):

```bash
scp -P 2222 dump_banco.sql.gz usuario@10.0.254.10:/home/usuario/
```

Fluxo:
- Usuário no Postgres conecta em `10.0.254.10:2222`
- Bastion redireciona via túnel reverso para **seu PC**
- Arquivo é recebido pelo servidor SSH do seu lado

E o melhor disso tudo é que em nenhum momento precisamos lidar com a arquitetura de rede envolvida nesse processo todo. Só o `bastion` precisa estar acessível.

O arquivo vai direto pro seu PC. O Postgres _"vê"_ a porta `2222` do `bastion` como um SSH local, mas por baixo dos panos é o túnel reverso chegando até o **seu PC**.

```
POSTGRES ──> BASTION:2222 ──[túnel reverso]──> SEU_PC:22
```

Vale notar: por padrão, o OpenSSH faz o `-R` escutar apenas em `127.0.0.1` no servidor. Se você quiser que outros hosts da rede interna também usem essa porta, precisa habilitar `GatewayPorts yes` no `/etc/ssh/sshd_config` do `bastion`.

## Terceiro Cenário - Proxy Dinâmico: `-D`

Chegamos no mais poderoso dos três: o **proxy SOCKS**. Diferente dos outros dois que lidam com portas específicas, o `-D` transforma todo o seu tráfego de rede num túnel pelo `bastion`. É como se seu PC "emprestasse" o endereço IP do `bastion` pra navegar na rede interna.

É exatamente pra isso que serve o **proxy dinâmico** (`-D`).

### "Eu quero que meu tráfego todo saia como se fosse o servidor"

```bash
ssh -D [porta_local] usuario@ip_publico_bastion
```

Da mesma forma que os outros, é só isso. O `-D` é o mais diferente dos três. Ele não redireciona uma porta específica para um destino fixo. Ele abre um **proxy SOCKS** no seu PC. Você aponta seus aplicativos pra esse proxy, e toda conexão que eles fizerem vai passar pelo `bastion` antes de chegar ao destino final.

É o comportamento mais próximo de uma VPN que você consegue com SSH puro, sem instalar nada extra.

E o mais interessante de tudo é: o SOCKS é universal. Funciona com navegadores, `curl`, `psql`, qualquer coisa que suporte o protocolo SOCKS. Você configura uma vez e usa pra tudo.

### Exemplo: acessar o painel web restrito por IP

O `dashboard` em `10.0.254.50/admin` tem um firewall que bloqueia qualquer IP fora da rede interna, em `10.0.254.0/24`.

No seu PC:

```bash
ssh -D 9999 usuario@ip_publico_bastion
```

Agora, configure o seu navegador preferido pra usar SOCKS proxy no endereço localhost:9999.

```
SEU_NAVEGADOR ──> SOCKS:9999 ──[túnel]──> BASTION ──> DASHBOARD:10.0.254.50
```

E o melhor: funciona pra qualquer site/serviço da rede interna, não só pro dashboard. Uma configuração, tráfego ilimitado. Inclusive, se o `bastion` têm rota padrão para a internet, é possível inclusive navegar para fora da rede por essa conexão. Por isso inclusive que ela é uma opção **extremamente poderosa** (e usada frequentemente por atacantes para esconder tráfego).

## Caso Especial - ProxyJump: `-J`

Às vezes você só quer entrar num servidor da rede interna que **também tem SSH**, mas não tem acesso direto. O ProxyJump resolve isso sem precisar de túnel nenhum.

É exatamente pra isso que serve o **ProxyJump** (`-J`).

O `ProxyJump` permite **pular pelo bastion** para abrir uma sessão SSH em outra máquina da rede interna. Ele não cria redirecionamento de porta nenhum — simplesmente usa o `bastion` como relay transparente pra uma nova conexão SSH.

É útil quando o servidor de destino também tem SSH e você só quer um terminal nele. Mas se o objetivo é acessar um serviço (banco, web, etc.), você vai precisar das flags de túnel de verdade.

### "Eu só quero um terminal no servidor interno"

```bash
ssh -J usuario@bastion usuario@postgres
```

É só isso. O `-J` usa o `bastion` como **trampolim transparente** pra uma nova conexão SSH. Você digita comandos normalmente, mas por baixo dos panos passa pelo `bastion`.

**Diferença crucial para os túneis:** aqui ele não mexe com portas, não redireciona tráfego, não cria proxy. É só SSH ─> SSH.

### Exemplo: entrar no servidor Postgres

O Postgres (`10.0.254.25`) tem SSH na porta 22, mas só acessível da rede interna.

```bash
ssh -J usuario@ip_publico_bastion usuario@10.0.254.25
```

Você abre um terminal direto no Postgres. O `bastion` só "repassa" a conexão SSH, sem abrir portas extras ou criar túneis.

```
SEU_PC ──[SSH]──> BASTION ──[SSH]──> POSTGRES:22
```

## Resumo definitivo

| Flag | Quem escuta? | Ponto de vista do endereço de destino? | Quando usar |
|------|--------------|-----------------|-------------|
| `-L` | Seu PC | Bastion | Serviços internos (banco, API) |
| `-R` | Bastion | Seu PC | Receber conexões (arquivos, ferramentas) |
| `-D` | Seu PC (SOCKS) | Bastion | Navegação total na rede interna (ou internet) |
| `-J` | Relay SSH | - | Terminal em máquina interna |

## Conclusão

O SSH tem recursos que a maioria dos programadores e pessoal de ops **nunca chega a conhecer**. Não por serem obscuros ou difíceis, mas porque ninguém nunca realmente parou para ler direito como funciona (ou fazer playground para aprender o comportamento).

E tem um outro lado dessa moeda que não dá pra ignorar: essas mesmas técnicas que simplificam tanto a vida do pessoal de ops também criam **vetores de navegação lateral praticamente invisíveis**. Uma porta SSH legítima pode facilmente virar canal pra evasão de regras de firewall internas: você pula de máquina em máquina sem tocar nas políticas de rede que o time de segurança passou meses configurando.

Por isso a **microsegmentação** é tão crucial hoje. Security Groups (AWS, GCP), Network Policies (Kubernetes), listas de permissão granulares, tudo isso existe exatamente pra garantir que **só quem deve** acessar um recurso consiga. Uma porta SSH no `bastion` não deveria, por princípio de menor privilégio, ter acesso irrestrito pra todo o resto da rede interna.

Em outro post futuro, pretendo falar de outro recurso muito poderoso do SSH, chamado **SSH-Based Virtual Private Networks** (`-w`), que permite criar túneis TAP/TUN de camada 2/3 completos — a **VPN nativa do SSH** que tenho certeza que a maioria das pessoas usuárias de SSH nem sonham que existe.

**É conhecimento de ops que todo mundo deveria ter. E de segurança que todo mundo deveria temer quando usado errado.**

## Bibliografia

1. **[man ssh](https://man7.org/linux/man-pages/man1/ssh.1.html)** - A Fonte. Procure por "Local port forwarding", "Remote port forwarding" e "Dynamic forwarding";
1. **[SSH.com: Complete Guide to SSH Tunneling](https://www.ssh.com/academy/ssh/tunneling-example)** - Exemplos práticos + casos avançados (inclusive com port forwarding múltiplo);
1. **[MITRE ATT&CK T1021.004](https://attack.mitre.org/techniques/T1021/004/)** - SSH tunneling como técnica de navegação lateral oficializada;
1. **[Sygnia: ESXi Ransomware via SSH Tunneling](https://www.sygnia.co/blog/esxi-ransomware-ssh-tunneling-defense-strategies/)** - Caso real de ransomware usando `-R` para se manter oculto no VMware;
1. **[Red Canary: Lateral Movement with SSH](https://redcanary.com/blog/threat-detection/lateral-movement-with-secure-shell/)** - Detecção de abuso de SSH tunneling em produção;
1. **[Kubernetes Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/)** - Conceitos de microsegmentação para Kubernetes.

---
layout: post
title: "12-Factor App: Como Fazer (e os Pesadelos de Como Não Fazer)"
subtitle: "Uma autópsia de sistemas legados, traumas de deploy e as doze regras para manter a sanidade em produção"
author:
  - "Eduardo N. S. R."
date: 2026-08-21 18:57:00 GMT-3
permalink: /posts/12-factor-app-pesadelos-e-pratica/
tags: [DevOps, Arquitetura, 12-Factor, SysAdmin, Engenharia de Software]
---

Se você trabalha com desenvolvimento ou infraestrutura há tempo suficiente, certamente guarda na memória um sistema que te dava calafrios. Aquele monstro sagrado da empresa que ninguém tinha coragem de reiniciar numa sexta-feira. Aquele software cujo processo de deploy parecia um ritual de invocação medieval, com quinze passos manuais, três rezas e uma oferenda aos deuses do hipervisor.

No meu caso, esse monumento ao caos foi um sistema acadêmico que herdei quando eu ainda era um analista de infraestrutura novato, dando os primeiros passos sérios na profissão.

Ele era uma colcha de retalhos espetacular: Java EE, Struts, Velocity, Spring arcaico, AspectJ, JasperReports, JSF e RichFaces, tudo empilhado em cima de um JBoss que já era considerado peça de museu quando foi instalado. O sistema funcionava? Funcionava, no sentido estrito de que elétrons passavam pelos circuitos e algumas páginas eventualmente não carregavam. Mas operá-lo era um exercício diário de sobrevivência biológica.

Para coroar o cenário, o contrato de sustentação com a empresa terceirizada acabou pouco tempo depois da minha chegada. O sistema passou inacreditáveis **oito anos sem receber um único update de código**. Nem um patch de segurança, nem uma linha de refatoração. 

Como o negócio não podia parar, coube a mim a missão inglória de manter o dinossauro vivo. Mais do que isso: tive que migrar o monstro inteiro para a nuvem da AWS (um *lift-and-shift* em instâncias EC2 com um malabarismo de rede colossal para os módulos continuarem enxergando o banco). Como o código estava congelado no tempo, qualquer vulnerabilidade crítica que explodia no mundo (como o infame bug do Log4j ou falhas de execução remota de código na *expression language* do RichFaces/JSF) não podia ser corrigida no fonte. A gente tinha que segurar o tranco no perímetro da infraestrutura: empilhando regras acrobáticas no Apache com `mod_security`, `mod_evasive`, `mod_ratelimit` e bloqueando na marreta as URLs que disparavam os erros.

> 🙈🙉🙊 *Desabafo Sincero*: Que fique claro: este post não tem o objetivo de apontar dedos ou falar mal de pessoas específicas. O foco aqui é expor a sucessão infinita de processos tortos e decisões arquiteturais que transformavam a gestão de infraestrutura em uma dança de forró em salão encerado segurando uma bandeja de copos de cerveja empilhados. Rir dos nossos traumas do passado é a única forma de não repeti-los em produção.

Muito do que sou hoje como sysadmin, analista de infraestrutura e de DevOps nasceu desse batismo de fogo. Foi precisando inventar soluções e diagnósticos para as bizarrices desse sistema que aprendi, na marra, o valor de cada boa prática de engenharia.

Anos mais tarde, quando me deparei pela primeira vez com o manifesto dos **12-Factor App** [^1] criado pelos engenheiros do Heroku, tudo o que eu tinha sofrido na pele finalmente fez sentido.

Cada um daqueles doze fatores não era teoria acadêmica descolada da realidade. Cada linha era uma resposta direta a um pesadelo real que alguém, em algum lugar da história dos servidores, sofreu na pele às duas horas da manhã.

Vamos dissecar cada um dos doze fatores. Mas não do jeito asséptico dos manuais acadêmicos: vamos ver o princípio técnico e os pesadelos reais que acontecem quando você decide ignorá-lo

## I. Base de Código: Uma base de código rastreada, muitos deploys

O princípio é direto: deve haver uma única base de código rastreada em controle de versão (Git) para cada aplicação, e essa mesma base dá origem a múltiplos deploys (desenvolvimento local, homologação, produção). Se múltiplos serviços compartilham o mesmo código, esse código compartilhado deve ser extraído para uma biblioteca e versionado via gerenciador de dependências, nunca copiado e colado.

Sem uma base rastreada, você perde a capacidade de auditar o que mudou entre uma versão e outra, rastrear a origem de um bug ou sequer confirmar qual versão exata do código está rodando em produção neste momento. Cada deploy vira um ato de fé.

> 🤡 *O Circo de Horrores da Infra*: A gênese do nosso sistema acadêmico já era fruto de uma aberração de base de código: ele não nascera na empresa contratada, mas fora herdado de outra universidade. A terceirizada fora contratada para "customizar" o código para a nossa realidade. Como não havia pipeline nem governança de repositório, o controle de versão virou ficção científica. As versões eram entregues como arquivos `.zip` anexados em chamados, com nome poético como `sistema_academico.war` todas as vezes.
>
> Certa vez, a empresa substituiu o arquivo em produção copiando o `.war` quebrado diretamente por cima do antigo no servidor. Sem histórico, sem commit, sem volta. O pânico foi tão generalizado que precisei criar um repositório Git local dentro do servidor de aplicação só para versionar os binários compilados que eles nos enviavam, porque o arquivo anterior tinha ido de arrasta pra cima.

No mundo moderno, a regra é clara: uma aplicação, um repositório.

Se você está construindo uma aplicação, seja ela web, desktop, monolítica ou modular, ela reside em seu repositório Git. O que muda de desenvolvimento para produção não é o código-fonte, mas o ambiente no qual o mesmo artefato é executado. Monorepos modernos (com ferramentas como Nx ou Cargo workspaces) são válidos, desde que cada serviço independente tenha seu próprio ciclo de deploy isolado e suas bibliotecas compartilhadas tratadas como dependências internas explícitas.

## II. Dependências: Declare e isole explicitamente as dependências

Uma aplicação 12-factor nunca presume a existência implícita de pacotes ou ferramentas instaladas globalmente no sistema operacional hospedeiro. Todas as dependências devem ser declaradas de ponta a ponta através de um manifesto de dependências (`pom.xml` no Maven, `mix.exs` no Elixir, `package.json` no Node) e isoladas durante a execução.

Quando dependências são implícitas, você perde a capacidade de recriar o ambiente do zero. O servidor vira um artefato artesanal insubstituível: se a máquina morrer, ninguém sabe quais pacotes foram instalados na mão, quais versões de bibliotecas nativas estão no `/usr/lib` e quais variáveis de ambiente foram configuradas por tentativa e erro ao longo dos anos.

> 🤮 *Traumas Não Superados*: O sistema do nosso causo tinha uma dependência central cujo código-fonte simplesmente foi perdido no tempo pela empresa desenvolvedora. Eles tinham apenas um arquivo `.jar` obscuro. Quando a JVM precisou ser atualizada, o jar parou de carregar. A solução da equipe de desenvolvimento? Descompilaram o binário na força bruta, alteraram meia dúzia de instruções no arquivo `.class` gerado e empacotaram de volta sem testes. Ninguém no planeta sabia exatamente o que aquela biblioteca fazia, mas ela ficava solta na pasta `/lib` global do JBoss junto com jars do RichFaces e do JSF (pra citar esses em específico). Se o servidor fosse recriado do zero, o sistema morria sem deixar pistas.

Em aplicações contemporâneas, o isolamento ocorre em duas camadas:

1. **Na linguagem:** O Maven Wrapper (`./mvnw`) ou o Mix do Elixir garantem que as bibliotecas sejam baixadas com versões travadas e integridade checada via hash.
2. **No sistema operacional:** O uso de imagens de contêiner OCI (Docker/Podman) empacota o runtime exato, bibliotecas de suporte e fontes tipográficas. A máquina host não precisa ter nada além do runtime de contêineres.

Se a sua aplicação precisa do `curl` ou do `imagemagick` para rodar, isso deve estar declarado na receita da sua instalação, e não instalado na base do `sudo apt-get install` na mão dentro do servidor de produção.

## III. Configurações: Armazene as configurações no ambiente

A configuração de uma aplicação é tudo aquilo que varia entre ambientes de deploy: credenciais de banco de dados, chaves de API, URLs de serviços externos e portas de escuta. O 12-factor exige uma separação estrita: **o código é estático e público; a configuração é dinâmica e fornecida pelo ambiente**.

O teste definitivo para saber se você cumpre esse fator é simples: *você poderia abrir o código-fonte do seu projeto no GitHub agora mesmo, como repositório público, sem vazar nenhuma senha ou comprometer a segurança da infraestrutura?*

> 😵💫 *O Malabarismo do Caos*: No nosso querido monólito, a configuração era um festival de horrores. Havia senhas de banco de dados em texto puro dentro de arquivos XML no meio do pacote compilado. Mas a maior bizarrice vinha dos relatórios: para renderizar o logotipo da instituição no cabeçalho dos PDFs gerados pelo JasperReports, o sistema não lia a imagem do disco local. Ele fazia uma requisição HTTP via URL absoluta para o próprio servidor (`http://[IP_ADDRESS]/img/logo.png`), e esse IP ficava gravado dentro de uma tabela de configurações no banco de dados. Quando migramos as VMs para a AWS EC2 com outra faixa de IP, a emissão de históricos escolares travou o servidor inteiro com timeouts de rede até descobrirmos essa pérola.

Nas arquiteturas modernas, a regra é consumir variáveis de ambiente do sistema operacional:

* **Spring Boot:** Mapeia variáveis de ambiente diretamente nas chaves do YAML através do mecanismo de interpolação `${DB_URL:jdbc:postgresql://localhost:5432/nome_do_banco}`.
* **Elixir:** Utiliza `System.fetch_env!("DATABASE_URL")` no arquivo `config/runtime.exs`, avaliado em tempo de execução no boot da release.
* **Kubernetes:** Injeta esses valores através de `ConfigMaps` para parâmetros gerais e `Secrets` criptografados para credenciais sensíveis.

O mesmo artefato binário compilado no seu pipeline de CI deve ser capaz de rodar na sua máquina, no cluster de testes e na nuvem, sem recompilar uma única linha.

## IV. Serviços de Apoio: Trate serviços de apoio como recursos anexados

Serviços de apoio (*backing services*) são todos os recursos externos que a aplicação consome pela rede durante sua operação normal: bancos de dados relacionais (PostgreSQL, MariaDB), filas de mensageria (RabbitMQ, Kafka), servidores SMTP e caches em memória (Redis).

Para a aplicação, não deve haver distinção entre um banco local rodando em contêiner na máquina do desenvolvedor e um banco gerenciado em nuvem (como o AWS RDS ou Google Cloud SQL). Ambos são apenas recursos anexados acessíveis via URL e credenciais fornecidas pela configuração.

```
[ Aplicação Web ] 
       │
       ├───> (URL: postgres://...) ─────> [ Banco de Dados PostgreSQL ]
       ├───> (URL: redis://...) ────────> [ Cache Redis ]
       └───> (URL: amqp://...) ─────────> [ Fila RabbitMQ ]
```

> 💀 *Crônicas do Apocalipse*: No nosso querido monólito, o conceito de tratar serviços de apoio como recursos desacoplados simplesmente não existia. Para armazenamento de arquivos, em vez de usar um storage de objetos anexado via rede, os uploads eram gravados como campos BLOB gigantescos direto dentro do banco de dados relacional. Em pouco tempo, descobrimos usuários subindo arquivos de centenas de megabytes e até vários gigabytes dentro das tabelas: imagens ISO, vídeos, coleções inteiras de documentos. O banco relacional virou um depósito de entulho digital, transformando qualquer rotina de backup em uma verdadeira sessão de tortura.
>
> Para piorar, para compartilhar arquivos estáticos entre as instâncias, alguém montou um compartilhamento NFS de rede diretamente dentro do diretório de deploy do JBoss. Quando a rede oscilava e o NFS caía silenciosamente, as instâncias travavam uma a uma em cascata com erros bizarros de I/O.

Tratar serviços como recursos anexados dá a você o poder do **desacoplamento**: se o banco principal falhar, você deve ser capaz de apontar a aplicação para uma réplica promovida apenas alterando a variável de ambiente `DATABASE_URL`, sem tocar no código e sem reiniciar a esteira de build.

## V. Construa, Lance, Execute: Separe estritamente os estágios de build, release e run

O ciclo de vida de uma entrega de software deve ser dividido em três etapas rigorosamente separadas e unidirecionais:

1. **Construção (*Build*):** O código-fonte é transformado em um artefato binário executável (compilação de bytecode, download de dependências, empacotamento do JAR ou da release OTP do Elixir).
2. **Lançamento (*Release*):** O artefato gerado no *Build* é combinado com as configurações específicas do ambiente de destino, recebendo um identificador único e imutável (como uma tag semântica ou o hash do commit).
3. **Execução (*Run*):** O processo da aplicação é iniciado no ambiente operacional a partir da *Release* gerada.

```
┌───────────────┐      ┌───────────────────┐      ┌────────────────┐
│     BUILD     │ ───> │      RELEASE      │ ───> │      RUN       │
│ Código + Libs │      │ Build + Configs   │      │ Execução em    │
│ (Artefato)    │      │ (Versão Imutável) │      │ Produção       │
└───────────────┘      └───────────────────┘      └────────────────┘
```

> 🤡 *Gambiarras que a Vida Ensina*: Como não tínhamos pipeline, o nosso *release* era um trabalho manual de artesanato. Para conseguir voltar atrás quando as coisas explodiam, criei uma estratégia com links simbólicos no Linux: o arquivo físico recebia o nome `sistema_vX.Y.Z_cti_AAAAMMDDHHmm.war` e eu criava um link simbólico `ln -sf` apontando `sistema_academico.war` para ele. Eram cinco módulos e nove bibliotecas interconectadas gerenciadas na base do `ln` e de um script bash caseiro. Esse era o melhor jeito que tínhamos para voltar para uma versão anterior sem precisar fazer deploy novamente.
>
> E era feito geralmente à noite para não atrapalhar o funcionamento do sistema. Lembro de uma vez que foi preciso fazer isso durante o lançamento de notas de alunos, e os professores ligando desesperados porque não conseguiam lançar as notas. Foi tenso. Um erro de digitação no terminal e metade dos módulos apontava para a versão de agosto e a outra metade para a versão de maio. Tivemos que parar o sistema por um tempo para corrigir.

A regra fundamental aqui é a **imutabilidade**. É estritamente proibido alterar código diretamente em tempo de execução (*runtime*). Se você precisa aplicar uma correção rápida (*hotfix*), ela deve nascer como um commit no repositório, passar pelo estágio de build, gerar uma nova release e ser implantada formalmente.

## VI. Processos: Execute a aplicação como um ou mais processos que não armazenam estado

Os processos da aplicação devem ser **completamente sem estado (*stateless*) e não compartilhar nada (*share-nothing*)**. Qualquer dado que precise persistir além do ciclo de vida de uma única requisição HTTP deve ser gravado em um serviço de apoio com estado (banco de dados ou cache distribuído).

A memória do processo ou o sistema de arquivos local podem ser usados apenas como rascunho temporário e volátil durante a execução de uma operação única. Nunca presuma que algo gravado na memória no request A estará disponível no request B.

> 😵 *Sessões Fantasmas e o Pânico dos Professores*: Nosso JBoss distribuía sessões HTTP através de replicação de memória entre as instâncias e o famigerado `mod_jk` no Apache. Quando um professor estava lançando as notas finais de quinhentos alunos e o balanceador de carga decidia alternar o tráfego para a outra VM, a sincronização de sessão em memória falhava miseravelmente. O resultado? O professor era sumariamente desconectado no meio do lançamento, perdia todas as notas digitadas e a diretoria de TI recebia ligações em chamas.
>
> A culpa não era dos professores: era da arquitetura que insistia em guardar estado dentro da memória volátil do processo em vez de delegar para um cache compartilhado.

Em arquiteturas modernas:
* Sessões de autenticação usam tokens criptografados e autocontidos (JWT) ou são armazenadas em instâncias de Redis compartilhadas.
* Uploads de arquivos são enviados diretamente para storages de objetos (como AWS S3, MinIO ou Google Cloud Storage), nunca salvos como campos BLOB que explodem o tamanho do banco relacional nem jogados na pasta `/tmp` do servidor local.

Isso permite que você destrua, reinicie ou multiplique processos sem que nenhum usuário final perceba qualquer instabilidade.

## VII. Vínculo de Porta: Exporte serviços por ligação de porta

A aplicação 12-factor é **completamente autocontida**. Ela não depende da injeção de um servidor web ou de um servidor de aplicações externo (como os antigos containers Tomcat, JBoss ou WebLogic compartilhados que eram instalados e configurados manualmente pela equipe de infraestrutura).

A própria aplicação inclui seu servidor web embutido como dependência de biblioteca e escuta requisições vinculando-se diretamente a uma porta de rede (geralmente informada pela variável de ambiente `PORT` ou configurada no arquivo base).

```
[ Requisição HTTP ] ──> Porta 8080 ──> [ Processo da Aplicação (com Tomcat Embutido) ]
```

> 🤡 *O Labirinto do AJP e DNS Round Robin*: Nossa aplicação não escutava diretamente em uma porta de forma autocontida. Para colocar o sistema no ar, dependíamos de uma teia maluca: quatro instâncias de JBoss rodando em duas VMs, comunicando-se via protocolo binário proprietário AJP com dois servidores Apache com `mod_jk`, que por sua vez eram balanceados na base da sorte através de Round Robin no DNS.
>
> Qualquer oscilação em um desses intermediários gerava telas de erro 500 bizarras que ninguém sabia em qual camada do labirinto haviam sido geradas. Era um verdadeiro pesadelo. Foram tantas quedas que a turma de TI até criou uma gíria interna: quando o sistema estava instável, diziam que ele estava em **"modo mistério"**, porque ninguém conseguia diagnosticar a causa real da instabilidade.

No ecossistema Java moderno, o Spring Boot faz exatamente isso ao embarcar o Tomcat, Jetty ou Undertow dentro do `.jar` executável gerado pelo Maven. No Elixir, o servidor HTTP (Bandit ou Cowboy) é iniciado como parte da árvore de supervisão da própria aplicação Phoenix.

Essa autonomia elimina a clássica disputa entre times: *"o problema não é no meu código, é na versão do JBoss que a infraestrutura instalou"*. A aplicação carrega seu próprio motor de execução.

## VIII. Concorrência: Dimensione através do modelo de processos

Quando a carga de acessos aumenta, como a sua aplicação escala? A resposta tradicional dos servidores monolíticos legados era aumentar a máquina virtual: colocar mais memória RAM, mais núcleos de CPU e torcer para o garbage collector da JVM não congelar a aplicação durante coletas longas (a famosa escala vertical).

O 12-factor dita que a escala deve acontecer **horizontalmente através do modelo de processos**. Aplicações devem ser divididas em tipos de processos especializados conforme o perfil da carga de trabalho:

* **Processos Web:** Responsáveis por receber requisições HTTP rápidas e responder com payloads JSON ou HTML.
* **Processos Worker:** Responsáveis por processar tarefas pesadas e demoradas em segundo plano consumindo mensagens de uma fila (envio de e-mails em massa, geração de relatórios, processamento de vídeos).
* **Processos Clock / Cron:** Responsáveis por disparar eventos periódicos e agendamentos.

```
                  ├───> [ Processo Web 1 ]
[ Load Balancer ] ├───> [ Processo Web 2 ]
                  └───> [ Processo Web 3 ]

                  ├───> [ Worker de Filas 1 ]
[ Fila RabbitMQ ] └───> [ Worker de Filas 2 ]
```

> 🤮 *O Método de Login com 200 Parâmetros e o Botão Proibido*: No nosso monólito, a concorrência não era apenas ineficiente; ela era uma autodestruição programada de memória. Havia um método no sistema, acionado na tela de LOGIN (no simples ato de fazer login), cuja assinatura ostentava mais de **duzentos parâmetros**. Essa aberração fazia uma varredura tão profunda no banco que o primeiro login de um usuário alocava quase **2 GB** direto na memória da JVM para checar memorandos e avisos de qualquer perfil (de aluno a diretor).
>
> Para piorar, processos pesados de negócio rodavam síncronos na mesma thread HTTP: a funcionalidade de "depreciação de bens" no patrimônio tinha um aviso espiritual em letras garrafais colado na mente de todos: "não clica na ***** dessa funcionalidade", porque o cálculo demorava tanto que a página do RichFaces expirava o timeout e o processo era interrompido no meio da execução, deixando os saldos contábeis do patrimônio corrompidos pela metade.

Se o número de requisições web explodir, você escala apenas os processos web. Se a fila de relatórios estiver acumulada, você adiciona mais instâncias de workers sem sobrecarregar o tráfego HTTP dos usuários. 

No Kubernetes, isso se traduz diretamente em múltiplos `Deployments` (ou mesmo `StatefulSets`) independentes apontando para a mesma imagem de contêiner, mas executando comandos de inicialização diferentes.

## IX. Descartabilidade: Maximize a robustez com inicialização rápida e desligamento gracioso

Os processos da aplicação devem ser **descartáveis**: eles podem ser iniciados ou desligados a qualquer momento sem aviso prévio. Isso exige duas características vitais:

1. **Inicialização rápida (*Fast Startup*):** O processo deve levar poucos segundos do momento em que o binário é chamado até estar pronto para receber tráfego real. Inicializações rápidas permitem deploys contínuos sem indisponibilidade e elasticidade real em autoscaling.
2. **Desligamento gracioso (*Graceful Shutdown*):** Ao receber um sinal de término do sistema operacional (`SIGTERM`), o processo deve parar de aceitar novas requisições, concluir com calma as transações que já estão em andamento, liberar conexões de banco de dados e sair limpamente com código zero.

> 💀 *O Ritual Místico de Inicialização*: O boot do nosso servidor legado levava inacreditáveis **quinze minutos por instância**. E não parava por aí: havia uma ordem mística de subida. Primeiro a VM 1, Instância 1. Você tinha que abrir o log no terminal, esperar ela emitir uma mensagem específica de inicialização, e só então subir a Instância 2 da VM 1, para depois repetir o processo na VM 2, porque todas as instâncias dependiam da primeira para bootstrap. Reiniciar o cluster em um incidente era uma operação de uma hora de tela travada e stress.

Em ambientes modernos de contêineres e orquestração (como o Kubernetes), os pods são destruídos e recriados constantemente por balanceamento de nós ou políticas de autoscaling. Se a sua aplicação não respeitar o `SIGTERM` ou demorar minutos para subir, o orquestrador matará o processo com `SIGKILL` forçado, derrubando requisições de clientes no meio do caminho.

## X. Paridade Dev/Prod: Mantenha desenvolvimento, homologação e produção o mais idênticos possível

Historicamente, existiam abismos gigantescos entre o ambiente de desenvolvimento e o de produção:

* **Abismo de tempo:** O código levava meses para sair da máquina do desenvolvedor e chegar aos servidores reais.
* **Abismo de equipe:** Desenvolvedores escreviam código; operadores de infraestrutura tentavam fazer o código rodar em produção.
* **Abismo de ferramentas:** O desenvolvedor usava SQLite ou H2 no Windows; a produção rodava PostgreSQL ou Oracle no Linux.

O 12-factor exige **paridade máxima**: reduza o intervalo de deploy para horas ou minutos, faça os próprios autores do código participarem da operação e use rigorosamente os mesmos serviços de apoio em todos os ambientes.

> 🤡 *O Clone Sagrado de 400 GB*: A paridade do sistema antigo era resolvida da pior forma possível: para criar um ambiente de testes, a equipe clonava a imagem inteira da máquina virtual de produção no hipervisor (uma VM colossal de mais de 400 GB). Como ninguém sabia como instalar o sistema do zero, essa era a única maneira de ter um ambiente "parecido". Mas como os testes eram feitos alterando dados diretamente dentro dessa cópia, o ambiente de desenvolvimento rapidamente apodrecia e ficava tão corrompido que os bugs testados lá não tinham relação nenhuma com a realidade de produção.

Hoje, ferramentas como o **Docker Compose** e o **Testcontainers** sepultaram a desculpa do *"na minha máquina funciona"*. 

Você não precisa mais usar um banco H2 em memória nos testes para depois descobrir que o dialeto SQL do PostgreSQL em produção rejeitou a sua query. Você sobe o mesmo PostgreSQL, no mesmo container, com a mesma versão, tanto no laptop do desenvolvedor quanto no cluster de produção.

## XI. Logs: Trate logs como fluxo de eventos

A aplicação **nunca deve se preocupar com o roteamento, armazenamento ou rotação dos seus arquivos de log**. Ela não deve escrever em arquivos físicos como `/var/log/app.log` nem tentar gerenciar políticas de rotação de log dentro do código.

Em vez disso, cada processo escreve seu fluxo de eventos de forma contínua e sem buffer diretamente na saída padrão (`stdout`) e na saída de erro (`stderr`).

Durante o desenvolvimento local, o programador visualiza esse fluxo impresso diretamente em seu terminal. Em ambientes de produção e homologação, o ambiente de execução (Docker, systemd, Kubernetes) captura esses fluxos de `stdout` e os encaminha para plataformas especializadas de roteamento e indexação (como Vector, Fluentbit, Loki, Elasticsearch ou Datadog).

> 😵 *A Partição /var em Chamas*: No nosso sistema de estimação, o Log4j gerenciava arquivos de log locais com rotação diária (e não por tamanho). Em épocas de matrícula ou lançamento de notas, a verbosidade configurada em `INFO` gerava dezenas de gigabytes por dia. Como o processo frequentemente travava a rotina de exclusão de arquivos antigos, a partição `/var` do servidor lotava 100% de espaço em disco com frequência estarrecedora. O resultado? O sistema caía porque não conseguia mais alocar descritores de arquivo. Chegamos ao ponto humilhante de ter um lembrete fixo na agenda diária da equipe de infraestrutura: "Entrar no servidor pela manhã e apagar logs antigos na mão".

Logs são **fluxos contínuos de eventos ordenados no tempo**, e não arquivos estáticos sob responsabilidade do desenvolvedor. A aplicação emite; a infraestrutura coleta e agrega.

## XII. Processos Administrativos: Execute tarefas de administração e manutenção como processos pontuais

Tarefas administrativas pontuais (como migrações de esquema de banco de dados com Flyway ou Ecto, execução de rotinas de higienização de dados em lote ou scripts de correção emergencial) devem ser executadas como **processos únicos e descartáveis (*one-off processes*)**.

Esses processos devem rodar exatamente no mesmo ambiente, com a mesma release e com as mesmas configurações da aplicação principal. O código dessas tarefas deve ser versionado junto com o código da aplicação para evitar discrepâncias entre o que o script assume e o que o modelo de dados realmente suporta. Isso inclui rotinas de recálculo, consolidação de relatórios e qualquer tarefa de manutenção que precise operar sobre os mesmos dados e regras de negócio da aplicação principal.

> 💀 *O DBA Acidental e a Normalização -1000*: Na época do nosso sistema acadêmico, além de analista de infraestrutura, acabei virando o "DBA acidental" da instituição por pura falta de opção. Cada atualização vinha acompanhada de um script SQL gigantesco enviado por e-mail, escrito à mão pelos desenvolvedores. Cabia a mim abrir o pgAdmin conectado diretamente no banco de produção, colar centenas de linhas de `ALTER TABLE` e `UPDATE` e torcer para o script não quebrar na metade. Como os scripts frequentemente falhavam por erros de sintaxe ou violação de constraints, tirar um snapshot completo da VM do banco antes de cada execução era uma questão de pura autopreservação.
>
> A mitologia institucional contava ainda que a migração inicial dos dados consistira em exportar o banco antigo para uma única planilha colossal com normalização na escala -1000: um atentado relacional tão brutal que faria Edgar Codd e Martin Fowler caírem de joelhos querendo a nossa pele. No dia a dia, o setor de almoxarifado precisava seguir um roteiro manual de recálculos para fazer o Relatório Mensal de Almoxarifado (RMA) fechar as contas no final do mês, porque as rotinas internas do sistema erravam os saldos com tanta frequência que ninguém confiava mais nelas. E quando alguém acidentalmente rodava a famigerada depreciação de bens e corrompia os registros, o processo de correção via scripts manuais no banco era tão excruciante e tedioso que a solução definitiva adotada foi simplesmente proibir o uso da funcionalidade.

Em aplicações modernas, tarefas administrativas são processos formais: migrações de banco rodam via Flyway ou Ecto em esteiras de CI/CD, correções de dados são scripts versionados executados como Jobs no Kubernetes, e rotinas de consolidação rodam como workers dedicados com auditoria de execução.

## O tratado de paz entre desenvolvimento e operações

Quando você analisa os 12 fatores em conjunto, percebe que eles não tratam de uma linguagem ou framework específico. Eles tratam de **contratos de convivência**.

Aplicações que violam os 12 fatores exigem equipes de operações heroicas, daquelas que passam madrugadas em claro aplicando correções manuais, monitorando espaços em disco com planilhas, operando WAFs no desespero para tapar buracos de frameworks abandonados e rezando para que uma máquina virtual antiga nunca desligue.

Aplicações que seguem os 12 fatores são previsíveis, portáveis e modulares. Elas nascem prontas para o fluxo natural de esteiras modernas: compilam limpo, configuram-se organicamente com variáveis de ambiente e escalam sem atrito em qualquer cluster.

Depois de passar anos como refém de um monólito em chamas, minha visão sobre arquitetura mudou para sempre: não construa catedrais frágeis de arquivos copiados à mão. Projete processos descartáveis, transparentes e resilientes. A sua equipe de operações (e o seu próprio sono de fim de semana) agradecerão.

## Referências

[^1]: **The Twelve-Factor App** {*Adam Wiggins / Heroku*} ([Link](https://12factor.net/pt_br/))

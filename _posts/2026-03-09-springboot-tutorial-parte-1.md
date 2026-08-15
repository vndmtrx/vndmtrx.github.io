---
layout: post
title: "Spring Boot Tutorial, Parte 1 - Ambiente"
subtitle: "Construindo o ambiente de desenvolvimento"
author:
- "Eduardo N. S. R."
date: 2026-03-09 11:20:00 GMT-3
modified_date: 2026-05-10 09:49:00 GMT-3
permalink: /posts/spring-boot-tutorial-parte-1-ambiente/
tags: [Spring Boot, Java]
series: Spring Boot Tutorial
---

E se de repente a gente decidisse escrever um tutorial de Spring Boot? Pois é, eu decidi começar essa seara de estudo do framework pela parte que ninguém liga, mas que geralmente é a que quebra tudo quando não é feito do jeito certo: o ambiente de desenvolvimento. Parece bobo, mas sem ele sólido desde o começo, o resto vira dor de cabeça infinita.

> 🔔 *Nota da Série*: Este post faz parte da série **"Spring Boot Tutorial"**, onde eu construo, passo a passo, uma API backend moderna usando **Spring Boot**. Aqui o foco é o backend: modelagem, persistência, resiliência, testes, observabilidade e deploy. A linguagem usada no projeto será Java, versão 25+. O frontend vem depois, quando a API estiver bem cuidada por dentro.

Nos últimos anos eu venho me focando mais na área de segurança, infraestrutura e de DevOps na maior parte dos projetos em que eu participo. Isso inclui migrações para nuvem, deploy de serviços com automação e gerenciamento de esteiras de deploy automatizado, na maioria dos casos diretamente com VMs e mais recentemente com contêineres. Dito isso, desenvolvimento nunca foi um forte na minha vida profissional, mas uma coisa sempre me incomodou nisso, que é a forma como vários projetos eram desenvolvidos.

A inspiração pra este projeto veio da série de posts [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world), do Miguel Grinberg, uma série que sempre admirei pela forma progressiva e prática com que ensina. A ideia aqui é trazer esse mesmo espírito “aprenda fazendo”, mas no universo do Spring Boot, enfatizando boas práticas de backend moderno, observabilidade e automação.

Eu sei que vcs vão dizer que eu por ser de infra vou sempre ter uma visão diferente do dev, e vcs não estão errados. E é por isso que estou me propondo a fazer essa série de posts. Minha ideia é aprender ao mesmo tempo que vou documentando as várias coisas que eu aprendi nas minhas áreas de trabalho com esse estudo de uma nova linguagem, um novo framework, para começar.

A ideia aqui, com essa série, é que você consiga acompanhar desde o ambiente de desenvolvimento, passando por banco, segurança, cache, testes, observabilidade, até chegar em Docker e Kubernetes, vendo os trade-offs e as pequenas decisões que normalmente ficam escondidas nos tutoriais bonitinhos, e para isso eu decidi criar uma aplicação clássica do tipo TODO, onde a parte da complexidade da solução é deixada de lado para focarmos efetivamente no uso das tecnologias na melhoria do projeto.

Eu queria começar essa série de posts pela parte "menos glamourosa" do projeto: o ambiente de desenvolvimento. Não é banco, não é Redis, não é Kubernetes. É só... deixar o editor e o runtime do Java pronto. E mesmo assim, quase todo projeto que vejo tropeça exatamente nessa etapa (ou intui que o usuário já tem um ambiente bem definido).

E por que disso? Porque na maioria das vezes a gente perde tempo com o clássico *"Na minha máquina funciona"* (quando alguém desenvolve em Java 17 enquanto o servidor roda Java 11), com a falta de reprodutibilidade das builds no CI, ou com conflitos gerados por configurações díspares entre quem usa IntelliJ e quem usa VS Code.

Nada do que vou propor aqui é revolucionário. É só uma sugestão minha para começar algo de forma padronizada. Todos vcs são livres para fazer como quiserem (ou mesmo não fazer), mas não vão poder reclamar depois.

Dada essa fala inicial, vamos efetivamente ao texto.

## Preparando o Ambiente Base: Debian e SDKMAN

Então, a primeira coisa que vamos pensar: qual sistema operacional? Não vou me alongar aqui, pois cada um tem sua opção. Eu irei focar tudo em **Debian Trixie**, pois é geralmente meu ambiente de trabalho base.

A primeira coisa que eu faço aqui é instalar o **SDKMAN** [^1]. Ele é um gerenciador de SDKs do ambiente do Java que permite, entre outras coisas, vc ter várias versões diferentes do mesmo software. A instalação é simples de boba:

```bash
$ curl -s "https://get.sdkman.io" | bash
# Instala o sdkman usando o formato recomendado pelo projeto

$ source "$HOME/.sdkman/bin/sdkman-init.sh"
# Ajusta o ENV para já poder usar o sdkman após a instalação (sem precisar reiniciar o perfil de usuário)
```

A instalação das versões do Java seguem uma dinâmica super simples:

```bash
$ sdk install java 26-tem
# Baixa e instala a versão Temurin 26 do Java

$ sdk default java 26-tem
# Define o Java 26 (Temurin) como versão padrão global para todos os shells

$ java --version
# Confirma se a versão configurada é a esperada
```

Você pode instalar outras versões concomitantes e usar elas de forma bem simples, conforme o shell abaixo:

```bash
$ java --version
# Exibe a versão Java atualmente configurada
openjdk 26 2026-03-17
OpenJDK Runtime Environment Temurin-26+35 (build 26+35)
OpenJDK 64-Bit Server VM Temurin-26+35 (build 26+35, mixed mode, sharing)

$ sdk use java 25-tem
# Troca temporariamente para a versão 25 apenas nesta sessão

$ java --version
# Mostra a nova versão ativa na sessão atual
openjdk 25 2025-09-16 LTS
OpenJDK Runtime Environment Temurin-25+36 (build 25+36-LTS)
OpenJDK 64-Bit Server VM Temurin-25+36 (build 25+36-LTS, mixed mode, sharing)
```

No primeiro caso, foi definido o Java 26 como versão padrão para todo o usuário, e no segundo caso o Java 25 foi definido somente para aquela sessão de shell, voltando ao 26 após fechar e abrir novamente.

No fim do dia, apesar de simples, não é muito prático ficar trocando o SDK toda vez que mudar de projeto, e para isso o SDKMAN possui uma funcionalidade de configuração de ambiente:

```bash
$ sdk env init
# Cria um arquivo .sdkmanrc no diretório atual para definir versões específicas por projeto

$ cat .sdkmanrc 
# Enable auto-env through the sdkman_auto_env config
# Add key=value pairs of SDKs to use below
java=26-tem
```

Isso permite que os comandos de shell rodados no escopo do projeto sempre usem a versão Java correta e inclusive a instalação das dependências com o comando `sdk env install`.

É importante citar também que não precisa ser só o Java. O Sdkman tem vários runtimes para instalar, como o SpringBoot, o Gradle, o Maven, entre outros. Você pode ver usando o comando `sdk list`, que irá mostrar todos os runtimes disponíveis.

Feito isso, e após a configuração do ambiente base pelo script de instalação, estamos prontos para a próxima etapa.

### Instalação do VS Codium

Agora que temos o JDK sob controle, a próxima opção nossa é o Editor de Código. Aqui eu vou sugerir o uso do VS Codium, só pq ele é Open Source e livre das telemetrias da Micro$oft. Além de tudo ele é leve e fácil de mexer.

No **Debian Trixie**, a instalação é super fácil:

```bash
$ sudo extrepo enable vscodium
# Habilita o repositório externo do VS Codium no Debian

$ sudo apt update && sudo apt install codium
# Atualiza a lista de pacotes e instala o editor VS Codium
```

Feito isso, o VS Codium está instalado. Eu vou inclusive sugerir a instalação de algumas extensões que eu pretendo usar, que serão muito úteis no andamento desse Tutorial:

```bash
$ codium --install-extension MS-CEINTL.vscode-language-pack-pt-BR
# Adiciona o pacote de idioma em português (tradução da interface)

$ codium --install-extension vscjava.vscode-java-pack
# Instala o pacote oficial de ferramentas Java para desenvolvimento

$ codium --install-extension VMware.vscode-boot-dev-pack
# Instala o Spring Boot Pack, com suporte a inicialização de projetos e depuração
```

Com essas extensões instaladas, o Codium já traz autocompletar, debug e suporte ao Spring Boot prontos para uso.

### Um test-drive rápido com o JShell

Antes de encerrarmos, como já instalamos o Java, que tal um teste rápido? A partir do Java 9 a linguagem passou a contar com o **JShell** [^2], um REPL (Read-Eval-Print Loop) que permite executar código Java de forma interativa sem a necessidade de criar classes ou compilar arquivos.

Isso é extremamente útil para explorar APIs, testar pequenos algoritmos ou validar comportamentos da linguagem antes de colocá-los no projeto de fato. Para brincar um pouco, abra seu terminal e digite `jshell`:

```bash
$ jshell
|  Welcome to JShell -- Version 26
|  For an introduction type: /help intro

jshell> var saudacao = "Olá, Spring Boot e JShell!"
saudacao ==> "Olá, Spring Boot e JShell!"

jshell> System.out.println(saudacao.toUpperCase())
OLÁ, SPRING BOOT E JSHELL!
```

Um outro exemplo é o uso de `records`, que entraram no Java 16 e são estruturas imutáveis muito úteis para DTOs. Aqui podemos declarar e testar um diretamente no console:

```bash
jshell> record Todo(int id, String titulo, boolean concluido) {}
|  created record Todo

jshell> var tarefa = new Todo(1, "Aprender Spring Boot", false)
tarefa ==> Todo[id=1, titulo="Aprender Spring Boot", concluido=false]

jshell> tarefa.titulo()
$5 ==> "Aprender Spring Boot"
```

E para fechar, o JShell permite carregar bibliotecas externas (JARs) ou o diretório de classes do seu próprio projeto para dentro da sessão. Isso será fundamental lá na frente, quando quisermos interagir com os serviços e os *Beans* do Spring Boot diretamente no console.

Para carregar libs externas, usamos o comando `/env -class-path`. Como ainda não geramos a estrutura do nosso projeto Spring Boot, se tentarmos passar uma pasta de `build` agora, o JShell retornará um erro. Para fins de demonstração, vamos adicionar apenas o diretório atual (`.`) ao *classpath* da nossa sessão e, em seguida, importar a API de datas do Java para trabalhar:

```bash
jshell> /env -class-path .
|  Setting new options and restoring state.

jshell> import java.time.format.DateTimeFormatter

jshell> var formatador = DateTimeFormatter.ofPattern("dd/MM/yyyy")
formatador ==> Value(DayOfMonth,2)'/'Value(MonthOfYear,2)'/'Value(YearOfEra,4,19,EXCEEDS_PAD)

jshell> System.out.println("Projeto iniciado em: " + java.time.LocalDate.now().format(formatador))
Projeto iniciado em: 10/05/2026

jshell> /exit
|  Goodbye
```

Esse modelo de testar código interativamente reflete uma cultura muito forte em outras linguagens (como Python, Ruby ou Lisp) conhecida como **REPL-Driven Development** ou, mais informalmente, um desenvolvimento orientado a *tinkering* (experimentação contínua). 

Em vez de escrevermos um bloco enorme de código, recompilar o projeto inteiro, subir um servidor pesado e torcer para funcionar, nós testamos pequenas hipóteses em tempo real. Saber "brincar" com a linguagem no terminal nos dá um ciclo de feedback absurdamente rápido. Conseguimos validar se uma API nativa funciona de um jeito específico, ou como um método se comporta, em questão de segundos.

Durante o andamento dessa série, expandiremos essa ideia além do console puro. Veremos como interagir de forma semelhante usando o **Spring Boot DevTools** [^3], ganhando agilidade parecida no ecossistema da nossa aplicação.

## Conclusão

Aqui chegamos ao final desse primeiro post, que é curto mas é para falar um pouco sobre a criação de ambientes iniciais.

Olhando o que montamos, vejo algo simples mas que resolve o essencial: reprodutibilidade. Não é sobre ter o editor mais caro ou a distro perfeita, mas criar um espaço onde o foco vai pro código: O Java sempre o esperado, a navegação fluida no Spring. É o tipo de base que, na prática, evita horas perdidas com *"na minha máquina roda"*, deixando energia pra decisões que realmente importam, que é o estudo do Spring Boot, e de como criar uma aplicação resiliente.

A internet já está cheia de tutoriais sobre Spring Boot (e LLMs que geram código inteiro num piscar de olhos). Então por que isso aqui? Pra mim, é forma de estudar: escrevendo pra outros, organizo ideias, testo na prática e descubro os bugs que não aparecem no `^C` / `^V`. Se ajudar alguém a pular uma armadilha ou repensar o setup, já valeu. Na Parte 2, iremos tratar do setup inicial do projeto no Spring Initializr e nosso primeiro endpoint.

## Referências

[^1]: **SDKMAN! Usage** {*SDKMAN!*} ([Link](https://sdkman.io/usage))

[^2]: **JShell User's Guide** {*Oracle*} ([Link](https://docs.oracle.com/en/java/javase/21/jshell/introduction-jshell.html))

[^3]: **Developer Tools** {*Spring Boot Reference*} ([Link](https://docs.spring.io/spring-boot/reference/using/devtools.html))

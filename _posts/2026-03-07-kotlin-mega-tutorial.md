---
title: "Spring Boot e Kotlin Mega Tutorial, Parte 1: Ambiente de desenvolvimento"
date: 2026-03-09 11:20:00
permalink: /posts/spring-boot-kotlin-mega-tutorial-parte-1-ambiente/
tags: Spring Boot, Kotlin, Backend, API
series: Spring Boot e Kotlin Mega Tutorial
---

> Este post faz parte da série **“Spring Boot e Kotlin Mega Tutorial”**, onde eu construo, passo a passo, uma API backend moderna usando **Spring Boot** e **Kotlin**.
> Aqui o foco é o backend: modelagem, persistência, resiliência, testes, observabilidade e deploy. O frontend vem depois, quando a API estiver bem cuidada por dentro.

Nos últimos anos eu venho me focando mais na área de segurança, infraestrutura e de DevOps na maior parte dos projetos em que eu participo. Isso inclui migrações para nuvem, deploy de serviços com automação e gerenciamento de esteiras de deploy automatizado, na maioria dos casos diretamente com VMs e mais recentemente com conteiners. Dito isso, desenvolvimento nunca foi um forte na minha vida profissional, mas uma coisa sempre me incomodou nisso, que é a forma como vários projetos eram desenvolvidos.

A inspiração pra este projeto veio da série de posts [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world), do Miguel Grinberg, uma série que sempre admirei pela forma progressiva e prática com que ensina. A ideia aqui é trazer esse mesmo espírito “aprenda fazendo”, mas no universo do Spring Boot com Kotlin, enfatizando boas práticas de backend moderno, observabilidade e automação.

Eu sei que vcs vão dizer que eu por ser de infra vou sempre ter uma visão diferente do dev, e vcs não estão errados. E é por isso que estou me propondo a fazer essa série de posts. Minha idéia é aprender ao mesmo tempo que vou documentando as várias coisas que eu aprendi nas minhas áreas de trabalho com esse estudo de uma nova linguagem, um novo framework, para começar.

A ideia aqui, com essa série, é que você consiga acompanhar desde o ambiente de desenvolvimento, passando por banco, segurança, cache, testes, observabilidade, até chegar em Docker e Kubernetes, vendo os trade-offs e as pequenas decisões que normalmente ficam escondidas nos tutoriais bonitinhos, e para isso eu decidi criar uma aplicação clássica do tipo TODO, onde a parte da complexidade da solução é deixada de lado para focarmos efetivamente no uso das tecnologias na melhoria do projeto.

Eu queria começar essa série de posts pela parte “menos glamourosa” do projeto: o ambiente de desenvolvimento. Não é banco, não é Redis, não é Kubernetes. É só... deixar o editor e o Java prontos. E mesmo assim, quase todo projeto que vejo tropeça exatamente nessa etapa (ou intui que o usuário já têm um ambiente bem definido).

E por que disso? Porque na maioria das vezes a gente perde um monte de tempo com coisas como:
- O clássico *“Na minha máquina funciona”* porque alguém tava fazendo tudo com Java 17 e o ambiente em si rodando com com Java 11;
- Falta de reprodutibilidade das builds dos softwares desenvolvidos, principalmente no CI;
- Ambientes de desenvolvimentos mistos. Pois sempre têm um usando um IntelliJ e outro usando um VS Code.

Nada do que vou propor aqui é revolucionário. É só uma sugestão minha para começar algo de forma padronizada. Todos vcs são livres para fazer como quiserem (ou mesmo não fazer), mas não vão poder reclamar depois.

Dada essa fala inicial, vamos efetivamente ao texto.

## Spring Boot e Kotlin Mega Tutorial: Ambiente de desenvolvimento

Então, a primeira coisa que vamos pensar: qual sistema operacional? Não vou me alongar aqui, pois cada um têm sua opção. Eu irei focar tudo em Debian trixie, pois é geralmente meu ambiente de trabalho base.

A primeira coisa que eu faço aqui é instalar o [SDKMAN](https://sdkman.io/). Ele é um gerenciador de SDKs do Java que permite, entre outras coisas, vc ter várias versões diferentes do mesmo software. A instalação é simples de boba:

```bash
$ curl -s "https://get.sdkman.io" | bash
# Instala o sdkman usando o formato recomendado pelo projeto

$ source "$HOME/.sdkman/bin/sdkman-init.sh"
# Ajusta o ENV para já poder usar o sdkman após a instalação (sem precisar reiniciar o perfil de usuário)
```

A instalação das versões do Java seguem uma dinâmica super simples:

```bash
$ sdk install java 24-tem
# Baixa e instala a versão Temurin 24 do Java

$ sdk default java 24-tem
# Define o Java 24 como versão padrão global do usuário

$ java --version
# Confirma se a versão configurada é a esperada
```

Você pode instalar outras versões concomitantes e usar elas de forma bem simples, conforme o shell abaixo:

```bash
$ sdk default java 24-tem
# Define o Java 24 (Temurin) como versão padrão global para todos os shells

$ java --version
# Exibe a versão Java atualmente configurada
openjdk 24 2025-03-18
OpenJDK Runtime Environment Temurin-24+36 (build 24+36)
OpenJDK 64-Bit Server VM Temurin-24+36 (build 24+36, mixed mode, sharing)

$ sdk use java 25-tem
# Troca temporariamente para a versão 25 apenas nesta sessão

$ java --version
# Mostra a nova versão ativa na sessão atual
openjdk 25 2025-09-16 LTS
OpenJDK Runtime Environment Temurin-25+36 (build 25+36-LTS)
OpenJDK 64-Bit Server VM Temurin-25+36 (build 25+36-LTS, mixed mode, sharing)
```

No primeiro caso, foi definido o Java 24 como versão padrão para todo o usuário, e no segundo caso o Java 25 foi definido somente para aquela sessão de shell, voltando ao 24 após fechar e abrir novamente.

No fim do dia, apesar de simples, não é muito prático ficar trocando o SDK toda vez que mudar de projeto, e para isso o SDKMAN possui uma funcionalidade de configuração de ambiente:

```bash
$ sdk env init
# Cria um arquivo .sdkmanrc no diretório atual para definir versões específicas por projeto

$ cat .sdkmanrc 
# Enable auto-env through the sdkman_auto_env config
# Add key=value pairs of SDKs to use below
java=24-tem
```

Isso permite que os comandos de shell rodados no escopo do projeto sempre usem a versão Java correta e inclusive a instalação das dependências com o comando `sdk env install`.

Feito isso, e após a configuração do ambiente base pelo script de instalação, estamos prontos para a próxima etapa.

### Instalação do VS Codium

Agora que temos o JDK sob controle, a próxima opção nossa é o Editor de Código. Aqui eu vou sugerir o uso do VS Codium, só pq ele é Open Source e livre das telemetrias da Micro$oft. Além de tudo ele é leve e fácil de mexer.

No Debian Trixie, a instalação é super fácil:

```bash
$ sudo extrepo enable vscodium
# Habilita o repositório externo do VS Codium no Debian

$ sudo apt update && sudo apt install codium
# Atualiza a lista de pacotes e instala o editor VS Codium
```

Feito isso, o VS Codium está instalado. Eu vou inclusive sugerir a instalação de algumas extensões que eu pretendo usar, que serão muito úteis no andamento desse Mega Tutorial:

```bash
$ codium --install-extension MS-CEINTL.vscode-language-pack-pt-BR
# Adiciona o pacote de idioma em português (tradução da interface)

$ codium --install-extension vscjava.vscode-java-pack
# Instala o pacote oficial de ferramentas Java para desenvolvimento JVM

$ codium --install-extension VMware.vscode-boot-dev-pack
# Inclui o Spring Boot Pack, com suporte a inicialização de projetos e depuração

$ codium --install-extension fwcd.kotlin
# Adiciona o linter e suporte à linguagem Kotlin
```

Com essas extensões instaladas, o Codium já traz autocompletar, debug e suporte ao Spring Boot prontos para uso.

## Conclusão

Aqui chegamos ao final desse primeiro post, que é curto mas é para falar um pouco sobre a criação de ambientes iniciais.

Olhando o que montamos, vejo algo simples mas que resolve o essencial: reprodutibilidade. Não é sobre ter o editor mais caro ou a distro perfeita, mas criar um espaço onde o foco vai pro código: O Java sempre o esperado, a navegação fluida no Spring. É o tipo de base que, na prática, evita horas perdidas com "na minha máquina roda", deixando energia pra decisões que realmente importam, que é o estudo do Spring Boot, do Kotlin e de como criar uma aplicação resiliente com esses dois.

A internet tá cheia de tutoriais sobre Spring Boot (e LLMs que geram código inteiro num piscar de olhos). Então por que isso aqui? Pra mim, é forma de estudar: escrevendo pra outros, organizo ideias, testo na prática e descubro os bugs que não aparecem no `^C` / `^V`. Se ajudar alguém a pular uma armadilha ou repensar o setup, já valeu. Na Parte 2, iremos tratar do setup inicial do projeto no Spring Initializr e nosso primeiro endpoint.
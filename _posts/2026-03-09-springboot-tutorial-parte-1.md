---
layout: post
title: "Spring Boot Tutorial, Parte 1 - Ambiente de Desenvolvimento"
subtitle: "Configurando o ambiente base com Debian Trixie, SDKMAN, VS Codium e JShell"
author:
  - "Eduardo N. S. R."
date: 2026-03-09 11:20:00 GMT-3
modified_date: 2026-08-19 09:30:00 GMT-3
permalink: /posts/spring-boot-tutorial-parte-1-ambiente/
tags: [Spring Boot, Java, DevOps, Linux]
series: Spring Boot Tutorial
---

E se de repente a gente decidisse escrever um tutorial de Spring Boot? Pois é, eu decidi começar essa seara de estudo do framework pela parte que ninguém liga, mas que geralmente é a que quebra tudo quando não é feito do jeito certo: o ambiente de desenvolvimento. Parece bobo, mas sem ele sólido desde o começo, o resto vira dor de cabeça infinita.

> 🔔 *Nota da Série*: Este post inaugura a série **"Spring Boot Tutorial"**, onde construímos do zero uma API backend de produção com **Spring Boot**, explorando boas práticas de arquitetura, contratos, persistência, resiliência, observabilidade e nuvem. O código-fonte de apoio e os projetos dos capítulos práticos estão disponíveis no repositório parceiro [vndmtrx/estudos_springboot](https://github.com/vndmtrx/estudos_springboot).

Nos últimos anos, minha rotina profissional tem sido focada quase que inteiramente em segurança, infraestrutura e DevOps. Isso envolve migrações complexas para a nuvem, automação de esteiras de CI/CD e governança de clusters de VMs e contêineres. Olhando o desenvolvimento sob essa lente operacional, uma coisa sempre salta aos olhos: a negligência com o setup local de quem programa cobra juros altíssimos em produção. O clássico "na minha máquina funciona" quase sempre nasce aqui.

A inspiração para esta série vem do clássico [Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world), do Miguel Grinberg [^1]. A proposta aqui é resgatar essa jornada progressiva de "aprender fazendo", mas no universo do Spring Boot e Java moderno. Em vez de criarmos apenas um CRUD descartável, vamos usar uma API de gerenciamento de tarefas (a nossa `tarefas-api`) como pretexto para dissecar decisões arquiteturais reais: desacoplamento de contratos, resiliência sob estresse, migrações com Flyway no Postgres 18, telemetria unificada e empacotamento para Kubernetes.

E para construir uma catedral que fique de pé, precisamos cavar fundações sólidas. Por isso, começaremos pelo terminal.

## O alicerce do host: Debian Trixie e SDKMAN

A escolha do sistema operacional de trabalho não precisa ser um dogma, mas precisa ser consistente. Por aqui, utilizo o **Debian GNU/Linux 13 (Trixie)** como distribuição padrão para infraestrutura e desenvolvimento. Ele entrega uma base estável, enxuta e previsível.

O primeiro grande erro em ambientes Java é instalar o JDK via gerenciador de pacotes da distribuição (`apt install default-jdk`). Fazer isso amarra o seu sistema a uma versão engessada, polui diretórios globais como `/usr/lib/jvm` e transforma a troca de versão entre projetos diferentes em um pesadelo manual.

A solução definitiva para esse problema é o **SDKMAN** [^2]. Ele gerencia múltiplos kits de desenvolvimento de forma isolada dentro da sua *home*, sem exigir privilégios de superusuário para alternar entre versões de JDK, Gradle ou Maven.

A instalação é direta e roda inteiramente no espaço de usuário:

```bash
$ curl -s "https://get.sdkman.io" | bash
# Baixa e executa o instalador oficial do SDKMAN

$ source "$HOME/.sdkman/bin/sdkman-init.sh"
# Carrega as funções e variáveis de ambiente do SDKMAN na sessão atual do terminal
```

Com o SDKMAN operacional, instalamos a distribuição **Eclipse Temurin** do OpenJDK na versão 26. O Temurin é mantido pela Eclipse Foundation e pela iniciativa Adoptium, sendo hoje um dos padrões da indústria em termos de confiabilidade e conformidade com a especificação Java SE:

```bash
$ sdk install java 26-tem
# Faz o download e a compilação/instalação do Temurin JDK 26

$ sdk default java 26-tem
# Define o Java 26 Temurin como o runtime padrão global para o seu usuário
```

Podemos validar imediatamente se o binário correto está respondendo no `$PATH`:

```bash
$ java --version
# Valida a versão do JDK ativa globalmente
openjdk 26 2026-03-17
OpenJDK Runtime Environment Temurin-26+35 (build 26+35)
OpenJDK 64-Bit Server VM Temurin-26+35 (build 26+35, mixed mode, sharing)
```

Ter múltiplos JDKs na máquina é trivial. Caso você precise rodar um projeto legado em Java 25 em uma aba isolada do terminal, basta invocar `sdk use`:

```bash
$ sdk use java 25-tem
# Altera temporariamente a versão do Java apenas para a sessão atual do shell

$ java --version
# Confirma a alteração pontual
openjdk 25 2025-09-16 LTS
OpenJDK Runtime Environment Temurin-25+36 (build 25+36-LTS)
OpenJDK 64-Bit Server VM Temurin-25+36 (build 25+36-LTS, mixed mode, sharing)
```

No entanto, confiar na memória para trocar de versão sempre que trocar de repositório é receita para erro humano. Para garantir paridade absoluta entre todas as pessoas do time e esteiras de integração contínua, o SDKMAN oferece o arquivo de configuração `.sdkmanrc`.

Basta inicializar o arquivo na raiz do seu repositório:

```bash
$ sdk env init
# Gera o arquivo .sdkmanrc no diretório atual com a versão ativa do Java

$ cat .sdkmanrc
# Enable auto-env through the sdkman_auto_env config
# Add key=value pairs of SDKs to use below
java=26-tem
```

A partir desse momento, qualquer pessoa que clonar o projeto pode simplesmente rodar `sdk env install` para baixar e travar exatamente a mesma versão de compilador e runtime. O mito do "na minha máquina roda diferente" morre aqui.

## O editor leve e sem telemetria: VS Codium

Com o runtime sob controle, a próxima peça do quebra-cabeça é onde vamos escrever código. E aqui entramos no terreno sagrado das guerras santas de IDEs.

Eu sei que a comunidade Java adora o IntelliJ IDEA. Não tiro a razão de quem usa, é uma ferramenta muito madura. O meu problema com essa abordagem é o modelo da dita IDE "open source" onde as funcionalidades realmente úteis e legais (como o suporte de primeira classe ao ecossistema Spring) ficam trancadas atrás de um *paywall* salgado na versão Ultimate. Do outro lado da história temos os clássicos: o Eclipse com seus *workspaces* enigmáticos e o NetBeans (deus me livre e guarde de voltar a mexer com NetBeans nesta vida).

Para quem, como eu, sempre teve um carinho especial por editores modulares (saudades eternas do saudoso Atom Editor), o **VS Codium** [^3] é o ponto de equilíbrio perfeito.

O VS Codium é o binário limpo do Visual Studio Code, compilado diretamente a partir do código-fonte livre sob licença MIT. A grande sacada em relação ao executável da Microsoft é que ele vem completamente livre de rastreadores, telemetria invasiva e chamadas de rede em segundo plano. É leve, consome uma fração da memória de uma IDE tradicional e não fica tentando adivinhar a sua vida.

No Debian Trixie, a instalação é muito simples através do `extrepo` (caso seu sistema seja uma instalação mínima, certifique-se de ter o `curl` e o `extrepo` instalados com `sudo apt install curl extrepo`):

```bash
$ sudo extrepo enable vscodium
# Habilita o repositório oficial e seguro do VS Codium nas fontes do apt

$ sudo apt update && sudo apt install codium
# Sincroniza a lista de pacotes e instala o editor no sistema
```

Com o editor no sistema, o segredo da produtividade está em três extensões essenciais. O suporte a Java no ecossistema do VS Code amadureceu absurdamente nos últimos anos através do pacote oficial da Microsoft/Red Hat (`vscjava`) e as ferramentas de Spring mantidas pela própria VMware. Instalamos tudo direto pelo terminal:

```bash
$ codium --install-extension MS-CEINTL.vscode-language-pack-pt-BR
# Instala o pacote de localização em português para a interface

$ codium --install-extension vscjava.vscode-java-pack
# Adiciona suporte completo ao Java (LSP, depuração, Maven/Gradle e testes integrados)

$ codium --install-extension VMware.vscode-boot-dev-pack
# Instala o pacote oficial de suporte ao ecossistema Spring Boot
```

Esses três entregam tudo o que precisamos para o dia a dia: autocompletar inteligente via Language Server Protocol (LSP), navegação profunda em símbolos do Spring, atalhos de execução de testes e depuração integrada. Mais para frente falaremos com calma sobre como tirar melhor proveito dessas ferramentas. Por enquanto, temos um editor rápido (dentro do que o Electron permite ser), moderno e funcional sem pagar assinatura de software ou fritar a memória da máquina (não culpem o VS Codium por isso, culpem o Electron e as extensões pesadas).

## O ciclo de feedback rápido: REPL-Driven Development com JShell

Existe um preconceito histórico que pinta o ecossistema Java como burocrático e lento para experimentação. Desenvolvedores de linguagens dinâmicas (como Python, Ruby ou Elixir) frequentemente apontam a necessidade de compilar arquivos e criar classes inteiras apenas para testar uma única função.

Desde o Java 9, essa barreira foi demolida com a chegada do **JShell** [^4]. O JShell é um REPL (*Read-Eval-Print Loop*) oficial que permite executar trechos de código Java de forma interativa e instantânea direto no terminal.

Para iniciar uma sessão de experimentação, digite `jshell`:

```bash
$ jshell
|  Welcome to JShell -- Version 26
|  For an introduction type: /help intro

jshell> var saudacao = "Olá, Spring Boot e JShell!"
saudacao ==> "Olá, Spring Boot e JShell!"

jshell> System.out.println(saudacao.toUpperCase())
OLÁ, SPRING BOOT E JSHELL!
```

O valor do JShell vai muito além de imprimir textos simples. Ele permite prototipar estruturas de dados e testar regras de negócio antes de commitar qualquer arquivo no projeto.

Por exemplo, podemos experimentar a sintaxe de **Java Records** (introduzidos de forma definitiva no Java 16), que serão as peças fundamentais para a criação dos nossos DTOs desacoplados:

```bash
jshell> record Tarefa(int id, String titulo, boolean concluido) {}
|  created record Tarefa

jshell> var tarefa = new Tarefa(1, "Configurar ambiente com SDKMAN", true)
tarefa ==> Tarefa[id=1, titulo="Configurar ambiente com SDKMAN", concluido=true]

jshell> tarefa.titulo()
$3 ==> "Configurar ambiente com SDKMAN"

jshell> tarefa.concluido()
$4 ==> true
```

Outro cenário clássico do dia a dia é testar formatações de datas e manipulações de tipos complexos sem precisar rodar uma suite inteira de testes unitários. Podemos manipular o *classpath* da sessão e carregar as bibliotecas nativas:

```bash
jshell> /env -class-path .
|  Setting new options and restoring state.

jshell> import java.time.format.DateTimeFormatter
jshell> import java.time.LocalDate

jshell> var formatador = DateTimeFormatter.ofPattern("dd/MM/yyyy")
formatador ==> Value(DayOfMonth,2)'/'Value(MonthOfYear,2)'/'Value(YearOfEra,4,19,EXCEEDS_PAD)

jshell> var hoje = LocalDate.now().format(formatador)
hoje ==> "19/08/2026"

jshell> System.out.println("Sessao iniciada em: " + hoje)
Sessao iniciada em: 19/08/2026

jshell> /exit
|  Goodbye
```

Essa abordagem incorpora a filosofia de **REPL-Driven Development** e a cultura de *tinkering* (experimentação contínua). Em vez de esperar pelo ciclo lento de escrever código, compilar o projeto inteiro e subir a aplicação para descobrir uma inconsistência em um formatador ou num cálculo, validamos hipóteses no terminal em frações de segundo.

Mais adiante na série, levaremos essa mentalidade de feedback instantâneo para dentro da nossa aplicação viva com o **Spring Boot DevTools** [^5], permitindo recargas a quente e reinicializações automáticas durante o desenvolvimento.

## Exercícios

Para fixar a dinâmica do JShell e experimentar recursos modernos do Java no terminal, teste estes três desafios diretamente na sua sessão interativa.

**1. Cálculo de prazos e manipulação de datas com java.time**

A API moderna de datas do Java (`java.time`) é expressiva e imutável. No JShell, importe as classes de data e crie uma data representando o prazo de entrega de uma tarefa para daqui a 5 dias a partir de hoje (`LocalDate.now().plusDays(5)`). Em seguida, formate a data no padrão brasileiro (`dd/MM/yyyy`) e calcule quantos dias restam até o prazo final utilizando `ChronoUnit.DAYS.between()`.

<details markdown="1">
<summary>Ver resposta</summary>

```java
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

var hoje = LocalDate.now();
var prazo = hoje.plusDays(5);
var formatador = DateTimeFormatter.ofPattern("dd/MM/yyyy");

System.out.println("Hoje: " + hoje.format(formatador));
System.out.println("Prazo limite: " + prazo.format(formatador));

long diasRestantes = ChronoUnit.DAYS.between(hoje, prazo);
System.out.println("Dias restantes: " + diasRestantes);
```

</details>

**2. Filtragem de tarefas com Streams**

Aproveitando o record `Tarefa` que declaramos na sessão interativa do JShell, crie uma lista imutável com múltiplas tarefas (algumas concluídas e outras pendentes). Em seguida, use a Stream API para filtrar apenas as tarefas pendentes (`!tarefa.concluido()`), extrair seus títulos com `map(Tarefa::titulo)` e exibi-los no terminal.

<details markdown="1">
<summary>Ver resposta</summary>

```java
record Tarefa(int id, String titulo, boolean concluido) {}

var tarefas = List.of(
    new Tarefa(1, "Instalar SDKMAN", true),
    new Tarefa(2, "Configurar VS Codium", true),
    new Tarefa(3, "Escrever primeiro endpoint", false),
    new Tarefa(4, "Configurar banco de dados", false)
);

// Filtrando tarefas pendentes e extraindo titulos no JShell
var pendentes = tarefas.stream().filter(t -> !t.concluido()).map(Tarefa::titulo).toList();

System.out.println("Tarefas pendentes: " + pendentes);
```

*A Stream API combinada com method references (Tarefa::titulo) e records torna a transformação e filtragem de coleções concisa e legível.*

</details>

**3. Blindagem de dados com construtor compacto de Records**

Crie no JShell um record `ItemTarefa(int id, String descricao, int prioridade)` que valide suas invariantes no momento da criação: a `descricao` não pode ser nula nem em branco (`isBlank()`), e a `prioridade` deve ser um valor inteiro entre 1 e 5. Caso alguma regra seja violada, lance uma `IllegalArgumentException`. Teste uma criação com sucesso e force um erro passando valores inválidos.

<details markdown="1">
<summary>Ver resposta</summary>

```java
record ItemTarefa(int id, String descricao, int prioridade) {
    public ItemTarefa {
        if (descricao == null || descricao.isBlank()) {
            throw new IllegalArgumentException("A descricao nao pode ser vazia.");
        }
        if (prioridade < 1 || prioridade > 5) {
            throw new IllegalArgumentException("A prioridade deve estar entre 1 e 5.");
        }
    }
}

// Teste de sucesso
var tarefaOk = new ItemTarefa(1, "Configurar SDKMAN", 5);

// Teste de falha (deve estourar IllegalArgumentException)
var tarefaInvalida = new ItemTarefa(2, "", 10);
```

*No JShell, definições de nível superior assumem visibilidade pública por padrão. Por isso, o construtor compacto precisa do modificador public explícito para não violar a visibilidade do record. Ele roda exatamente antes dos campos serem inicializados, sendo o lugar ideal para validações de integridade sem boilerplate.*

</details>

## O ponto de partida

Montar um ambiente de desenvolvimento limpo não é sobre preciosismo técnico ou exibicionismo de ferramentas. É sobre disciplina de engenharia e respeito pelo próprio tempo.

Ao estabelecermos o Debian Trixie como host, o SDKMAN com `.sdkmanrc` para travar o JDK 26 Temurin, o VS Codium sem telemetria e o JShell para experimentação ágil, eliminamos ruídos desnecessários. O foco passa a ser unicamente a arquitetura e a qualidade do código que vamos escrever.

No [segundo post da série](/posts/spring-boot-tutorial-parte-2-projeto-base/), daremos o pontapé inicial na nossa aplicação: vamos criar o projeto base com Maven, explorar a filosofia do **12-Factor App** para desacoplamento de configurações e escrever nosso primeiro endpoint com testes automatizados.

## Referências

[^1]: **The Flask Mega-Tutorial** {*Miguel Grinberg*} ([Link](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world))

[^2]: **SDKMAN! Usage and Documentation** {*SDKMAN!*} ([Link](https://sdkman.io/usage))

[^3]: **VSCodium: Free/Libre Open Source Software Binaries of VS Code** {*VSCodium*} ([Link](https://vscodium.com/))

[^4]: **JShell User's Guide (Java SE 21+)** {*Oracle Documentation*} ([Link](https://docs.oracle.com/en/java/javase/21/jshell/introduction-jshell.html))

[^5]: **Spring Boot Developer Tools Reference** {*Spring Boot Reference Guide*} ([Link](https://docs.spring.io/spring-boot/reference/using/devtools.html))

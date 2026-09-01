---
layout: post
title: "Spring Boot Tutorial, Parte 2 - Projeto Base"
subtitle: "Inicialização com Maven, variáveis de ambiente e perfis de execução"
author:
  - "Eduardo N. S. R."
date: 2026-08-19 16:31:00 GMT-3
modified_date: 2026-08-26 10:17:00 GMT-3
permalink: /posts/spring-boot-tutorial-parte-2-projeto-base/
tags: [Spring Boot, Java, Maven, DevOps]
series: Spring Boot Tutorial
---

No [primeiro post da série](/posts/spring-boot-tutorial-parte-1-ambiente/), montamos nossa bancada de trabalho com Debian Trixie, SDKMAN travando o JDK 26 e o VS Codium livre de telemetrias. Com as ferramentas no lugar, o impulso natural da maioria dos tutoriais é abrir o editor e sair cuspindo código de negócio desordenado. Mas se queremos construir uma aplicação que sobreviva ao mundo real, precisamos falar antes sobre como uma aplicação nasce e como ela lida com seus ambientes.

> [!NOTE] Nota da Série
> Este post faz parte da série **"Spring Boot Tutorial"**, onde construímos do zero uma API backend de produção com **Spring Boot**, explorando boas práticas de arquitetura, contratos, persistência, resiliência, observabilidade e nuvem. O código-fonte de apoio e os projetos de cada capítulo estão organizados no repositório parceiro [vndmtrx/estudos_springboot](https://github.com/vndmtrx/estudos_springboot).

Quem trabalha com infraestrutura e operações aprende rápido uma verdade incômoda: a esmagadora maioria dos incidentes de deploy não acontece por falha de sintaxe, mas por confusão de configuração. É o desenvolvedor que chumba a URL do banco local no meio do código, comita credenciais sensíveis no repositório ou assume que a aplicação vai rodar para sempre no mesmo caminho de diretório.

Para evitar esse tipo de armadilha desde o primeiro commit, o ecossistema de nuvem e microsserviços se apoia na metodologia dos **12-Factor App** [^1]. Criada pelos desenvolvedores da plataforma Heroku, ela define doze princípios para criar aplicações portáveis, resilientes e escaláveis (se você quiser se aprofundar em cada um deles com causos reais de pesadelos de infraestrutura, confira o nosso post [12-Factor App: Como Fazer (e os Pesadelos de Como Não Fazer)](/posts/12-factor-app-pesadelos-e-pratica/)).

Neste momento da série, dois desses fatores nos interessam diretamente:

1. **Fator III (Configurações):** Armazene as configurações estritamente no ambiente. A aplicação deve ser agnóstica a onde está rodando; o mesmo pacote binário compilado precisa servir tanto para o seu notebook quanto para o cluster de produção, mudando apenas as variáveis externas fornecidas a ele.
2. **Fator X (Paridade Dev/Prod):** Mantenha o ambiente de desenvolvimento, homologação e produção o mais similares possível.

Com esses princípios em mente, vamos inicializar nosso projeto e estruturar sua gestão de perfis e configurações.

## A inicialização do projeto com Maven e Spring Initializr

A forma mais limpa e padronizada de iniciar um projeto Spring Boot é através do **Spring Initializr** [^2]. 

Se você abrir a página [start.spring.io](https://start.spring.io/) no navegador, encontrará uma interface visual completa para montar seu projeto do jeito que preferir:

* **Project:** Maven
* **Language:** Java
* **Spring Boot:** 4.1.x (ou a versão estável mais recente)
* **Project Metadata:** Group (`io.github.vndmtrx`), Artifact (`tarefas-api`), Name (`tarefas-api`), Package name (`io.github.vndmtrx.tarefas-api`)
* **Configuration:** YAML (`configurationFileFormat=yaml`)
* **Packaging:** Jar
* **Java:** 26
* **Dependencies:** Clicando no botão *Add Dependencies* (ou usando o atalho `Ctrl + B`), basta buscar e adicionar `Spring Web` e `Spring Boot DevTools`.

Pela página, você pode clicar no botão **GENERATE** (ou teclar `Ctrl + Enter`), baixar o arquivo `.zip` gerado e descompactá-lo na pasta de trabalho.

A interface web é excelente para explorar dependências e visualizar opções. No entanto, para o nosso laboratório, podemos baixar o arquivo compactado da estrutura inicial diretamente via `curl`:

```bash
$ curl https://start.spring.io/starter.tgz \
    -d type=maven-project \
    -d language=java \
    -d bootVersion=4.1.1 \
    -d baseDir=tarefas-api \
    -d configurationFileFormat=yaml \
    -d groupId=io.github.vndmtrx \
    -d artifactId=tarefas-api \
    -d name=tarefas-api \
    -d packageName=io.github.vndmtrx.tarefas-api \
    -d javaVersion=26 \
    -d dependencies=web,devtools \
    -o tarefas-api.tgz
# Baixa o arquivo compactado com a estrutura base do projeto
```

Basta descompactar o arquivo `.tgz` no seu diretório de trabalho ou, se preferir, clonar e abrir diretamente o código deste capítulo no [repositório parceiro](https://github.com/vndmtrx/estudos_springboot). Todos os exemplos a partir de agora serão baseados neste projeto. O código desse post está na pasta [estudos_springboot/parte2](https://github.com/vndmtrx/estudos_springboot/tree/main/parte2).

Repare que na raiz do projeto temos o arquivo `mvnw` (o **Maven Wrapper**) [^3]. O Maven Wrapper é fundamental para a reprodutibilidade: ele garante que qualquer pessoa (ou servidor de CI) que clone o repositório execute exatamente a mesma versão do Maven sem precisar ter o binário instalado globalmente no sistema operacional.

Podemos compilar e rodar a aplicação imediatamente:

```bash
$ ./mvnw spring-boot:run
# Inicia a aplicacao usando o wrapper do Maven
```

A aplicação subirá em poucos segundos, escutando por padrão na porta `8080`.

Se você abrir `http://localhost:8080` no navegador (ou rodar `curl -i http://localhost:8080` no terminal), se deparará com a famosa **Whitelabel Error Page**:

```text
Whitelabel Error Page
This application has no explicit mapping for /error, so you are seeing this as a fallback.

Wed Aug 19 15:01:52 GMT-03:00 2026
There was an unexpected error (type=Not Found, status=404).
No static resource .
```

Não se assuste: esse comportamento é totalmente esperado. Ele confirma que o servidor embutido (Apache Tomcat) subiu com sucesso e que o despachante de requisições do Spring (`DispatcherServlet`) está ativo. Como ainda não criamos nenhum controller ou recurso estático para responder na rota raiz (`/`), o Spring retorna o status HTTP `404 Not Found`.

Podemos encerrar a aplicação com `Ctrl + C` no terminal.

## Configurações no padrão 12-Factor: application.yaml e variáveis de ambiente

Ao selecionarmos o formato YAML diretamente no Spring Initializr (ou através do parâmetro `configurationFileFormat=yaml` no nosso comando), o projeto já nasce com o arquivo `src/main/resources/application.yaml` nativo, dispensando o antigo formato `.properties` e entregando uma estrutura hierárquica e muito mais legível.

Agora vem o ponto crucial: como o Spring Boot consome configurações?

O Spring possui uma hierarquia sofisticada de resolução de propriedades chamada **Environment Abstraction** [^4]. Quando a aplicação precisa de um valor, ela busca em diversas fontes na seguinte ordem de prioridade (da mais alta para a mais baixa):

1. Argumentos de linha de comando (`--app.mensagem="Texto"`)
2. Variáveis de ambiente do sistema operacional (`APP_MENSAGEM="Texto"`)
3. Arquivos de propriedades específicos de perfil (`application-dev.yaml`)
4. Arquivo de propriedades padrão da aplicação (`application.yaml`)

Isso significa que podemos definir valores padrão seguros para desenvolvimento local no `application.yaml`, enquanto permitimos que variáveis de ambiente sobrescrevam esses valores em outros ambientes sem tocar no código.

A sintaxe de interpolação com valor de reserva (*fallback*) do Spring Boot segue a estrutura `${NOME_VARIAVEL:valor_padrao}`. Vamos editar o `src/main/resources/application.yaml`:

```yaml
spring:
  application:
    name: tarefas-api

app:
  mensagem: ${APP_MENSAGEM:Ola, bem-vindo a API de Tarefas!}
  versao: "1.0.0"
```

Se executarmos a aplicação normalmente, ela usará a frase padrão `"Ola, bem-vindo a API de Tarefas!"`. Mas se exportarmos uma variável no terminal antes de iniciar o processo:

```bash
$ APP_MENSAGEM="Servidor rodando em modo customizado" ./mvnw spring-boot:run
# Inicia o Spring Boot injetando a variavel de ambiente diretamente pelo shell
```

O Spring Boot detectará automaticamente a variável `APP_MENSAGEM` e substituirá o valor padrão. Nenhuma recompilação, nenhuma edição de arquivo. Isso é o 12-Factor App em ação.

## Isolando ambientes com Spring Profiles e Maven

Em projetos reais, nem toda configuração se resume a uma única variável solta. Frequentemente precisamos alternar blocos inteiros de comportamento entre o ambiente de desenvolvimento local (`dev`) e o ambiente de produção (`prod`).

O Spring Boot resolve isso com o mecanismo de **Profiles** [^5]. A convenção é criar arquivos complementares seguindo o padrão de nomenclatura `application-{profile}.yaml`.

Vamos criar dois arquivos de perfil em `src/main/resources/`:

O arquivo de desenvolvimento local `src/main/resources/application-dev.yaml`:

```yaml
app:
  ambiente: "Desenvolvimento Local"

logging:
  level:
    root: INFO
    "[org.springframework.web]": DEBUG
    "[io.github.vndmtrx.tarefas_api]": DEBUG
```

E o arquivo de produção `src/main/resources/application-prod.yaml`:

```yaml
app:
  ambiente: "Producao"

logging:
  level:
    root: ERROR
    "[io.github.vndmtrx.tarefas_api]": INFO
```

> [!WARNING] Aviso
> Repare no uso de colchetes e aspas duplas `"[nome.do.pacote]"` sob `logging.level`: em arquivos YAML, como os pacotes Java contêm pontos (`.`), essa sintaxe de escape é a convenção oficial recomendada pelo Spring Boot para evitar que o interpretador YAML confunda o nome do pacote com nós aninhados [^6].

* No perfil `dev`, ativamos o nível `DEBUG` para a camada web e para o nosso pacote `io.github.vndmtrx.tarefas_api`, permitindo inspecionar o roteamento e detalhes internos durante os testes.
* No perfil `prod`, elevamos o nível geral (`root`) para `ERROR` para silenciar ruídos de bibliotecas de terceiros, liberando apenas mensagens `INFO` relevantes do nosso próprio sistema.

Para ativar um perfil durante a execução, podemos usar três estratégias diferentes:

1. **Via argumento no terminal:**
   ```bash
   $ ./mvnw spring-boot:run -Dspring-boot.run.profiles=dev
   # Ativa explicitamente o perfil dev
   ```

2. **Via variável de ambiente (padrão em contêineres e Kubernetes):**
   ```bash
   $ SPRING_PROFILES_ACTIVE=prod ./mvnw spring-boot:run
   # Define o perfil ativo atraves de variavel de ambiente do sistema operacional
   ```

3. **Via perfil ativo no arquivo base `application.yaml`:**
   ```yaml
   spring:
     profiles:
       active: dev
   ```

Essa separação garante clareza absoluta: o arquivo `application.yaml` centraliza a estrutura geral, enquanto os arquivos de profile refinam apenas os valores específicos de cada contexto.

### Inspecionando o perfil ativo nos logs de inicialização

O Spring Boot sempre informa com clareza nos logs de inicialização qual perfil está em execução. Repare na linha emitida logo abaixo do banner ASCII em cada cenário:

* **Sem perfil informado (comportamento padrão):**
  ```text
  INFO ... TarefasApiApplication : No active profile set, falling back to 1 default profile: "default"
  ```

* **Com o perfil `dev` ativado (`-Dspring-boot.run.profiles=dev`):**
  ```text
  INFO ... TarefasApiApplication : The following 1 profile is active: "dev"
  ```

* **Com o perfil `prod` ativado (`SPRING_PROFILES_ACTIVE=prod`):**
  ```text
  INFO ... TarefasApiApplication : The following 1 profile is active: "prod"
  ```

Essa linha de log é o seu feedback visual imediato de que a sobreposição correta (`application-dev.yaml` ou `application-prod.yaml`) foi carregada com sucesso sobre o arquivo base.

## Construindo o primeiro endpoint REST

Com o projeto inicializado e as configurações parametrizadas, vamos construir nosso primeiro endpoint REST para validar o fluxo de ponta a ponta.

No pacote `io.github.vndmtrx.tarefas_api`, criaremos um Java Record para representar a resposta estruturada de status da nossa API:

Arquivo `src/main/java/io/github/vndmtrx/tarefas_api/StatusResposta.java`:

```java
package io.github.vndmtrx.tarefas_api;

public record StatusResposta(String status, String mensagem, String versao) {}
```

Em seguida, criamos o controller que responderá na rota `/api/status`:

Arquivo `src/main/java/io/github/vndmtrx/tarefas_api/StatusController.java`:

```java
package io.github.vndmtrx.tarefas_api;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/status")
public class StatusController {

    private final String mensagem;
    private final String versao;

    public StatusController(
            @Value("${app.mensagem}") String mensagem,
            @Value("${app.versao:1.0.0}") String versao) {
        this.mensagem = mensagem;
        this.versao = versao;
    }

    @GetMapping
    public ResponseEntity<StatusResposta> verificarStatus() {
        var resposta = new StatusResposta("UP", mensagem, versao);
        return ResponseEntity.ok(resposta);
    }
}
```

Preste atenção em um detalhe arquitetural fundamental: colocamos a anotação `@Value` nos parâmetros do **construtor** em vez de anotá-la diretamente nas variáveis de classe.

Há duas razões cruciais para essa escolha:

1. **Imutabilidade e rigor do compilador:** Em Java, atributos declarados como `final` precisam obrigatoriamente ser inicializados no momento da declaração ou no corpo do construtor. Se tentássemos fazer `@Value(...) private final String mensagem;` sem construtor, o compilador do Java geraria um erro imediato de compilação (*"variable might not have been initialized"*). Remover o modificador `final` apenas para forçar o Spring a injetar via reflexão oculta quebra a imutabilidade e abre margem para mutações acidentais de estado.
2. **Testabilidade e desacoplamento:** Com injeção por construtor, o controller é uma classe Java pura (POJO). Não dependemos do container do Spring ou de reflexão para criar instâncias: podemos chamar `new StatusController("Texto", "1.0.0")` em qualquer lugar, seja em testes de unidade puros ou no próprio terminal.

Para propriedades simples e pontuais como a nossa mensagem e versão, o `@Value` no construtor é a solução mais enxuta. Conforme a aplicação evoluir e acumular conjuntos complexos de propriedades (como regras de segurança, parâmetros de mensageria e tuning de conexões), veremos mais adiante como agrupar essas configurações em Records tipados usando `@ConfigurationProperties`.

## Experimentação rápida: JShell no classpath do projeto

Antes de subirmos o servidor HTTP ou escrevermos arquivos de teste formais, podemos validar nosso record e nossos controllers diretamente no **JShell** com todo o ambiente do projeto carregado.

Para que o JShell enxergue tanto as nossas classes compiladas quanto as bibliotecas do Spring (como o `ResponseEntity`), precisamos de duas coisas simples:
1. Compilar o projeto com o Maven para gerar o bytecode em `target/classes`.
2. Gerar o caminho completo das dependências do Spring gerenciadas pelo Maven.

Fazemos isso em poucos comandos no terminal:

```bash
$ ./mvnw compile
# Compila os fontes Java e gera o bytecode em target/classes

$ ./mvnw dependency:build-classpath -Dmdep.outputFile=.classpath.txt
# Exporta a lista de JARs de dependencias do Spring para o arquivo .classpath.txt

$ jshell --class-path target/classes:$(cat .classpath.txt)
# Abre o REPL com acesso as nossas classes e a todo o ecossistema Spring
```

Dentro da sessão interativa, veja como podemos importar nossas classes, instanciar o record e chamar o método do controller diretamente:

```bash
jshell> import io.github.vndmtrx.tarefas_api.*;

jshell> var status = new StatusResposta("UP", "Testando interativamente", "1.0.0");
status ==> StatusResposta[status=UP, mensagem=Testando interativamente, versao=1.0.0]

jshell> var controller = new StatusController("Ola do JShell!", "1.0.0");
controller ==> io.github.vndmtrx.tarefas_api.StatusController@4de5031f

jshell> var resposta = controller.verificarStatus();
resposta ==> <200 OK OK,StatusResposta[status=UP, mensagem=Ola do JShell!, versao=1.0.0],[]>

jshell> resposta.getBody();
$4 ==> StatusResposta[status=UP, mensagem=Ola do JShell!, versao=1.0.0]

jshell> resposta.getStatusCode();
$5 ==> 200 OK

jshell> /exit
|  Goodbye
```

Repare no grande ganho arquitetural: ao adotarmos **injeção por construtor** em vez de campos privados anotados, nosso controller se comporta como uma classe Java pura, 100% instanciável e testável de forma isolada sem depender de mágica ou reflexão oculta do framework.

No entanto, para validar o comportamento integrado em runtime (como o mapeamento de rotas HTTP no Tomcat e a serialização JSON), precisamos formalizar a garantia de qualidade com testes automatizados.

## O contrato de testes unitários com MockMvc

Aqui entra a regra de ouro que adotaremos em toda a série: **nenhum código avança sem testes automatizados**.

A boa notícia é que não precisamos configurar bibliotecas de teste externas do zero: o Spring Initializr já inclui por padrão no nosso `pom.xml` o artefato `spring-boot-starter-webmvc-test`. Esse pacote empacota o **JUnit 5**, o **Mockito** e o utilitário **MockMvc** prontos para uso.

Vamos escrever um teste unitário para o `StatusController` utilizando o `MockMvc`. Com a anotação `@WebMvcTest`, o Spring inicializa exclusivamente a camada web (controllers e serialização JSON), permitindo simular requisições HTTP e validar o payload de resposta diretamente na memória, sem abrir portas de rede ou subir um servidor web completo:

Arquivo `src/test/java/io/github/vndmtrx/tarefas_api/StatusControllerTest.java`:

```java
package io.github.vndmtrx.tarefas_api;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.webmvc.test.autoconfigure.WebMvcTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@WebMvcTest(StatusController.class)
class StatusControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    @DisplayName("Deve retornar status 200 e payload de saude com sucesso")
    void deveRetornarStatusComSucesso() throws Exception {
        mockMvc.perform(get("/api/status")
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.status").value("UP"))
                .andExpect(jsonPath("$.versao").value("1.0.0"));
    }
}
```

Executamos a suite de testes no terminal:

```bash
$ ./mvnw test
# Executa todos os testes automatizados da aplicacao
```

O resultado deve confirmar 100% de sucesso para a suíte (incluindo o teste base `TarefasApiApplicationTests` gerado pelo Initializr e o nosso `StatusControllerTest`):

```
[INFO] Results:
[INFO] 
[INFO] Tests run: 2, Failures: 0, Errors: 0, Skipped: 0
[INFO] 
[INFO] BUILD SUCCESS
```

## O ciclo de feedback rápido: DevTools no desenvolvimento contínuo

Para manter o fluxo de trabalho ágil durante o desenvolvimento, adicionamos a dependência `spring-boot-devtools` [^7] logo na inicialização do projeto.

O DevTools atua em duas frentes principais:

1. **Reinicialização Automática (*Automatic Restart*):** O Spring Boot monitora as classes compiladas no *classpath*. Sempre que você altera um arquivo e salva no editor (ou compila com `./mvnw compile`), o DevTools reinicia o contexto da aplicação em frações de segundo, utilizando dois *classloaders* distintos para reaproveitar as bibliotecas de terceiros e recarregar apenas o código do seu projeto.
2. **Desativação de Caches de Templates:** Garante que alterações em recursos estáticos sejam refletidas imediatamente sem necessidade de reiniciar o servidor.

## Exercícios

Para fixar a dinâmica de configuração externa, perfis e testes, execute os exercícios abaixo no terminal.

**1. Sobrescrita de propriedade via linha de comando**

Inicie a aplicação passando uma mensagem personalizada através da variável de ambiente `APP_MENSAGEM` e, em outro terminal, faça uma requisição HTTP via `curl` para a rota `/api/status` validando se o JSON retornado reflete o novo texto.

<details markdown="1">
<summary>Ver resposta</summary>

```bash
# Terminal 1: Iniciar com a variavel customizada
$ APP_MENSAGEM="Mensagem injetada via ENV" ./mvnw spring-boot:run

# Terminal 2: Testar o endpoint
$ curl -s http://localhost:8080/api/status
{"status":"UP","mensagem":"Mensagem injetada via ENV","versao":"1.0.0"}
```

*O Spring Boot mapeia automaticamente variaveis de ambiente em letras maiusculas e com underscores para as chaves correspondentes do YAML.*

</details>

**2. Execução de testes unitários filtrados no Maven**

Em projetos grandes com centenas de testes, rodar a suíte completa a cada pequena alteração pode ser demorado. Utilize a flag `-Dtest` do Maven para executar exclusivamente a classe `StatusControllerTest`.

<details markdown="1">
<summary>Ver resposta</summary>

```bash
$ ./mvnw test -Dtest=StatusControllerTest
# Executa apenas os testes da classe especificada
```

*A propriedade -Dtest aceita o nome simples da classe ou padroes com asterisco (ex: -Dtest=*ControllerTest).*

</details>

**3. Criando um novo campo no Record e atualizando o teste**

Adicione um novo campo booleano `boolean manutencao` no record `StatusResposta`, ajuste o `StatusController` para retornar `false` por padrão e adicione uma nova asserção no teste unitário `StatusControllerTest` para validar que o campo `$.manutencao` vem com o valor esperado.

<details markdown="1">
<summary>Ver resposta</summary>

No record `StatusResposta.java`:
```java
package io.github.vndmtrx.tarefas_api;

public record StatusResposta(String status, String mensagem, String versao, boolean manutencao) {}
```

No `StatusController.java`:
```java
@GetMapping
public ResponseEntity<StatusResposta> verificarStatus() {
    var resposta = new StatusResposta("UP", mensagem, versao, false);
    return ResponseEntity.ok(resposta);
}
```

No teste `StatusControllerTest.java`, adicione o teste abaixo para validar o novo campo:
```java
@Test
@DisplayName("Deve retornar status 200 com mensagem, versão e manutencao")
void deveRetornarStatusComSucessoComMensagemVersaoEManutencao() throws Exception {
    mockMvc.perform(get("/api/status")
            .contentType(MediaType.APPLICATION_JSON))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.status").value("UP"))
            .andExpect(jsonPath("$.versao").value("1.0.0"))
            .andExpect(jsonPath("$.manutencao").value(false));
}
```

Execute `./mvnw test` para validar a suíte de testes.

</details>

## O ponto de partida para o domínio

Neste segundo passo da série, estabelecemos as fundações de arquitetura do nosso backend: inicializamos o projeto com Maven, adotamos a filosofia dos 12-Factor App para externalizar configurações no `application.yaml`, estruturamos o isolamento por perfis e garantimos que todo endpoint nasce acompanhado de testes unitários automatizados.

Com o esqueleto da aplicação de pé e o ciclo de feedback azeitado pelo DevTools, estamos prontos para avançar para as regras de negócio. 

Na Parte 3, entraremos no domínio da nossa aplicação de tarefas: vamos modelar a entidade `Tarefa`, configurar a persistência em memória com H2, estruturar as camadas de Repository, Service e Controller, e introduzir as variáveis de infraestrutura de banco de dados.

## Referências

[^1]: **The Twelve-Factor App** {*Adam Wiggins / Heroku*} ([Link](https://12factor.net/pt_br/))

[^2]: **Spring Initializr** {*VMware Tanzu*} ([Link](https://start.spring.io/))

[^3]: **Maven Wrapper Documentation** {*Apache Maven Project*} ([Link](https://maven.apache.org/wrapper/))

[^4]: **Externalized Configuration in Spring Boot** {*Spring Boot Reference Documentation*} ([Link](https://docs.spring.io/spring-boot/reference/features/external-config.html))

[^5]: **Spring Boot Profiles** {*Spring Boot Reference Documentation*} ([Link](https://docs.spring.io/spring-boot/reference/features/profiles.html))

[^6]: **Relaxed Binding on Maps in Spring Boot** {*Spring Boot Reference Documentation*} ([Link](https://docs.spring.io/spring-boot/reference/features/external-config.html#features.external-config.typesafe-configuration-properties.relaxed-binding.maps))

[^7]: **Developer Tools (DevTools) Guide** {*Spring Boot Reference Documentation*} ([Link](https://docs.spring.io/spring-boot/reference/using/devtools.html))

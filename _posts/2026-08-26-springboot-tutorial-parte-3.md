---
layout: post
title: "Spring Boot Tutorial, Parte 3 - Core API em Camadas"
subtitle: "Do H2 parametrizado ao JpaRepository: a primeira fatia de domínio com serviço transacional e testes de persistência"
author:
  - "Eduardo N. S. R."
date: 2026-08-26 08:43:00 GMT-3
permalink: /posts/spring-boot-tutorial-parte-3-core-api/
tags: [Spring Boot, Java, JPA, Backend]
series: Spring Boot Tutorial
---

Se você chegou até aqui com a aplicação da Parte 2 no ar, então já tem um servidor que sobe, troca de perfil e responde o `/api/status`. O que você não tem ainda é domínio. Não existe tarefa, não existe estado, não existe nada para persistir. A aplicação é um esqueleto saudável, mas ainda é um esqueleto.

> 🔔 *Nota da Série*: Este post faz parte da série **"Spring Boot Tutorial"**, onde construímos do zero uma API backend de produção com **Spring Boot**, explorando boas práticas de arquitetura, contratos, persistência, resiliência, observabilidade e nuvem. O código-fonte de apoio e os projetos de cada capítulo estão organizados no repositório parceiro [vndmtrx/estudos_springboot](https://github.com/vndmtrx/estudos_springboot). O código desta parte está na pasta [parte3](https://github.com/vndmtrx/estudos_springboot/tree/main/parte3).

A tentação nesse ponto é honesta: abrir o controller, despejar ali toda a lógica de negócio e ir para casa. É o caminho mais curto entre a ideia e o HTTP. E é também o caminho que, aos poucos, transforma projeto promissor em um código espaguete: controller consultando banco, service inventado depois por remorso, teste que só descobre regressão em produção.

Quem vive de infraestrutura já viu esse filme repetidas vezes. Aplicação que funciona na máquina do dev e explode no deploy. Schema alterado na mão, sem histórico de migração. `ddl-auto=update` rodando em produção como se a JVM tivesse passe livre para reescrever o banco. O mesmo descuido que, na Parte 2, apontamos nas variáveis de configuração agora se manifesta na persistência, só que com potencial de estrago bem maior.

Por isso, nesta parte a gente faz o oposto do impulso: constrói a primeira fatia de domínio da `tarefas-api` em camadas separadas, com o banco parametrizado no padrão 12-Factor e com testes em cada fronteira importante. O controller, por ora, vai continuar rústico de propósito. Na Parte 4, a gente o enterra com Records, MapStruct e Bean Validation.

## Onde cada classe vai morar: a decisão que os tutoriais pulam

Antes de escrever a primeira entidade, há uma pergunta que quase todo tutorial esconde debaixo do tapete: em qual pacote cada classe vai morar?

O Spring Boot não obriga organização nenhuma. Ele escaneia a partir do pacote raiz e encontra componentes em qualquer subpacote. Essa liberdade é um convite ao acaso, e o acaso, em projeto Java, costuma se materializar em dois desenhos: **Package by Layer** e **Package by Feature**. Entender a diferença é o que separa um código que cresce de um código que incha.

### Package by Layer: o mapa que reflete a tecnologia

É a organização clássica de MVC, agrupada por papel técnico:

```
src/main/java
└── io/github/vndmtrx/tarefas_api
    ├── controller/
    │   ├── TarefaController.java
    │   └── StatusController.java
    ├── service/
    │   └── TarefaService.java
    ├── repository/
    │   └── TarefaRepository.java
    ├── model/
    │   └── Tarefa.java
    └── dto/
        └── TarefaRequest.java
```

Ela seduz pela simetria: todo controller mora em `controller`, todo service em `service`. Para quem acabou de conhecer o framework, o mapa corresponde à nomenclatura mental. Camada é pasta, pasta é camada.

O problema aparece quando uma feature precisa mudar. Alterar uma regra de tarefa pode tocar `controller/`, `service/` e `repository/` ao mesmo tempo: pacotes distantes para uma mudança conceitualmente única. É o *shotgun surgery*: um espirro no domínio e a alteração se espalha por cinco pastas.

Há uma perda mais sutil, e talvez a mais dolorosa: a visibilidade `package-private`. No Java, uma classe sem modificador só é visível dentro do seu próprio pacote. No Package by Layer, `service` e `repository` ficam em pacotes diferentes; a intenção "o repositório é detalhe interno do serviço" não consegue ser expressa sem recorrer ao `public`. Tudo vira público, anunciando para a base inteira que ali dentro é zona franca.

### Package by Feature: o mapa que reflete o domínio

A alternativa agrupa por assunto, não por papel técnico. É o desenho que adotamos nesta série:

```
src/main/java
└── io/github/vndmtrx/tarefas_api
    ├── TarefasApiApplication.java
    ├── status/
    │   ├── StatusController.java
    │   └── StatusResposta.java
    └── todo/
        ├── Tarefa.java
        ├── TarefaController.java
        ├── TarefaRepository.java
        ├── TarefaRequest.java
        └── TarefaService.java
```

Aqui, `todo` é uma unidade de negócio. Tudo que diz respeito a tarefas mora sob o mesmo teto. A mudança de uma regra de tarefa tende a permanecer em um único diretório: é a *feature cohesion* em ação. Repare que o Package by Feature não abole as camadas: controller, service e repository continuam existindo; eles apenas deixam de viver em guetos técnicos separados.

De quebra, o `package-private` volta a ter significado. Como `TarefaController`, `TarefaService`, `TarefaRepository` e `TarefaRequest` só fazem sentido dentro do pacote `todo`, eles não precisam ser `public`. Apenas a entidade `Tarefa` fica pública, por exigência do mapeamento da JPA.

Os testes espelham a mesma geografia:

```
src/test/java
└── io/github/vndmtrx/tarefas_api
    ├── TarefasApiApplicationTests.java
    ├── status/
    │   └── StatusControllerTest.java
    └── todo/
        ├── TarefaRepositoryTest.java
        └── TarefaServiceTest.java
```

O pacote `todo` de teste enxerga as classes package-private do pacote `todo` de produção, porque compartilham o mesmo nome. É o primeiro benefício concreto da decisão.

### E o Hexagonal?

Existe um terceiro caminho, o Hexagonal (Ports & Adapters). Nele, o domínio fica no centro e as fronteiras técnicas viram adaptadores plugáveis: o repositório se transforma em uma porta de saída, a persistência em um adaptador, e o Spring só enxerga a casca.

É o desenho com maior isolamento dos três. É também o mais caro. Para uma API com uma única agregação, a indireção de portas e adaptadores não paga o aluguel. A regra que seguimos aqui é a da proporção: Package by Feature agora, Hexagonal quando houver domínio que justifique o isolamento. Mais adiante na série, essa conversa volta com mais bagagem.

Com o mapa definido, é hora de preparar o terreno do banco.

## Infraestrutura parametrizada: H2 e as variáveis do banco

Antes de qualquer linha de domínio, o terreno precisa estar pronto. A escolha desta fase é o **H2** [^3], um banco relacional em memória que sobe junto com a aplicação e desaparece quando o processo termina. Para desenvolvimento e testes, é o paraíso: zero instalação, zero container, zero desculpa para não testar persistência. Na Parte 5, o Postgres 18 entra em cena via Docker e Flyway, e o H2 passa a ser apenas o aliado dos testes rápidos. Por ora, ele carrega o peso sozinho.

Para isso, adicionamos duas dependências no `pom.xml`: o starter de persistência JPA e o driver do H2.

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>runtime</scope>
</dependency>
```
*O starter reúne Hibernate, Spring Data JPA e o gerenciamento do pool de conexões HikariCP. O H2 entra apenas em runtime.*

Na sequência, expandimos o `src/main/resources/application.yaml` criado na Parte 2. Lembra da mecânica de *fallback* `${VARIAVEL:valor_padrao}`? É exatamente ela que vai parametrizar o banco:

```yaml
spring:
  application:
    name: tarefas-api
  datasource:
    url: ${DB_URL:jdbc:h2:mem:tarefasdb;DB_CLOSE_DELAY=-1}
    username: ${DB_USER:sa}
    password: ${DB_PASS:}
  jpa:
    hibernate:
      ddl-auto: ${DDL_AUTO:create-drop}
    open-in-view: false

app:
  mensagem: ${APP_MENSAGEM:Ola, bem-vindo a API de Tarefas!}
  versao: "1.0.0"
```
*Com os defaults, o H2 cria a base `tarefasdb` na memória e a mantém viva enquanto a JVM estiver de pé. Em outro ambiente, basta exportar `DB_URL`, `DB_USER` e `DB_PASS`.*

Agora o ponto que separa a sanidade da catástrofe: a propriedade `ddl-auto` [^5]. O valor `create-drop` faz o Hibernate criar o schema no início e destruí-lo no fim, combinação perfeita para o H2 em memória. O valor `update` tenta sincronizar o schema com as entidades a cada boot.

Soa inofensivo. Não é. Em produção, `ddl-auto=update` é um passaporte para o incidente: o Hibernate altera colunas, cria estruturas e, em alguns casos, derruba e recria sem histórico nenhum. Adicionou um campo? O schema muda sozinho. Renomeou uma coluna? O Hibernate enxerga uma coluna antiga e uma entidade nova e faz o que bem entende, muitas vezes com um `drop` no meio do caminho. É a receita do downtempo noturno.

> ⚠️ *Aviso*: Jamais use `ddl-auto=update` em produção. Na Parte 5, o Flyway assume a gestão do schema com migrations versionadas e o `ddl-auto` vira `validate`.

Também desligamos o `open-in-view`, que por padrão mantém a sessão do JPA aberta durante a serialização da resposta HTTP. Desligado, o Hibernate libera a conexão assim que a transação termina. Na prática, isso nos obriga a buscar os dados dentro da transação e elimina surpresas de *lazy loading* na camada web.

## A entidade Tarefa sem atalhos

O coração do domínio é quase banal: uma tarefa tem `id`, `titulo`, `descricao` e um *flag* `concluido`. Simples o suficiente para a gente se concentrar nas decisões ao redor dela sem ruído.

Apesar do carinho pelos Java Records que cultivamos na Parte 1, aqui a entidade nasce como classe. A JPA exige um construtor sem argumentos para instanciar via reflexão e lida melhor com mutabilidade [^2]. Records, imutáveis por definição e sem construtor padrão, não se encaixam bem nesse papel. Eles voltarão triunfantes na Parte 4, agora como DTOs.

A entidade:

```java
package io.github.vndmtrx.tarefas_api.todo;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Tarefa {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 120)
    private String titulo;

    @Column(length = 500)
    private String descricao;

    @Column(nullable = false)
    private boolean concluido = false;

    protected Tarefa() {
        // exigido pela JPA
    }

    public Tarefa(String titulo, String descricao) {
        this.titulo = titulo;
        this.descricao = descricao;
    }

    public Long getId() { return id; }
    public String getTitulo() { return titulo; }
    public void setTitulo(String titulo) { this.titulo = titulo; }
    public String getDescricao() { return descricao; }
    public void setDescricao(String descricao) { this.descricao = descricao; }
    public boolean isConcluido() { return concluido; }

    public void concluir() {
        this.concluido = true;
    }

    @Override
    public String toString() {
        return "Tarefa{id=%d, titulo='%s', concluido=%s}".formatted(id, titulo, concluido);
    }
}
```
Vamos dissecar cada atributo, porque cada anotação é uma decisão de domínio disfarçada de metadado.

O `id` carrega duas anotações que trabalham juntas. `@Id` transforma o campo na chave primária da tabela, o endereço único de cada linha que permite ao Hibernate rastrear e sincronizar o estado da entidade com o banco. `@GeneratedValue(strategy = GenerationType.IDENTITY)` delega a geração desse número ao próprio banco. No H2, isso vira uma coluna auto-increment, nada de sequências nem tabelas auxiliares. O `IDENTITY` foi escolhido de propósito: é a estratégia mais simples para um banco embarcado e mantém o Hibernate longe das tabelas de geração que ele criaria por padrão em outros bancos, com surpresas que ninguém quer descobrir em produção.

O `titulo` é a menor unidade de domínio com identidade própria. A anotação `@Column(nullable = false, length = 120)` tem efeito duplo: o `nullable = false` gera uma coluna `NOT NULL` no schema, e o `length = 120` limita a coluna a 120 caracteres. É a barreira de saneamento: título obrigatório e curto o suficiente para não virar um laudo.

A `descricao` guarda o texto auxiliar, aquele detalhe que não cabe no título. Ela é opcional por natureza, e por isso não recebe `nullable = false`. O `length = 500` aparece como proteção contra o abuso, não como convite: uma descrição de tarefa não deveria virar uma monografia.

O `concluido` é um `boolean` primitivo, e essa escolha tem camadas. O primitivo nasce falso, então nenhuma tarefa surge concluída sem querer. A coluna gerada é `NOT NULL`, sem os três estados que um `Boolean` empacotado traria ao introduzir o nulo. E o acesso é assimétrico: há getter `isConcluido()`, mas não existe `setConcluido()`. O estado só muda pelo método `concluir()`, encapsulando uma transição de domínio. É o mesmo espírito do record com construtor compacto que validamos no JShell da Parte 1: invariantes protegidas no ponto de entrada.

> ⚠️ *Aviso*: Você pode estar se perguntando: cadê o Lombok? Ele existe, é maduro e elimina exatamente esse bloco de getters e setters com `@Getter`, `@Setter` e `@Builder`. As vantagens são reais: menos linhas, menos manutenção manual e menos ruído visual. As desvantagens também: é mágica em tempo de compilação, depende de um processador de anotações que historicamente corre atrás de cada *release* nova do JDK e esconde os métodos que a JPA realmente lê para mapear a entidade. Neste momento da série, essa visibilidade importa mais do que a economia de linhas: queremos enxergar o Hibernate lendo os getters, os setters e as anotações `@Column` de forma explícita. Os Records já vão eliminar boa parte do *boilerplate* na Parte 4, agora como DTOs. Futuramente, se o projeto crescer e o time decidir, a gente revisita o Lombok com a devida cerimônia.

Além dos atributos, três decisões estruturais merecem destaque. O construtor sem argumentos é `protected`, cumprindo a exigência da JPA sem convidar o resto do código a criar tarefas vazias. O `toString` sobrescrito devolve uma representação legível da tarefa em vez do hash padrão `Tarefa@4de5031f`, o que vai facilitar os logs e a sessão de JShell daqui a pouco. E o `id` numérico é provisório: na Parte 5, ele dá lugar ao `UUIDv7` com Flyway. Nada aqui é definitivo, e isso é proposital.

## O repositório que escreve SQL sozinho

Com a entidade definida, a camada de repositório quase se escreve sozinha. Não é força de expressão. O **Spring Data JPA** [^1] gera a implementação em tempo de execução a partir de uma interface:

```java
package io.github.vndmtrx.tarefas_api.todo;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface TarefaRepository extends JpaRepository<Tarefa, Long> {

    List<Tarefa> findByConcluido(boolean concluido);

    List<Tarefa> findByTituloContainingIgnoreCase(String fragmento);

    long countByConcluido(boolean concluido);

    @Query("""
        SELECT t FROM Tarefa t
        WHERE LOWER(t.titulo) LIKE LOWER(CONCAT('%', :fragmento, '%'))
          AND t.concluido = false
        ORDER BY t.titulo ASC
    """)
    List<Tarefa> buscarPendentesPorTitulo(@Param("fragmento") String fragmento);
}
```
*Consultas derivadas automáticas combinadas a uma consulta customizada com JPQL.*

Herda-se `save`, `findById`, `findAll`, `delete` e companhia. Mas a grande mágica inicial reside nas **consultas derivadas**: o Spring lê `findByConcluido`, separa o prefixo `findBy` da propriedade `concluido` e gera a query SQL correspondente. `findByTituloContainingIgnoreCase` vira um `LIKE` com caixa ignorada. `countByConcluido` vira um `COUNT`.

Esse recurso é ágil, mas tem limites claros. Tentar expressar critérios compostos por derivação pode gerar monstros como `findByTituloContainingIgnoreCaseAndConcluidoFalseOrderByTituloAsc`. O método até compila, mas vira um trava-línguas ilegível e frágil.

É exatamente aqui que entram as **Custom Queries com `@Query`**. Com a anotação `@Query`, escrevemos a consulta diretamente em JPQL (*Java Persistence Query Language*), mantendo a consulta expressa sobre o modelo de objetos (`Tarefa t`) em vez de tabelas SQL cruas, e batizamos o método com um nome limpo e de intenção clara de negócio: `buscarPendentesPorTitulo(fragmento)`.

Repare no uso do parâmetro nomeado `:fragmento` casado com `@Param("fragmento")`. Em vez de amarrar a query à ordem dos argumentos com parâmetros posicionais (`?1`), os parâmetros nomeados tornam a instrução autoexplicativa e imune a quebras quando a assinatura do método for refatorada. Além disso, resolver a concatenação dos curingas diretamente no JPQL com `CONCAT('%', :fragmento, '%')` isola a responsabilidade de busca dentro do repositório: quem consome o método passa apenas a palavra limpa (`"estudar"`), sem a obrigação de poluir o código Java externo colando `%` nas pontas. Por baixo dos panos, o Hibernate traduz isso para variáveis de ligação (*bind parameters*) em um *Prepared Statement* do JDBC, blindando a consulta contra injeção de SQL por definição.

Contudo, mesmo o `@Query` tem suas restrições: ele é estático. Se o usuário da nossa API quiser combinar múltiplos filtros opcionais dinamicamente em tempo de execução (por exemplo, filtrar por status, por título ou por intervalos de datas em qualquer combinação), criar dezenas de variações de `@Query` seria inviável. É para resolver essa dor de forma definitiva que, na **Parte 9**, introduziremos o `JpaSpecificationExecutor` combinado ao vanguardista verbo **HTTP QUERY (RFC 9734)**.

> 💡 *Dica*: O nome do método derivado é o contrato. Renomeou a propriedade `titulo`? O método derivado quebra em tempo de compilação. Por isso, os testes de repositório no final desta parte não são penduricalhos: eles confirmam o comportamento que cada consulta promete.

## O serviço transacional e a regra que não mora no controller

Se o repositório responde pela persistência, quem responde pelas regras? O serviço. É nele que moram a validação do título vazio, a busca com exceção para id inexistente e a transição de estado da tarefa.

A classe:

```java
package io.github.vndmtrx.tarefas_api.todo;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class TarefaService {

    private final TarefaRepository repository;

    public TarefaService(TarefaRepository repository) {
        this.repository = repository;
    }

    @Transactional(readOnly = true)
    public List<Tarefa> listar() {
        return repository.findAll();
    }

    @Transactional(readOnly = true)
    public Tarefa buscarPorId(Long id) {
        return buscarTarefaPorId(id);
    }

    @Transactional
    public Tarefa criar(String titulo, String descricao) {
        validarTitulo(titulo);
        return repository.save(new Tarefa(titulo, descricao));
    }

    @Transactional
    public Tarefa atualizar(Long id, String titulo, String descricao) {
        validarTitulo(titulo);
        Tarefa tarefa = buscarTarefaPorId(id);
        tarefa.setTitulo(titulo);
        tarefa.setDescricao(descricao);
        return tarefa;
    }

    @Transactional
    public void excluir(Long id) {
        Tarefa tarefa = buscarTarefaPorId(id);
        repository.delete(tarefa);
    }

    @Transactional
    public Tarefa concluir(Long id) {
        Tarefa tarefa = buscarTarefaPorId(id);
        tarefa.concluir();
        return tarefa;
    }

    private Tarefa buscarTarefaPorId(Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("Tarefa nao encontrada: " + id));
    }

    private void validarTitulo(String titulo) {
        if (titulo == null || titulo.isBlank()) {
            throw new IllegalArgumentException("O titulo da tarefa nao pode ser vazio.");
        }
        if (titulo.length() > 120) {
            throw new IllegalArgumentException("O titulo ultrapassa 120 caracteres.");
        }
    }
}
```
*Repare que os métodos `atualizar` e `concluir` não chamam `repository.save()`: a entidade é gerenciada pelo Hibernate dentro da transação, e o dirty checking sincroniza o estado automaticamente.*

Três detalhes aqui merecem uma lupa atenta, porque mudam a forma como pensamos persistência e segurança de tipos no ecossistema JPA.

O primeiro é a ausência deliberada de `repository.save()` nos métodos de alteração. Quem veio do JDBC puro ou de DAOs procedurais costuma carregar o vício de mandar salvar cada objeto manualmente. No JPA, a mecânica é orientada a estado. Quando o método `buscarTarefaPorId` executa dentro de uma transação ativa (`@Transactional`), o Hibernate carrega a entidade para dentro do seu **contexto de persistência** no estado gerenciado (*managed*), guardando uma cópia fiel daquele registro (um *snapshot* em memória).

Quando você altera os atributos de `tarefa` (seja via setters ou pelo método de negócio `concluir()`), o objeto na memória muda, mas nenhuma instrução SQL é disparada de imediato. Ao final do método, quando o Spring prepara o *commit* da transação, o Hibernate executa a fase de *flush*: ele compara a entidade em memória com o *snapshot* inicial. Esse mecanismo é o **dirty checking** (*detecção de estado modificado*). Detectada a diferença, o próprio Hibernate gera e dispara o comando SQL `UPDATE` correspondente no banco. Invocar `save()` em uma entidade que já está no estado *managed* é redundância inócua.

O segundo detalhe é a gestão das fronteiras com `@Transactional`. O `@Transactional(readOnly = true)` nos métodos de listagem e busca sinaliza ao Hibernate que ele não precisa guardar *snapshots* nem rastrear alterações para aquela sessão, economizando memória e permitindo otimizações de leitura pura na conexão JDBC. Nos métodos de escrita, a anotação assegura atomicidade: se qualquer regra for violada ou uma exceção estourar no meio do caminho, o Spring comanda o *rollback* imediato e nada contamina o banco.

Há ainda um terceiro ponto no método auxiliar `buscarTarefaPorId`: o uso do `Optional` e a mentalidade funcional. Em código Java clássico, métodos de busca frequentemente devolviam `null`, transferindo para quem chama o fardo de lembrar do `if (tarefa == null)` sob pena de tomar o clássico `NullPointerException`. No Spring Data JPA, o `repository.findById()` retorna um `Optional<Tarefa>`, transformando a possibilidade de ausência em um contrato explícito no sistema de tipos.

O `Optional` não é um recurso isolado: ele faz parte do kit de ferramentas de **programação funcional** que o ecossistema Java adotou a partir do Java 8 (junto com Lambdas, Streams e o pacote `java.util.function`). Ele foi desenhado para se compor naturalmente com interfaces funcionais consagradas:

* **`Supplier<T>`:** No nosso `.orElseThrow(() -> new IllegalArgumentException(...))`, passamos uma função fornecedora. A vantagem é a avaliação preguiçosa (*lazy evaluation*): a exceção só é instanciada se o valor de fato não existir, economizando alocações de memória e o custo computacional de montar a *stacktrace*.
* **`Predicate<T>`:** Permite filtros declarativos via `.filter()`, testando condições sobre o valor embrulhado (ex: `optional.filter(Tarefa::isConcluido)`) sem recorrer a blocos `if` aninhados.
* **`Function<T, R>`:** Viabiliza transformações imutáveis com `.map()` e `.flatMap()`, convertendo a entidade em outro tipo apenas se ela estiver presente.
* **`Consumer<T>`:** Executa ações diretas sobre o valor com `.ifPresent()`, dispensando verificações manuais de existência.

Essa abordagem substitui o velho código imperativo e defensivo por fluxos declarativos, seguros e autoexplicativos. Ao longo da série, essa mesma fundação funcional reaparecerá em momentos decisivos: desde o processamento de coleções com Streams até a construção de filtros dinâmicos de banco de dados com `Predicate` e `Specification` na Parte 9.

Para o ponto atual desta série, usaremos o ferramental padronizado do Java com a exceção `IllegalArgumentException` para sinalizar tanto o título inválido quanto o id inexistente. Na Parte 4, quando apresentarmos o `@ControllerAdvice` e o tratamento global de erros, criaremos nossas próprias exceções de negócio desacopladas e as mapearemos para respostas HTTP `404` bem desenhadas.

## O controller rústico: apenas HTTP, por ora

O controller desta parte faz uma única coisa: traduzir HTTP para chamadas do serviço. Nada de SQL, nada de regra, nada de `if` espalhado. Ele ainda devolve a entidade diretamente no payload, e isso é um pecado que vamos confessar e corrigir na Parte 4. Agora, o objetivo é enxergar o fluxo inteiro funcionando.

Primeiro, um record mínimo para receber o corpo das requisições de criação e atualização:

```java
package io.github.vndmtrx.tarefas_api.todo;

public record TarefaRequest(String titulo, String descricao) {}
```
*O record evita que o corpo JSON seja desserializado direto na entidade JPA.*

Depois, o controller:

```java
package io.github.vndmtrx.tarefas_api.todo;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/tarefas")
public class TarefaController {

    private final TarefaService service;

    public TarefaController(TarefaService service) {
        this.service = service;
    }

    @GetMapping
    public List<Tarefa> listar() {
        return service.listar();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Tarefa> buscarPorId(@PathVariable Long id) {
        return ResponseEntity.ok(service.buscarPorId(id));
    }

    @PostMapping
    public ResponseEntity<Tarefa> criar(@RequestBody TarefaRequest request) {
        Tarefa criada = service.criar(request.titulo(), request.descricao());
        return ResponseEntity.status(HttpStatus.CREATED).body(criada);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Tarefa> atualizar(@PathVariable Long id, @RequestBody TarefaRequest request) {
        return ResponseEntity.ok(service.atualizar(id, request.titulo(), request.descricao()));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> excluir(@PathVariable Long id) {
        service.excluir(id);
        return ResponseEntity.noContent().build();
    }

    @PatchMapping("/{id}/concluir")
    public ResponseEntity<Tarefa> concluir(@PathVariable Long id) {
        return ResponseEntity.ok(service.concluir(id));
    }
}
```
*Os status seguem a semântica HTTP: 200 para leitura e atualização, 201 para criação e 204 para exclusão.*

O `TarefaRequest` não é a camada de DTOs que a aplicação merece. É um remendo honesto para não bater a entidade inteira no JSON de entrada. A resposta, porém, ainda expõe a entidade nua. Na Parte 4, a coisa muda de figura: DTOs de visão, MapStruct e Bean Validation entram para valer.

## O JShell com o contexto inteiro do Spring

Na Parte 2, o JShell serviu para inspecionar Record e `ResponseEntity` isolados. Dá para ir além? Dá. Agora dá para subir o contexto completo do Spring dentro do REPL, H2 e tudo, sem servidor web no caminho.

O ritual é o mesmo de antes:

```bash
$ ./mvnw compile
# Recompila as classes novas e as já existentes

$ ./mvnw dependency:build-classpath -Dmdep.outputFile=.classpath.txt
# Reexporta o classpath com JPA, Hibernate e H2

$ jshell --class-path target/classes:$(cat .classpath.txt)
# Abre o REPL enxergando as classes compiladas e as dependencias
```

Dentro do JShell, o truque é iniciar o `SpringApplication` com o perfil web desativado. Assim o contexto sobe com JPA e H2, mas sem abrir porta HTTP:

```bash
jshell> import org.springframework.boot.SpringApplication;
jshell> import io.github.vndmtrx.tarefas_api.*;
jshell> import io.github.vndmtrx.tarefas_api.todo.*;

jshell> var contexto = SpringApplication.run(TarefasApiApplication.class, "--spring.main.web-application-type=none");
# O console despeja os logs do Hibernate; ao final, o contexto fica no ar

jshell> var service = contexto.getBean(TarefaService.class);
service ==> io.github.vndmtrx.tarefas_api.todo.TarefaService@2f9f7a5c

jshell> var t1 = service.criar("Estudar Spring Data JPA", "Ler a documentacao");
t1 ==> Tarefa{id=1, titulo='Estudar Spring Data JPA', concluido=false}

jshell> var t2 = service.criar("Preparar o ambiente JShell", "");
t2 ==> Tarefa{id=2, titulo='Preparar o ambiente JShell', concluido=false}

jshell> service.concluir(2L);
$7 ==> Tarefa{id=2, titulo='Preparar o ambiente JShell', concluido=true}

jshell> service.listar();
$8 ==> [Tarefa{id=1, titulo='Estudar Spring Data JPA', concluido=false}, Tarefa{id=2, titulo='Preparar o ambiente JShell', concluido=true}]

jshell> contexto.close();
# Encerra o contexto e descarta o banco em memoria

jshell> /exit
|  Goodbye
```

> ℹ️ *Nota*: Esse warning do H2 no `contexto.close()` é esperado e inofensivo. O Hibernate fecha o banco antes que o bean `inMemoryDatabaseShutdownExecutor` do Spring Boot tente o `SHUTDOWN` final; daí o *"Database is already closed"*. O encerramento continua normalmente em seguida, com o pool do HikariCP sendo fechado e o JShell saindo com `Goodbye`.

Isso não é teste automatizado, e não substitui um. É exploração guiada, a mesma lógica de REPL-Driven Development da Parte 1: provar a hipótese no terminal antes de formalizar a garantia. O `toString` da entidade, que adicionamos sem grande alarde, agora paga a conta da legibilidade.

## O contrato de testes: serviço e persistência

Explorar no JShell é o aquecimento. A regra da série continua a mesma: código avança com a suíte verde.

Para o serviço, o teste é unitário puro. O repositório vira mock e o serviço é exercitado como uma classe Java comum, herança direta da injeção por construtor que adotamos na Parte 2:

```java
package io.github.vndmtrx.tarefas_api.todo;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class TarefaServiceTest {

    @Mock
    private TarefaRepository repository;

    private TarefaService service;

    @BeforeEach
    void setUp() {
        service = new TarefaService(repository);
    }

    @Test
    @DisplayName("Deve criar tarefa valida persistindo no repositorio")
    void deveCriarTarefaComSucesso() {
        when(repository.save(any(Tarefa.class))).thenReturn(new Tarefa("Estudar JPA", ""));

        Tarefa criada = service.criar("Estudar JPA", "");

        assertEquals("Estudar JPA", criada.getTitulo());
        verify(repository).save(any(Tarefa.class));
    }

    @Test
    @DisplayName("Deve rejeitar titulo vazio sem tocar no repositorio")
    void deveRejeitarTituloVazio() {
        assertThrows(IllegalArgumentException.class,
                () -> service.criar("", "Sem titulo"));

        verify(repository, never()).save(any(Tarefa.class));
    }

    @Test
    @DisplayName("Deve concluir uma tarefa existente")
    void deveConcluirTarefaExistente() {
        when(repository.findById(1L)).thenReturn(Optional.of(new Tarefa("Pagar contas", "")));

        Tarefa concluida = service.concluir(1L);

        assertTrue(concluida.isConcluido());
        verify(repository).findById(1L);
    }

    @Test
    @DisplayName("Deve lancar excecao para id inexistente")
    void deveLancarExcecaoParaIdInexistente() {
        when(repository.findById(99L)).thenReturn(Optional.empty());

        assertThrows(IllegalArgumentException.class,
                () -> service.buscarPorId(99L));
    }
}
```
*Quatro cenários cobrindo o caminho feliz, uma validação, uma transição de estado e a ausência do recurso.*

Para o repositório, o teste é de fatia com `@DataJpaTest`. Ele sobe o H2 de verdade, cria o schema a partir das entidades e deixa a gente bater na base sem mocks [^4]:

```java
package io.github.vndmtrx.tarefas_api.todo;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.data.jpa.test.autoconfigure.DataJpaTest;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@DataJpaTest
class TarefaRepositoryTest {

    @Autowired
    private TarefaRepository repository;

    @Test
    @DisplayName("Deve persistir e contar tarefas por status")
    void devePersistirEContarPorStatus() {
        repository.save(new Tarefa("Fazer cafe", ""));
        Tarefa concluida = new Tarefa("Dormir", "");
        concluida.concluir();
        repository.save(concluida);

        assertEquals(2, repository.count());
        assertEquals(1L, repository.countByConcluido(false));
        assertEquals(1L, repository.countByConcluido(true));
    }

    @Test
    @DisplayName("Deve filtrar por fragmento do titulo ignorando caixa")
    void deveFiltrarPorFragmentoDeTituloIgnorandoCaixa() {
        repository.save(new Tarefa("Configurar Flyway", ""));
        repository.save(new Tarefa("Configurar CORS", ""));
        repository.save(new Tarefa("Deploy no Kubernetes", ""));

        List<Tarefa> resultado = repository.findByTituloContainingIgnoreCase("configurar");

        assertEquals(2, resultado.size());
        assertTrue(resultado.stream().allMatch(t -> t.getTitulo().toLowerCase().contains("configurar")));
    }

    @Test
    @DisplayName("Deve buscar tarefas pendentes por fragmento de titulo ordenadas")
    void deveBuscarPendentesPorFragmentoDeTituloOrdenadas() {
        Tarefa t1 = new Tarefa("Estudar Spring Data JPA", "");
        Tarefa t2 = new Tarefa("Estudar Hibernate", "");
        Tarefa t3 = new Tarefa("Estudar Docker", "");
        t3.concluir();

        repository.save(t1);
        repository.save(t2);
        repository.save(t3);

        List<Tarefa> resultado = repository.buscarPendentesPorTitulo("estudar");

        assertEquals(2, resultado.size());
        assertEquals("Estudar Hibernate", resultado.get(0).getTitulo());
        assertEquals("Estudar Spring Data JPA", resultado.get(1).getTitulo());
    }
}
```
*Repare no pacote `boot.data.jpa.test.autoconfigure`, herança da reorganização de módulos do Spring Boot 4.*

Rodamos tudo:

```bash
$ ./mvnw test
# Executa a suite completa da aplicacao
```

O resultado esperado é a suíte inteira verde, somando os dois testes da Parte 2 aos sete novos:

```
[INFO] Results:
[INFO]
[INFO] Tests run: 9, Failures: 0, Errors: 0, Skipped: 0
[INFO]
[INFO] BUILD SUCCESS
```

Nove testes verdes significam que a fatia de domínio está segura para evoluir. É o critério de saída que importa.

## Exercícios

Para fixar a dinâmica de camadas, persistência e testes, execute os desafios abaixo.

**1. Endpoint de listagem por status**

Adicione no serviço um método `listarPorStatus(boolean concluido)` que delegue ao `repository.findByConcluido` e exponha no controller um endpoint `GET /api/tarefas?concluida=true` que filtre pelo *flag* de conclusão.

<details markdown="1">
<summary>Ver resposta</summary>

No `TarefaService.java`, adicione:

```java
@Transactional(readOnly = true)
public List<Tarefa> listarPorStatus(boolean concluido) {
    return repository.findByConcluido(concluido);
}
```

No `TarefaController.java`, adicione o mapeamento com parâmetro:

```java
@GetMapping(params = "concluida")
public List<Tarefa> listarPorStatus(@RequestParam("concluida") boolean concluida) {
    return service.listarPorStatus(concluida);
}
```

Teste com `curl` após subir a aplicação:

```bash
$ curl -s "http://localhost:8080/api/tarefas?concluida=false"
[{"id":1,"titulo":"Fazer cafe","descricao":"","concluido":false}]
```

*O `@GetMapping(params = "concluida")` separa o mapeamento com query param do GET simples, sem conflito de rotas.*

</details>

**2. Criando e listando tarefas via HTTP**

Suba a aplicação com `./mvnw spring-boot:run` e use o `curl` para criar uma tarefa com `POST` e listar a coleção com `GET`, validando o JSON de ida e volta.

<details markdown="1">
<summary>Ver resposta</summary>

```bash
# Terminal 1: Iniciar a aplicacao
$ ./mvnw spring-boot:run

# Terminal 2: Criar uma tarefa
$ curl -s -X POST http://localhost:8080/api/tarefas \
    -H "Content-Type: application/json" \
    -d '{"titulo":"Organizar a estante","descricao":"Livros tecnicos"}'
{"id":1,"titulo":"Organizar a estante","descricao":"Livros tecnicos","concluido":false}

# Terminal 2: Listar as tarefas persistidas
$ curl -s http://localhost:8080/api/tarefas
[{"id":1,"titulo":"Organizar a estante","descricao":"Livros tecnicos","concluido":false}]
```

*O H2 em memória persiste os dados enquanto o processo estiver no ar. Ao encerrar com `Ctrl + C`, o banco some junto.*

</details>

**3. Testando a exclusão de id inexistente**

Escreva um teste unitário para o cenário em que `excluir(7L)` é chamado, mas o repositório não encontra a tarefa. A exceção esperada é `IllegalArgumentException`.

<details markdown="1">
<summary>Ver resposta</summary>

No `TarefaServiceTest.java`, adicione:

```java
@Test
@DisplayName("Deve lancar excecao ao excluir id inexistente")
void deveLancarExcecaoAoExcluirIdInexistente() {
    when(repository.findById(7L)).thenReturn(Optional.empty());

    assertThrows(IllegalArgumentException.class,
            () -> service.excluir(7L));

    verify(repository, never()).delete(any(Tarefa.class));
}
```

Execute `./mvnw test -Dtest=TarefaServiceTest` para validar o novo cenário.

</details>

## O ponto de partida para o refinamento

Uma aplicação que persiste de verdade muda o tom da jornada. Deixamos de ter um esqueleto educado e passamos a ter um organismo: tarefa nasce, é buscada, alterada, concluída, removida. E em nenhum momento o H2, o Hibernate ou o repositório vazaram para dentro do controller.

Mas esta parte deixa uma dívida técnica assumida. A resposta da API ainda é a entidade nua. Não há DTOs separando visões. Não há validação declarativa nos corpos de entrada. Um erro de negócio ainda vira stacktrace genérico em vez de um JSON de erro desenhado.

Isso é dívida deliberada, não omissão. Na Parte 4, a camada de apresentação é reconstruída em cima de Java Records como DTOs, MapStruct para as conversões e Bean Validation com captura global via `@ControllerAdvice`. O "JPA no controller" morre de vez, e o serviço deixa de ver a entidade cruzar a fronteira do HTTP.

Até lá, a base está firme: banco parametrizado no padrão 12-Factor, persistência em camadas e oito testes garantindo o contrato. Agora dá para refinar sem medo de desmoronar.

## Referências

[^1]: **Spring Data JPA Reference Documentation** {*Spring / VMware Tanzu*} ([Link](https://docs.spring.io/spring-data/jpa/reference/))

[^2]: **Jakarta Persistence 3.2 Specification** {*Jakarta EE / Eclipse Foundation*} ([Link](https://jakarta.ee/specifications/persistence/3.2/))

[^3]: **H2 Database Engine Documentation** {*H2 Database*} ([Link](https://h2database.com/html/main.html))

[^4]: **Testing with @DataJpaTest** {*Spring Boot Reference Documentation*} ([Link](https://docs.spring.io/spring-boot/reference/testing/spring-boot-applications.html#testing.spring-boot-applications.autoconfigured-spring-data-jpa))

[^5]: **Hibernate ORM User Guide: Schema Generation (hbm2ddl.auto)** {*Hibernate ORM*} ([Link](https://docs.hibernate.org/orm/current/userguide/html_single/#schema-generation))
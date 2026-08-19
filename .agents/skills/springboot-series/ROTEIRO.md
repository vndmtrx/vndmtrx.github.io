# Roteiro Completo - Série Spring Boot Tutorial

Série de posts para o blog `vndmtrx.github.io` abordando o ecossistema Spring Boot com Java 26, focando em boas práticas de engenharia de software, observabilidade, resiliência, automação e infraestrutura de produção.

---

## Estrutura da Série

| Bloco | Posts | Foco Principal | Descrição |
| :--- | :--- | :--- | :--- |
| **Fundação e Arquitetura** | 1 a 4 | Setup, 12-Factor, Core & DTOs | Do ambiente zero telemetria ao desacoplamento de entidades com Records e MapStruct |
| **Persistência e Contratos** | 5 a 7 | Postgres 18, Design-First OpenAPI & HATEOAS | Versionamento de banco com Flyway, Swagger Editor isolado e RESTful nível 3 |
| **Maturidade e Especificações** | 8 a 10 | BDD / Testcontainers, HTTP QUERY & Jobs | Testes reais com Docker, RFC 9734 (HTTP QUERY) e automações assíncronas |
| **Segurança e Produção** | 11 a 13 | JWT / Envers, OpenTelemetry & Resilience4J | Auditoria completa, telemetria unificada e padrões de resiliência com Redis |
| **Deploy e Distribuição** | 14 a 15 | K8s / Helm & Mensageria EDA | Empacotamento em imagens OCI, Helm charts e mensageria distribuída com DLQ |

---

## Detalhamento das 15 Partes

### Parte 1: Ambiente de Desenvolvimento
- **OS**: Debian Trixie como base de trabalho
- **SDKMAN**: Gerenciamento de SDKs e uso de `.sdkmanrc` para garantir paridade de versão (JDK Temurin 26)
- **Editor**: VS Codium (Open Source/Telemetry-free via `extrepo`)
- **Extensões**: Language Pack (pt-BR), Extension Pack for Java (`vscjava`) e Spring Boot Extension Pack (`VMware`)
- **Interação**: Introdução ao **JShell (Java REPL)** para exploração de APIs (records, dates) e cultura de *tinkering*
- **Objetivo**: Configurar um ambiente local produtivo, padronizado, livre de telemetria e focado em agilidade via CLI.
- **Entregável**: Terminal operacional com JDK 26 via SDKMAN e VS Codium pronto com ciclo de feedback via JShell validado.

### Parte 2: Projeto Base e a Filosofia 12-Factor
- **Conceito Teórico**: Introdução aos **12-Factor App** (foco em Config, Backing Services e Paridade Dev/Prod)
- **Ferramentas**: Inicialização via Spring Initializr (selecionando Maven)
- **Dependências**: `spring-boot-starter-web`, `spring-boot-devtools`
- **Prática**: Hello endpoint (que evoluirá para health check) e configuração externa via ENV VARS no `application.yaml` (`DB_URL`, `DB_USER`, `DB_PASS`, `DDL_AUTO`, `JWT_SECRET`)
- **Testes**: Teste unitário inicial do Controller e garantia de 100% de sucesso para avançar.
- **Interação**: Uso do **JShell (Java REPL)** integrado ao contexto do Spring Boot para exploração em tempo real e o papel do **DevTools** no ciclo de feedback rápido.
- **Objetivo**: Estruturar a base da aplicação seguindo boas práticas de isolamento de ambiente e configuração externa.
- **Entregável**: Projeto Spring Boot funcional, inicializado via Gradle, com endpoint básico e propriedades de infraestrutura parametrizadas por variáveis de ambiente.

### Parte 3: Core API (Model/Repo/Service/Controller)
- **Dependências**: `spring-boot-starter-data-jpa`, `com.h2database:h2`
- **Domínio**: Entidade `Todo` (id, título, conteúdo, concluído)
- **Persistência**: `JpaRepository` com H2 + `findByConcluido` + custom queries básicas
- **Camadas**: Service e Controller REST manuais (temporários, preparando o terreno para o desacoplamento)
- **Interação**: Usando o REPL/JShell para interagir com o `@Service`
- **Testes**: Implementação de testes unitários de Service (com mocks) e persistência (`@DataJpaTest`). Sucesso total como critério de saída.
- **Objetivo**: Implementar o fluxo básico de persistência e regras de negócio usando a arquitetura tradicional em camadas.
- **Entregável**: CRUD de transações de persistência isolado na camada de serviço e exposto em endpoints REST rudimentares com cobertura de testes.

### Parte 4: Refinamento e Contratos (O fim do "JPA no Controller")
- **Dependências**: `spring-boot-starter-validation`, `org.mapstruct:mapstruct`
- **Padrão**: DTOs com Java Records (desacoplando a Entidade da API) com configurações específicas (insert, visões de listagem, campos ocultos)
- **Conversão**: Mapeamento Service <-> Controller usando MapStruct
- **Validação**: Bean Validation (`@Valid`) nos Records e tratamento global de erros com `@ControllerAdvice` e Exceptions customizadas
- **Testes**: Testes unitários para validar regras de negócio nos Records, DTOs e lógica do MapStruct. Sucesso de 100% obrigatório.
- **Objetivo**: Blindar a integridade dos dados e desacoplar o modelo de banco de dados da camada pública da API.
- **Entregável**: Camada de apresentação reestruturada exclusivamente com Java Records validados e mapeados via MapStruct, capturando falhas globalmente.

### Parte 5: Persistência Real com Postgres 18
- **Dependências**: `org.postgresql:postgresql`, `org.flywaydb:flyway-core`, `org.flywaydb:flyway-database-postgresql`
- **Infra**: Postgres 18 em Docker + Flyway para migrations (versionamento de schema)
- **Estratégia**: `create-drop` (H2) vs `validate` (Postgres) com Flyway
- **Config**: Profiles Spring (H2 para testes rápidos, Postgres para dev/homolog) expandindo ENV vars (`DB_URL` postgres)
- **Compatibilidade**: Dialeto Postgres no H2 para garantir paridade dev/test
- **PG Tech**: Uso de `UUIDv7` e campos `JSONB` para metadados/tags
- **HikariCP**: Tuning básico do pool de conexões (auto-config)
- **Testes**: Ajuste dos testes unitários/persistência para garantir compatibilidade entre H2 e Postgres 18. Sucesso total.
- **Objetivo**: Migrar o armazenamento em memória para um banco de dados relacional de produção utilizando versionamento estruturado de schema.
- **Entregável**: Banco de dados Postgres 18 ativo via Docker Compose, histórico de tabelas controlado por migrations Flyway e uso nativo de tipos avançados (UUIDv7/JSONB).

### Parte 6: Contrato Independente e Documentação Viva (Design-First)
- **Contextualização Crítica**: Explicação sobre a existência do SpringDoc e a abordagem Code-First (anotações poluindo o código). Discussão sobre o problema real de incompatibilidade do SpringDoc com o ecossistema do Spring Boot 4.x / versões modernas.
- **Comparação Visual**: Exibição de um exemplo simples de documentação automática com SpringDoc em um endpoint "Hello World" versus os benefícios de seguir com o design limpo proposto na série. Decisão arquitetural de seguir sem o SpringDoc para total independência do ecossistema.
- **Ferramentas**: Subida do **Swagger Editor local via Docker** para apoio à escrita. Uso do `openapi-generator-maven-plugin` (ou equivalente Gradle) + WebJar `swagger-ui` (ou Scalar).
- **Prática**: Modelagem visual do contrato inicial em OpenAPI 3.0 usando o painel bicoluna e validação em tempo real do Swagger Editor. Salvamento do contrato final como `openapi.yaml` em `src/main/resources/static/docs/`.
- **QoL**: Criação de um `index.html` estático consumindo o WebJar para renderizar o Swagger UI local por conta própria. Configuração do plugin de compilação para gerar as interfaces dos controllers de forma autônoma.
- **Testes**: Adaptação e execução dos testes existentes contra as novas interfaces Java autogeradas.
- **Objetivo**: Romper a dependência de varreduras em tempo de execução através da adoção da filosofia Design-First com ferramentas isoladas da JVM.
- **Entregável**: Interface gráfica do Swagger UI servida estaticamente em `/docs/index.html` a partir de um contrato criado via Swagger Editor Docker, gerando código Java limpo.

### Parte 7: Arquitetura: RESTful vs RPC
- **Dependências**: `spring-boot-starter-hateoas`
- **Teoria**: Níveis de maturidade de Richardson e o "pecado" do RPC disfarçado de REST. Verbos HTTP tradicionais e as limitações de usar `POST` para buscas complexas.
- **Prática**: Retorno ao **Swagger Editor local** para evoluir a especificação do contrato `openapi.yaml`, adicionando o mapeamento estrutural dos objetos de hipermídia (`_links`). Ativação da flag de suporte a HATEOAS nas propriedades do plugin gerador de código. Implementação de navegação dinâmica via hipermídia nos Controllers.
- **Testes**: Testes unitários focados na validação dos links HATEOAS e estrutura RESTful. Sucesso total de 100%.
- **Objetivo**: Elevar a API ao nível máximo de maturidade REST através da inclusão de hipermídia diretamente na definição do contrato e na resposta do servidor.
- **Entregável**: Contrato OpenAPI atualizado com objetos de link e payloads JSON de produção contendo referências dinâmicas de navegação HATEOAS (`_links`).

### Parte 8: Testes de Integração e Specs (Elevando a Maturidade)
- **Dependências**: `org.testcontainers:postgresql`, `org.testcontainers:junit-jupiter`, `io.cucumber:cucumber-java`, `com.github.tomakehurst:wiremock-jre8-standalone`
- **Estratégia**: Testes de Unidade (JUnit 5) vs Testes de Integração Reais com Testcontainers (Docker real)
- **BDD**: Escrita de specs com Cucumber (Gherkin) usando `features/*.feature`
- **Resiliência**: Simulando falhas de serviços externos com WireMock (ex: Redis/Postgres down)
- **Objetivo**: Implementar uma suíte de testes robusta baseada em comportamento (BDD) e infraestrutura idêntica à de produção.
- **Entregável**: Testes automatizados executando contra cenários reais de banco de dados no Testcontainers e simulações de interrupção de rede validadas via WireMock.

### Parte 9: Paginação, Filtros Dinâmicos e o Novo Verbo HTTP QUERY
- **Conceito Vanguardista**: Introdução ao método **HTTP QUERY (RFC 9734)**. Discussão sobre a morte do "POST de busca" e como passar payloads complexos de filtragem de forma segura e idempotente sem estourar limites de URL.
- **Contrato**: Uso do **Swagger Editor** para modelar o endpoint `/todos/search` utilizando o método `QUERY` com um objeto de filtragem estruturado no `requestBody`.
- **Prática**: Captura do método `QUERY` usando `@RequestMapping(method = RequestMethod.QUERY)` no Spring Boot. Implementação de `Pageable` e uso de `JpaSpecificationExecutor` para realizar consultas complexas direto no campo `JSONB` (ex: `tag=urgente` AND `concluido=false`).
- **Testes**: Garantia de 100% de sucesso na lógica de filtragem dinâmica disparando requisições com o verbo `QUERY`.
- **Objetivo**: Resolver restrições históricas de busca em APIs REST através do uso legítimo da especificação oficial do novo verbo HTTP QUERY.
- **Entregável**: Mecanismo de busca avançada paginada em campo JSONB exposto por meio de requisições idempotentes com corpo utilizando o método QUERY.

### Parte 10: Calendário, Agendamento e Background Jobs
- **Domínio**: Introdução do sistema de calendário com o campo `dataPrevista`
- **Agendamento**: `@EnableScheduling` e `@Scheduled` para automação de tarefas (ex: ajustar status baseado na `dataPrevista`)
- **Fila Local**: Implementação de fila local com `BlockingQueue` + `ExecutorService` ou uso de `@Async` com `TaskExecutor` customizado
- **Testes**: Testes de unidade para garantir que os agendamentos e tarefas assíncronas rodam conforme o esperado. Sucesso total obrigatório.
- **Objetivo**: Habilitar a execução de processamento assíncrono e tarefas temporizadas em segundo plano dentro do ciclo do Spring.
- **Entregável**: Rotinas de varredura automatizadas por cron e agendador nativo processando tarefas de segundo plano sem bloquear a linha de resposta HTTP.

### Parte 11: Usuários, Security e Auditoria Completa
- **Dependências**: `spring-boot-starter-security`, `io.jsonwebtoken:jjwt`, `org.hibernate.orm:hibernate-envers`
- **Security**: Entidade `User` e autenticação Stateless via JWT (segredo via `JWT_SECRET`). Proteção de APIs de escrita (login required). Liberação explícita das rotas estáticas `/docs/**` e `/webjars/**` no `SecurityFilterChain`.
- **Auditoria**: Uso de `MappedSuperclass` para campos de controle (`@CreatedBy`, `@LastModifiedBy`) e histórico via Hibernate Envers (tabelas `*_AUD` no schema)
- **Contexto**: Implementação de `AuditorAware<String>` integrado ao `SecurityContext` para capturar o usuário logado automaticamente
- **Testes**: Testes de segurança (MockMvc) e validação dos logs de auditoria. Sucesso total de 100%.
- **Objetivo**: Estabelecer controle de acesso seguro e trilha de auditoria automatizada para monitoramento de alterações de estado.
- **Entregável**: Fluxo de emissão e validação de tokens JWT ativo com rotas de documentação liberadas e versionamento automático de alterações via tabelas Envers.

### Parte 12: Observabilidade (O que acontece em produção?)
- **Dependências**: `spring-boot-starter-actuator`, `io.micrometer:micrometer-registry-prometheus`
- **Métricas**: Exposição de métricas para Prometheus e logs estruturados em JSON
- **Saúde**: Customização de Health Checks no Actuator e exploração dos endpoints de controle (`/actuator/*`)
- **Tracing**: Introdução ao rastreamento distribuído com **OpenTelemetry**, integrando métricas, logs e traces.
- **Testes**: Garantia de 100% de sucesso nos testes unitários.
- **Objetivo**: Tornar a aplicação transparente e monitorável em tempo real através da coleta unificada de telemetria de produção.
- **Entregável**: Endpoints do Actuator customizados expondo telemetria estruturada em formato OpenTelemetry e JSON para instrumentação de plataformas externas.

### Parte 13: Caches e Resiliência (Padrões de Escala)
- **Dependências**: `spring-boot-starter-data-redis`, `io.github.resilience4j:resilience4j-spring-boot3`
- **Performance**: Cache distribuído com Redis (docker, `REDIS_URL`) via `@Cacheable`
- **Padrões**: Implementação completa de Resilience4J: `@CircuitBreaker`, `@Retry`, `@TimeLimiter`, `@Bulkhead` e fallbacks
- **Métricas**: Monitoramento via Actuator (`/circuitbreakerevents`, `/retries`)
- **Testes**: Garantia de 100% de sucesso.
- **Objetivo**: Proteger a estabilidade e otimizar os tempos de resposta do sistema sob condições severas de estresse ou falhas de terceiros.
- **Entregável**: Camada de cache distribuída em Redis integrada ao Spring e circuitos de contingência Resilience4J ativos com estratégias de fallback validadas.

### Parte 14: Containerização e o Caminho para o K8s
- **Tooling**: Gradle/Maven para configurar `bootBuildImage` (OCI via Cloud Native Buildpacks)
- **Infra**: `Dockerfile` + `docker-compose.yml` (App + Postgres + Redis)
- **K8s**: Manifestos (Deployment, Service, ConfigMap) e uso de Probes do Actuator no Helm Chart
- **Config**: Endpoint prefixes via ENV (`server.servlet.context-path=${API_PATH:/api}`, `management.endpoints.web.base-path=${ACTUATOR_PATH:/actuator}`)
- **Helm**: Gerenciamento de secrets (DB/JWT), probes e replicas
- **Deploy**: Ciclo completo: `docker-compose up` até `kubectl apply` / `helm install`
- **Testes Final**: Verificação total do sistema rodando em container.
- **Objetivo**: Empacotar a aplicação dentro dos padrões de distribuição em nuvem e estruturar a orquestração para ambientes Kubernetes.
- **Entregável**: Imagem OCI otimizada via Buildpacks e pacote de gráficos Helm configurado com liveness/readiness probes pronto para implantação em cluster.

### Parte 15: Bônus - Mensageria Distribuída e EDA
- **Dependências**: `spring-boot-starter-amqp` (RabbitMQ) ou `spring-kafka`
- **Conceito**: A transição da Fila Local (Parte 10) para uma Arquitetura Orientada a Eventos (EDA)
- **Padrões**: Implementação de Producers/Consumers, tratamento de retentativas e Dead Letter Queues (DLQ)
- **Testes**: Uso de Testcontainers para subir o Broker (Rabbit/Kafka) nos testes de integração. Sucesso total de 100%.
- **Objetivo**: Desacoplar a comunicação de microsserviços migrando do processamento síncrono local para troca assíncrona de mensagens distribuídas.
- **Entregável**: Produtores e consumidores de mensagens resilientes operando em cima de filas distribuídas com tratamento automático de erros via DLQ.

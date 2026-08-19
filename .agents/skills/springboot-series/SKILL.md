---
name: springboot-series
description: >
  Skill e roteiro para a série "Spring Boot Tutorial" do blog vndmtrx.github.io.
  Contém as convenções arquiteturais, decisões de design, stack tecnológica e o
  roteiro de 15 partes (do setup de ambiente ao deploy em Kubernetes e mensageria).
---

# Skill: Série Spring Boot Tutorial

Diretrizes, convenções técnicas e arquiteturais para os posts da série **Spring Boot Tutorial** no blog `vndmtrx.github.io`.

---

## 1. Visão Geral e Filosofia da Série

A série **Spring Boot Tutorial** acompanha a construção progressiva de uma API backend moderna para gerenciamento de tarefas (*TODO*), abordada sob a perspectiva de um engenheiro de infraestrutura, segurança e DevOps. 

O objetivo não é reinventar a roda com um CRUD trivial, mas usar um domínio simples para explorar a fundo decisões de arquitetura de produção, resiliência, observabilidade, conformidade com o 12-Factor App e padrões de engenharia modernos.

### Convenções de Publicação
- **Série no Front Matter:** `series: Spring Boot Tutorial`
- **Padrão de Título:** `title: "Spring Boot Tutorial, Parte X - [Tema]"`
- **Subtítulo:** `subtitle: "[Frase descritiva e direta sobre o tema técnico abordado]"`
- **Tags Recomendadas:** `[Spring Boot, Java, Backend, DevOps, Infraestrutura, Arquitetura]` (conforme o tema do post)
- **Callout de Abertura:** Sempre incluir na abertura:
  ```markdown
  > 🔔 *Nota da Série*: Este post faz parte da série **"Spring Boot Tutorial"**, onde construímos do zero uma API backend de produção com **Spring Boot**, explorando boas práticas de arquitetura, contratos, persistência, resiliência, observabilidade e nuvem.
  ```

---

## 2. Stack Tecnológica e Decisões Arquiteturais

| Camada / Tópico | Escolha Tecnológica | Racional e Diretriz |
| :--- | :--- | :--- |
| **Sistema Operacional** | Debian GNU/Linux 13 (Trixie) | Base estável, minimalista e padrão para labs de infraestrutura. |
| **Runtime & SDK** | Eclipse Temurin JDK 26 via SDKMAN | Paridade rigorosa de versão garantida por `.sdkmanrc` em cada projeto. |
| **IDE / Editor** | VS Codium via `extrepo` | Ambiente de desenvolvimento livre de telemetria e open source com extensões oficiais Java/Spring. |
| **Experimentação** | Java JShell (REPL) & DevTools | Cultura de *tinkering* e REPL-driven development para validação rápida de APIs antes da escrita formal. |
| **Build Tool** | Apache Maven | Builds determinísticas e declarativas com `pom.xml` e plugins padrão do ecossistema. |
| **Persistência** | H2 (in-memory dev/test) -> PostgreSQL 18 (Docker) | Migração estruturada com Flyway, uso nativo de `UUIDv7` e campos `JSONB` para metadados/tags. |
| **Contrato & Docs** | OpenAPI 3.0 (Swagger Editor) & SpringDoc OpenAPI v3.1.0+ | Comparação prática: Design-First (contrato estático e geração via plugin) vs SpringDoc integrado em runtime no Spring Boot. |
| **Protocolo HTTP** | RESTful com HATEOAS & **HTTP QUERY (RFC 9734)** | Maturidade Richardson nível 3 e uso do verbo `QUERY` para buscas idempotentes com payload complexo. |
| **Testes** | JUnit 5, Mockito, Testcontainers, Cucumber (BDD) e WireMock | Testes de unidade estritos (100% de sucesso) combinados com testes de integração reais em containers. |
| **Segurança & Auditoria** | Spring Security + JWT Stateless + Hibernate Envers | Autenticação limpa, `AuditorAware` e rastreabilidade total de auditoria em tabelas `*_AUD`. |
| **Observabilidade** | Actuator, Prometheus & OpenTelemetry | Telemetria distribuída com logs estruturados em JSON, métricas e tracing unificado. |
| **Resiliência & Cache** | Redis + Resilience4J | Caching distribuído e padrões `@CircuitBreaker`, `@Retry`, `@Bulkhead` e `@TimeLimiter`. |
| **Deploy & Nuvem** | Cloud Native Buildpacks (`bootBuildImage`) + Helm / K8s | Imagens OCI otimizadas e manifestos Kubernetes com Probes integradas ao Actuator. |
| **Mensageria** | RabbitMQ / Apache Kafka com Testcontainers | Evolução de filas locais em memória para arquiteturas orientadas a eventos (EDA) com DLQ. |

---

## 3. Roteiro e Estrutura dos Posts

Consulte o arquivo [`ROTEIRO.md`](file:///home/rolim/du/dev/github/vndmtrx.github.io/.agents/skills/springboot-series/ROTEIRO.md) para a ementa completa das 15 partes.

Cada post deve seguir o arco narrativo definido na skill [`blog-posts`](file:///home/rolim/du/dev/github/vndmtrx.github.io/.agents/skills/blog-posts/SKILL.md):
1. **Abertura:** Contextualização do problema real de engenharia (sem enrolação ou clichês de IA).
2. **Desenvolvimento em Seções `##`:** Problema -> Racional da Solução -> Implementação Prática -> Comandos e Código comentados.
3. **Ritmo e Cadência Fractal:** Alternância de blocos densos (sístole) com respiros ágeis (diástole) e períodos *staccato* / *legato*.
4. **Fechamento:** Reflexão técnica sobre os trade-offs e gancho orgânico para o próximo post da série.
5. **Referências:** Footnotes `[^n]` listados na seção `## Referências`.

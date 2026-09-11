---
layout: post
title: "Contêineres na Prática: Docker, Compose e Podman"
subtitle: "Do Dockerfile ao docker compose up: construindo, orquestrando e protegendo contêineres para o mundo real"
author:
  - "Eduardo N. S. R."
date: 2026-10-02 14:00:00 GMT-3
permalink: /posts/conteineres-pratica/
tags: [Docker, Podman, Contêineres, Linux, DevOps, Infraestrutura]
series: Contêineres de Cabo a Rabo
published: false
---

Na primeira parte desta série, mergulhamos nas entranhas do kernel Linux. Vimos que contêineres não são máquinas virtuais mágicas: são processos comuns isolados visualmente por *namespaces*, restritos em consumo de hardware por *cgroups* v2 e alimentados por um sistema de arquivos em camadas montado pelo driver *OverlayFS*. Chegamos ao ponto de empacotar todas essas primitivas em um script em shell de cinquenta linhas capaz de rodar um ambiente Linux funcional a partir do zero.

Agora que desmistificamos a física quântica dos contêineres, é hora de voltar para a superfície e encarar a engenharia do dia a dia. No mundo corporativo real, ninguém cria diretórios cgroup na mão ou calcula offsets de montagem de disco para subir microsserviços. Nós utilizamos ferramentas de alto nível consolidadas pela indústria para automatizar esse ciclo: Docker, Docker Compose e Podman.

O objetivo deste segundo post é transformar aquela base conceitual profunda em maestria prática. Vamos entender como as instruções de um `Dockerfile` se traduzem fisicamente nas camadas de união que estudamos, como estruturar construções em múltiplos estágios para gerar imagens ultraleves, como os contêineres se comunicam através de pontes de rede virtuais e como declarar ambientes inteiros de desenvolvimento com múltiplos serviços interligados.

Também vamos explorar a arquitetura revolucionária sem daemons do Podman, aprender a blindar contêineres contra ameaças reais de segurança e entender exatamente quando a orquestração em uma única máquina bate no teto, preparando o terreno definitivo para a nossa jornada na série {% include post-ref.html slug="k8sbox-visao-geral" text="Kubernetes in a Box" %} e na Parte 14 da série {% include post-ref.html slug="spring-boot-tutorial-parte-1-ambiente" text="Spring Boot Tutorial" %}.

> [!NOTE] Nota da Série
> Este post fecha a série **"Contêineres de Cabo a Rabo"**. Se você caiu de paraquedas aqui, recomendo conferir o {% include post-ref.html slug="conteineres-historia" text="Post Zero: A História dos Contêineres" %} para entender a evolução do conceito e a {% include post-ref.html slug="conteineres-fundamentos" text="Parte 1: Fundamentos e Anatomia" %} para ver o que o kernel faz por baixo do capô. Compreender como o sistema operacional manipula chamadas de sistema, limites de recursos e montagens torna as decisões práticas que tomaremos aqui infinitamente mais claras e intuitivas.

## Estrutura do Post

Para guiar o seu estudo prático pelas ferramentas e padrões de produção, estruturei este post nos seguintes tópicos:

| Seção | Foco Principal |
| :--- | :--- |
| [Docker na Prática: A Anatomia de uma Imagem](#docker-na-prática-a-anatomia-de-uma-imagem) | Instruções do Dockerfile, camadas OCI, CMD vs ENTRYPOINT e builds multi-stage |
| [Ciclo de Vida e Operação de Contêineres](#ciclo-de-vida-e-operação-de-contêineres) | Estados de execução, sinais de encerramento, inspeção e estratégias de volumes |
| [Redes no Docker: Como Contêineres se Conversam](#redes-no-docker-como-contêineres-se-conversam) | Drivers bridge, host e macvlan, resolução por DNS e pontes veth no kernel |
| [Docker Compose: Orquestrando Stacks Locais](#docker-compose-orquestrando-stacks-locais) | Stacks declarativas completas, dependências com healthcheck e isolamento de rede |
| [Podman: A Revolução Sem Daemon e Sem Root](#podman-a-revolução-sem-daemon-e-sem-root) | Arquitetura fork/exec, contêineres rootless nativos e a criação de Pods locais |
| [Segurança de Contêineres: O Que Pode Dar Errado](#segurança-de-contêineres-o-que-pode-dar-errado) | Scanners de vulnerabilidades, vazamento de segredos, capabilities e o perigo do docker.sock |
| [Exercícios](#exercícios) | Desafios práticos com volumes, redes compostas e auditoria Trivy |
| [O Caminho para a Orquestração](#o-caminho-para-a-orquestração) | Os limites do Docker Compose e a transição natural para clusters Kubernetes |
| [Referências](#referências) | Documentações oficiais, guias de segurança e benchmarks da indústria |

## Docker na Prática: A Anatomia de uma Imagem

No coração do ecossistema Docker reside o arquivo de receita que todo desenvolvedor conhece: o `Dockerfile`. Mas quando você olha para aquele arquivo de texto simples, o que você enxerga? Apenas comandos executados em sequência ou a construção física de uma pilha de fatias de disco OverlayFS?

Como aprendemos na Parte 1, uma imagem de contêiner no padrão OCI nada mais é do que uma coleção de arquivos compactados em formato *tarball*, onde cada camada armazena apenas a diferença de arquivos em relação à camada imediatamente anterior. O `Dockerfile` é a especificação que dita como essas camadas devem ser produzidas pelo motor de compilação (*build engine*).

No entanto, existe uma distinção crucial que muitos profissionais ignoram: **nem toda instrução cria uma camada física de arquivos no disco**. Algumas instruções criam camadas reais (adicionando ou modificando arquivos), enquanto outras apenas alteram metadados gravados no arquivo de manifesto JSON da imagem.

A tabela a seguir detalha essa distinção para as instruções fundamentais:

| Instrução | O que faz no sistema | Cria Camada em Disco? | Tipo de Impacto |
| :--- | :--- | :--- | :--- |
| **FROM** | Define a imagem base de onde o processo parte | Sim | Importa a pilha de camadas da imagem de origem |
| **RUN** | Executa comandos de terminal durante a compilação | Sim | Grava todos os arquivos criados ou modificados |
| **COPY** | Copia arquivos do computador hospedeiro para a imagem | Sim | Grava os novos arquivos diretamente na camada |
| **ADD** | Copia arquivos, descompacta arquivos tar e baixa URLs | Sim | Grava o conteúdo descompactado ou baixado |
| **WORKDIR** | Define o diretório padrão de trabalho para os comandos | Não | Grava apenas metadado no manifesto JSON |
| **ENV** | Define variáveis de ambiente disponíveis na execução | Não | Grava apenas metadado no manifesto JSON |
| **EXPOSE** | Documenta as portas de rede que o processo pretende usar | Não | Metadado puramente informativo (não abre portas) |
| **USER** | Especifica com qual usuário ou UID o processo deve rodar | Não | Grava metadado de segurança no manifesto JSON |
| **CMD** | Define os parâmetros ou comando padrão de inicialização | Não | Grava metadado de execução no manifesto JSON |
| **ENTRYPOINT** | Define o executável fixo e permanente do contêiner | Não | Grava metadado de execução no manifesto JSON |

### O Eterno Dilema: CMD versus ENTRYPOINT

Se existe um ponto que gera confusão diária entre desenvolvedores, é a diferença entre as instruções `CMD` e `ENTRYPOINT` [^1].

Pense da seguinte forma: o **ENTRYPOINT** representa o **programa executável fixo** que o contêiner foi criado para rodar. O **CMD** representa os **argumentos padrão** que serão entregues a esse programa, caso quem disparou o contêiner não forneça nenhum argumento alternativo na linha de comando.

Quando você executa `docker run imagem argumento1 argumento2`, qualquer valor que você passar após o nome da imagem **substitui completamente o CMD**, mas é concatenado como parâmetro ao final do `ENTRYPOINT`.

A matriz de comportamento a seguir demonstra como essas combinações funcionam na prática:

| Configuração no Dockerfile | Executando `docker run app` | Executando `docker run app backup` |
| :--- | :--- | :--- |
| `CMD ["echo", "padrao"]` | Executa: `echo padrao` | Executa: `backup` (falha se backup não for executável) |
| `ENTRYPOINT ["myapp"]` | Executa: `myapp` (sem argumentos) | Executa: `myapp backup` |
| `ENTRYPOINT ["myapp"]` + `CMD ["--serve"]` | Executa: `myapp --serve` | Executa: `myapp backup` (substitui apenas o argumento padrão) |

Sempre utilize a sintaxe de vetor JSON (conhecida como *exec form*, entre colchetes e com aspas duplas, como `ENTRYPOINT ["java", "-jar", "app.jar"]`). Evite a sintaxe livre em string pura (*shell form*, como `ENTRYPOINT java -jar app.jar`), pois a forma livre força o Docker a disparar um subprocesso `/bin/sh -c`, fazendo com que o shell assuma o PID 1 e impedindo que a sua aplicação Java ou Node receba os sinais de desligamento do sistema operacional.

### O Papel Fundamental do Arquivo .dockerignore

Quando você executa `docker build -t minha-app .`, a primeira mensagem que pisca no terminal é:
`Sending build context to Docker daemon...`

O ponto final (`.`) diz ao cliente do Docker para empacotar todos os arquivos do diretório atual e enviá-los via socket para o daemon que fará a compilação. Se você não tiver um arquivo `.dockerignore` configurado, você enviará gigabytes desnecessários contendo histórico git, pastas de dependências locais como `node_modules` ou arquivos de compilação temporários.

Um arquivo `.dockerignore` eficiente deve fazer parte da raiz de todo projeto sério:

```
# .dockerignore: mantendo o contexto de compilação limpo
.git
.gitignore
.idea
.vscode
node_modules
target
build
*.log
.env
docker-compose*.yml
```
*O arquivo .dockerignore evita que credenciais, histórico de código e artefatos de compilação locais poluam o processo de build do Docker.*

### Compilação em Múltiplos Estágios: Multi-Stage Builds

No início da história do Docker, criar imagens enxutas exigia malabarismos complexos: você precisava de um script para compilar a aplicação no hospedeiro, gerar o binário e depois copiar apenas o artefato final para o contêiner. Se você colocasse o compilador dentro do Dockerfile, a imagem final acabava com mais de um gigabyte de tamanho contendo compiladores, bibliotecas de cabeçalho e ferramentas de teste que jamais deveriam estar presentes no ambiente de produção.

A introdução dos **Multi-stage Builds** [^2] resolveu esse problema de forma definitiva. Com múltiplos estágios declarados em um único arquivo, você pode utilizar uma imagem rica com todas as ferramentas de compilação no primeiro estágio, e em seguida copiar exclusivamente o binário compilado para uma imagem base ultraleve de produção.

Vejamos um exemplo prático aplicando esse padrão para uma aplicação Java com Spring Boot (que estudamos a fundo no ecossistema da nossa série Spring Boot):

```dockerfile
# ===== Estágio 1: Ambiente de Compilação (Build) =====
FROM eclipse-temurin:21-jdk-alpine AS builder

WORKDIR /workspace

# Otimização de cache: copiar primeiro apenas o manifesto de dependências
COPY pom.xml .
COPY .mvn .mvn
COPY mvnw .

# Baixar dependências em uma camada isolada
RUN ./mvnw dependency:go-offline -B

# Copiar o código-fonte da aplicação
COPY src src

# Compilar o pacote da aplicação ignorando testes de unidade para velocidade
RUN ./mvnw clean package -DskipTests -B

# ===== Estágio 2: Ambiente de Execução Enxuto (Runtime) =====
FROM eclipse-temurin:21-jre-alpine AS runner

# Criação de usuário sem privilégios para segurança operacional
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

# Copiar exclusivamente o arquivo JAR gerado no estágio anterior
COPY --from=builder /workspace/target/*.jar /app/aplicacao.jar

# Ajustar permissões para o usuário sem privilégios
RUN chown -R appuser:appgroup /app
USER appuser

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/app/aplicacao.jar"]
```
*O uso de multi-stage builds permite compilar a aplicação no primeiro estágio e transferir apenas o artefato final para a imagem de produção.*

O resultado dessa abordagem é dramático. No primeiro estágio (`builder`), temos um JDK completo pesando mais de 600 MB com o Maven e ferramentas de depuração. No segundo estágio (`runner`), utilizamos apenas a máquina virtual de execução (JRE) sobre Alpine Linux, entregando uma imagem final de aproximadamente 160 MB, sem código-fonte, sem compilador e sem dependências de desenvolvimento.

### Regras de Ouro para Dockerfiles de Alto Nível

Para garantir compilações rápidas e imagens seguras, memorize estas cinco diretrizes:

1. **Ordene as instruções por frequência de alteração**: O Docker invalida o cache de camadas a partir da primeira instrução cujos arquivos foram modificados. Copie manifestos de dependências (`pom.xml`, `package.json`, `go.mod`) e baixe os pacotes antes de copiar o código-fonte (`COPY src/ src/`).
2. **Combine comandos de atualização e instalação no mesmo RUN**: Em distribuições baseadas em Debian, nunca execute `RUN apt-get update` em uma linha e `RUN apt-get install` na seguinte. Se a primeira camada ficar presa no cache, a instalação futura receberá pacotes desatualizados. Use sempre `RUN apt-get update && apt-get install -y --no-install-recommends pacote && rm -rf /var/lib/apt/lists/*`.
3. **Prefira imagens base mínimas**: Utilize variantes baseadas em Alpine Linux ou projetos como o Google Distroless para minimizar a quantidade de binários instalados e a superfície de vulnerabilidades.
4. **Nunca execute como root**: Adicione um usuário comum de sistema com a diretiva `USER` antes de declarar o `ENTRYPOINT`.
5. **Use tags de versão explícitas**: Jamais utilize a tag `:latest` em arquivos de produção. Fixe versões imutáveis para evitar que atualizações inesperadas quebrem a sua esteira de entrega contínua.

## Ciclo de Vida e Operação de Contêineres

Subir um contêiner é fácil. O desafio real começa quando você precisa manter dezenas deles rodando de forma confiável, respondendo a falhas e sendo atualizados sem indisponibilidade. Para isso, precisamos dominar a máquina de estados que governa a vida de um contêiner no Docker.

```
                   docker create
                         │
                         ▼
                   ┌───────────┐
                   │  CREATED  │
                   └─────┬─────┘
                         │ docker start
                         ▼
┌───────────┐      ┌───────────┐      ┌───────────┐
│  PAUSED   │<────>│  RUNNING  │─────>│  STOPPED  │
│           │pause/│           │stop/ │ (EXITED)  │
│           │unp.  │           │kill  │           │
└───────────┘      └───────────┘      └─────┬─────┘
                                            │ docker rm
                                            ▼
                                      ┌───────────┐
                                      │  REMOVED  │
                                      └───────────┘
```

A transição entre esses estados é coordenada por comandos específicos da interface de linha de comando. Vamos examinar a anatomia dos comandos indispensáveis para a operação em produção.

### As Flags Indispensáveis do docker run

O comando `docker run` é a porta de entrada para a criação de instâncias. Em ambientes de produção e homologação, ele nunca deve ser executado sem parâmetros explícitos de governança:

```bash
$ docker run -d \
    --name api-tarefas \
    -p 8080:8080 \
    -v dados-app:/var/dados \
    -e SPRING_PROFILES_ACTIVE=prod \
    --restart unless-stopped \
    --memory=512m \
    --cpus=1.5 \
    minha-api:1.0.0
```
*Cada parâmetro traduz diretamente uma configuração de governança do kernel Linux:*
- `-d`: Executa o contêiner em segundo plano (*detached mode*), liberando o terminal.
- `--name api-tarefas`: Atribui um identificador legível para o contêiner, facilitando a automação e o gerenciamento.
- `-p 8080:8080`: Mapeia a porta 8080 do hospedeiro para a porta 8080 interna do contêiner criando regras de redirecionamento de rede.
- `-v dados-app:/var/dados`: Conecta um volume persistente do Docker na pasta indicada, garantindo sobrevivência de dados.
- `-e SPRING_PROFILES_ACTIVE=prod`: Injeta variáveis de ambiente no processo do contêiner.
- `--restart unless-stopped`: Política de reinicialização que sobe o contêiner automaticamente em caso de falha ou após o reinício do servidor hospedeiro.
- `--memory=512m` e `--cpus=1.5`: Aplica limites rígidos de cgroups para memória RAM e fatias de processador.

> [!TIP] Comandos de Diagnóstico em Produção
> Além do `docker run`, três comandos formam o kit de primeiros socorros para diagnosticar contêineres em operação: `docker exec -it <nome> sh` abre um terminal interativo dentro do contêiner (internamente é um `nsenter` nos namespaces do processo, como vimos na Parte 1); `docker logs -f --tail 50 <nome>` exibe em tempo real a saída padrão e de erros do processo com PID 1; e `docker inspect <nome>` retorna um raio-X completo em JSON contendo IP de rede, caminhos do OverlayFS, variáveis de ambiente e status de execução.

### A Diferença Crítica entre docker stop e docker kill

Quando você precisa desligar uma aplicação, a forma como o encerramento é solicitado faz toda a diferença entre uma desconexão graciosa e um banco de dados corrompido:

- **`docker stop` (Desligamento Gracioso)**: O Docker envia primeiramente o sinal padrão do sistema operacional `SIGTERM` (Signal Terminate, código 15) diretamente para o processo com PID 1. Esse sinal comunica educadamente à aplicação: *"Por favor, encerre suas atividades"*. Uma aplicação bem construída intercepta o `SIGTERM`, para de receber novas requisições HTTP, aguarda a finalização das transações de banco de dados que já estão em andamento e fecha as conexões de rede de forma segura. O Docker aguarda por padrão um período de tolerância (*grace period*) de 10 segundos. Se o processo não se encerrar voluntariamente dentro desse tempo limite, o Docker envia o sinal forçado `SIGKILL`.
- **`docker kill` (Abate Imediato)**: O Docker envia imediatamente o sinal `SIGKILL` (Signal Kill, código 9) para o processo. No Linux, o sinal `SIGKILL` não pode ser interceptado, tratado ou bloqueado por nenhum processo em espaço de usuário. O kernel simplesmente suspende a execução da tarefa no mesmo nanossegundo e libera as páginas de memória. Transações incompletas são interrompidas pela metade e conexões remotas ficam órfãs.

Em esteiras de entrega contínua e procedimentos de manutenção, sempre utilize `docker stop` para garantir que o *grace period* permita à aplicação desocupar recursos com integridade.

### Estratégias de Armazenamento: Volumes versus Bind Mounts versus tmpfs

Como vimos na Parte 1, a camada de escrita do sistema OverlayFS é efêmera: quando o contêiner é destruído com `docker rm`, todos os arquivos gravados nela desaparecem para sempre. Para persistir informações de forma confiável ou injetar arquivos do computador hospedeiro, o Docker disponibiliza três estratégias distintas de armazenamento:

| Mecanismo | Sintaxe de Uso | Gerenciado pelo Docker? | Caso de Uso Recomendado |
| :--- | :--- | :--- | :--- |
| **Volumes Nomeados** | `-v meu-volume:/caminho` | Sim (em `/var/lib/docker/volumes/`) | Bancos de dados, uploads persistentes e arquivos de produção |
| **Bind Mounts** | `-v /caminho/host:/caminho` | Não (aponta para pasta arbitrária) | Código-fonte em desenvolvimento e arquivos de configuração do host |
| **tmpfs Mounts** | `--tmpfs /caminho` | N/A (vive estritamente na RAM) | Dados sensíveis, segredos efêmeros e caches temporários voláteis |

## Redes no Docker: Como Contêineres se Conversam

Na Parte 1, vimos que quando um novo namespace de rede é criado, ele nasce completamente isolado do mundo, possuindo apenas a interface local de *loopback*. Como o Docker conecta essas ilhas isoladas entre si e com a internet?

O Docker possui um subsistema extensível de drivers de rede que resolvem diferentes cenários de conectividade:

| Driver de Rede | Mecanismo de Funcionamento | Quando Deve Ser Utilizado |
| :--- | :--- | :--- |
| **bridge** (Padrão) | Cria uma ponte virtual de rede gerenciada por software com sub-rede e NAT | A esmagadora maioria das aplicações isoladas no mesmo host |
| **host** | Remove o isolamento de rede; o processo divide as portas diretamente com o host | Aplicações que exigem altíssimo tráfego de rede e baixíssima latência |
| **none** | Desliga completamente a pilha de rede, mantendo apenas a interface de loopback | Tarefas isoladas de cálculo matemático pesado e cargas de segurança |
| **overlay** | Cria uma rede virtual sobreposta interligando múltiplos servidores físicos | Orquestração de contêineres em cluster (como Docker Swarm) |
| **macvlan** | Atribui um endereço MAC real ao contêiner, fazendo-o parecer um computador na LAN | Aplicações legadas que precisam se comunicar diretamente na rede física |

### A Diferença Vital da Rede Bridge Customizada

Quando você instala o Docker, ele cria automaticamente uma interface de rede ponte chamada `docker0`. Se você rodar contêineres sem especificar uma rede, eles serão conectados nessa ponte padrão.

No entanto, em ambientes profissionais, **nunca utilize a rede bridge padrão para conectar aplicações interdependentes**.

Na rede bridge padrão, os contêineres só conseguem se comunicar conhecendo os endereços IP uns dos outros. Como os endereços IP de contêineres são dinâmicos e mudam a cada reinício, isso exigiria gambiarras com arquivos de configuração.

Quando você cria uma **rede bridge customizada** com o comando `docker network create`, o Docker ativa um servidor DNS interno automático. Os contêineres anexados a essa rede conseguem se comunicar simplesmente utilizando o nome do próprio contêiner como nome de domínio de rede:

```bash
# Criar uma rede bridge customizada dedicada
$ docker network create rede-aplicacao

# Subir um contêiner de banco de dados anexado a essa rede
$ docker run -d --name meu-postgres --network rede-aplicacao -e POSTGRES_PASSWORD=teste postgres:17-alpine

# Subir uma aplicação de teste na mesma rede e pingar o banco pelo NOME
$ docker run --rm --network rede-aplicacao alpine ping -c 3 meu-postgres
PING meu-postgres (172.19.0.2): 56 data bytes
64 bytes from 172.19.0.2: seq=0 ttl=64 time=0.082 ms
64 bytes from 172.19.0.2: seq=1 ttl=64 time=0.075 ms
64 bytes from 172.19.0.2: seq=2 ttl=64 time=0.078 ms
```
*O servidor DNS embutido do Docker resolveu o nome meu-postgres instantaneamente para o endereço IP interno 172.19.0.2.*

### O Que Acontece por Baixo dos Panos: veth pairs e iptables

Se conectarmos essa operação com a teoria que vimos na Parte 1, o que o Docker fez no kernel do hospedeiro para viabilizar essa comunicação?

1. Criou uma ponte virtual de rede Linux (visível com o comando `ip link show type bridge`).
2. Criou um par de interfaces virtuais conectadas (*veth pair*). Imagine um cabo de rede virtual: a interface `vethXXXX` fica conectada à ponte no computador hospedeiro, enquanto a outra ponta é movida para dentro do namespace NET do contêiner e renomeada para `eth0`.
3. Injetou regras na tabela NAT do utilitário `iptables` do hospedeiro para realizar mascaramento (*IP Masquerading*). Quando o contêiner envia pacotes para a internet, o kernel altera o IP de origem para o IP físico do hospedeiro, permitindo que a resposta retorne com sucesso.

## Docker Compose: Orquestrando Stacks Locais

À medida que os projetos crescem, uma aplicação moderna raramente roda sozinha: ela precisa de um banco de dados relacional, uma camada de cache em memória, um corretor de mensagens e painéis de administração.

Subir tudo isso na linha de comando com dezenas de instruções `docker run`, calculando portas, redes e variáveis de ambiente na cabeça é uma receita certa para o caos.

Para resolver essa orquestração local de múltiplos contêineres de forma declarativa e versionável, a ferramenta padrão da indústria é o **Docker Compose** [^3].

Com o Compose, você descreve toda a sua infraestrutura de desenvolvimento em um arquivo legível e estruturado chamado `compose.yaml` (anteriormente conhecido como `docker-compose.yml`).

### Uma Stack de Produção Declarativa

Abaixo temos um exemplo completo de manifesto representando uma arquitetura clássica: uma API construída sob medida com Spring Boot, um banco de dados relacional PostgreSQL com verificação contínua de integridade (*healthcheck*), uma instância de cache Redis e uma ferramenta de administração visual (Adminer) ativada apenas sob demanda através de perfis (*profiles*).

```yaml
# compose.yaml: Especificação declarativa de serviços
# Nota: o campo legado 'version' não é mais necessário nas versões modernas do Compose

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: backend-api
    ports:
      - "8080:8080"
    environment:
      DB_HOST: db
      DB_PORT: 5432
      DB_NAME: tarefas_db
      DB_USER: tarefas_user
      DB_PASSWORD: ${DB_PASSWORD}
      REDIS_HOST: cache
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    networks:
      - rede-backend
    restart: unless-stopped

  db:
    image: postgres:17-alpine
    container_name: postgres-dados
    environment:
      POSTGRES_DB: tarefas_db
      POSTGRES_USER: tarefas_user
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - dados-banco:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tarefas_user -d tarefas_db"]
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 10s
    networks:
      - rede-backend
    restart: unless-stopped

  cache:
    image: redis:7-alpine
    container_name: redis-cache
    command: redis-server --maxmemory 128mb --maxmemory-policy allkeys-lru
    networks:
      - rede-backend
    restart: unless-stopped

  adminer:
    image: adminer:latest
    container_name: painel-adminer
    ports:
      - "8090:8080"
    networks:
      - rede-backend
    profiles:
      - debug

volumes:
  dados-banco:

networks:
  rede-backend:
    driver: bridge
```
*Manifesto Compose integrando verificação de saúde entre serviços, volumes persistentes e perfis sob demanda.*

Para manter dados sensíveis fora do controle de versão, as senhas e credenciais devem residir em um arquivo paralelo `.env` mantido fora do Git:

```bash
# .env: Configurações sensíveis para o ambiente local
DB_PASSWORD=senha_altamente_segura_de_desenvolvimento_123
```

### Decisões Cruciais de Arquitetura no Compose

Preste atenção em três detalhes desse manifesto que separam o amador do profissional de infraestrutura:

1. **A condição `service_healthy` no `depends_on`**: A instrução clássica `depends_on` do Docker apenas aguarda o processo filho subir na tabela de processos. No caso de bancos de dados, o processo do PostgreSQL sobe quase instantaneamente, mas ele leva vários segundos lendo arquivos e inicializando antes de começar a aceitar conexões TCP. Sem o bloco `condition: service_healthy`, a aplicação web tenta conectar imediatamente no banco, toma um erro de conexão recusada e quebra logo na inicialização. Com a verificação de saúde configurada via `pg_isready`, o Compose segura a inicialização da aplicação até que o banco declare estar pronto para trabalhar.
2. **Perfis com a diretiva `profiles`**: O serviço do Adminer foi marcado com o perfil `debug`. Isso significa que, ao rodar `docker compose up -d`, o Adminer não será iniciado por padrão, economizando memória e portas do seu computador. Ele só subirá se você declarar explicitamente a flag `--profile debug`.
3. **Limitação de memória no Redis**: Passamos argumentos de linha de comando limitando a memória do Redis a 128 MB e definindo a política de desalocação LRU (*Least Recently Used*), evitando que o cache devore toda a memória do hospedeiro.

### Comandos de Operação do Docker Compose

No seu fluxo de trabalho diário, memorize estes comandos de controle:

```bash
# Subir toda a stack em segundo plano
$ docker compose up -d

# Recompilar a imagem da aplicação e subir as alterações
$ docker compose up -d --build

# Subir a stack incluindo o serviço de depuração (Adminer)
$ docker compose --profile debug up -d

# Visualizar o status de saúde e portas de todos os contêineres da stack
$ docker compose ps

# Acompanhar os logs contínuos de um serviço específico
$ docker compose logs -f app

# Executar uma sessão de terminal dentro do banco de dados da stack
$ docker compose exec db psql -U tarefas_user -d tarefas_db

# Parar a execução da stack mantendo os dados gravados nos volumes
$ docker compose down

# Parar e DESTRUIR todos os contêineres e volumes da stack (CUIDADO: apaga dados)
$ docker compose down -v
```
*O comando docker compose unifica a governança de toda a arquitetura em operações atômicas.*

## Podman: A Revolução Sem Daemon e Sem Root

O Docker revolucionou a tecnologia de contêineres, mas à medida que o ecossistema avançou, arquitetos de infraestrutura e especialistas em segurança começaram a apontar duas grandes fragilidades em seu desenho original:

1. **O Daemon Centralizado como Ponto Único de Falha**: O Docker depende de um serviço contínuo rodando em segundo plano (`dockerd`). Se esse serviço travar ou for encerrado, a comunicação com todos os contêineres é interrompida. Além disso, se o processo do daemon morrer, todos os contêineres monitorados por ele podem ficar órfãos ou instáveis.
2. **A Dependência de Privilégios de Root**: Historicamente, o `dockerd` roda como o usuário `root` do sistema operacional. Conceder a um desenvolvedor acesso ao socket do Docker equivale tecnicamente a conceder permissões de superusuário irrestritas no computador hospedeiro.

Para solucionar essas dores com base nos padrões abertos da OCI, a Red Hat liderou o desenvolvimento de uma ferramenta moderna chamada **Podman** (*Pod Manager*) [^4].

```
        ARQUITETURA DOCKER                           ARQUITETURA PODMAN

┌──────────────────────────────┐              ┌──────────────────────────────┐
│          docker CLI          │              │          podman CLI          │
└──────────────┬───────────────┘              └──────────────┬───────────────┘
               │ API REST                                    │ Chamada direta
               │ (/var/run/docker.sock)                      │ (fork / execve)
               ▼                                             ▼
┌──────────────────────────────┐              ┌──────────────────────────────┐
│           dockerd            │              │            conmon            │
│       (Daemon em ROOT!)      │              │   (Monitor leve por contêiner)│
└──────────────┬───────────────┘              └──────────────┬───────────────┘
               │ gRPC                                        │ Execução OCI
               ▼                                             ▼
┌──────────────────────────────┐              ┌──────────────────────────────┐
│          containerd          │              │         crun / runc          │
└──────────────┬───────────────┘              └──────────────┬───────────────┘
               │                                             │
               ▼                                             ▼
┌──────────────────────────────┐              ┌──────────────────────────────┐
│             runc             │              │      Processo da Aplicação   │
└──────────────────────────────┘              │   (Rodando sem root no host!)│
                                              └──────────────────────────────┘
```

A comparação visual ilustra a mudança de paradigma:
- O Podman **não possui nenhum daemon central**. Ele segue a tradicional filosofia Unix: quando você digita `podman run`, o cliente simplesmente faz uma bifurcação direta de processos (*fork/exec*) através de um monitor levíssimo em C chamado `conmon`.
- O Podman é **100% rootless por padrão**. Você pode executar contêineres a partir da sua conta de usuário comum, sem usar `sudo`, sem pedir permissão ao administrador do sistema e sem abrir portas privilegiadas no sistema operacional.

### Como o Podman Mapeia Usuários com User Namespaces

Lembre-se do Exercício 1 da Parte 1, onde usamos *User Namespaces*. O Podman utiliza esse mesmo recurso do kernel Linux de forma automatizada:

```bash
# Executar um contêiner com Podman sem usar sudo
$ podman run --rm alpine whoami
root

# Consultar o mapeamento real de usuários efetuado pelo Podman no kernel
$ podman unshare cat /proc/self/uid_map
         0       1000          1
         1     100000      65536
```
*A saída demonstra o isolamento: o UID 0 dentro do contêiner corresponde estritamente ao UID 1000 (seu usuário normal) no computador hospedeiro.*

Se um processo dentro de um contêiner Podman tentar explorar uma falha para invadir o computador hospedeiro, para o kernel ele terá exatamente os mesmos privilégios do seu usuário comum. Ele não consegue alterar arquivos de sistema em `/etc`, não consegue mexer em módulos do kernel e não consegue comprometer os outros usuários da máquina.

### O Conceito de Pods Nativos do Podman

Outro diferencial extraordinário do Podman é o suporte nativo ao conceito de **Pods**.

O Pod é a menor unidade de execução do Kubernetes: ele representa um grupo de um ou mais contêineres que compartilham rigorosamente os mesmos namespaces de rede, IPC e armazenamento.

No Docker tradicional, contêineres são sempre unidades individuais isoladas. No Podman, você pode criar Pods locais idênticos aos do Kubernetes:

```bash
# 1. Criar um Pod expondo a porta 8080 para o hospedeiro
$ podman pod create --name pod-web -p 8080:80

# 2. Adicionar uma aplicação web Nginx dentro do Pod
$ podman run -d --pod pod-web --name servidor-web nginx:alpine

# 3. Adicionar um contêiner auxiliar (sidecar) dentro do MESMO Pod
$ podman run -d --pod pod-web --name monitor-sidecar alpine sleep 3600

# 4. Do contêiner auxiliar, acessar o Nginx via localhost!
$ podman exec monitor-sidecar wget -qO- http://localhost:80 | head -n 4
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
```
*Como os dois contêineres compartilham o mesmo namespace de rede do Pod, eles se comunicam através da interface local de loopback como se fossem processos na mesma máquina.*

E a integração com o Kubernetes vai além: o Podman consegue transformar esse ambiente local em manifestos oficiais do Kubernetes com um único comando:

```bash
# Gerar a especificação YAML do Kubernetes correspondente ao Pod criado
$ podman generate kube pod-web > pod-web.yaml

# Visualizar o arquivo pronto para ser implantado em um cluster de produção
$ head -n 20 pod-web.yaml
```

> [!TIP] Executando Pods no Debian e Ubuntu
> Em distribuições baseadas em Debian ou Ubuntu, certifique-se de instalar o pacote `catatonit` (`sudo apt install catatonit`), que fornece o binário de *pause* exigido pelo Podman para orquestrar o ciclo de vida dos Pods. Além disso, para permitir o download com nomes curtos de imagens (como `nginx:alpine` sem precisar digitar o caminho completo `docker.io/library/nginx:alpine`), configure `unqualified-search-registries = ["docker.io"]` no arquivo `/etc/containers/registries.conf`.

| Característica de Design | Docker | Podman |
| :--- | :--- | :--- |
| **Arquitetura de Execução** | Baseada em daemon centralizado (`dockerd`) | Sem daemon (*fork/exec* direto via `conmon`) |
| **Execução Sem Root** | Suportada como modo alternativo configurável | Padrão e nativa desde o primeiro dia de design |
| **Compatibilidade de Comandos** | Referência original da indústria | Quase 100% compatível (`alias docker=podman`) |
| **Conceito Nativo de Pods** | Inexistente (apenas contêineres isolados) | Nativo e compatível com modelos do Kubernetes |
| **Exportação para Kubernetes** | Requer ferramentas de terceiros | Integrado via `podman generate kube` |
| **Integração com systemd** | Gerenciado via serviço de sistema do daemon | Gera arquivos de serviço individuais por contêiner |
| **Runtime OCI Padrão** | `runc` (escrito em Go) | `crun` (escrito em C, mais rápido e leve) |

## Segurança de Contêineres: O Que Pode Dar Errado

A facilidade com que contêineres são baixados e executados cria uma falsa sensação de segurança. Muitos times assumem que, por estarem rodando uma aplicação em um contêiner, ela está automaticamente protegida contra ameaças externas.

Essa presunção é perigosa. Como aprendemos na Parte 1, o contêiner compartilha o mesmo kernel do computador hospedeiro. Se uma aplicação for comprometida e o contêiner estiver mal configurado, a distância entre um ataque isolado e o sequestro total da máquina física é de apenas alguns comandos.

Vamos dissecar as quatro maiores armadilhas de segurança no mundo dos contêineres e como neutralizá-las.

### O Perigo Fatal: Montar o Socket do Docker (/var/run/docker.sock)

Em tutoriais de esteiras de CI/CD ou ferramentas visuais de administração, você frequentemente encontra instruções recomendando o seguinte comando:
`docker run -v /var/run/docker.sock:/var/run/docker.sock ...`

**Nunca faça isso a menos que você compreenda exatamente o risco catastrófico envolvido.**

O arquivo `/var/run/docker.sock` é a porta de comunicação do daemon do Docker. Quem tem permissão de leitura e escrita nesse arquivo consegue enviar qualquer comando para a API do Docker. E como o daemon do Docker tradicional roda como `root`, quem controla o socket controla o sistema hospedeiro inteiro.

Veja como é trivial escapar de um contêiner que possui o socket montado:

```bash
# Simulação de invasão: o invasor está dentro de um contêiner com o socket montado
# Ele usa o cliente do Docker para criar um contêiner privilegiado com o disco host montado
$ docker run --rm -v /:/host-raiz alpine chroot /host-raiz whoami
root
```
*Montar o socket do Docker permite ao processo interno subir contêineres paralelos com acesso total ao sistema de arquivos do computador hospedeiro.*

Se você precisa construir contêineres dentro de esteiras de integração contínua (o famoso padrão *Docker-in-Docker*), utilize alternativas projetadas especificamente para ambientes seguros que não exigem privilégios de root, como o **Kaniko** [^5] da Google ou o **Buildah** da Red Hat.

### Limpeza de Vulnerabilidades em Imagens com Trivy

Outro erro recorrente é utilizar imagens base populares sem auditar os pacotes instalados nelas. Uma imagem genérica como `node:20` ou `python:3.12` baseada em distribuições completas traz centenas de utilitários de sistema operacional que a sua aplicação nunca usará, carregando consigo dezenas de vulnerabilidades conhecidas (*CVEs*).

Para auditar e identificar falhas de segurança antes do envio para produção, a ferramenta padrão recomendada é o **Trivy** [^6]:

```bash
# Varrer uma imagem comum do ecossistema Node.js
$ trivy image --severity HIGH,CRITICAL node:22

# A saída exibirá dezenas de falhas graves em pacotes do sistema operacional
```

Ao trocar a base para uma imagem mínima baseada em Alpine Linux (`node:22-alpine`) ou em uma imagem *Distroless*, a quantidade de componentes de sistema cai vertiginosamente, eliminando até 90% das vulnerabilidades reportadas.

### O Antipadrão Fatal: Segredos Gravados no Dockerfile

Um dos erros de segurança mais silenciosos e devastadores no ecossistema Docker é embutir senhas, tokens de API ou chaves criptográficas diretamente dentro das instruções do Dockerfile. Uma linha aparentemente inofensiva como `ENV DB_PASSWORD=segredo123` grava aquela credencial permanentemente nos metadados da imagem. Qualquer pessoa com acesso à imagem pode extraí-la trivialmente com o comando `docker history`:

```bash
# Visualizar o histórico completo de instruções da imagem
$ docker history minha-app:1.0.0 --no-trunc
IMAGE         CREATED BY                                      SIZE
...           ENV DB_PASSWORD=segredo123                       0B
...           RUN echo "$DB_PASSWORD" > /app/config.txt        15B
```
*Qualquer instrução ENV ou ARG fica registrada para sempre no histórico de camadas da imagem.*

O mesmo vale para a instrução `ARG`: embora variáveis de compilação declaradas com `ARG` não persistam como variáveis de ambiente no contêiner final, seus valores ficam gravados no manifesto da imagem e expostos pelo `docker history`.

Para lidar com credenciais de forma segura, aplique uma dessas estratégias:

1. **Variáveis de ambiente em tempo de execução**: Injete segredos apenas no momento de rodar o contêiner com a flag `-e` ou via arquivo `.env` no Docker Compose. Esses valores vivem na memória do processo e não ficam gravados na imagem.
2. **Build secrets do BuildKit**: O Docker BuildKit oferece a diretiva `--mount=type=secret` dentro de instruções `RUN`, que disponibiliza o segredo durante a compilação sem gravá-lo em nenhuma camada da imagem:
   ```dockerfile
   RUN --mount=type=secret,id=db_pass \
       cat /run/secrets/db_pass > /tmp/setup && ./configure.sh && rm /tmp/setup
   ```
3. **Ferramentas de gerenciamento de segredos**: Em ambientes de produção orquestrados, utilize mecanismos dedicados como o Docker Secrets (Swarm), Kubernetes Secrets ou cofres externos como HashiCorp Vault e AWS Secrets Manager.

### O Princípio do Menor Privilégio com Linux Capabilities

No Linux tradicional, o modelo de permissões era binário: ou você era um usuário comum sem poder algum, ou você era o superusuário `root` com poderes absolutos para alterar qualquer aspecto do sistema.

Para quebrar esse monopólio perigoso, o kernel introduziu as **Capabilities** [^7]. As *capabilities* dividem os superpoderes do `root` em pequenos blocos independentes (como permissão para escutar em portas baixas, alterar relógios do sistema ou carregar módulos de kernel).

Por padrão, o Docker já descarta cerca de vinte *capabilities* perigosas ao criar um contêiner. Mas uma aplicação em contêiner ainda mantém permissões que ela raramente precisa.

A postura de segurança recomendada em produção é a técnica do **Drop All**: remova todas as permissões concedidas e adicione de volta exclusivamente as que forem estritamente necessárias para o funcionamento do serviço:

```bash
# Executar contêiner web removendo TODOS os privilégios e adicionando apenas a capacidade de abrir portas
$ docker run -d \
    --name web-seguro \
    --cap-drop=ALL \
    --cap-add=NET_BIND_SERVICE \
    --read-only \
    --tmpfs /tmp \
    --security-opt=no-new-privileges \
    -p 80:80 \
    nginx:alpine
```
*A combinação de cap-drop total com sistema de arquivos somente leitura impede que invasores baixem ou executem binários maliciosos no contêiner.*

Repare nas camadas combinadas:
- `--cap-drop=ALL`: Remove todos os superpoderes do processo.
- `--cap-add=NET_BIND_SERVICE`: Devolve apenas a autorização necessária para escutar em portas abaixo de 1024.
- `--read-only`: Torna o sistema de arquivos do contêiner totalmente imutável; nada pode ser gravado ou alterado em disco.
- `--tmpfs /tmp`: Disponibiliza uma pasta temporária montada na memória RAM para a aplicação gravar arquivos transitórios.
- `--security-opt=no-new-privileges`: Bloqueia tentativas de processos filhos de adquirir privilégios extras através de binários com a flag *setuid*.

#### Levando o Hardening para o Docker Compose com Âncoras YAML

Na rotina real de engenharia, quase ninguém sobe contêineres digitando comandos de terminal com vinte parâmetros manuais. A governança em produção vive em manifestos declarativos versionados no repositório. Além disso, como defendemos no artigo sobre o {% include post-ref.html slug="12-factor-app-pesadelos-e-pratica" text="12-Factor App na Prática" %}, a paridade entre ambientes exige que a postura de segurança usada em produção seja reproduzida desde os testes locais na máquina do desenvolvedor.

Todas as restrições de kernel que dissecamos na linha de comando possuem suporte nativo de primeira classe dentro da especificação do Docker Compose:

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "80:80"
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
    tmpfs:
      - /tmp:rw,noexec,nosuid,size=64M
```
*A declaração no Compose traduz exatamente as mesmas restrições de kernel da linha de comando.*

O grande obstáculo prático é a proliferação de código: em uma stack corporativa com múltiplos serviços interligados, copiar e colar esse mesmo bloco de segurança repetidamente gera um manifesto inflado e difícil de manter.

Para resolver isso de forma elegante, a especificação do Compose [^11] suporta **campos de extensão e âncoras YAML** (`&` e `*`).

Com esse recurso, você define o perfil base de menor privilégio (*hardening baseline*) uma única vez no topo do arquivo e o reutiliza em múltiplos serviços utilizando o operador de mesclagem (`<<`):

```yaml
# Perfil base de segurança reutilizável (Hardening Baseline)
x-security-defaults: &security-defaults
  security_opt:
    - no-new-privileges:true
  cap_drop:
    - ALL
  read_only: true
  tmpfs:
    - /tmp:rw,noexec,nosuid,size=100M
  restart: unless-stopped

services:
  api:
    image: minha-api:1.0.0
    <<: *security-defaults
    ports:
      - "8080:8080"
    # A API herda o baseline: roda sem capabilities extras e com disco imutável

  proxy:
    image: nginx:alpine
    <<: *security-defaults
    ports:
      - "80:80"
    # Herda o baseline e adiciona exclusivamente a permissão de abrir portas baixas
    cap_add:
      - NET_BIND_SERVICE
```
*Com âncoras YAML, você padroniza o endurecimento de segurança de toda a stack sem redundância de código.*

Essa abordagem declarativa não apenas organiza o seu ambiente local, mas cria a ponte mental direta para o que veremos na série {% include post-ref.html slug="k8sbox-visao-geral" text="Kubernetes in a Box" %}: no Kubernetes, esse exato padrão de menor privilégio é traduzido nos blocos de `securityContext` de cada Pod.

## Exercícios

Para fixar a dinâmica de ferramentas, volumes, orquestração local com Compose e análise de segurança, execute os desafios abaixo no terminal.

**1. Persistência de dados com volumes em bancos relacionais**

Crie um contêiner executando o banco PostgreSQL utilizando um volume nomeado para persistir seus arquivos de dados:

```bash
$ docker run -d --name pg-banco \
    -e POSTGRES_PASSWORD=segredo123 \
    -v dados-postgres:/var/lib/postgresql/data \
    postgres:17-alpine
```

Aguarde alguns segundos para a inicialização e acesse o banco de dados criando uma tabela e gravando um registro:

```bash
$ docker exec -i pg-banco psql -U postgres -c "CREATE TABLE clientes (id serial PRIMARY KEY, nome varchar(50)); INSERT INTO clientes (nome) VALUES ('Empresa Exemplo');"
```

Em seguida, destrua sumariamente o contêiner em execução com `docker rm -f pg-banco`. Por fim, suba um contêiner novo, com outro nome (`pg-novo`), conectando o mesmo volume `dados-postgres`, e consulte os registros da tabela `clientes`. O que aconteceu com a informação e por que os dados sobrevivem?

<details markdown="1">
<summary>Ver resposta</summary>

Ao executar o comando de consulta no novo contêiner:

```bash
$ docker exec -i pg-novo psql -U postgres -c "SELECT * FROM clientes;"
```

A tabela retornará intacta com o registro `'Empresa Exemplo'` cadastrado.

Isso ocorre porque o volume nomeado `dados-postgres` não faz parte da camada OverlayFS do contêiner. Ele é um diretório gerenciado pelo Docker localizado no sistema de arquivos do computador hospedeiro (geralmente sob `/var/lib/docker/volumes/dados-postgres/_data`). Quando o primeiro contêiner foi destruído com o parâmetro forçado `-f`, o volume continuou existindo no disco. Ao subir o segundo contêiner apontando para o mesmo volume, o novo processo do PostgreSQL simplesmente assumiu a base preexistente sem perda de dados.

*Para limpar o volume de testes após o exercício, execute `docker rm -f pg-novo && docker volume rm dados-postgres`.*

</details>

**2. Segregação de redes e proxy reverso no Compose**

Como você alteraria o arquivo `compose.yaml` apresentado nesta seção para adicionar um servidor Nginx atuando como *Reverse Proxy* na frente da aplicação, isolando as redes de forma que:

1. O Nginx escute na porta 80 do computador hospedeiro e repasse o tráfego para `http://app:8080`.
2. A aplicação participe de duas redes: `rede-publica` (onde fala com o Nginx) e `rede-privada` (onde fala com o banco e o Redis).
3. O Nginx NÃO consiga em hipótese alguma estabelecer conexões diretas com o banco de dados PostgreSQL.

<details markdown="1">
<summary>Ver resposta</summary>

Para implementar esse isolamento de segurança em camadas (*Defense in Depth*), declare duas redes no arquivo Compose:

```yaml
networks:
  rede-publica:
  rede-privada:
```

Em seguida, configure as participações de rede de cada serviço:
- O serviço `nginx` é mapeado exclusivamente na `rede-publica`.
- O serviço `app` é mapeado em ambas as redes (`rede-publica` e `rede-privada`).
- Os serviços `db` e `cache` são mapeados exclusivamente na `rede-privada`.

Com essa arquitetura de rede, mesmo que um invasor consiga comprometer o servidor web Nginx, ele estará preso em um namespace de rede que não possui rotas nem visibilidade física para alcançar a porta 5432 do banco de dados.

</details>

**3. Comparação de superfície de ataque com Trivy**

Instale ou execute o utilitário Trivy via contêiner para comparar a quantidade de vulnerabilidades de segurança entre duas imagens oficiais da mesma tecnologia:

```bash
$ docker run --rm aquasec/trivy:latest image --severity CRITICAL python:3.12
$ docker run --rm aquasec/trivy:latest image --severity CRITICAL python:3.12-alpine
```

Compare os resultados obtidos. Quantas vulnerabilidades críticas foram encontradas em cada imagem e o que justifica essa diferença?

<details markdown="1">
<summary>Ver resposta</summary>

Na imagem `python:3.12` padrão (baseada em Debian GNU/Linux), o relatório do Trivy frequentemente aponta múltiplas vulnerabilidades críticas e dezenas de vulnerabilidades de severidade alta em bibliotecas de sistema, compiladores e utilitários auxiliares.

Na imagem `python:3.12-alpine`, o número de vulnerabilidades críticas despenca para zero ou para um número residual. Isso ocorre porque o Alpine Linux utiliza a biblioteca leve `musl libc` em conjunto com o conjunto enxuto de ferramentas `BusyBox`, descartando centenas de utilitários desnecessários. Menos código rodando no disco significa diretamente menor superfície de ataque em produção.

</details>

## O Caminho para a Orquestração

Ao longo desta série, construímos uma visão técnica completa sobre o funcionamento dos contêineres: desde as chamadas de sistema elementares no kernel do Linux até a orquestração de múltiplos serviços com Docker Compose e a arquitetura sem daemons do Podman.

Tudo o que fizemos até agora opera com excelência para ambientes de desenvolvimento, testes automatizados e até mesmo para pequenos serviços rodando em uma única máquina virtual ou servidor dedicado.

Mas e quando o seu sistema precisa atender milhões de requisições simultâneas? E quando a máquina física onde a sua aplicação está rodando queima a placa-mãe no meio da madrugada?

É nesse ponto que o modelo de gerenciamento em uma única máquina encontra seus limites naturais:
1. **Ausência de Tolerância a Falhas Físicas**: Se o servidor cair, todos os contêineres caem com ele.
2. **Escalabilidade Manual**: O Docker Compose não sabe como distribuir cópias de uma mesma aplicação entre cinco servidores diferentes e balancear o tráfego de rede entre eles.
3. **Falta de Autorrecuperação Automática Distribuída**: Se um contêiner travar por exaustão de hardware em um servidor sobrecarregado, o Compose não tem a inteligência de recriar essa carga em outro nó com recursos livres.

Para solucionar a operação distribuída em escala de data center, a indústria migrou em peso para os **Orquestradores de Contêineres**, coroados pelo padrão absoluto da computação em nuvem: o **Kubernetes** [^8].

E agora vem a grande revelação: **o Kubernetes não inventou nenhuma tecnologia mágica de contêineres**. 

Todo o funcionamento de um cluster Kubernetes é a aplicação em escala de rede exatamente dos mesmos conceitos que dominamos nesta série:
- O **Pod** do Kubernetes é a união de múltiplos contêineres dividindo os mesmos *namespaces* de rede e IPC, exatamente como demonstramos nos Pods do Podman.
- As diretivas de **Resource Requests e Limits** que você declara nos manifestos do Kubernetes nada mais são do que instruções repassadas diretamente para os arquivos `cpu.max` e `memory.max` do *cgroups* v2 em cada nó do cluster.
- As imagens baixadas pelo Kubernetes seguem estritamente as especificações de camadas da **OCI** que dissecamos no OverlayFS.
- A comunicação entre os nós e os Pods através de plugins CNI (*Container Network Interface*) utiliza os mesmos pares de interfaces virtuais *veth* e regras de roteamento que analisamos na seção de redes do Docker.

Quando você compreende a anatomia do contêiner na raiz do sistema operacional, o Kubernetes deixa de ser uma caixa preta assustadora e se transforma no que ele realmente é: um sistema de controle distribuído brilhante que conversa diretamente com o kernel Linux.

É com essa bagagem técnica consolidada que encerramos nossa série de fundamentos e abrimos as portas para os próximos passos práticos do blog. Se você quer ver como orquestrar esses contêineres construindo um cluster local na mão com máquinas virtuais e automação Ansible, siga diretamente para a série {% include post-ref.html slug="k8sbox-visao-geral" text="Kubernetes in a Box" %}. E se o seu objetivo é empacotar serviços corporativos Java com excelência técnica para rodar nesse ecossistema, nos encontramos na Parte 14 da nossa série {% include post-ref.html slug="spring-boot-tutorial-parte-1-ambiente" text="Spring Boot Tutorial" %}.

## Referências

[^1]: **Dockerfile Reference Guide** {*Docker Documentation, docs.docker.com*} ([Link](https://docs.docker.com/reference/dockerfile/))

[^2]: **Multi-Stage Builds Documentation** {*Docker Documentation, docs.docker.com*} ([Link](https://docs.docker.com/build/building/multi-stage/))

[^3]: **The Compose Specification** {*Docker Documentation / Compose Spec Community*} ([Link](https://docs.docker.com/compose/compose-file/))

[^4]: **Podman Official Documentation and Architecture Guide** {*Containers Organization / Red Hat*} ([Link](https://docs.podman.io/en/latest/))

[^5]: **Kaniko: Build Container Images In Kubernetes Without Docker Daemon** {*Google Container Tools, GitHub*} ([Link](https://github.com/GoogleContainerTools/kaniko))

[^6]: **Trivy: Comprehensive Security Scanner for Container Images** {*Aqua Security, trivy.dev*} ([Link](https://trivy.dev/))

[^7]: **capabilities(7) - Overview of Linux Capabilities** {*Linux Programmer's Manual, man7.org*} ([Link](https://man7.org/linux/man-pages/man7/capabilities.7.html))

[^8]: **Kubernetes Container Runtimes and Architecture Documentation** {*The Kubernetes Authors, kubernetes.io*} ([Link](https://kubernetes.io/docs/setup/production-environment/container-runtimes/))

[^9]: **CIS Docker Benchmark v1.6.0** {*Center for Internet Security (CIS)*} ([Link](https://www.cisecurity.org/benchmark/docker))

[^10]: **Using Docker-in-Docker for your CI or testing environment? Think twice.** {*Jérôme Petazzoni, jpetazzo.github.io, 2015*} ([Link](https://jpetazzo.github.io/2015/09/03/do-not-use-docker-in-docker-for-ci/))

[^11]: **Compose Specification: Extension Fields and YAML Fragments** {*Docker Documentation, docs.docker.com*} ([Link](https://docs.docker.com/reference/compose-file/fragments/))

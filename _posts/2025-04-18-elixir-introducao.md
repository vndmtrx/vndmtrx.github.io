---
layout: post
title: "Aprendendo Elixir - Introdução"
author:
  - "Eduardo N. S. R."
date: 2025-04-18 15:09:00 GMT-3
modified_date: 2026-08-14 15:25:00 GMT-3
permalink: /posts/elixir-introducao/
tags: [Programação, Programação Funcional, Elixir]
series: Aprendendo Elixir
---

Este post inaugura uma série intitulada *Aprendendo Elixir*, na qual registro minha jornada de aprendizado com essa linguagem. Minha ideia aqui é descrever meu aprendizado (e escrever sobre isso é uma forma de consolidar esse processo). Ao longo dos próximos módulos, iremos construir uma base sólida em Elixir por meio de projetos práticos, cada um introduzindo novos conceitos e boas práticas da programação funcional. Espero que este conteúdo te ajude tanto quanto está me ajudando.

Sempre tive afinidade com linguagens funcionais. Meu primeiro contato foi ainda nos anos 90, quando usava AutoLisp no AutoCAD R14. O AutoLisp despertou meu interesse pelo paradigma funcional de forma totalmente inesperada. Mais tarde, usei Python extensivamente, não apenas pela clareza sintática, mas principalmente pelos recursos funcionais que ele mescla com a programação imperativa e orientação a objetos. Também sempre tive bastante apreço por Java: mesmo não sendo funcional, sua estrutura e clareza sempre me pareceram convidativas à manutenção e organização do código.

Agora, com Elixir, sinto um misto desses mundos: a elegância e concisão da sintaxe, combinadas com o poder do paradigma funcional. Recursos como o operador `|>` (*pipe*) e o *pattern matching* moldam a forma de pensar, e vou abordar cada um deles com calma ao longo da série.

## Entendendo o Elixir e sua proposta

Antes de sair instalando pacotes e compilando código, vale entender por que o Elixir é tão interessante e o que ele traz para a mesa.

O Elixir [^1] é uma linguagem funcional, concorrente e tolerante a falhas, construída sobre a máquina virtual do Erlang, a BEAM. Essa base não é um detalhe técnico qualquer: a BEAM foi criada na Ericsson nos anos 80 para sistemas de telecomunicações que simplesmente não podiam parar. A herança direta disso são processos leves aos milhares, isolamento de falhas e um modelo de concorrência que não envolve memória compartilhada. O Elixir herda toda essa robustez com uma sintaxe moderna, limpa e produtiva.

Por ser funcional, o Elixir trabalha com imutabilidade de dados e funções puras. Na prática, você não altera o estado de um objeto: você recebe dados, aplica transformações e retorna novos dados. No começo parece uma restrição estranha para quem vem da orientação a objetos tradicional, mas logo fica claro como isso elimina categorias inteiras de bugs e torna o código previsível e testável.

O ecossistema também se destaca pela consistência. O `mix` [^2] gerencia projetos, compilação, tarefas e dependências; o `ExUnit` [^3] é o *framework* de testes nativo, sem necessidade de ferramentas externas; e o IEx é o REPL interativo, excelente para experimentar código ao vivo.

Neste primeiro módulo, vamos configurar o ambiente do zero com o ASDF, entender como funcionam as versões do Erlang e do Elixir, criar um projeto básico com `mix`, implementar nossa primeira função e escrever testes automatizados com `ExUnit`. Todo o código deste exemplo está no diretório [01-saudacao](https://github.com/vndmtrx/estudo_elixir/tree/main/01-saudacao) do repositório parceiro no GitHub [^4].

## Antes de instalar: uma nota sobre versões

> ⚠️ *Atenção*: Erlang e Elixir têm ciclos de vida independentes e versões que chegam ao fim do suporte com regularidade. Antes de seguir com a instalação, recomendo verificar as versões ativas no [endoflife.date/erlang](https://endoflife.date/erlang) [^5] e no [endoflife.date/elixir](https://endoflife.date/elixir) [^6]. Neste guia, usamos o **Erlang 27.3.2** e o **Elixir 1.18.3-otp-27**, que formam uma combinação estável e suportada.

Um ponto importante sobre a nomenclatura das versões: quando você instala o Elixir via ASDF, o sufixo `-otp-XX` indica com qual versão principal do Erlang/OTP aquele *build* do Elixir foi compilado. Usar `1.18.3-otp-27` significa que temos o Elixir 1.18.3 compilado contra o OTP 27, casando exatamente com o Erlang 27 instalado. Misturar versões incompatíveis resulta em erros crípticos de inicialização na BEAM, então sempre preste atenção a esse sufixo.

## Instalação do ASDF e das dependências

> ⚠️ *Aviso*: Este guia de instalação foi testado no Debian 12 (Bookworm) e Debian 13 (Trixie). Os comandos e pacotes listados podem variar ligeiramente dependendo da sua distribuição Linux ou sistema operacional. A documentação oficial do ASDF [^7] fornece instruções específicas para cada ambiente.

### Dependências para compilação do Erlang

Antes de instalar o ASDF e compilar as linguagens, precisamos garantir as bibliotecas de desenvolvimento, ferramentas de compilação e suporte a SSL no sistema:

```bash
sudo apt update && sudo apt install -y git curl autoconf \
  build-essential libssl-dev libncurses-dev unzip
```

*Instala compiladores, bibliotecas SSL e utilitários essenciais para compilar o Erlang a partir do código-fonte.*

### Download e instalação do ASDF

O ASDF [^7] é um gerenciador de versões universal. Ele permite manter múltiplas versões de linguagens em paralelo (Erlang, Elixir, Node, Python, etc.) e alternar automaticamente entre elas via arquivo `.tool-versions`.

A partir da versão 0.16, o ASDF passou a distribuir um binário pré-compilado em Go, eliminando a necessidade do antigo clone via Git. A convenção moderna é instalar o executável no diretório `~/.local/bin/`:

```bash
ASDF_VERSION="v0.16.5"
curl -LO "https://github.com/asdf-vm/asdf/releases/download/${ASDF_VERSION}/asdf-${ASDF_VERSION}-linux-amd64.tar.gz"
tar -xzf asdf-${ASDF_VERSION}-linux-amd64.tar.gz
mkdir -p ~/.local/bin
mv asdf ~/.local/bin/
rm asdf-${ASDF_VERSION}-linux-amd64.tar.gz
```

*Baixa a release binária do ASDF, descompacta o arquivo e move o executável para o diretório local do usuário.*

Agora configuramos os *shims* do ASDF e garantimos que `~/.local/bin` faça parte do seu `$PATH`:

```bash
echo 'export PATH="${ASDF_DATA_DIR:-$HOME/.asdf}/shims:$PATH"' >> ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

*Registra os shims do ASDF e o diretório de binários locais no `.bashrc` e recarrega o ambiente da shell.*

Para confirmar que o ASDF foi instalado e está acessível no terminal:

```bash
type -a asdf
```

*Verifica a localização do binário do ASDF no PATH.*

A saída esperada deve apontar para `asdf is /home/seu_usuario/.local/bin/asdf`.

### Instalação dos plugins Erlang e Elixir

Com o ASDF configurado, adicionamos os *plugins* de cada linguagem para permitir buscar e gerenciar suas respectivas versões:

```bash
asdf plugin add erlang
asdf plugin add elixir
```

*Adiciona os plugins oficiais de Erlang e Elixir ao ASDF.*

Para consultar a lista completa de versões disponíveis para instalação:

```bash
asdf list all erlang
asdf list all elixir
```

*Lista todas as versões publicadas de cada linguagem nos repositórios oficiais.*

Agora, instalamos o Erlang e o Elixir correspondente:

```bash
asdf install erlang 27.3.2
asdf install elixir 1.18.3-otp-27
```

*Compila o Erlang 27.3.2 a partir do código-fonte e instala a versão compatível do Elixir.*

> 💡 *Dica*: A compilação do Erlang leva alguns minutos porque o ASDF compila o código-fonte diretamente na sua máquina.

Para definir essas versões como padrão global para o seu usuário:

```bash
asdf set --home erlang 27.3.2
asdf set --home elixir 1.18.3-otp-27
```

*Define as versões padrão para o usuário atual (o comando `asdf set --home` substitui o antigo `asdf global`).*

Para travar as versões em um projeto específico, usamos o comando `asdf set` dentro da pasta do projeto:

```bash
asdf set erlang 27.3.2
asdf set elixir 1.18.3-otp-27
```

*Gera o arquivo `.tool-versions` no diretório atual, garantindo que o ASDF ative automaticamente essas versões ao entrar na pasta.*

## Primeiro teste com IEx

Antes de criar nosso primeiro projeto, vale fazer um teste rápido no terminal para garantir que a BEAM e o Elixir estão respondendo corretamente.

Para abrir o console interativo, basta executar `iex` no terminal:

```bash
iex
```

*Inicia o console interativo IEx exibindo as versões do Erlang/OTP e do Elixir.*

No *prompt* do IEx, executamos a tradicional saudação:

```elixir
IO.puts("Olá, Elixir!")
```

*Imprime a mensagem no terminal e retorna o átomo `:ok`.*

A saída será:

```elixir
Olá, Elixir!
:ok
```

*O retorno do átomo `:ok` indica o sucesso da operação, uma convenção amplamente usada em todo o ecossistema.*

Para sair do IEx a qualquer momento, pressione `Ctrl+C` duas vezes ou digite `System.halt()`.

## Criação do primeiro projeto Elixir

Com o ambiente pronto e validado, criamos a estrutura do nosso primeiro projeto com o `mix`:

```bash
mix new saudacao
cd saudacao
```

*Gera a estrutura inicial do projeto Elixir com o Mix e entra no diretório criado.*

> ⚠️ *Aviso*: O nome da pasta no repositório de exemplos é `01-saudacao` para manter a organização sequencial dos posts, mas a estrutura e o código são rigorosamente os mesmos.

A árvore de arquivos gerada pelo `mix new` segue a organização padrão do ecossistema:

```
saudacao/
├── lib/
│   └── saudacao.ex       <- código-fonte principal da aplicação
├── test/
│   ├── test_helper.exs   <- inicialização do ExUnit
│   └── saudacao_test.exs <- testes automatizados
└── mix.exs               <- configurações, metadados e dependências
```

O arquivo `mix.exs` gerencia o nome da aplicação, versão e dependências externas. O diretório `lib/` guarda os módulos da aplicação e o `test/` abriga os testes unitários.

## Implementação da função principal

**Arquivo:** `lib/saudacao.ex`

```elixir
defmodule Saudacao do
  @moduledoc """
  Módulo responsável por gerar saudações personalizadas.
  """

  @doc """
  Retorna uma saudação com o nome informado.

  ## Exemplos

      iex> Saudacao.ola("Dudu")
      "Olá, Dudu!"

  """
  def ola(nome) when is_binary(nome) do
    "Olá, #{nome}!"
  end
end
```

*Define o módulo `Saudacao` com documentação formatada, exemplos em doctest e guard clause restringindo o tipo a binários.*

Nesta estrutura inicial, temos alguns pontos fundamentais:

- `@moduledoc`: Fornece a documentação descritiva do módulo como um todo. Esse texto é lido por geradores de documentação como o `ExDoc` e exibido interativamente no terminal via comando `h Saudacao` no IEx.
- `@doc`: Documenta a função específica `ola/1`, incluindo um bloco `## Exemplos` com a sintaxe do IEx. Esse exemplo não é apenas texto: ele será executado como teste pelo `doctest`.
- `when is_binary(nome)`: É uma *guard clause* (*guarda*) que garante que a função só será executada se o argumento passado for uma string (que internamente em Elixir é um binário UTF-8). Caso contrário, a BEAM rejeita o casamento de cláusula e lança um erro `FunctionClauseError`.

### Testando interativamente no IEx

Para testar o módulo que acabamos de escrever sem precisar compilar tudo manualmente, iniciamos o IEx passando a flag `-S mix`:

```bash
iex -S mix
```

*Compila os arquivos em `lib/` e carrega todos os módulos do projeto no console interativo.*

No *prompt*, podemos chamar a função diretamente:

```elixir
Saudacao.ola("Dudu")
```

*Executa a função `Saudacao.ola/1` no IEx.*

A saída exibida será a string interpolada:

```elixir
"Olá, Dudu!"
```

*Retorno da execução com o texto formatado.*

## Criação de testes com ExUnit

O Elixir inclui o *framework* `ExUnit` de fábrica. Não é preciso instalar bibliotecas de testes de terceiros nem configurar runners complexos.

**Arquivo:** `test/saudacao_test.exs`

```elixir
defmodule SaudacaoTest do
  use ExUnit.Case, async: true
  doctest Saudacao

  describe "ola/1" do
    test "retorna uma saudação personalizada" do
      assert Saudacao.ola("Dudu") == "Olá, Dudu!"
    end

    test "retorna corretamente com nomes diferentes" do
      assert Saudacao.ola("Leitor") == "Olá, Leitor!"
    end

    test "emite erro quando o argumento não é uma string" do
      assert_raise FunctionClauseError, fn ->
        Saudacao.ola(123)
      end
    end
  end
end
```

*Define a suíte de testes assíncronos com ExUnit, validação via doctest e asserção de erro com `assert_raise`.*

Analisando a estrutura do teste:

- `use ExUnit.Case, async: true`: Habilita a execução paralela dos testes deste arquivo, tirando proveito de múltiplos núcleos de CPU.
- `doctest Saudacao`: Lê os exemplos contidos na anotação `@doc` do módulo `Saudacao` e os executa como testes reais. Se o exemplo na documentação ficar desatualizado em relação ao comportamento do código, o teste falha na hora.
- `describe "ola/1"`: Agrupa os cenários de teste relacionados à função em um bloco temático.
- `assert`: Macro de asserção que verifica se o resultado retornado é idêntico ao esperado.
- `assert_raise FunctionClauseError`: Garante que passar um tipo inválido (como o inteiro `123`) dispara a exceção esperada definida pelo *guard* `when is_binary`.

Para rodar os testes da aplicação:

```bash
mix test
```

*Executa todos os testes do projeto e apresenta o relatório de sucesso no terminal.*

A saída esperada no terminal:

```
....

Finished in 0.03 seconds (0.02s async, 0.01s sync)
4 tests, 0 failures
```

*Relatório de execução do ExUnit indicando 4 testes executados com sucesso (1 doctest + 3 testes do describe).*

## Exercícios

**1. Crie uma função `ola/2` que aceita uma saudação customizada**

A função deve receber a saudação como primeiro argumento e o nome como segundo, retornando a frase formatada (ex: `Saudacao.ola("Bom dia", "Dudu")` -> `"Bom dia, Dudu!"`). Garanta com *guards* que ambos os parâmetros sejam strings.

<details markdown="1">
<summary>Ver resposta</summary>

```elixir
@doc """
Retorna uma saudação personalizada com prefixo customizado.

## Exemplos

    iex> Saudacao.ola("Bom dia", "Dudu")
    "Bom dia, Dudu!"

"""
def ola(saudacao, nome) when is_binary(saudacao) and is_binary(nome) do
  "#{saudacao}, #{nome}!"
end
```

*Em Elixir, funções com o mesmo nome mas quantidades diferentes de argumentos são tratadas como funções distintas (aridade `ola/1` vs `ola/2`). O operador `and` no guard combina as duas validações de tipo.*

</details>

**2. Escreva um teste no ExUnit para a função `ola/2`**

Adicione um teste dentro do bloco `describe` validando o comportamento de `ola/2`.

<details markdown="1">
<summary>Ver resposta</summary>

```elixir
describe "ola/2" do
  test "retorna saudação com prefixo customizado" do
    assert Saudacao.ola("Boa tarde", "Eduardo") == "Boa tarde, Eduardo!"
  end

  test "emite erro se algum dos argumentos não for string" do
    assert_raise FunctionClauseError, fn ->
      Saudacao.ola(123, "Eduardo")
    end

    assert_raise FunctionClauseError, fn ->
      Saudacao.ola("Olá", :eduardo)
    end
  end
end
```

*O teste valida o caso de sucesso e também garante que qualquer parâmetro com tipo incompatível seja barrado pelos guards.*

</details>

## Considerações Finais

Este primeiro módulo estabelece uma base sólida e limpa para começar com o Elixir: ambiente configurado com ASDF, projeto gerenciado com `mix`, código modular com documentação e testes automatizados rodando com `ExUnit`.

No próximo post da série, vamos dar um passo importante na organização de código: explorar a arquitetura modular com a estrutura Guarda-Chuva (*Umbrella*), aprendendo a dividir aplicações complexas em subprojetos menores e coesos dentro do mesmo repositório.

Até a próxima!

## Referências

[^1]: **Elixir (linguagem de programação)** {*Wikipedia*} ([Link](https://pt.wikipedia.org/wiki/Elixir_(linguagem_de_programa%C3%A7%C3%A3o)))

[^2]: **Guia do Mix** {*HexDocs*} ([Link](https://hexdocs.pm/mix/Mix.html))

[^3]: **Guia do ExUnit** {*HexDocs*} ([Link](https://hexdocs.pm/ex_unit/ExUnit.html))

[^4]: **Repositório de Estudos em Elixir** {*GitHub*} ([Link](https://github.com/vndmtrx/estudo_elixir))

[^5]: **Erlang - End of Life** {*endoflife.date*} ([Link](https://endoflife.date/erlang))

[^6]: **Elixir - End of Life** {*endoflife.date*} ([Link](https://endoflife.date/elixir))

[^7]: **Documentação do ASDF** {*ASDF VM*} ([Link](https://asdf-vm.com/))

